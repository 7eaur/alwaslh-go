import postgres from 'postgres';

const databaseUrl = process.env.DATABASE_URL;
if (!databaseUrl) throw new Error('DATABASE_URL is required');

const sql = postgres(databaseUrl, { max: 1, connect_timeout: 15, idle_timeout: 5, prepare: false });

const targetSection = {
  slug: 'curated-english9-pb3-unit-2-describing-making-plans',
  title: 'Unit 2 - Describing: Making plans',
  position: 2,
};

const targetLesson = {
  slug: 'curated-english9-pb3-u2-describing-people-and-animals',
  title: 'Describing people and animals',
  position: 4,
};

const pages = [
  { order: 0, bookPage: 5, sourcePage: 9, legacyPageId: '706771c2-2145-4682-9bdd-4e7df5c69bf9', path: 'public.lessons/706771c2-2145-4682-9bdd-4e7df5c69bf9/image/0', sha256: 'fc9e15f23d3f5c9a7928aecc70888e30be2c454ab16883e1a3c82290fd581fdb' },
  { order: 1, bookPage: 6, sourcePage: 10, legacyPageId: '71ba9a99-e009-401f-b65f-8a956218a633', path: 'public.lessons/71ba9a99-e009-401f-b65f-8a956218a633/image/0', sha256: 'fd99f85698dd4870bf8fccf85aa53f47bf484d19b2052473155540627f6aa420' },
  { order: 2, bookPage: 7, sourcePage: 11, legacyPageId: '710cb3d4-e2c1-4d05-a1ef-2c0a1bbede2b', path: 'public.lessons/710cb3d4-e2c1-4d05-a1ef-2c0a1bbede2b/image/0', sha256: '3b7415622af90557ad09585eef776b5ce3fe2c68776a1963b4a2cbf677f5ba61' },
  { order: 3, bookPage: 8, sourcePage: 12, legacyPageId: '4b6090c2-744e-4fc6-8908-87c211a8713b', path: 'public.lessons/4b6090c2-744e-4fc6-8908-87c211a8713b/image/0', sha256: '3678974564e2a219840da4fc175d62d9811bd80666d01c81d4f9b49f2328e258' },
];

function assert(condition, message) {
  if (!condition) throw new Error(`IMPORT001_GATE_FAIL: ${message}`);
}

const rollbackSentinel = 'IMPORT001_EXPECTED_ROLLBACK';
let passSummary = null;
let beforeSnapshot = null;

