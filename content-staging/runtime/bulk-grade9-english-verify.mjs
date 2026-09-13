import { readFile } from 'node:fs/promises';
import postgres from 'postgres';

const databaseUrl = process.env.DATABASE_URL;
if (!databaseUrl) throw new Error('DATABASE_URL is required');
const manifest = JSON.parse(await readFile(new URL('../curated/grade-9/english/pupil-book-3/reconstruction-candidates.json', import.meta.url), 'utf8'));
const rawPages = manifest.page_candidates ?? [];
function assert(ok, message) { if (!ok) throw new Error(`BULK_G9_EN_VERIFY_FAIL: ${message}`); }
function uniq(values) { return [...new Set(values)]; }
assert(rawPages.length === 69 && manifest.counts?.raw_pages === 69 && manifest.counts?.raw_images === 69, 'manifest page/image drift');
assert(manifest.counts?.questions === 104 && manifest.counts?.sections === 8 && manifest.counts?.source_manifest_only_pages === 1, 'manifest question/section/gap drift');
const pages = rawPages.map((p) => ({ legacyPageId: p.legacy_page_id, section: p.section, path: `public.lessons/${p.legacy_page_id}/image/0`, sha256: p.raw_image?.sha256 }));
assert(uniq(pages.map((p) => p.legacyPageId)).length === 69, 'duplicate manifest identities');
const sectionNames = uniq(pages.map((p) => p.section));
assert(sectionNames.length === 8, `section names=${sectionNames.length}`);
const sql = postgres(databaseUrl, { max: 1, connect_timeout: 15, idle_timeout: 5, prepare: false });
try {
  const scope = await sql`
    select c.id class_id, s.id subject_id
      from classes c
      join subject_class_links scl on scl.class_id = c.id
      join subjects s on s.id = scl.subject_id
     where c.slug = 'grade-9' and s.slug = 'english'
       and c.status = 'active' and s.status = 'active' and scl.status = 'active'
  `;
  assert(scope.length === 1, `active scope count=${scope.length}`);
  const { class_id: classId, subject_id: subjectId } = scope[0];
  const sections = await sql`
    select id, title, slug, position, status
      from curriculum_sections
     where class_id = ${classId} and subject_id = ${subjectId}
       and title in ${sql(sectionNames)}
     order by position, id
  `;
  assert(sections.length === 8, `target section rows=${sections.length}`);
  for (const title of sectionNames) assert(sections.filter((s) => s.title === title).length === 1, `section identity count ${title}=${sections.filter((s) => s.title === title).length}`);
  assert(sections.every((s) => s.status === 'active'), 'target section status drift');
  const rows = [];
  for (const page of pages) {
    const found = await sql`
      select csa.id source_asset_id, csa.source_path, csa.checksum_sha256, csa.is_present,
             ma.id media_asset_id, ma.status media_status, ma.source_checksum_sha256,
             la.id lesson_asset_id, la.publication_status, la.asset_published_at,
             l.id lesson_id, l.status lesson_status, l.published_at lesson_published_at,
             cs.title section_title
        from content_source_assets csa
        join media_assets ma on ma.content_source_asset_id = csa.id
        join lesson_assets la on la.media_asset_id = ma.id
        join lessons l on l.id = la.lesson_id
        join curriculum_sections cs on cs.id = l.section_id
       where csa.source_path = ${page.path}
         and l.class_id = ${classId} and l.subject_id = ${subjectId}
    `;
    assert(found.length === 1, `final chain ${page.legacyPageId} count=${found.length}`);
    const row = found[0];
    assert(row.is_present === true, `source absent ${page.legacyPageId}`);
    assert(row.checksum_sha256 === page.sha256 && row.source_checksum_sha256 === page.sha256, `checksum mismatch ${page.legacyPageId}`);
    assert(row.media_status === 'ready', `media status ${page.legacyPageId}=${row.media_status}`);
    assert(row.publication_status === 'draft' && row.asset_published_at === null, `asset publication drift ${page.legacyPageId}`);
    assert(row.lesson_status === 'active' && row.lesson_published_at === null, `lesson status/publication drift ${page.legacyPageId}`);
    assert(row.section_title === page.section, `section mismatch ${page.legacyPageId}: ${row.section_title} -> ${page.section}`);
    rows.push(row);
  }
  assert(new Set(rows.map((r) => r.source_asset_id)).size === 69, 'source identities not unique 69');
  assert(new Set(rows.map((r) => r.media_asset_id)).size === 69, 'media identities not unique 69');
  assert(new Set(rows.map((r) => r.lesson_asset_id)).size === 69, 'lesson asset identities not unique 69');
  const sourceIds = rows.map((r) => r.source_asset_id);
  const [questions] = await sql`
    select count(distinct qbr.id)::int revisions,
           count(*)::int source_rows,
           count(distinct qbr.id) filter (where qbr.published_at is not null)::int published
      from question_bank_revision_sources qrs
      join question_bank_revisions qbr on qbr.id = qrs.revision_id
     where qrs.content_source_asset_id in ${sql(sourceIds)}
  `;
  assert(questions.revisions === 104 && questions.source_rows === 104 && questions.published === 0,
    `question verification revisions=${questions.revisions} rows=${questions.source_rows} published=${questions.published}`);
  const [publications] = await sql`
    select count(distinct l.id) filter (where l.published_at is not null)::int lessons,
           count(distinct la.id) filter (where la.publication_status <> 'draft' or la.asset_published_at is not null)::int assets
      from lesson_assets la
      join lessons l on l.id = la.lesson_id
     where la.id in ${sql(rows.map((r) => r.lesson_asset_id))}
  `;
  assert(publications.lessons === 0 && publications.assets === 0, `publication leakage lessons=${publications.lessons} assets=${publications.assets}`);
  const involvedLessons = new Set(rows.map((r) => r.lesson_id)).size;
  console.log('BULK_G9_EN_VERIFY_PASS', JSON.stringify({
    task: 'BULK-GRADE9-ENGLISH-IMPORT', mode: 'verify', pagesVerified: 69, rawImagesVerifiedByChecksum: 69,
    mediaAssetsVerified: 69, lessonAssetsVerified: 69, involvedLessons, sectionsVerified: 8,
    questionRevisionsPreserved: 104, sourceManifestOnlyPagesPreservedAsEvidenceOnly: 1,
    publishedLessons: 0, publishedAssets: 0, publishedQuestions: 0,
    rawMutations: 0, mediaMutations: 0, questionMutations: 0,
  }));
} catch (error) {
  console.error(error?.stack || error);
  await sql.end({ timeout: 1 });
  process.exit(1);
}
await sql.end({ timeout: 1 });
