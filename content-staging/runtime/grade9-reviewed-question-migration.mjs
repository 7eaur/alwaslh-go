import postgres from 'postgres';

const databaseUrl = process.env.DATABASE_URL;
if (!databaseUrl) throw new Error('DATABASE_URL is required');
const sql = postgres(databaseUrl, { max: 1, connect_timeout: 15, idle_timeout: 5, prepare: false });
const ROLLBACK = 'G9_U2_QUESTION_EXPECTED_ROLLBACK';

const targets = {
  describing: 'curated-english9-pb3-u2-describing-people-and-animals',
  time: 'curated-english9-pb3-u2-time-and-meeting',
};

const pages = [
  {
    page: 5, target: 'describing', candidate: 'fa9da9ae20399803687f',
    path: 'public.lessons/706771c2-2145-4682-9bdd-4e7df5c69bf9/image/0', sha: 'fc9e15f23d3f5c9a7928aecc70888e30be2c454ab16883e1a3c82290fd581fdb',
    questions: [
      ['The first person described weighs 79 kilos.', ['True','False'], 0],
      ['What colour are his eyes?', ['brown','blue','green','black'], 0],
      ['What is the weight of the tall, slim person described first?', ['79 kilos','40 kilos','90 kilos','46 kilos'], 0],
    ],
  },
  {
    page: 6, target: 'describing', candidate: '4beeaad26a5b1e608d26',
    path: 'public.lessons/71ba9a99-e009-401f-b65f-8a956218a633/image/0', sha: 'fd99f85698dd4870bf8fccf85aa53f47bf484d19b2052473155540627f6aa420',
    questions: [
      ['Which person has a bad memory?', ['Tom','Simon','Jim','John'], 0],
    ],
  },
  {
    page: 7, target: 'describing', candidate: '151a2c4ae5b692970b7d',
    path: 'public.lessons/710cb3d4-e2c1-4d05-a1ef-2c0a1bbede2b/image/0', sha: '3b7415622af90557ad09585eef776b5ce3fe2c68776a1963b4a2cbf677f5ba61',
    questions: [
      ['Ali weighs 27 kilos.', ['False','True'], 0],
      ["Hassan's favourite bird is the black stork.", ['True','False'], 0],
      ['How much does Ali weigh?', ['63 kilos','27 kilos','55 kilos','60 kilos'], 0],
      ["What is Fatma's hair like?", ['long and black','short and fair','long and fair','short and black'], 0],
      ["What is Hassan's favourite bird?", ['the black stork','the eagle','the falcon','the parrot'], 0],
    ],
  },
  {
    page: 8, target: 'describing', candidate: 'd27c56c43ab65d4691ff',
    path: 'public.lessons/4b6090c2-744e-4fc6-8908-87c211a8713b/image/0', sha: '3678974564e2a219840da4fc175d62d9811bd80666d01c81d4f9b49f2328e258',
    questions: [
      ['The animal described has a long tail.', ['True','False'], 0],
      ['What colour is the animal described?', ['brown','white','black','grey'], 0],
      ['What does the animal eat?', ['fruit and nuts','grass and leaves','fish and meat','seeds and insects'], 0],
    ],
  },
  {
    page: 9, target: 'time', candidate: '15ac9f56ef455c22bc33',
    path: 'public.lessons/b2449f0f-71f1-4e36-a739-cf64340f9c90/image/0', sha: '28ad2275248bb707102b4025d97d083d1da7685730fd2772034383b8d9df7208',
    questions: [
      ["How is 12:15 expressed in the lesson?", ["It’s quarter past twelve.","It’s half past twelve.","It’s quarter to twelve.","It’s fifteen to one."], 0],
      ['How many minutes are there in an hour?', ['sixty','thirty','fifteen','twenty'], 0],
      ['How many minutes are there in half an hour?', ['thirty','sixty','fifteen','forty-five'], 0],
      ['There are sixty minutes in an hour.', ['True','False'], 0],
    ],
  },
  {
    page: 10, target: 'time', candidate: 'a6f1884b4bce0b65e763',
    path: 'public.lessons/75616176-b12d-47bb-bb6e-34cc3f902901/image/0', sha: '2a05b5dcb686f4de391ec22c297fdab382d7506c1bbe3281d63caa96bcd8d36f',
    questions: [
      ['Football is scheduled at 5.15.', ['True','False'], 0],
      ['What time is the football activity on the schedule?', ['5.15','5.00','6.30','7.45'], 0],
      ['When is Rashid meeting mentioned in the dialogue?', ["at six o'clock","at five o'clock","at seven o'clock","at eight o'clock"], 0, 'When is Fuad helping Dad on Saturday?'],
    ],
  },
];

