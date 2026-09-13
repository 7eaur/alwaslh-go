import postgres from 'postgres';

const databaseUrl = process.env.DATABASE_URL;
if (!databaseUrl) throw new Error('DATABASE_URL is required');

const sql = postgres(databaseUrl, { max: 1, connect_timeout: 15, idle_timeout: 5, prepare: false });
const rollbackSentinel = 'CURATION002_EXPECTED_ROLLBACK';

const targetSection = {
  slug: 'curated-english9-pb3-unit-2-describing-making-plans',
  title: 'Unit 2 - Describing: Making plans',
};
const targetLesson = {
  slug: 'curated-english9-pb3-u2-time-and-meeting',
  title: 'Telling time and arranging a meeting',
  position: 8,
};
const pages = [
  {
    order: 0,
    bookPage: 9,
    legacyPageId: 'b2449f0f-71f1-4e36-a739-cf64340f9c90',
    path: 'public.lessons/b2449f0f-71f1-4e36-a739-cf64340f9c90/image/0',
    sha256: '28ad2275248bb707102b4025d97d083d1da7685730fd2772034383b8d9df7208',
  },
  {
    order: 1,
    bookPage: 10,
    legacyPageId: '75616176-b12d-47bb-bb6e-34cc3f902901',
    path: 'public.lessons/75616176-b12d-47bb-bb6e-34cc3f902901/image/0',
    sha256: '2a05b5dcb686f4de391ec22c297fdab382d7506c1bbe3281d63caa96bcd8d36f',
  },
];

function assert(condition, message) {
  if (!condition) throw new Error(`CURATION002_FAIL: ${message}`);
}

async function resolveScope(q, lock = false) {
  const rows = lock
    ? await q`
        select c.id class_id, s.id subject_id
        from classes c
        join subject_class_links scl on scl.class_id = c.id
        join subjects s on s.id = scl.subject_id
        where c.slug = 'grade-9' and s.slug = 'english'
          and c.status = 'active' and s.status = 'active' and scl.status = 'active'
        for update of scl
      `
    : await q`
        select c.id class_id, s.id subject_id
        from classes c
        join subject_class_links scl on scl.class_id = c.id
        join subjects s on s.id = scl.subject_id
        where c.slug = 'grade-9' and s.slug = 'english'
          and c.status = 'active' and s.status = 'active' and scl.status = 'active'
      `;
  assert(rows.length === 1, `grade-9/english scope count=${rows.length}`);
  return rows[0];
}

async function resolveSection(q, classId, subjectId, lock = false) {
  const rows = lock
    ? await q`
        select id, title, position, status
        from curriculum_sections
        where class_id = ${classId} and subject_id = ${subjectId} and slug = ${targetSection.slug}
        for update
      `
    : await q`
        select id, title, position, status
        from curriculum_sections
        where class_id = ${classId} and subject_id = ${subjectId} and slug = ${targetSection.slug}
      `;
  assert(rows.length === 1, `target section count=${rows.length}`);
  assert(rows[0].title === targetSection.title && rows[0].status === 'active', 'target section identity/status drift');
  return rows[0];
}

