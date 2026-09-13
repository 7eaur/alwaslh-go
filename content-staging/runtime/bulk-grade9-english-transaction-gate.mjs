import { readFile } from 'node:fs/promises';
import postgres from 'postgres';

const databaseUrl = process.env.DATABASE_URL;
if (!databaseUrl) throw new Error('DATABASE_URL is required');

const manifest = JSON.parse(await readFile(new URL('../curated/grade-9/english/pupil-book-3/reconstruction-candidates.json', import.meta.url), 'utf8'));
const pages = (manifest.page_candidates ?? []).map((page) => ({
  bookPage: page.book_page,
  sourcePage: page.source_page,
  legacyPageId: page.legacy_page_id,
  title: page.manifest_title ?? page.legacy_title,
  section: page.section,
  path: `public.lessons/${page.legacy_page_id}/image/0`,
  sha256: page.raw_image?.sha256,
}));

function assert(condition, message) {
  if (!condition) throw new Error(`BULK_G9_EN_GATE_FAIL: ${message}`);
}
function slugify(value) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 72);
}
function uniq(values) {
  return [...new Set(values)];
}

assert(manifest.counts?.page_candidates === 69 && pages.length === 69, 'manifest page count drift');
assert(manifest.counts?.raw_images === 69 && manifest.counts?.raw_pages === 69, 'manifest RAW count drift');
assert(manifest.counts?.sections === 8, 'manifest section count drift');
assert(uniq(pages.map((p) => p.legacyPageId)).length === 69, 'duplicate legacy page identities');

const sectionNames = uniq(pages.map((p) => p.section));
assert(sectionNames.length === 8, `section names count=${sectionNames.length}`);
const targetSections = sectionNames.map((title, index) => ({
  title,
  position: index + 1,
  slug: `bulk-english9-pb3-${String(index + 1).padStart(2, '0')}-${slugify(title)}`,
}));
const sectionByTitle = new Map(targetSections.map((s) => [s.title, s]));

const sql = postgres(databaseUrl, { max: 1, connect_timeout: 15, idle_timeout: 5, prepare: false });
const rollbackSentinel = 'BULK_G9_EN_EXPECTED_ROLLBACK';
let beforeLessonSections = [];
let beforeSectionCount = 0;
let passSummary = null;