function assert(condition, message) {
  if (!condition) throw new Error(`G9_U2_QUESTION_MIGRATION_FAIL: ${message}`);
}
function sameJson(a, b) { return JSON.stringify(a) === JSON.stringify(b); }

const expectedCount = pages.reduce((n, p) => n + p.questions.length, 0);
assert(expectedCount === 19, `static expected question count=${expectedCount}`);

async function resolve(q, lock = false) {
  const scope = lock
    ? await q`select c.id class_id, s.id subject_id from classes c join subject_class_links scl on scl.class_id=c.id join subjects s on s.id=scl.subject_id where c.slug='grade-9' and s.slug='english' and c.status='active' and s.status='active' and scl.status='active' for update of scl`
    : await q`select c.id class_id, s.id subject_id from classes c join subject_class_links scl on scl.class_id=c.id join subjects s on s.id=scl.subject_id where c.slug='grade-9' and s.slug='english' and c.status='active' and s.status='active' and scl.status='active'`;
  assert(scope.length === 1, `scope count=${scope.length}`);
  const { class_id: classId, subject_id: subjectId } = scope[0];

  const lessonRows = await q`
    select id, slug, title, section_id, status, published_at
    from lessons
    where class_id=${classId} and subject_id=${subjectId}
      and slug in ${q(Object.values(targets))}
    order by slug
  `;
  assert(lessonRows.length === 2, `target lesson count=${lessonRows.length}`);
  const targetByKey = {};
  for (const [key, slug] of Object.entries(targets)) {
    const row = lessonRows.find((x) => x.slug === slug);
    assert(row && row.status === 'active' && row.published_at === null, `target ${key} missing/published`);
    targetByKey[key] = row;
    if (lock) {
      const locks = await q`select id from lessons where id=${row.id} for update`;
      assert(locks.length === 1, `target ${key} lock failure`);
    }
  }

  const resultPages = [];
  for (const page of pages) {
    const source = await q`
      select id, source_path, checksum_sha256, is_present
      from content_source_assets
      where source_path=${page.path} and checksum_sha256=${page.sha} and is_present=true
    `;
    assert(source.length === 1, `page ${page.page} source identity count=${source.length}`);
    const sourceId = source[0].id;

    const revisions = await q`
      select qbr.id, qbr.prompt, qbr.options, qbr.correct_option_index, qbr.answer_text,
             qbr.status, qbr.published_at,
             qrl.lesson_id
      from question_bank_revision_sources qrs
      join question_bank_revisions qbr on qbr.id=qrs.revision_id
      join question_bank_revision_lessons qrl on qrl.revision_id=qbr.id
      where qrs.content_source_asset_id=${sourceId}
      order by qbr.id
    `;
    assert(revisions.length === page.questions.length, `page ${page.page} linked revision rows=${revisions.length}, expected=${page.questions.length}`);
    assert(new Set(revisions.map((x) => x.id)).size === page.questions.length, `page ${page.page} revision/link uniqueness drift`);
    assert(revisions.every((x) => x.status === 'draft' && x.published_at === null), `page ${page.page} revision publication/status drift`);

    const matched = [];
    for (const expected of page.questions) {
      const [oldPrompt, options, correctIndex, newPrompt] = expected;
      const validPrompts = newPrompt ? [oldPrompt, newPrompt] : [oldPrompt];
      const candidates = revisions.filter((x) => validPrompts.includes(x.prompt));
      assert(candidates.length === 1, `page ${page.page} prompt locator drift: ${oldPrompt}`);
      const row = candidates[0];
      assert(sameJson(row.options, options), `page ${page.page} options drift: ${row.prompt}`);
      assert(row.correct_option_index === correctIndex, `page ${page.page} correct index drift: ${row.prompt}`);
      matched.push({ ...row, oldPrompt, newPrompt: newPrompt ?? null, targetLessonId: targetByKey[page.target].id });
    }
    assert(new Set(matched.map((x) => x.id)).size === page.questions.length, `page ${page.page} matched revision uniqueness drift`);
    resultPages.push({ ...page, sourceId, targetLessonId: targetByKey[page.target].id, revisions: matched });
  }

  const all = resultPages.flatMap((p) => p.revisions);
  assert(all.length === 19 && new Set(all.map((x) => x.id)).size === 19, `global revision count/uniqueness drift=${all.length}`);

  const sourceSlugs = pages.map((p) => `legacy-sb-${p.candidate}`);
  const legacy = await q`
    select l.id, l.slug, l.section_id, l.status, l.published_at, count(la.id)::int asset_count
    from lessons l
    left join lesson_assets la on la.lesson_id=l.id
    where l.class_id=${classId} and l.subject_id=${subjectId} and l.slug in ${q(sourceSlugs)}
    group by l.id,l.slug,l.section_id,l.status,l.published_at
    order by l.slug
  `;
  assert(legacy.length === 6, `legacy source lesson count=${legacy.length}`);
  assert(legacy.every((x) => x.status === 'active' && x.published_at === null && x.section_id === null && x.asset_count === 0), 'legacy source lesson state drift');

  const qrs = await q`
    select qrs.revision_id, qrs.content_source_asset_id
    from question_bank_revision_sources qrs
    where qrs.revision_id in ${q(all.map((x) => x.id))}
    order by qrs.revision_id, qrs.content_source_asset_id
  `;
  assert(qrs.length === 19, `provenance row count=${qrs.length}`);
  assert(new Set(qrs.map((x) => x.revision_id)).size === 19, 'provenance revision uniqueness drift');

  return { classId, subjectId, targetByKey, resultPages, all, legacy, qrs };
}