async function resolveSources(q, classId, subjectId, sectionId, lock = false) {
  const resolved = [];
  for (const page of pages) {
    const rows = await q`
      select csa.id source_asset_id, csa.source_path, csa.checksum_sha256, csa.is_present,
             ma.id media_asset_id, ma.status media_status, ma.source_checksum_sha256,
             la.id lesson_asset_id, la.lesson_id, la.position lesson_asset_position,
             la.publication_status, la.asset_published_at,
             l.slug source_lesson_slug, l.title source_lesson_title, l.position source_lesson_position,
             l.status source_lesson_status, l.published_at source_lesson_published_at, l.section_id source_section_id
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
    assert(rows.length === 1, `page ${page.bookPage} source chain count=${rows.length}`);
    const row = rows[0];
    assert(row.publication_status === 'draft' && row.asset_published_at === null, `page ${page.bookPage} asset publication drift`);
    assert(row.source_lesson_status === 'active' && row.source_lesson_published_at === null, `page ${page.bookPage} source lesson publication/status drift`);
    assert(row.source_section_id === sectionId, `page ${page.bookPage} source section drift`);
    if (lock) {
      const assetLock = await q`select id from lesson_assets where id = ${row.lesson_asset_id} for update`;
      const lessonLock = await q`select id from lessons where id = ${row.lesson_id} for update`;
      assert(assetLock.length === 1 && lessonLock.length === 1, `page ${page.bookPage} lock failure`);
    }
    resolved.push({ ...page, ...row });
  }
  assert(new Set(resolved.map((x) => x.lesson_id)).size === 2, 'source lessons are not unique');
  assert(new Set(resolved.map((x) => x.lesson_asset_id)).size === 2, 'source lesson assets are not unique');
  assert(new Set(resolved.map((x) => x.media_asset_id)).size === 2, 'source media assets are not unique');
  return resolved.sort((a, b) => a.order - b.order);
}

async function sourceQuestions(q, lessonIds) {
  return q`
    select r.id, rl.lesson_id, r.status, r.published_at
    from question_bank_revisions r
    join question_bank_revision_lessons rl on rl.revision_id = r.id
    where rl.lesson_id in ${q(lessonIds)}
    order by r.id, rl.lesson_id
  `;
}

async function assertTargetAbsent(q, classId, subjectId) {
  const rows = await q`
    select id from lessons
    where class_id = ${classId} and subject_id = ${subjectId} and slug = ${targetLesson.slug}
  `;
  assert(rows.length === 0, `target lesson already exists count=${rows.length}`);
}

let rollbackSnapshot;
let gateSummary;

try {
  await sql.begin(async (tx) => {
    await tx`set local lock_timeout = '5s'`;
    await tx`set local statement_timeout = '60s'`;

    const { class_id: classId, subject_id: subjectId } = await resolveScope(tx, true);
    const section = await resolveSection(tx, classId, subjectId, true);
    await assertTargetAbsent(tx, classId, subjectId);
    const sources = await resolveSources(tx, classId, subjectId, section.id, true);
    const sourceLessonIds = sources.map((x) => x.lesson_id);
    const beforeQuestions = await sourceQuestions(tx, sourceLessonIds);
    assert(beforeQuestions.length === 7, `expected 7 preserved question revisions, got ${beforeQuestions.length}`);
    assert(beforeQuestions.every((q) => q.published_at === null), 'source question publication drift');

    rollbackSnapshot = {
      assets: sources.map((x) => ({ id: x.lesson_asset_id, lessonId: x.lesson_id, position: x.lesson_asset_position })),
      lessons: sources.map((x) => ({ id: x.lesson_id, sectionId: x.source_section_id })),
      questions: beforeQuestions,
    };

    const [lesson] = await tx`
      insert into lessons (class_id, subject_id, section_id, slug, title, position, status, published_at)
      values (${classId}, ${subjectId}, ${section.id}, ${targetLesson.slug}, ${targetLesson.title}, ${targetLesson.position}, 'active', null)
      returning id
    `;

    for (const source of sources) {
      const moved = await tx`
        update lesson_assets
        set lesson_id = ${lesson.id}, position = ${source.order}
        where id = ${source.lesson_asset_id}
          and lesson_id = ${source.lesson_id}
          and publication_status = 'draft'
          and asset_published_at is null
        returning id
      `;
      assert(moved.length === 1, `page ${source.bookPage} dry-run asset move count=${moved.length}`);
    }

    const unsectioned = await tx`
      update lessons
      set section_id = null
      where id in ${tx(sourceLessonIds)}
        and section_id = ${section.id}
        and published_at is null
      returning id
    `;
    assert(unsectioned.length === 2, `dry-run unsectioned source lesson count=${unsectioned.length}`);

    const targetAssets = await tx`
      select la.position, la.publication_status, la.asset_published_at,
             csa.source_path, csa.checksum_sha256, ma.status media_status
      from lesson_assets la
      join media_assets ma on ma.id = la.media_asset_id
      join content_source_assets csa on csa.id = ma.content_source_asset_id
      where la.lesson_id = ${lesson.id}
      order by la.position
    `;
    assert(targetAssets.length === 2, `dry-run target asset count=${targetAssets.length}`);
    for (let i = 0; i < 2; i++) {
      assert(targetAssets[i].position === i, `dry-run target asset position mismatch at ${i}`);
      assert(targetAssets[i].source_path === pages[i].path && targetAssets[i].checksum_sha256 === pages[i].sha256, `dry-run target provenance mismatch at ${i}`);
      assert(targetAssets[i].media_status === 'ready' && targetAssets[i].publication_status === 'draft' && targetAssets[i].asset_published_at === null, `dry-run target publication/media drift at ${i}`);
    }

    const afterQuestions = await sourceQuestions(tx, sourceLessonIds);
    assert(JSON.stringify(afterQuestions) === JSON.stringify(beforeQuestions), 'dry-run source questions changed');

    const targetQuestionLinks = await tx`
      select count(*)::int count
      from question_bank_revision_lessons
      where lesson_id = ${lesson.id}
    `;
    assert(targetQuestionLinks[0].count === 0, `dry-run target question links=${targetQuestionLinks[0].count}`);

    gateSummary = {
      mode: 'rollback-only',
      task: 'CURATION-002-STRUCTURAL-IMPORT',
      targetLesson,
      movedAssets: 2,
      preservedSourceLessons: 2,
      preservedQuestionRevisions: 7,
      questionMutations: 0,
      publicationChanges: 0,
      rawMutations: 0,
      mediaMutations: 0,
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

{
  const { class_id: classId, subject_id: subjectId } = await resolveScope(sql, false);
  await assertTargetAbsent(sql, classId, subjectId);
  for (const asset of rollbackSnapshot.assets) {
    const rows = await sql`select lesson_id, position from lesson_assets where id = ${asset.id}`;
    assert(rows.length === 1 && rows[0].lesson_id === asset.lessonId && rows[0].position === asset.position, `post-rollback asset ${asset.id} drift`);
  }
  for (const lesson of rollbackSnapshot.lessons) {
    const rows = await sql`select section_id from lessons where id = ${lesson.id}`;
    assert(rows.length === 1 && rows[0].section_id === lesson.sectionId, `post-rollback source lesson ${lesson.id} drift`);
  }
  const questions = await sourceQuestions(sql, rollbackSnapshot.lessons.map((x) => x.id));
  assert(JSON.stringify(questions) === JSON.stringify(rollbackSnapshot.questions), 'post-rollback question drift');
}
console.log('CURATION002_TRANSACTION_GATE_PASS', JSON.stringify({ ...gateSummary, rollbackVerified: true, committedBusinessWrites: 0 }));

let applied;
await sql.begin(async (tx) => {
  await tx`set local lock_timeout = '5s'`;
  await tx`set local statement_timeout = '60s'`;

  const { class_id: classId, subject_id: subjectId } = await resolveScope(tx, true);
  const section = await resolveSection(tx, classId, subjectId, true);
  await assertTargetAbsent(tx, classId, subjectId);
  const sources = await resolveSources(tx, classId, subjectId, section.id, true);
  const sourceLessonIds = sources.map((x) => x.lesson_id);
  const beforeQuestions = await sourceQuestions(tx, sourceLessonIds);
  assert(beforeQuestions.length === 7 && beforeQuestions.every((q) => q.published_at === null), 'apply question invariant drift');

  const [lesson] = await tx`
    insert into lessons (class_id, subject_id, section_id, slug, title, position, status, published_at)
    values (${classId}, ${subjectId}, ${section.id}, ${targetLesson.slug}, ${targetLesson.title}, ${targetLesson.position}, 'active', null)
    returning id
  `;

  for (const source of sources) {
    const moved = await tx`
      update lesson_assets
      set lesson_id = ${lesson.id}, position = ${source.order}
      where id = ${source.lesson_asset_id}
        and lesson_id = ${source.lesson_id}
        and publication_status = 'draft'
        and asset_published_at is null
      returning id
    `;
    assert(moved.length === 1, `page ${source.bookPage} apply asset move count=${moved.length}`);
  }

  const unsectioned = await tx`
    update lessons
    set section_id = null
    where id in ${tx(sourceLessonIds)}
      and section_id = ${section.id}
      and published_at is null
    returning id
  `;
  assert(unsectioned.length === 2, `apply unsectioned source lesson count=${unsectioned.length}`);

  const afterQuestions = await sourceQuestions(tx, sourceLessonIds);
  assert(JSON.stringify(afterQuestions) === JSON.stringify(beforeQuestions), 'apply source questions changed');

  applied = {
    targetLessonId: lesson.id,
    sourceLessonIds,
    sourceLessonAssets: sources.map((x) => x.lesson_asset_id),
    preservedQuestionRevisions: beforeQuestions.length,
  };
});
console.log('CURATION002_APPLY_PASS', JSON.stringify({ task: 'CURATION-002-STRUCTURAL-IMPORT', ...applied, publicationChanges: 0, questionMutations: 0, rawMutations: 0, mediaMutations: 0 }));

{
  const { class_id: classId, subject_id: subjectId } = await resolveScope(sql, false);
  const section = await resolveSection(sql, classId, subjectId, false);
  const target = await sql`
    select id, title, position, status, published_at, section_id
    from lessons
    where class_id = ${classId} and subject_id = ${subjectId} and slug = ${targetLesson.slug}
  `;
  assert(target.length === 1, `verify target lesson count=${target.length}`);
  assert(target[0].id === applied.targetLessonId && target[0].title === targetLesson.title && target[0].position === targetLesson.position, 'verify target identity drift');
  assert(target[0].section_id === section.id && target[0].status === 'active' && target[0].published_at === null, 'verify target section/status/publication drift');

  const assets = await sql`
    select la.id, la.position, la.publication_status, la.asset_published_at,
           csa.source_path, csa.checksum_sha256, ma.status media_status
    from lesson_assets la
    join media_assets ma on ma.id = la.media_asset_id
    join content_source_assets csa on csa.id = ma.content_source_asset_id
    where la.lesson_id = ${target[0].id}
    order by la.position
  `;
  assert(assets.length === 2, `verify target asset count=${assets.length}`);
  for (let i = 0; i < 2; i++) {
    assert(assets[i].position === i, `verify asset position mismatch at ${i}`);
    assert(assets[i].source_path === pages[i].path && assets[i].checksum_sha256 === pages[i].sha256, `verify provenance mismatch at ${i}`);
    assert(assets[i].media_status === 'ready' && assets[i].publication_status === 'draft' && assets[i].asset_published_at === null, `verify asset status/publication drift at ${i}`);
  }

  const legacy = await sql`
    select l.id, l.section_id, l.status, l.published_at, count(la.id)::int asset_count
    from lessons l
    left join lesson_assets la on la.lesson_id = l.id
    where l.id in ${sql(applied.sourceLessonIds)}
    group by l.id, l.section_id, l.status, l.published_at
    order by l.id
  `;
  assert(legacy.length === 2, `verify source lesson count=${legacy.length}`);
  assert(legacy.every((x) => x.section_id === null && x.status === 'active' && x.published_at === null && x.asset_count === 0), 'verify source legacy lesson preservation drift');

  const questions = await sourceQuestions(sql, applied.sourceLessonIds);
  assert(questions.length === 7 && questions.every((q) => q.published_at === null), `verify preserved question count/publication drift count=${questions.length}`);
  const targetQuestionLinks = await sql`select count(*)::int count from question_bank_revision_lessons where lesson_id = ${target[0].id}`;
  assert(targetQuestionLinks[0].count === 0, `verify unauthorized target question links=${targetQuestionLinks[0].count}`);

  console.log('CURATION002_VERIFY_PASS', JSON.stringify({
    task: 'CURATION-002-STRUCTURAL-IMPORT',
    targetLessonId: target[0].id,
    pages: [9, 10],
    targetAssets: 2,
    sourceLegacyLessonsPreserved: 2,
    preservedQuestionRevisions: 7,
    targetQuestionLinks: 0,
    publicationChanges: 0,
    rawMutations: 0,
    mediaMutations: 0,
  }));
}

console.log('CURATION002_FULL_PASS', JSON.stringify({ task: 'CURATION-002-STRUCTURAL-IMPORT', status: 'COMMITTED_STATE_VERIFIED' }));
await sql.end({ timeout: 1 });
