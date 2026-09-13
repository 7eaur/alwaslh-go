import postgres from 'postgres';

const databaseUrl = process.env.DATABASE_URL;
if (!databaseUrl) throw new Error('DATABASE_URL is required');
const sql = postgres(databaseUrl, { max: 1, connect_timeout: 15, idle_timeout: 5, prepare: false });

const targetSectionSlug = 'curated-english9-pb3-unit-2-describing-making-plans';
const targetLesson = {
  slug: 'curated-english9-pb3-u2-time-and-meeting',
  title: 'Telling time and arranging a meeting',
  position: 8,
};
const sourceLegacyLessonIds = [
  '10919a45-a96d-4aa1-9ec9-3640f326665a',
  'abb6441f-9be5-4511-b5da-d00e5958aeec',
];
const expectedAssets = [
  { position: 0, path: 'public.lessons/b2449f0f-71f1-4e36-a739-cf64340f9c90/image/0', sha256: '28ad2275248bb707102b4025d97d083d1da7685730fd2772034383b8d9df7208' },
  { position: 1, path: 'public.lessons/75616176-b12d-47bb-bb6e-34cc3f902901/image/0', sha256: '2a05b5dcb686f4de391ec22c297fdab382d7506c1bbe3281d63caa96bcd8d36f' },
];

function assert(condition, message) {
  if (!condition) throw new Error(`CURATION002_RECONCILE_FAIL: ${message}`);
}

const scope = await sql`
  select c.id class_id, s.id subject_id
  from classes c
  join subject_class_links scl on scl.class_id = c.id
  join subjects s on s.id = scl.subject_id
  where c.slug = 'grade-9' and s.slug = 'english'
    and c.status = 'active' and s.status = 'active' and scl.status = 'active'
`;
assert(scope.length === 1, `scope count=${scope.length}`);
const { class_id: classId, subject_id: subjectId } = scope[0];

const sections = await sql`
  select id, title, position, status
  from curriculum_sections
  where class_id = ${classId} and subject_id = ${subjectId} and slug = ${targetSectionSlug}
`;
assert(sections.length === 1, `section count=${sections.length}`);
const section = sections[0];
assert(section.title === 'Unit 2 - Describing: Making plans' && section.status === 'active', 'section identity/status drift');

const targets = await sql`
  select id, title, position, status, published_at, section_id
  from lessons
  where class_id = ${classId} and subject_id = ${subjectId} and slug = ${targetLesson.slug}
`;
assert(targets.length === 1, `target lesson count=${targets.length}`);
const target = targets[0];
assert(target.title === targetLesson.title, `target title=${target.title}`);
assert(target.position === targetLesson.position, `target position=${target.position}`);
assert(target.status === 'active' && target.published_at === null, 'target status/publication drift');
assert(target.section_id === section.id, 'target section drift');

const assets = await sql`
  select la.id lesson_asset_id, la.position, la.publication_status, la.asset_published_at,
         ma.id media_asset_id, ma.status media_status, ma.source_checksum_sha256,
         csa.id source_asset_id, csa.source_path, csa.checksum_sha256, csa.is_present
  from lesson_assets la
  join media_assets ma on ma.id = la.media_asset_id
  join content_source_assets csa on csa.id = ma.content_source_asset_id
  where la.lesson_id = ${target.id}
  order by la.position
`;
assert(assets.length === 2, `target asset count=${assets.length}`);
for (let i = 0; i < expectedAssets.length; i++) {
  const actual = assets[i];
  const expected = expectedAssets[i];
  assert(actual.position === expected.position, `asset ${i} position=${actual.position}`);
  assert(actual.source_path === expected.path, `asset ${i} path=${actual.source_path}`);
  assert(actual.checksum_sha256 === expected.sha256 && actual.source_checksum_sha256 === expected.sha256, `asset ${i} checksum drift`);
  assert(actual.is_present === true && actual.media_status === 'ready', `asset ${i} presence/media status drift`);
  assert(actual.publication_status === 'draft' && actual.asset_published_at === null, `asset ${i} publication drift`);
}

const legacy = await sql`
  select l.id, l.slug, l.title, l.section_id, l.status, l.published_at, count(la.id)::int asset_count
  from lessons l
  left join lesson_assets la on la.lesson_id = l.id
  where l.id in ${sql(sourceLegacyLessonIds)}
  group by l.id, l.slug, l.title, l.section_id, l.status, l.published_at
  order by l.id
`;
assert(legacy.length === 2, `legacy lesson count=${legacy.length}`);
assert(legacy.every((x) => x.status === 'active' && x.published_at === null), 'legacy status/publication drift');
assert(legacy.every((x) => x.section_id === null), `legacy lessons still sectioned=${JSON.stringify(legacy.map(x => ({id:x.id, sectionId:x.section_id})))}`);
assert(legacy.every((x) => x.asset_count === 0), `legacy lessons still own assets=${JSON.stringify(legacy.map(x => ({id:x.id, assets:x.asset_count})))}`);

const questions = await sql`
  select r.id revision_id, rl.lesson_id, r.status, r.published_at
  from question_bank_revisions r
  join question_bank_revision_lessons rl on rl.revision_id = r.id
  where rl.lesson_id in ${sql(sourceLegacyLessonIds)}
  order by r.id, rl.lesson_id
`;
assert(questions.length === 7, `preserved question revisions=${questions.length}`);
assert(questions.every((q) => q.published_at === null), 'preserved question publication drift');

const targetQuestionLinks = await sql`
  select count(*)::int count
  from question_bank_revision_lessons
  where lesson_id = ${target.id}
`;
assert(targetQuestionLinks[0].count === 0, `unauthorized target question links=${targetQuestionLinks[0].count}`);

const published = await sql`
  select
    count(*) filter (where l.published_at is not null)::int published_lessons,
    count(*) filter (where la.publication_status <> 'draft' or la.asset_published_at is not null)::int published_assets
  from lessons l
  left join lesson_assets la on la.lesson_id = l.id
  where l.id = ${target.id}
  group by l.id
`;
assert(published.length === 1 && published[0].published_lessons === 0 && published[0].published_assets === 0, 'publication invariant changed');

console.log('CURATION002_RECONCILE_PASS', JSON.stringify({
  status: 'COMMITTED_STATE_VERIFIED',
  targetLessonId: target.id,
  targetLessonSlug: targetLesson.slug,
  pages: [9, 10],
  targetAssets: 2,
  legacyLessonsPreserved: 2,
  preservedQuestionRevisions: 7,
  targetQuestionLinks: 0,
  publicationChanges: 0,
  provenanceVerified: 2,
}));
console.log('CURATION002_FULL_PASS', JSON.stringify({ task: 'CURATION-002-STRUCTURAL-IMPORT', status: 'COMMITTED_STATE_VERIFIED' }));
await sql.end({ timeout: 1 });