function classify(state) {
  let legacyLinks = 0;
  let targetLinks = 0;
  for (const row of state.all) {
    if (row.lesson_id === row.targetLessonId) targetLinks++;
    else legacyLinks++;
  }
  const corrected = state.all.find((x) => x.newPrompt);
  assert(corrected, 'corrected question not resolved');
  const promptState = corrected.prompt === corrected.oldPrompt ? 'legacy' : corrected.prompt === corrected.newPrompt ? 'corrected' : 'drift';
  if (targetLinks === 19 && legacyLinks === 0 && promptState === 'corrected') return 'applied';
  if (targetLinks === 0 && legacyLinks === 19 && promptState === 'legacy') return 'legacy';
  return `mixed(target=${targetLinks},legacy=${legacyLinks},prompt=${promptState})`;
}

async function verifyApplied(q, state) {
  const fresh = await resolve(q, false);
  const mode = classify(fresh);
  assert(mode === 'applied', `post state=${mode}`);
  const descCount = fresh.all.filter((x) => x.lesson_id === fresh.targetByKey.describing.id).length;
  const timeCount = fresh.all.filter((x) => x.lesson_id === fresh.targetByKey.time.id).length;
  assert(descCount === 12, `describing target links=${descCount}`);
  assert(timeCount === 7, `time target links=${timeCount}`);
  assert(sameJson(fresh.qrs, state.qrs), 'provenance rows changed');
  return fresh;
}

let initial = await resolve(sql, false);
let initialClass = classify(initial);
if (initialClass === 'applied') {
  await verifyApplied(sql, initial);
  console.log('G9_U2_QUESTION_MIGRATION_ALREADY_VERIFIED', JSON.stringify({ reviewed:19, approvedUnchanged:18, corrected:1, migratedLinks:19, describingLinks:12, timeLinks:7, publicationChanges:0, provenanceChanges:0 }));
  console.log('G9_U2_QUESTION_MIGRATION_FULL_PASS', JSON.stringify({ status:'COMMITTED_STATE_VERIFIED' }));
  await sql.end({ timeout: 1 });
  process.exit(0);
}
assert(initialClass === 'legacy', `initial state=${initialClass}`);

const snapshot = {
  links: initial.all.map((x) => ({ revisionId:x.id, lessonId:x.lesson_id })).sort((a,b) => a.revisionId.localeCompare(b.revisionId)),
  corrected: (() => { const x=initial.all.find((r)=>r.newPrompt); return { id:x.id, prompt:x.prompt }; })(),
  qrs: initial.qrs,
};

