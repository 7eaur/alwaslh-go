import postgres from 'postgres';

const sql = postgres(process.env.DATABASE_URL, {
  max: 1,
  connect_timeout: 15,
  idle_timeout: 5,
  prepare: false,
});

const lessons = [
  {
    legacyPageId: '2d98475c-91bf-4000-bfbc-79f7a6a854f9', position: 0, page: 1,
    legacySlug: 'legacy-sb-2d53aec17e54f46db304',
    slug: 'curated-english9-pb3-u1-p001-presents-from-london', title: 'Presents from London',
    sourcePath: 'public.lessons/2d98475c-91bf-4000-bfbc-79f7a6a854f9/image/0',
    rawPath: 'تاسع انجليزي/الانجليزي_تاسع/الصور/p001 - Presents from London.jpg',
    sha: 'ae3e89be65d1c9ec5f70e361a5e78ea903d6e305f22d399e2c88bf864f6c3a4f',
  },
  {
    legacyPageId: '5e207993-508f-426b-ae71-f00aa4f782df', position: 1, page: 2,
    legacySlug: 'legacy-sb-908a58f8e7b25f82c787',
    slug: 'curated-english9-pb3-u1-p002-whats-my-job', title: "What's my job?",
    sourcePath: 'public.lessons/5e207993-508f-426b-ae71-f00aa4f782df/image/0',
    rawPath: "تاسع انجليزي/الانجليزي_تاسع/الصور/p002 - What's my job -.jpg",
    sha: '1df05a27195e28e5543747c1f827a4d32c2bf937476c91ae69b0f4fe8b61b413',
  },
  {
    legacyPageId: 'dc1d6249-c0cb-4982-9711-092b1dcffee3', position: 2, page: 3,
    legacySlug: 'legacy-sb-4e1131b5222334610174',
    slug: 'curated-english9-pb3-u1-p003-the-holidays', title: 'The holidays',
    sourcePath: 'public.lessons/dc1d6249-c0cb-4982-9711-092b1dcffee3/image/0',
    rawPath: 'تاسع انجليزي/الانجليزي_تاسع/الصور/p003 - The holidays.jpg',
    sha: '78741ebd493e6b7dbbc05115472fec173edbeab9e05079b806a61acd1d7d13ac',
  },
  {
    legacyPageId: 'f2947d7f-5697-4bdc-b561-ad880a1afdf1', position: 3, page: 4,
    legacySlug: 'legacy-sb-840f23a0e0a98aaa674e',
    slug: 'curated-english9-pb3-u1-p004-a-postcard-from-london', title: 'A postcard from London',
    sourcePath: 'public.lessons/f2947d7f-5697-4bdc-b561-ad880a1afdf1/image/0',
    rawPath: 'تاسع انجليزي/الانجليزي_تاسع/الصور/p004 - A postcard from London.jpg',
    sha: '86d655468bfbc73248da92e0d16d4b4dcccc0217df241e69bac94f6cee6cf321',
  },
];

const questions = [
  [0, 0, 'How old is Saleh?', 'approved', 'multiple_choice', 'How old is Saleh?', null, null],
  [0, 1, 'Saleh is seventeen years old.', 'approved', 'true_false', 'Saleh is seventeen years old.', null, null],
  [0, 2, 'What does Mr Al Sabri want to buy for Saleh?', 'corrected', 'multiple_choice', 'What does Mr Al Sabri suggest Taha buy for Saleh?', ['a pair of shorts','a school uniform','a bicycle','a camera'], 0],
  [0, 3, 'What does Saleh like?', 'approved', 'multiple_choice', 'What does Saleh like?', null, null],
  [1, 0, 'Taha works in a clinic.', 'corrected', 'true_false', 'The dentist works in a clinic.', null, null],
  [1, 1, "What is Taha's job?", 'corrected', 'multiple_choice', "What is the job of the person who takes care of people's teeth?", ['a dentist','a teacher','a doctor','a police officer'], 0],
  [1, 2, 'What time does the office worker start work?', 'approved', 'multiple_choice', 'What time does the office worker start work?', null, null],
  [1, 3, 'Where does the doctor work?', 'corrected', 'multiple_choice', 'Where does the dentist work?', ['in a clinic','in an office','in a hospital','in a school'], 0],
  [2, 0, 'The family went to London for the holidays.', 'corrected', 'true_false', 'One speaker went to a village by the sea in the holidays.', null, null],
  [2, 1, 'What did Amna do every day?', 'corrected', 'multiple_choice', 'What did the first speaker do every day?', ['went swimming and fishing','stayed at home','went shopping','worked on a farm'], 0],
  [2, 2, 'Where did Mr Al Sabri and his family go on holiday?', 'corrected', 'multiple_choice', 'Where did the first speaker go in the holidays?', ['a village by the sea','London','Paris',"Sana'a"], 0],
  [3, 0, 'Amna wrote a postcard to Mariam.', 'approved', 'true_false', 'Amna wrote a postcard to Mariam.', null, null],
  [3, 1, 'What did Amna write to Mariam?', 'approved', 'multiple_choice', 'What did Amna write to Mariam?', null, null],
];

