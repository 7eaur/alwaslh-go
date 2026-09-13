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
  { order: 0, path: 'public.lessons/706771c2-2145-4682-9bdd-4e7df5c69bf9/image/0', sha256: 'fc9e15f23d3f5c9a7928aecc70888e30be2c454ab16883e1a3c82290fd581fdb' },
  { order: 1, path: 'public.lessons/71ba9a99-e009-401f-b65f-8a956218a633/image/0', sha256: 'fd99f85698dd4870bf8fccf85aa53f47bf484d19b2052473155540627f6aa420' },
  { order: 2, path: 'public.lessons/710cb3d4-e2c1-4d05-a1ef-2c0a1bbede2b/image/0', sha256: '3b7415622af90557ad09585eef776b5ce3fe2c68776a1963b4a2cbf677f5ba61' },
  { order: 3, path: 'public.lessons/4b6090c2-744e-4fc6-8908-87c211a8713b/image/0', sha256: '3678974564e2a219840da4fc175d62d9811bd80666d01c81d4f9b49f2328e258' },
];

function assert(condition, message) {
  if (!condition) throw new Error(`IMPORT001_VERIFY_FAIL: ${message}`);
}

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
  select id, title, position, status
  from curriculum_sections
  where class_id = ${classId} and subject_id = ${subjectId} and slug = ${targetSection.slug}
`;
assert(sections.length === 1, `target section count=${sections.length}`);
const section = sections[0];
assert(section.title === targetSection.title && section.position === targetSection.position && section.status === 'active', 'target section fields mismatch');

const lessons = await sql`
  select id, section_id, title, position, status, published_at
  from lessons
  where class_id = ${classId} and subject_id = ${subjectId} and slug = ${targetLesson.slug}
`;
assert(lessons.length === 1, `target lesson count=${lessons.length}`);
const lesson = lessons[0];
assert(lesson.section_id === section.id, 'target lesson section mismatch');
assert(lesson.title === targetLesson.title && lesson.position === targetLesson.position && lesson.status === 'active', 'target lesson fields mismatch');
assert(lesson.published_at === null, 'target lesson unexpectedly published');

const assets = await sql`
  select la.id lesson_asset_id, la.position, la.publication_status, la.asset_published_at,
         ma.id media_asset_id, ma.status media_status, ma.source_checksum_sha256,
         csa.id source_asset_id, csa.source_path, csa.checksum_sha256, csa.is_present
  from lesson_assets la
  join media_assets ma on ma.id = la.media_asset_id
  join content_source_assets csa on csa.id = ma.content_source_asset_id
  where la.lesson_id = ${lesson.id}
  order by la.position
`;
assert(assets.length === 4, `target lesson asset count=${assets.length}`);
for (let i = 0; i < assets.length; i++) {
  const a = assets[i];
  const p = pages[i];
  assert(a.position === i, `asset position mismatch at ${i}`);
  assert(a.source_path === p.path, `source path mismatch at ${i}`);
  assert(a.checksum_sha256 === p.sha256 && a.source_checksum_sha256 === p.sha256 && a.is_present === true, `checksum/presence mismatch at ${i}`);
  assert(a.media_status === 'ready', `media status mismatch at ${i}`);
  assert(a.publication_status === 'draft' && a.asset_published_at === null, `asset publication mismatch at ${i}`);
}
assert(new Set(assets.map((x) => x.lesson_asset_id)).size === 4, 'lesson asset identities are not unique');
assert(new Set(assets.map((x) => x.media_asset_id)).size === 4, 'media asset identities are not unique');
assert(new Set(assets.map((x) => x.source_asset_id)).size === 4, 'source asset identities are not unique');

const legacyLessonRows = await sql`
  select distinct l.id
  from lessons l
  join question_bank_revision_lessons rl on rl.lesson_id = l.id
  join question_bank_revisions r on r.id = rl.revision_id
  where l.class_id = ${classId} and l.subject_id = ${subjectId}
    and l.id <> ${lesson.id}
    and r.published_at is null
    and exists (
      select 1 from question_bank_revision_lessons rl2
      where rl2.lesson_id = l.id
    )
    and not exists (
      select 1 from lesson_assets la2 where la2.lesson_id = l.id
    )
`;

const linkedQuestions = await sql`
  select r.id, rl.lesson_id, r.status, r.published_at
  from question_bank_revisions r
  join question_bank_revision_lessons rl on rl.revision_id = r.id
  where rl.lesson_id in ${sql(legacyLessonRows.map((x) => x.id))}
`;
const sourceQuestionRows = linkedQuestions.filter((q) => q.published_at === null);
assert(sourceQuestionRows.length >= 12, `preserved unpublished legacy question revisions below expected floor: ${sourceQuestionRows.length}`);

const targetQuestionLinks = await sql`
  select count(*)::int count
  from question_bank_revision_lessons
  where lesson_id = ${lesson.id}
`;
assert(targetQuestionLinks[0].count === 0, `target lesson received unauthorized question links count=${targetQuestionLinks[0].count}`);

console.log('IMPORT001_POST_APPLY_VERIFY_PASS', JSON.stringify({
  task: 'IMPORT-001',
  targetSectionId: section.id,
  targetLessonId: lesson.id,
  targetAssets: assets.length,
  readyMediaAssets: assets.filter((x) => x.media_status === 'ready').length,
  draftUnpublishedAssets: assets.filter((x) => x.publication_status === 'draft' && x.asset_published_at === null).length,
  targetPublished: lesson.published_at !== null,
  unauthorizedTargetQuestionLinks: targetQuestionLinks[0].count,
  preservedLegacyQuestionRevisionFloor: sourceQuestionRows.length,
}));

await sql.end({ timeout: 1 });
