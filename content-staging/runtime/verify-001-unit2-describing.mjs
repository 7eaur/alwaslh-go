import postgres from 'postgres';

const databaseUrl = process.env.DATABASE_URL;
if (!databaseUrl) throw new Error('DATABASE_URL is required');
const sql = postgres(databaseUrl, { max: 1, connect_timeout: 15, idle_timeout: 5, prepare: false });

const expected = {
  sectionId: '434f9978-efae-471e-b37d-6b151edecc5b',
  sectionSlug: 'curated-english9-pb3-unit-2-describing-making-plans',
  lessonId: '1a6e3a6e-06e8-496e-8d18-c8d4545d1da9',
  lessonSlug: 'curated-english9-pb3-u2-describing-people-and-animals',
};

const pages = [
  { order: 0, lessonAssetId: 'd8dfb014-23bb-4db0-b6c2-3aa8e98862eb', mediaAssetId: '3d53954b-95ef-4833-ae06-407f2325e28e', path: 'public.lessons/706771c2-2145-4682-9bdd-4e7df5c69bf9/image/0', sha256: 'fc9e15f23d3f5c9a7928aecc70888e30be2c454ab16883e1a3c82290fd581fdb' },
  { order: 1, lessonAssetId: 'b474bec6-8828-45e9-8b28-40ff0b52a9c2', mediaAssetId: '9d4f61a2-8c00-44cf-9baa-7e48740e0ef6', path: 'public.lessons/71ba9a99-e009-401f-b65f-8a956218a633/image/0', sha256: 'fd99f85698dd4870bf8fccf85aa53f47bf484d19b2052473155540627f6aa420' },
  { order: 2, lessonAssetId: 'cec764c8-dce3-4917-8dea-66a36165ec89', mediaAssetId: '3aadf23a-432d-4391-bd2f-467eaefe486b', path: 'public.lessons/710cb3d4-e2c1-4d05-a1ef-2c0a1bbede2b/image/0', sha256: '3b7415622af90557ad09585eef776b5ce3fe2c68776a1963b4a2cbf677f5ba61' },
  { order: 3, lessonAssetId: 'bdaca047-29a2-4730-81d5-2abd173a93ce', mediaAssetId: 'b0b1d37e-1b9f-43a3-9987-4973423d822c', path: 'public.lessons/4b6090c2-744e-4fc6-8908-87c211a8713b/image/0', sha256: '3678974564e2a219840da4fc175d62d9811bd80666d01c81d4f9b49f2328e258' },
];

const legacyLessonIds = [
  'faddefc5-b895-4d33-8f18-fa3577ca4040',
  'c97f39b2-0adc-4a25-813e-82eb23d5cf64',
  'e417646b-c7e9-4e66-be41-6938794f3c3e',
  '061af5a7-4871-462d-8ebd-0a083b66d9f3',
];

function assert(condition, message) {
  if (!condition) throw new Error(`VERIFY001_FAIL: ${message}`);
}