function assert(condition, message) {
  if (!condition) throw new Error(`GATE_FAIL: ${message}`);
}

const rollbackSentinel = 'BATCH001_EXPECTED_ROLLBACK';
let passSummary = null;

try {
  await sql.begin(async (tx) => {
    await tx`set local lock_timeout = '5s'`;
    await tx`set local statement_timeout = '60s'`;

    const scope = await tx`
      select c.id as class_id, s.id as subject_id
      from classes c
      join subjects s on s.slug = 'english'
      join subject_class_links scl on scl.class_id = c.id and scl.subject_id = s.id
      where c.slug = 'grade-9' and c.status = 'active' and s.status = 'active' and scl.status = 'active'
      for update of scl
    `;
    assert(scope.length === 1, `expected 1 active grade-9/english offering, got ${scope.length}`);
    const { class_id: classId, subject_id: subjectId } = scope[0];

    // The RAW extraction path is documentary evidence only. PostgreSQL canonical source identity for
    // the legacy importer is public.lessons/<legacy page UUID>/image/0 plus the immutable byte SHA-256.
    const resolvedLessons = [];
    for (let lessonIndex = 0; lessonIndex < lessons.length; lessonIndex++) {
      const e = lessons[lessonIndex];
      const rows = await tx`
        select l.id as lesson_id, l.class_id, l.subject_id, l.slug as current_slug,
               l.title as current_title, l.position as current_position, l.section_id,
               l.status, l.published_at, la.id as lesson_asset_id, ma.id as media_asset_id,
               csa.id as source_asset_id
        from content_source_assets csa
        join media_assets ma on ma.content_source_asset_id = csa.id
        join lesson_assets la on la.media_asset_id = ma.id
        join lessons l on l.id = la.lesson_id
        where csa.is_present = true
          and csa.source_path = ${e.sourcePath}
          and csa.checksum_sha256 = ${e.sha}
          and ma.source_checksum_sha256 = ${e.sha}
          and ma.status = 'ready'
          and la.publication_status = 'draft'
          and la.asset_published_at is null
      `;
      assert(rows.length === 1, `source ${e.sourcePath} resolved ${rows.length} modern lessons; expected exactly 1`);
      const row = rows[0];
      assert(row.class_id === classId && row.subject_id === subjectId, `resolved lesson ${row.lesson_id} scope mismatch`);
      assert(row.status === 'active' && row.published_at === null, `resolved lesson ${row.lesson_id} is not active+unpublished`);
      assert(row.current_slug === e.legacySlug, `resolved lesson ${row.lesson_id} legacy slug drift: ${row.current_slug}`);
      const locked = await tx`select id from lessons where id = ${row.lesson_id} for update`;
      assert(locked.length === 1, `could not lock resolved lesson ${row.lesson_id}`);
      resolvedLessons.push({ ...e, lessonIndex, lessonId: row.lesson_id, sourceAssetId: row.source_asset_id });
    }
    assert(new Set(resolvedLessons.map((x) => x.lessonId)).size === 4, 'four sources did not resolve to four unique modern lessons');

    const lessonIds = resolvedLessons.map((x) => x.lessonId);
    const existingSection = await tx`
      select id from curriculum_sections
      where class_id = ${classId} and subject_id = ${subjectId}
        and slug = 'curated-english9-pb3-unit-1-revision'
    `;
    assert(existingSection.length === 0, `expected section absent before apply, got ${existingSection.length}`);

    const slugCollisions = await tx`
      select id, slug from lessons
      where class_id = ${classId} and subject_id = ${subjectId}
        and slug in ${tx(lessons.map((x) => x.slug))}
        and id not in ${tx(lessonIds)}
    `;
    assert(slugCollisions.length === 0, `target lesson slug collision count ${slugCollisions.length}`);

    const allDraft = await tx`
      select r.id, r.prompt, r.type, r.options, r.correct_option_index, r.answer_text,
             r.status, r.published_at, rl.lesson_id
      from question_bank_revisions r
      join question_bank_revision_lessons rl on rl.revision_id = r.id
      where rl.lesson_id in ${tx(lessonIds)} and r.status = 'draft' and r.published_at is null
      for update of r
    `;
    assert(allDraft.length === 13, `expected exactly 13 draft question revisions, got ${allDraft.length}`);

    const resolvedQuestions = [];
    for (const q of questions) {
      const [lessonIndex, sourceIndex, currentPrompt, decision, targetType, targetPrompt, targetOptions, targetIndex] = q;
      const lesson = resolvedLessons[lessonIndex];
      const matches = allDraft.filter((r) => r.lesson_id === lesson.lessonId && r.prompt === currentPrompt);
      assert(matches.length === 1, `question locator page${lesson.page}/${sourceIndex} resolved ${matches.length} rows`);
      const rev = matches[0];
      const source = await tx`
        select revision_id
        from question_bank_revision_sources
        where revision_id = ${rev.id}
          and page_number = ${lesson.page}
          and input_checksum_sha256 = ${lesson.sha}
          and content_source_asset_id = ${lesson.sourceAssetId}
      `;
      assert(source.length === 1, `question ${rev.id} provenance count ${source.length}`);
      resolvedQuestions.push({ rev, lesson, sourceIndex, decision, targetType, targetPrompt, targetOptions, targetIndex });
    }
    assert(new Set(resolvedQuestions.map((x) => x.rev.id)).size === 13, 'reviewed locators do not map to 13 unique revisions');
    assert(resolvedQuestions.filter((x) => x.decision === 'corrected').length === 7, 'correction count is not 7');

    const [section] = await tx`
      insert into curriculum_sections (class_id, subject_id, slug, title, position, status)
      values (${classId}, ${subjectId}, 'curated-english9-pb3-unit-1-revision', 'Unit 1 - Revision', 1, 'active')
      returning id
    `;

    let lessonUpdates = 0;
    for (const e of resolvedLessons) {
      const rows = await tx`
        update lessons
        set section_id = ${section.id}, slug = ${e.slug}, title = ${e.title}, position = ${e.position}
        where id = ${e.lessonId}
        returning id
      `;
      lessonUpdates += rows.length;
    }
    assert(lessonUpdates === 4, `lesson update count ${lessonUpdates}, expected 4`);

    let questionUpdates = 0;
    for (const x of resolvedQuestions.filter((r) => r.decision === 'corrected')) {
      let rows;
      if (x.targetOptions) {
        const answer = x.targetOptions[x.targetIndex];
        rows = await tx`
          update question_bank_revisions
          set type = ${x.targetType}::question_bank_question_type,
              prompt = ${x.targetPrompt}, options = ${tx.json(x.targetOptions)},
              correct_option_index = ${x.targetIndex}, answer_text = ${answer}
          where id = ${x.rev.id}
          returning id
        `;
      } else {
        rows = await tx`
          update question_bank_revisions
          set type = ${x.targetType}::question_bank_question_type, prompt = ${x.targetPrompt}
          where id = ${x.rev.id}
          returning id
        `;
      }
      questionUpdates += rows.length;
    }
    assert(questionUpdates === 7, `question update count ${questionUpdates}, expected 7`);

    const postLessons = await tx`
      select l.id, l.slug, l.title, l.position, l.published_at, cs.slug as section_slug
      from lessons l join curriculum_sections cs on cs.id = l.section_id
      where l.id in ${tx(lessonIds)}
    `;
    assert(postLessons.length === 4, `post lesson count ${postLessons.length}`);
    for (const row of postLessons) {
      const e = resolvedLessons.find((x) => x.lessonId === row.id);
      assert(row.slug === e.slug && row.title === e.title && row.position === e.position, `post lesson ${row.id} target mismatch`);
      assert(row.published_at === null && row.section_slug === 'curated-english9-pb3-unit-1-revision', `post lesson ${row.id} publication/section mismatch`);
    }

    let correctedPostCount = 0;
    for (const x of resolvedQuestions.filter((r) => r.decision === 'corrected')) {
      const [row] = await tx`
        select prompt, type, options, correct_option_index, answer_text, status, published_at
        from question_bank_revisions where id = ${x.rev.id}
      `;
      assert(row.prompt === x.targetPrompt && row.type === x.targetType, `post question ${x.rev.id} text/type mismatch`);
      assert(row.status === 'draft' && row.published_at === null, `post question ${x.rev.id} publication changed`);
      if (x.targetOptions) {
        assert(JSON.stringify(row.options) === JSON.stringify(x.targetOptions), `post question ${x.rev.id} options mismatch`);
        assert(row.correct_option_index === x.targetIndex && row.answer_text === x.targetOptions[x.targetIndex], `post question ${x.rev.id} answer mismatch`);
      }
      correctedPostCount++;
    }

    const [publishedAssets] = await tx`
      select count(*)::int as count from lesson_assets
      where lesson_id in ${tx(lessonIds)}
        and (publication_status <> 'draft' or asset_published_at is not null)
    `;
    assert(publishedAssets.count === 0, 'lesson asset publication invariant changed');

    const corrected = resolvedQuestions.filter((x) => x.decision === 'corrected');
    passSummary = {
      scope: 'grade-9/english',
      lessonIdentityMode: 'canonical_content_source_path+sha256->media->lesson_asset->lesson',
      rawPathRole: 'documentary_only_immutable',
      resolvedLessonIds: resolvedLessons.map((x) => x.lessonId),
      correctedRevisionIds: corrected.map((x) => x.rev.id),
      correctedOriginalPrompts: corrected.map((x) => x.rev.prompt),
      sectionInserts: 1,
      lessonUpdates,
      questionUpdates,
      questionNoops: 6,
      correctedPostCount,
      auditRowsRequiredBySchema: 0,
      publicationChanges: 0,
      unrelatedRows: 0,
      expectedRollback: true,
    };
    console.log('BATCH001_GATE_MUTATION_PHASE_PASS', JSON.stringify(passSummary));
    throw new Error(rollbackSentinel);
  });
} catch (error) {
  if (error?.message !== rollbackSentinel) {
    console.error('BATCH001_GATE_FAIL', error?.stack || error);
    await sql.end({ timeout: 1 });
    process.exit(1);
  }
}