try {
  await sql.begin(async (tx) => {
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
    assert(scope.length === 1, `active grade-9/english scope count=${scope.length}`);
    const { class_id: classId, subject_id: subjectId } = scope[0];

    const [sectionCountRow] = await tx`
      select count(*)::int count
        from curriculum_sections
       where class_id = ${classId} and subject_id = ${subjectId}
    `;
    beforeSectionCount = sectionCountRow.count;

    const resolved = [];
    for (const page of pages) {
      const rows = await tx`
        select csa.id source_asset_id, csa.source_path, csa.checksum_sha256, csa.is_present,
               ma.id media_asset_id, ma.status media_status, ma.source_checksum_sha256,
               la.id lesson_asset_id, la.lesson_id, la.position lesson_asset_position,
               la.publication_status, la.asset_published_at,
               l.slug lesson_slug, l.title lesson_title, l.position lesson_position,
               l.status lesson_status, l.published_at lesson_published_at, l.section_id,
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
           and l.class_id = ${classId}
           and l.subject_id = ${subjectId}
      `;
      assert(rows.length === 1, `source chain ${page.legacyPageId} count=${rows.length}`);
      const row = rows[0];
      assert(row.publication_status === 'draft' && row.asset_published_at === null, `asset publication drift ${page.legacyPageId}`);
      assert(row.lesson_status === 'active' && row.lesson_published_at === null, `lesson publication/status drift ${page.legacyPageId}`);
      await tx`select id from lesson_assets where id = ${row.lesson_asset_id} for update`;
      await tx`select id from lessons where id = ${row.lesson_id} for update`;
      resolved.push({ ...page, ...row });
    }

    assert(new Set(resolved.map((x) => x.source_asset_id)).size === 69, 'source assets are not exactly 69 unique rows');
    assert(new Set(resolved.map((x) => x.media_asset_id)).size === 69, 'media assets are not exactly 69 unique rows');
    assert(new Set(resolved.map((x) => x.lesson_asset_id)).size === 69, 'lesson assets are not exactly 69 unique rows');

    const lessonTargets = new Map();
    for (const row of resolved) {
      const entry = lessonTargets.get(row.lesson_id) ?? { lessonId: row.lesson_id, slug: row.lesson_slug, title: row.lesson_title, currentSectionId: row.section_id, currentSectionTitle: row.current_section_title, targetSections: new Set(), pages: [] };
      entry.targetSections.add(row.section);
      entry.pages.push(row.bookPage);
      lessonTargets.set(row.lesson_id, entry);
    }
    for (const lesson of lessonTargets.values()) {
      assert(lesson.targetSections.size === 1, `lesson ${lesson.slug} crosses manifest sections: ${[...lesson.targetSections].join(' | ')}`);
    }

    const lessonIds = [...lessonTargets.keys()];
    beforeLessonSections = lessonIds.length === 0 ? [] : await tx`
      select id, section_id from lessons where id in ${tx(lessonIds)} order by id
    `;

    const questionBefore = await tx`
      select qbr.id, qbr.status, qbr.published_at
        from question_bank_revisions qbr
       where qbr.id in (
         select distinct qrs.revision_id
           from question_bank_revision_sources qrs
           join content_source_assets csa on csa.id = qrs.content_source_asset_id
          where csa.id in ${tx(resolved.map((x) => x.source_asset_id))}
       )
       order by qbr.id
    `;
    assert(questionBefore.every((q) => q.published_at === null), 'question publication drift before bulk dry-run');

    const resolvedSections = new Map();
    let createSections = 0;
    for (const target of targetSections) {
      const exact = await tx`
        select id, slug, title, position, status
          from curriculum_sections
         where class_id = ${classId} and subject_id = ${subjectId} and title = ${target.title}
         for update
      `;
      assert(exact.length <= 1, `duplicate section title ${target.title} count=${exact.length}`);
      if (exact.length === 1) {
        resolvedSections.set(target.title, exact[0]);
        continue;
      }
      const slugCollision = await tx`
        select id, title from curriculum_sections
         where class_id = ${classId} and subject_id = ${subjectId} and slug = ${target.slug}
      `;
      assert(slugCollision.length === 0, `generated section slug collision ${target.slug}`);
      const [created] = await tx`
        insert into curriculum_sections (class_id, subject_id, slug, title, position, status)
        values (${classId}, ${subjectId}, ${target.slug}, ${target.title}, ${target.position}, 'active')
        returning id, slug, title, position, status
      `;
      resolvedSections.set(target.title, created);
      createSections += 1;
    }
    assert(resolvedSections.size === 8, `resolved section count=${resolvedSections.size}`);

    let assignLessons = 0;
    let reuseLessons = 0;
    for (const lesson of lessonTargets.values()) {
      const targetTitle = [...lesson.targetSections][0];
      const targetSection = resolvedSections.get(targetTitle);
      assert(targetSection, `missing resolved target section ${targetTitle}`);
      if (lesson.currentSectionId === null) {
        const updated = await tx`
          update lessons
             set section_id = ${targetSection.id}
           where id = ${lesson.lessonId}
             and section_id is null
             and published_at is null
             and status = 'active'
          returning id
        `;
        assert(updated.length === 1, `lesson section assignment failed ${lesson.slug}`);
        assignLessons += 1;
      } else {
        assert(lesson.currentSectionId === targetSection.id, `lesson ${lesson.slug} section mismatch: ${lesson.currentSectionTitle ?? lesson.currentSectionId} -> ${targetTitle}`);
        reuseLessons += 1;
      }
    }

    const finalChains = await tx`
      select csa.source_path, l.id lesson_id, l.section_id, cs.title section_title,
             l.published_at lesson_published_at,
             la.publication_status, la.asset_published_at,
             ma.status media_status
        from content_source_assets csa
        join media_assets ma on ma.content_source_asset_id = csa.id
        join lesson_assets la on la.media_asset_id = ma.id
        join lessons l on l.id = la.lesson_id
        join curriculum_sections cs on cs.id = l.section_id
       where csa.id in ${tx(resolved.map((x) => x.source_asset_id))}
       order by csa.source_path
    `;
    assert(finalChains.length === 69, `post-mutation dry-run chain count=${finalChains.length}`);
    const finalByPath = new Map(finalChains.map((row) => [row.source_path, row]));
    for (const page of pages) {
      const row = finalByPath.get(page.path);
      assert(row, `missing final chain ${page.legacyPageId}`);
      assert(row.section_title === page.section, `final section mismatch ${page.legacyPageId}`);
      assert(row.lesson_published_at === null, `lesson published during dry-run ${page.legacyPageId}`);
      assert(row.publication_status === 'draft' && row.asset_published_at === null, `asset published during dry-run ${page.legacyPageId}`);
      assert(row.media_status === 'ready', `media not ready ${page.legacyPageId}`);
    }

    const questionAfter = await tx`
      select qbr.id, qbr.status, qbr.published_at
        from question_bank_revisions qbr
       where qbr.id in (
         select distinct qrs.revision_id
           from question_bank_revision_sources qrs
           join content_source_assets csa on csa.id = qrs.content_source_asset_id
          where csa.id in ${tx(resolved.map((x) => x.source_asset_id))}
       )
       order by qbr.id
    `;
    assert(JSON.stringify(questionAfter) === JSON.stringify(questionBefore), 'question rows changed during bulk dry-run');

    passSummary = {
      mode: 'rollback-only',
      task: 'BULK-GRADE9-ENGLISH-IMPORT',
      manifestPages: 69,
      sourceAssets: 69,
      mediaAssets: 69,
      lessonAssets: 69,
      involvedLessons: lessonTargets.size,
      sectionsResolved: 8,
      createSections,
      assignLessons,
      reuseLessons,
      questionRevisionsPreserved: questionBefore.length,
      publicationChanges: 0,
      mediaMutations: 0,
      rawMutations: 0,
      questionMutations: 0,
      unrelatedMutations: 0,
    };

    throw new Error(rollbackSentinel);
  });
} catch (error) {
  if (error?.message !== rollbackSentinel) {
    console.error(error?.stack || error);
    await sql.end({ timeout: 1 });
    process.exit(1);
  }
}

const scope = await sql`
  select c.id class_id, s.id subject_id
    from classes c
    join subject_class_links scl on scl.class_id = c.id
    join subjects s on s.id = scl.subject_id
   where c.slug = 'grade-9' and s.slug = 'english'
`;
assert(scope.length === 1, 'post-rollback scope drift');
const [postSectionCountRow] = await sql`
  select count(*)::int count from curriculum_sections
   where class_id = ${scope[0].class_id} and subject_id = ${scope[0].subject_id}
`;
assert(postSectionCountRow.count === beforeSectionCount, `post-rollback section count=${postSectionCountRow.count}, expected=${beforeSectionCount}`);
for (const before of beforeLessonSections) {
  const rows = await sql`select section_id from lessons where id = ${before.id}`;
  assert(rows.length === 1 && rows[0].section_id === before.section_id, `post-rollback lesson section drift ${before.id}`);
}

console.log('BULK_G9_EN_TRANSACTION_GATE_PASS', JSON.stringify({ ...passSummary, rollbackVerified: true, committedBusinessWrites: 0 }));
await sql.end({ timeout: 1 });
