import { readFile } from 'node:fs/promises';
import postgres from 'postgres';

const databaseUrl = process.env.DATABASE_URL;
if (!databaseUrl) throw new Error('DATABASE_URL is required');
const manifest = JSON.parse(await readFile(new URL('../curated/grade-9/english/pupil-book-3/reconstruction-candidates.json', import.meta.url), 'utf8'));
const rawPages = manifest.page_candidates ?? [];
function assert(ok, message) { if (!ok) throw new Error(`BULK_G9_EN_APPLY_FAIL: ${message}`); }
function slugify(value) { return value.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 72); }
function uniq(values) { return [...new Set(values)]; }
assert(rawPages.length === 69 && manifest.counts?.raw_pages === 69 && manifest.counts?.raw_images === 69, 'manifest page/image drift');
assert(manifest.counts?.questions === 104 && manifest.counts?.sections === 8, 'manifest question/section drift');
const pages = rawPages.map((p) => ({
  bookPage: p.book_page,
  legacyPageId: p.legacy_page_id,
  section: p.section,
  path: `public.lessons/${p.legacy_page_id}/image/0`,
  sha256: p.raw_image?.sha256,
}));
assert(uniq(pages.map((p) => p.legacyPageId)).length === 69, 'duplicate legacy identities');
const sectionNames = uniq(pages.map((p) => p.section));
assert(sectionNames.length === 8, `section names=${sectionNames.length}`);
const sectionTargets = sectionNames.map((title, index) => ({
  title,
  position: index + 1,
  slug: `bulk-english9-pb3-${String(index + 1).padStart(2, '0')}-${slugify(title)}`,
}));
const sql = postgres(databaseUrl, { max: 1, connect_timeout: 15, idle_timeout: 5, prepare: false });
let summary;
try {
  summary = await sql.begin(async (tx) => {
    await tx`set local lock_timeout = '5s'`;
    await tx`set local statement_timeout = '120s'`;
    await tx`select pg_advisory_xact_lock(hashtext('content-rebuild:bulk-grade9-english-pb3'))`;
    const scope = await tx`
      select c.id class_id, s.id subject_id
        from classes c
        join subject_class_links scl on scl.class_id = c.id
        join subjects s on s.id = scl.subject_id
       where c.slug = 'grade-9' and s.slug = 'english'
         and c.status = 'active' and s.status = 'active' and scl.status = 'active'
       for update of scl
    `;
    assert(scope.length === 1, `active scope count=${scope.length}`);
    const { class_id: classId, subject_id: subjectId } = scope[0];
    const resolved = [];
    for (const page of pages) {
      const rows = await tx`
        select csa.id source_asset_id, csa.checksum_sha256, csa.is_present,
               ma.id media_asset_id, ma.status media_status, ma.source_checksum_sha256,
               la.id lesson_asset_id, la.lesson_id, la.publication_status, la.asset_published_at,
               l.slug lesson_slug, l.status lesson_status, l.published_at lesson_published_at, l.section_id,
               cs.title current_section_title
          from content_source_assets csa
          join media_assets ma on ma.content_source_asset_id = csa.id
          join lesson_assets la on la.media_asset_id = ma.id
          join lessons l on l.id = la.lesson_id
          left join curriculum_sections cs on cs.id = l.section_id
         where csa.source_path = ${page.path}
           and csa.checksum_sha256 = ${page.sha256}
           and csa.is_present = true
           and ma.source_checksum_sha256 = ${page.sha256}
           and ma.status = 'ready'
           and l.class_id = ${classId} and l.subject_id = ${subjectId}
      `;
      assert(rows.length === 1, `source chain ${page.legacyPageId} count=${rows.length}`);
      const row = rows[0];
      assert(row.publication_status === 'draft' && row.asset_published_at === null, `asset publication drift ${page.legacyPageId}`);
      assert(row.lesson_status === 'active' && row.lesson_published_at === null, `lesson publication/status drift ${page.legacyPageId}`);
      await tx`select id from lesson_assets where id = ${row.lesson_asset_id} for update`;
      await tx`select id from lessons where id = ${row.lesson_id} for update`;
      resolved.push({ ...page, ...row });
    }
    assert(new Set(resolved.map((x) => x.source_asset_id)).size === 69, 'source identities not unique 69');
    assert(new Set(resolved.map((x) => x.media_asset_id)).size === 69, 'media identities not unique 69');
    assert(new Set(resolved.map((x) => x.lesson_asset_id)).size === 69, 'lesson asset identities not unique 69');
    const lessonTargets = new Map();
    for (const row of resolved) {
      const item = lessonTargets.get(row.lesson_id) ?? { lessonId: row.lesson_id, slug: row.lesson_slug, currentSectionId: row.section_id, currentSectionTitle: row.current_section_title, sections: new Set() };
      item.sections.add(row.section);
      lessonTargets.set(row.lesson_id, item);
    }
    for (const lesson of lessonTargets.values()) assert(lesson.sections.size === 1, `lesson ${lesson.slug} crosses sections ${[...lesson.sections].join(' | ')}`);
    const qBefore = await tx`
      select count(distinct qbr.id)::int revisions,
             count(distinct qbr.id) filter (where qbr.published_at is not null)::int published
        from question_bank_revisions qbr
       where qbr.id in (
         select distinct qrs.revision_id from question_bank_revision_sources qrs
          where qrs.content_source_asset_id in ${tx(resolved.map((x) => x.source_asset_id))}
       )
    `;
    assert(qBefore[0].revisions === 104 && qBefore[0].published === 0, `question guard revisions=${qBefore[0].revisions} published=${qBefore[0].published}`);
    const sectionMap = new Map();
    let createSections = 0;
    let reuseSections = 0;
    for (const target of sectionTargets) {
      const exact = await tx`
        select id, slug, title, position, status
          from curriculum_sections
         where class_id = ${classId} and subject_id = ${subjectId} and title = ${target.title}
         for update
      `;
      assert(exact.length <= 1, `duplicate target section ${target.title} count=${exact.length}`);
      if (exact.length === 1) {
        assert(exact[0].status === 'active', `inactive target section ${target.title}`);
        sectionMap.set(target.title, exact[0]); reuseSections += 1; continue;
      }
      const collision = await tx`
        select id, title from curriculum_sections
         where class_id = ${classId} and subject_id = ${subjectId} and slug = ${target.slug}
      `;
      assert(collision.length === 0, `generated section slug collision ${target.slug}`);
      const [created] = await tx`
        insert into curriculum_sections (class_id, subject_id, slug, title, position, status)
        values (${classId}, ${subjectId}, ${target.slug}, ${target.title}, ${target.position}, 'active')
        returning id, slug, title, position, status
      `;
      sectionMap.set(target.title, created); createSections += 1;
    }
    let assignLessons = 0;
    let reuseLessons = 0;
    for (const lesson of lessonTargets.values()) {
      const title = [...lesson.sections][0];
      const target = sectionMap.get(title);
      assert(target, `unresolved target section ${title}`);
      if (lesson.currentSectionId === null) {
        const changed = await tx`
          update lessons set section_id = ${target.id}
           where id = ${lesson.lessonId} and section_id is null and published_at is null and status = 'active'
          returning id
        `;
        assert(changed.length === 1, `lesson assignment failed ${lesson.slug}`);
        assignLessons += 1;
      } else {
        assert(lesson.currentSectionId === target.id, `lesson ${lesson.slug} section mismatch ${lesson.currentSectionTitle ?? lesson.currentSectionId} -> ${title}`);
        reuseLessons += 1;
      }
    }
    const finalRows = await tx`
      select csa.source_path, csa.checksum_sha256,
             ma.source_checksum_sha256, ma.status media_status,
             la.publication_status, la.asset_published_at,
             l.id lesson_id, l.published_at lesson_published_at, cs.title section_title
        from content_source_assets csa
        join media_assets ma on ma.content_source_asset_id = csa.id
        join lesson_assets la on la.media_asset_id = ma.id
        join lessons l on l.id = la.lesson_id
        join curriculum_sections cs on cs.id = l.section_id
       where csa.id in ${tx(resolved.map((x) => x.source_asset_id))}
    `;
    assert(finalRows.length === 69, `final chain count=${finalRows.length}`);
    const byPath = new Map(finalRows.map((r) => [r.source_path, r]));
    for (const page of pages) {
      const row = byPath.get(page.path);
      assert(row, `missing final page ${page.legacyPageId}`);
      assert(row.checksum_sha256 === page.sha256 && row.source_checksum_sha256 === page.sha256, `checksum drift ${page.legacyPageId}`);
      assert(row.media_status === 'ready', `media not ready ${page.legacyPageId}`);
      assert(row.section_title === page.section, `section mismatch ${page.legacyPageId}`);
      assert(row.lesson_published_at === null && row.publication_status === 'draft' && row.asset_published_at === null, `publication drift ${page.legacyPageId}`);
    }
    const qAfter = await tx`
      select count(distinct qbr.id)::int revisions,
             count(distinct qbr.id) filter (where qbr.published_at is not null)::int published
        from question_bank_revisions qbr
       where qbr.id in (
         select distinct qrs.revision_id from question_bank_revision_sources qrs
          where qrs.content_source_asset_id in ${tx(resolved.map((x) => x.source_asset_id))}
       )
    `;
    assert(qAfter[0].revisions === 104 && qAfter[0].published === 0, 'question state changed');
    return {
      task: 'BULK-GRADE9-ENGLISH-IMPORT', mode: 'apply', pages: 69, mediaAssets: 69, lessonAssets: 69,
      involvedLessons: lessonTargets.size, targetSections: 8, createSections, reuseSections, assignLessons, reuseLessons,
      questionRevisionsPreserved: 104, rawMutations: 0, mediaMutations: 0, lessonAssetMutations: 0,
      questionMutations: 0, publicationChanges: 0, unrelatedMutations: 0,
    };
  });
  console.log('BULK_G9_EN_APPLY_PASS', JSON.stringify(summary));
} catch (error) {
  console.error(error?.stack || error);
  await sql.end({ timeout: 1 });
  process.exit(1);
}
await sql.end({ timeout: 1 });