const [post] = await sql`
  select count(*)::int as section_count
  from curriculum_sections cs
  join classes c on c.id = cs.class_id
  join subjects s on s.id = cs.subject_id
  where c.slug = 'grade-9' and s.slug = 'english'
    and cs.slug = 'curated-english9-pb3-unit-1-revision'
`;
assert(post.section_count === 0, `rollback verification expected target section count 0, got ${post.section_count}`);

let postRollbackLessonCount = 0;
for (let i = 0; i < lessons.length; i++) {
  const [row] = await sql`select slug, section_id, published_at from lessons where id = ${passSummary.resolvedLessonIds[i]}`;
  assert(row?.slug === lessons[i].legacySlug && row.section_id === null && row.published_at === null,
    `rollback verification failed for lesson ${passSummary.resolvedLessonIds[i]}`);
  postRollbackLessonCount++;
}

let postRollbackQuestionCount = 0;
for (let i = 0; i < passSummary.correctedRevisionIds.length; i++) {
  const [row] = await sql`select prompt, status, published_at from question_bank_revisions where id = ${passSummary.correctedRevisionIds[i]}`;
  assert(row?.prompt === passSummary.correctedOriginalPrompts[i] && row.status === 'draft' && row.published_at === null,
    `rollback verification failed for question revision ${passSummary.correctedRevisionIds[i]}`);
  postRollbackQuestionCount++;
}

console.log('BATCH001_GATE_PASS_ROLLBACK_VERIFIED', JSON.stringify({
  ...passSummary,
  postRollbackSectionCount: post.section_count,
  postRollbackLessonCount,
  postRollbackQuestionCount,
}));
await sql.end({ timeout: 1 });