try {
  const scope = await sql`
    select c.id class_id, s.id subject_id
    from classes c
    join subject_class_links scl on scl.class_id = c.id
    join subjects s on s.id = scl.subject_id
    where c.slug = 'grade-9' and s.slug = 'english'
      and c.status = 'active' and s.status = 'active' and scl.status = 'active'
  `;
  assert(scope.length === 1, `grade-9/english active scope count=${scope.length}`);
  const { class_id: classId, subject_id: subjectId } = scope[0];

  const sections = await sql`
    select id, title, slug, position, status
    from curriculum_sections
    where class_id = ${classId} and subject_id = ${subjectId} and slug = ${expected.sectionSlug}
  `;
  assert(sections.length === 1, `section identity count=${sections.length}`);
  assert(sections[0].id === expected.sectionId, `section id drift=${sections[0].id}`);
  assert(sections[0].status === 'active', `section status=${sections[0].status}`);

  const lessons = await sql`
    select id, section_id, title, slug, position, status, content_revision, published_at
    from lessons
    where class_id = ${classId} and subject_id = ${subjectId} and slug = ${expected.lessonSlug}
  `;
  assert(lessons.length === 1, `lesson identity count=${lessons.length}`);
  const lesson = lessons[0];
  assert(lesson.id === expected.lessonId, `lesson id drift=${lesson.id}`);
  assert(lesson.section_id === expected.sectionId, `lesson section drift=${lesson.section_id}`);
  assert(lesson.status === 'active', `lesson status=${lesson.status}`);
  assert(lesson.published_at === null, 'lesson unexpectedly published');

  const assets = await sql`
    select la.id lesson_asset_id, la.position, la.publication_status, la.asset_published_at,
           la.media_asset_id, la.checksum_sha256 lesson_checksum,
           ma.status media_status, ma.source_checksum_sha256,
           csa.id source_asset_id, csa.source_path, csa.checksum_sha256 source_checksum, csa.is_present
    from lesson_assets la
    join media_assets ma on ma.id = la.media_asset_id
    join content_source_assets csa on csa.id = ma.content_source_asset_id
    where la.lesson_id = ${expected.lessonId}
    order by la.position, la.id
  `;
  assert(assets.length === 4, `lesson asset count=${assets.length}`);
  for (let i = 0; i < pages.length; i++) {
    const a = assets[i];
    const p = pages[i];
    assert(a.position === p.order, `asset position mismatch at ${i}`);
    assert(a.lesson_asset_id === p.lessonAssetId, `lesson asset id mismatch at ${i}`);
    assert(a.media_asset_id === p.mediaAssetId, `media asset id mismatch at ${i}`);
    assert(a.source_path === p.path, `source path mismatch at ${i}`);
    assert(a.source_checksum === p.sha256 && a.source_checksum_sha256 === p.sha256, `provenance checksum mismatch at ${i}`);
    assert(a.is_present === true, `source asset absent at ${i}`);
    assert(a.media_status === 'ready', `media status=${a.media_status} at ${i}`);
    assert(a.publication_status === 'draft' && a.asset_published_at === null, `asset publication drift at ${i}`);
  }

  // Mirrors the StudentReaderService accessibility contract without requiring a student entitlement.
  // Since the lesson is unpublished, there must be no base lesson row eligible for Student Reader delivery.
  const readerEligibleLessons = await sql`
    select count(*)::int count
    from lessons l
    join classes c on c.id = l.class_id and c.status = 'active'
    join subjects s on s.id = l.subject_id and s.status = 'active'
    join subject_class_links scl
      on scl.class_id = l.class_id and scl.subject_id = l.subject_id and scl.status = 'active'
    left join curriculum_sections cs
      on cs.id = l.section_id and cs.class_id = l.class_id and cs.subject_id = l.subject_id
    where l.id = ${expected.lessonId}
      and l.status = 'active'
      and l.published_at is not null
      and l.published_at <= now()
      and (l.section_id is null or cs.status = 'active')
  `;
  assert(readerEligibleLessons[0].count === 0, `student-reader eligible lesson rows=${readerEligibleLessons[0].count}`);

  // Mirrors the asset-delivery publication guards. No asset from this reviewed slice may be student-deliverable yet.
  const readerEligibleAssets = await sql`
    select count(*)::int count
    from lesson_assets la
    join lessons l on l.id = la.lesson_id
    join classes c on c.id = l.class_id and c.status = 'active'
    join subjects s on s.id = l.subject_id and s.status = 'active'
    join subject_class_links scl
      on scl.class_id = l.class_id and scl.subject_id = l.subject_id and scl.status = 'active'
    left join curriculum_sections cs
      on cs.id = l.section_id and cs.class_id = l.class_id and cs.subject_id = l.subject_id
    join media_assets ma on ma.id = la.media_asset_id and ma.status = 'ready'
    where l.id = ${expected.lessonId}
      and la.publication_status = 'published'
      and l.status = 'active'
      and l.published_at is not null
      and l.published_at <= now()
      and (l.section_id is null or cs.status = 'active')
  `;
  assert(readerEligibleAssets[0].count === 0, `student-reader eligible asset rows=${readerEligibleAssets[0].count}`);

  const targetQuestionLinks = await sql`
    select count(*)::int count
    from question_bank_revision_lessons
    where lesson_id = ${expected.lessonId}
  `;
  assert(targetQuestionLinks[0].count === 0, `unauthorized target question links=${targetQuestionLinks[0].count}`);

  const legacyQuestions = await sql`
    select r.id, r.published_at, rl.lesson_id
    from question_bank_revisions r
    join question_bank_revision_lessons rl on rl.revision_id = r.id
    where rl.lesson_id in ${sql(legacyLessonIds)}
  `;
  assert(legacyQuestions.length === 12, `preserved legacy question revisions=${legacyQuestions.length}`);
  assert(legacyQuestions.every((q) => q.published_at === null), 'legacy question publication drift');

  const duplicateIdentities = await sql`
    select
      (select count(*)::int from curriculum_sections where class_id = ${classId} and subject_id = ${subjectId} and slug = ${expected.sectionSlug}) section_count,
      (select count(*)::int from lessons where class_id = ${classId} and subject_id = ${subjectId} and slug = ${expected.lessonSlug}) lesson_count
  `;
  assert(duplicateIdentities[0].section_count === 1, `section duplicate count=${duplicateIdentities[0].section_count}`);
  assert(duplicateIdentities[0].lesson_count === 1, `lesson duplicate count=${duplicateIdentities[0].lesson_count}`);

  console.log('VERIFY001_PASS', JSON.stringify({
    task: 'VERIFY-001',
    scope: 'Grade 9 English / Unit 2 / Describing people and animals / pages 5..8',
    sectionId: expected.sectionId,
    lessonId: expected.lessonId,
    lessonContentRevision: Number(lesson.content_revision),
    exactAssets: assets.length,
    readyMediaAssets: assets.filter((a) => a.media_status === 'ready').length,
    exactProvenanceAssets: assets.filter((a, i) => a.source_path === pages[i].path && a.source_checksum === pages[i].sha256 && a.source_checksum_sha256 === pages[i].sha256).length,
    draftUnpublishedAssets: assets.filter((a) => a.publication_status === 'draft' && a.asset_published_at === null).length,
    studentReaderEligibleLessons: readerEligibleLessons[0].count,
    studentReaderEligibleAssets: readerEligibleAssets[0].count,
    unauthorizedTargetQuestionLinks: targetQuestionLinks[0].count,
    preservedLegacyQuestionRevisions: legacyQuestions.length,
    publicationMutation: 0,
    rawMutation: 0,
    mediaBinaryMutation: 0,
    questionMutation: 0,
  }));
} finally {
  await sql.end({ timeout: 1 });
}