let gateSummary;
try {
  await sql.begin(async (tx) => {
    await tx`set local lock_timeout='5s'`;
    await tx`set local statement_timeout='60s'`;
    const state = await resolve(tx, true);
    assert(classify(state) === 'legacy', 'gate input no longer legacy');

    for (const row of state.all) {
      const moved = await tx`
        update question_bank_revision_lessons
        set lesson_id=${row.targetLessonId}
        where revision_id=${row.id} and lesson_id=${row.lesson_id}
        returning revision_id, lesson_id
      `;
      assert(moved.length === 1, `gate link move revision=${row.id}`);
    }
    const corrected = state.all.find((x) => x.newPrompt);
    const changed = await tx`
      update question_bank_revisions
      set prompt=${corrected.newPrompt}
      where id=${corrected.id} and prompt=${corrected.oldPrompt}
        and status='draft' and published_at is null
      returning id
    `;
    assert(changed.length === 1, 'gate corrected prompt update count');

    const inside = await resolve(tx, false);
    assert(classify(inside) === 'applied', `gate inside state=${classify(inside)}`);
    assert(sameJson(inside.qrs, state.qrs), 'gate provenance changed');

    gateSummary = { reviewed:19, approvedUnchanged:18, corrected:1, lessonLinkUpdates:19, revisionTextUpdates:1, publicationChanges:0, provenanceChanges:0, rawMutations:0, mediaMutations:0 };
    throw new Error(ROLLBACK);
  });
} catch (error) {
  if (error?.message !== ROLLBACK) {
    console.error(error?.stack || error);
    await sql.end({ timeout: 1 });
    process.exit(1);
  }
}

const rolledBack = await resolve(sql, false);
assert(classify(rolledBack) === 'legacy', `rollback state=${classify(rolledBack)}`);
const rbLinks = rolledBack.all.map((x) => ({ revisionId:x.id, lessonId:x.lesson_id })).sort((a,b) => a.revisionId.localeCompare(b.revisionId));
assert(sameJson(rbLinks, snapshot.links), 'post-rollback lesson links drift');
const rbCorrected = rolledBack.all.find((x) => x.id === snapshot.corrected.id);
assert(rbCorrected?.prompt === snapshot.corrected.prompt, 'post-rollback corrected prompt drift');
assert(sameJson(rolledBack.qrs, snapshot.qrs), 'post-rollback provenance drift');
console.log('G9_U2_QUESTION_TRANSACTION_GATE_PASS', JSON.stringify({ ...gateSummary, rollbackVerified:true, committedBusinessWrites:0 }));

await sql.begin(async (tx) => {
  await tx`set local lock_timeout='5s'`;
  await tx`set local statement_timeout='60s'`;
  const state = await resolve(tx, true);
  const current = classify(state);
  if (current === 'applied') return;
  assert(current === 'legacy', `apply input state=${current}`);

  for (const row of state.all) {
    const moved = await tx`
      update question_bank_revision_lessons
      set lesson_id=${row.targetLessonId}
      where revision_id=${row.id} and lesson_id=${row.lesson_id}
      returning revision_id
    `;
    assert(moved.length === 1, `apply link move revision=${row.id}`);
  }
  const corrected = state.all.find((x) => x.newPrompt);
  const changed = await tx`
    update question_bank_revisions
    set prompt=${corrected.newPrompt}
    where id=${corrected.id} and prompt=${corrected.oldPrompt}
      and status='draft' and published_at is null
    returning id
  `;
  assert(changed.length === 1, 'apply corrected prompt update count');
});
console.log('G9_U2_QUESTION_APPLY_PASS', JSON.stringify({ reviewed:19, approvedUnchanged:18, corrected:1, lessonLinkUpdates:19, revisionTextUpdates:1, publicationChanges:0, provenanceChanges:0 }));

const verified = await verifyApplied(sql, initial);
const corrected = verified.all.find((x) => x.newPrompt);
console.log('G9_U2_QUESTION_VERIFY_PASS', JSON.stringify({
  reviewed:19,
  approvedUnchanged:18,
  corrected:1,
  correctedRevisionId: corrected.id,
  correctedPrompt: corrected.prompt,
  migratedLinks:19,
  describingLinks:12,
  timeLinks:7,
  sourceProvenanceRows:19,
  publishedRevisions: verified.all.filter((x)=>x.published_at!==null).length,
  publicationChanges:0,
  rawMutations:0,
  mediaMutations:0,
}));
console.log('G9_U2_QUESTION_MIGRATION_FULL_PASS', JSON.stringify({ status:'COMMITTED_STATE_VERIFIED' }));
await sql.end({ timeout: 1 });