try {
  await sql.begin(async (tx) => {
    await tx`set local lock_timeout = '5s'`;
    await tx`set local statement_timeout = '60s'`;

    const scope = await tx`
      select c.id class_id, s.id subject_id
      from classes c
      join subject_class_links scl on scl.class_id = c.id
      join subjects s on s.id = scl.subject_id
      where c.slug = 'grade-9' and s.slug = 'english'
        and c.status = 'active' and s.status = 'active' and scl.status = 'active'
      for update of scl
    `;
    assert(scope.length === 1, `grade-9/english active scope count=${scope.length}`);
    const { class_id: classId, subject_id: subjectId } = scope[0];

    const existingSection = await tx`
      select id from curriculum_sections
      where class_id = ${classId} and subject_id = ${subjectId} and slug = ${targetSection.slug}
      for update
    `;
    assert(existingSection.length === 0, `target section already exists count=${existingSection.length}`);

    const existingTargetLesson = await tx`
      select id from lessons
      where class_id = ${classId} and subject_id = ${subjectId} and slug = ${targetLesson.slug}
      for update
    `;
    assert(existingTargetLesson.length === 0, `target lesson already exists count=${existingTargetLesson.length}`);

    const resolved = [];
    for (const page of pages) {
      const rows = await tx`
        select csa.id source_asset_id, csa.source_path, csa.checksum_sha256, csa.is_present,
               ma.id media_asset_id, ma.status media_status, ma.source_checksum_sha256,
               la.id lesson_asset_id, la.lesson_id, la.position lesson_asset_position,
               la.publication_status, la.asset_published_at,
               l.slug legacy_lesson_slug, l.title legacy_lesson_title, l.position legacy_lesson_position,
               l.status legacy_lesson_status, l.published_at legacy_lesson_published_at, l.section_id legacy_section_id
        from content_source_assets csa
        join media_assets ma on ma.content_source_asset_id = csa.id
        join lesson_assets la on la.media_asset_id = ma.id
        join lessons l on l.id = la.lesson_id
        where csa.source_path = ${page.path}
          and csa.checksum_sha256 = ${page.sha256}
          and csa.is_present = true
          and ma.source_checksum_sha256 = ${page.sha256}
          and ma.status = 'ready'
          and l.class_id = ${classId}
          and l.subject_id = ${subjectId}
      `;
      assert(rows.length === 1, `source ${page.legacyPageId} chain count=${rows.length}`);
      const row = rows[0];
      assert(row.publication_status === 'draft' && row.asset_published_at === null, `source ${page.legacyPageId} asset is not draft/unpublished`);
      assert(row.legacy_lesson_status === 'active' && row.legacy_lesson_published_at === null, `source ${page.legacyPageId} legacy lesson is not active/unpublished`);
      assert(row.legacy_section_id === null, `source ${page.legacyPageId} legacy lesson section drift`);
      const lockAsset = await tx`select id from lesson_assets where id = ${row.lesson_asset_id} for update`;
      const lockLesson = await tx`select id from lessons where id = ${row.lesson_id} for update`;
      assert(lockAsset.length === 1 && lockLesson.length === 1, `failed to lock source ${page.legacyPageId}`);
      resolved.push({ ...page, ...row });
    }

    assert(new Set(resolved.map((x) => x.source_asset_id)).size === 4, 'source assets are not unique');
    assert(new Set(resolved.map((x) => x.media_asset_id)).size === 4, 'media assets are not unique');
    assert(new Set(resolved.map((x) => x.lesson_asset_id)).size === 4, 'lesson assets are not unique');
    assert(new Set(resolved.map((x) => x.lesson_id)).size === 4, 'legacy lessons are not unique');

    const legacyLessonIds = resolved.map((x) => x.lesson_id);
    const beforeQuestions = await tx`
      select r.id, rl.lesson_id, r.status, r.published_at
      from question_bank_revisions r
      join question_bank_revision_lessons rl on rl.revision_id = r.id
      where rl.lesson_id in ${tx(legacyLessonIds)}
      order by r.id
    `;
    assert(beforeQuestions.length === 12, `expected 12 preserved legacy question revisions, got ${beforeQuestions.length}`);
    assert(beforeQuestions.every((q) => q.published_at === null), 'legacy question publication drift');

    beforeSnapshot = resolved.map((x) => ({
      lessonAssetId: x.lesson_asset_id,
      lessonId: x.lesson_id,
      position: x.lesson_asset_position,
      publicationStatus: x.publication_status,
      assetPublishedAt: x.asset_published_at,
    }));

    const [section] = await tx`
      insert into curriculum_sections (class_id, subject_id, slug, title, position, status)
      values (${classId}, ${subjectId}, ${targetSection.slug}, ${targetSection.title}, ${targetSection.position}, 'active')
      returning id
    `;

    const [lesson] = await tx`
      insert into lessons (class_id, subject_id, section_id, slug, title, position, status, published_at)
      values (${classId}, ${subjectId}, ${section.id}, ${targetLesson.slug}, ${targetLesson.title}, ${targetLesson.position}, 'active', null)
      returning id
    `;

    let reassigned = 0;
    for (const row of resolved.sort((a, b) => a.order - b.order)) {
      const updated = await tx`
        update lesson_assets
        set lesson_id = ${lesson.id}, position = ${row.order}
        where id = ${row.lesson_asset_id}
          and lesson_id = ${row.lesson_id}
          and publication_status = 'draft'
          and asset_published_at is null
        returning id
      `;
      assert(updated.length === 1, `lesson asset ${row.lesson_asset_id} reassignment count=${updated.length}`);
      reassigned += updated.length;
    }
    assert(reassigned === 4, `reassigned asset count=${reassigned}`);

    const targetAssets = await tx`
      select la.id lesson_asset_id, la.position, la.publication_status, la.asset_published_at,
             ma.id media_asset_id, ma.status media_status, csa.id source_asset_id,
             csa.source_path, csa.checksum_sha256, csa.is_present
      from lesson_assets la
      join media_assets ma on ma.id = la.media_asset_id
      join content_source_assets csa on csa.id = ma.content_source_asset_id
      where la.lesson_id = ${lesson.id}
      order by la.position
    `;
    assert(targetAssets.length === 4, `target lesson asset count=${targetAssets.length}`);
    for (let i = 0; i < targetAssets.length; i++) {
      const actual = targetAssets[i];
      const expected = pages[i];
      assert(actual.position === i, `target asset order mismatch at ${i}`);
      assert(actual.source_path === expected.path && actual.checksum_sha256 === expected.sha256 && actual.is_present === true, `target asset source/provenance mismatch at ${i}`);
      assert(actual.media_status === 'ready', `target asset media status mismatch at ${i}`);
      assert(actual.publication_status === 'draft' && actual.asset_published_at === null, `target asset publication changed at ${i}`);
    }

    const legacyAssetCounts = await tx`
      select l.id, count(la.id)::int asset_count
      from lessons l
      left join lesson_assets la on la.lesson_id = l.id
      where l.id in ${tx(legacyLessonIds)}
      group by l.id
      order by l.id
    `;
    assert(legacyAssetCounts.length === 4 && legacyAssetCounts.every((x) => x.asset_count === 0), 'legacy source lessons still hold reviewed page assets inside dry-run');

    const afterQuestions = await tx`
      select r.id, rl.lesson_id, r.status, r.published_at
      from question_bank_revisions r
      join question_bank_revision_lessons rl on rl.revision_id = r.id
      where rl.lesson_id in ${tx(legacyLessonIds)}
      order by r.id
    `;
    assert(JSON.stringify(afterQuestions) === JSON.stringify(beforeQuestions), 'legacy question rows/links changed during structural import dry-run');

    const [pub] = await tx`
      select
        count(*) filter (where l.published_at is not null)::int published_lessons,
        count(*) filter (where la.publication_status <> 'draft' or la.asset_published_at is not null)::int published_assets
      from lessons l
      left join lesson_assets la on la.lesson_id = l.id
      where l.id = ${lesson.id}
      group by l.id
    `;
    assert(pub.published_lessons === 0 && pub.published_assets === 0, 'target publication invariant changed');

    passSummary = {
      mode: 'rollback-only',
      task: 'IMPORT-001',
      scope: 'grade-9/english/pupil-book-3/unit-2/pages-5-8',
      intendedMutation: {
        createSections: 1,
        createLessons: 1,
        reassignLessonAssets: 4,
        createMediaAssets: 0,
        mutateMediaAssets: 0,
        mutateLegacyLessons: 0,
        mutateQuestions: 0,
        publicationChanges: 0,
        unrelatedRows: 0,
      },
      targetSection,
      targetLesson,
      reusedMediaAssets: resolved.map((x) => x.media_asset_id),
      reusedLessonAssets: resolved.sort((a, b) => a.order - b.order).map((x) => x.lesson_asset_id),
      preservedLegacyLessons: legacyLessonIds,
      preservedQuestionRevisions: beforeQuestions.length,
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
  from classes c join subject_class_links scl on scl.class_id = c.id
  join subjects s on s.id = scl.subject_id
  where c.slug = 'grade-9' and s.slug = 'english'
`;
assert(scope.length === 1, 'post-rollback scope drift');

const postSection = await sql`
  select id from curriculum_sections
  where class_id = ${scope[0].class_id} and subject_id = ${scope[0].subject_id} and slug = ${targetSection.slug}
`;
const postLesson = await sql`
  select id from lessons
  where class_id = ${scope[0].class_id} and subject_id = ${scope[0].subject_id} and slug = ${targetLesson.slug}
`;
assert(postSection.length === 0, `post-rollback target section count=${postSection.length}`);
assert(postLesson.length === 0, `post-rollback target lesson count=${postLesson.length}`);

for (const before of beforeSnapshot ?? []) {
  const rows = await sql`
    select lesson_id, position, publication_status, asset_published_at
    from lesson_assets where id = ${before.lessonAssetId}
  `;
  assert(rows.length === 1, `post-rollback lesson asset ${before.lessonAssetId} missing`);
  const row = rows[0];
  assert(row.lesson_id === before.lessonId && row.position === before.position, `post-rollback lesson asset ${before.lessonAssetId} ownership/order drift`);
  assert(row.publication_status === before.publicationStatus && row.asset_published_at === before.assetPublishedAt, `post-rollback lesson asset ${before.lessonAssetId} publication drift`);
}

console.log('IMPORT001_TRANSACTION_GATE_PASS', JSON.stringify({
  ...passSummary,
  rollbackVerified: true,
  committedBusinessWrites: 0,
}));

await sql.end({ timeout: 1 });
