import postgres from 'postgres';

const databaseUrl = process.env.DATABASE_URL;
if (!databaseUrl) throw new Error('DATABASE_URL is required');
const sql = postgres(databaseUrl, { max: 1, connect_timeout: 15, idle_timeout: 5, prepare: false });
const ROLLBACK = 'G9_U2_QUESTION_EXPECTED_ROLLBACK';

const targetSlugs = {
  describing: 'curated-english9-pb3-u2-describing-people-and-animals',
  time: 'curated-english9-pb3-u2-time-and-meeting',
};

const pages = [
  { page:5, target:'describing', initialLink:'none', candidate:'fa9da9ae20399803687f', path:'public.lessons/706771c2-2145-4682-9bdd-4e7df5c69bf9/image/0', sha:'fc9e15f23d3f5c9a7928aecc70888e30be2c454ab16883e1a3c82290fd581fdb', questions:[
    ['The first person described weighs 79 kilos.',['True','False'],0],
    ['What colour are his eyes?',['brown','blue','green','black'],0],
    ['What is the weight of the tall, slim person described first?',['79 kilos','40 kilos','90 kilos','46 kilos'],0],
  ]},
  { page:6, target:'describing', initialLink:'none', candidate:'4beeaad26a5b1e608d26', path:'public.lessons/71ba9a99-e009-401f-b65f-8a956218a633/image/0', sha:'fd99f85698dd4870bf8fccf85aa53f47bf484d19b2052473155540627f6aa420', questions:[
    ['Which person has a bad memory?',['Tom','Simon','Jim','John'],0],
  ]},
  { page:7, target:'describing', initialLink:'none', candidate:'151a2c4ae5b692970b7d', path:'public.lessons/710cb3d4-e2c1-4d05-a1ef-2c0a1bbede2b/image/0', sha:'3b7415622af90557ad09585eef776b5ce3fe2c68776a1963b4a2cbf677f5ba61', questions:[
    ['Ali weighs 27 kilos.',['False','True'],0],
    ["Hassan's favourite bird is the black stork.",['True','False'],0],
    ['How much does Ali weigh?',['63 kilos','27 kilos','55 kilos','60 kilos'],0],
    ["What is Fatma's hair like?",['long and black','short and fair','long and fair','short and black'],0],
    ["What is Hassan's favourite bird?",['the black stork','the eagle','the falcon','the parrot'],0],
  ]},
  { page:8, target:'describing', initialLink:'none', candidate:'d27c56c43ab65d4691ff', path:'public.lessons/4b6090c2-744e-4fc6-8908-87c211a8713b/image/0', sha:'3678974564e2a219840da4fc175d62d9811bd80666d01c81d4f9b49f2328e258', questions:[
    ['The animal described has a long tail.',['True','False'],0],
    ['What colour is the animal described?',['brown','white','black','grey'],0],
    ['What does the animal eat?',['fruit and nuts','grass and leaves','fish and meat','seeds and insects'],0],
  ]},
  { page:9, target:'time', initialLink:'legacy', candidate:'15ac9f56ef455c22bc33', path:'public.lessons/b2449f0f-71f1-4e36-a739-cf64340f9c90/image/0', sha:'28ad2275248bb707102b4025d97d083d1da7685730fd2772034383b8d9df7208', questions:[
    ["How is 12:15 expressed in the lesson?",["It’s quarter past twelve.","It’s half past twelve.","It’s quarter to twelve.","It’s fifteen to one."],0],
    ['How many minutes are there in an hour?',['sixty','thirty','fifteen','twenty'],0],
    ['How many minutes are there in half an hour?',['thirty','sixty','fifteen','forty-five'],0],
    ['There are sixty minutes in an hour.',['True','False'],0],
  ]},
  { page:10, target:'time', initialLink:'legacy', candidate:'a6f1884b4bce0b65e763', path:'public.lessons/75616176-b12d-47bb-bb6e-34cc3f902901/image/0', sha:'2a05b5dcb686f4de391ec22c297fdab382d7506c1bbe3281d63caa96bcd8d36f', questions:[
    ['Football is scheduled at 5.15.',['True','False'],0],
    ['What time is the football activity on the schedule?',['5.15','5.00','6.30','7.45'],0],
    ['When is Rashid meeting mentioned in the dialogue?',["at six o'clock","at five o'clock","at seven o'clock","at eight o'clock"],0,'When is Fuad helping Dad on Saturday?'],
  ]},
];

function assert(c,m){ if(!c) throw new Error(`G9_U2_QUESTION_MIGRATION_FAIL: ${m}`); }
function same(a,b){ return JSON.stringify(a)===JSON.stringify(b); }
assert(pages.reduce((n,p)=>n+p.questions.length,0)===19,'static question count');

async function resolve(q,{lock=false}={}){
  const scope=lock
    ? await q`select c.id class_id,s.id subject_id from classes c join subject_class_links x on x.class_id=c.id join subjects s on s.id=x.subject_id where c.slug='grade-9' and s.slug='english' and c.status='active' and s.status='active' and x.status='active' for update of x`
    : await q`select c.id class_id,s.id subject_id from classes c join subject_class_links x on x.class_id=c.id join subjects s on s.id=x.subject_id where c.slug='grade-9' and s.slug='english' and c.status='active' and s.status='active' and x.status='active'`;
  assert(scope.length===1,`scope=${scope.length}`);
  const {class_id:classId,subject_id:subjectId}=scope[0];

  const targetRows=await q`select id,slug,status,published_at from lessons where class_id=${classId} and subject_id=${subjectId} and slug in ${q(Object.values(targetSlugs))}`;
  assert(targetRows.length===2,`target lessons=${targetRows.length}`);
  const targetByKey={};
  for(const [key,slug] of Object.entries(targetSlugs)){
    const row=targetRows.find(x=>x.slug===slug);
    assert(row?.status==='active' && row.published_at===null,`target ${key} state`);
    targetByKey[key]=row;
    if(lock){ const r=await q`select id from lessons where id=${row.id} for update`; assert(r.length===1,`target ${key} lock`); }
  }

  const legacyRows=await q`
    select l.id,l.slug,l.section_id,l.status,l.published_at,count(la.id)::int asset_count
    from lessons l left join lesson_assets la on la.lesson_id=l.id
    where l.class_id=${classId} and l.subject_id=${subjectId}
      and l.slug in ${q(pages.map(p=>`legacy-sb-${p.candidate}`))}
    group by l.id,l.slug,l.section_id,l.status,l.published_at
  `;
  assert(legacyRows.length===6,`legacy lessons=${legacyRows.length}`);
  assert(legacyRows.every(x=>x.status==='active'&&x.published_at===null&&x.section_id===null&&x.asset_count===0),'legacy lesson state drift');
  const legacyBySlug=new Map(legacyRows.map(x=>[x.slug,x]));

  const resultPages=[];
  for(const page of pages){
    const source=await q`select id from content_source_assets where source_path=${page.path} and checksum_sha256=${page.sha} and is_present=true`;
    assert(source.length===1,`page ${page.page} source count=${source.length}`);
    const sourceId=source[0].id;
    const revisions=await q`
      select r.id,r.prompt,r.options,r.correct_option_index,r.answer_text,r.status,r.published_at,
             rl.lesson_id
      from question_bank_revision_sources rs
      join question_bank_revisions r on r.id=rs.revision_id
      left join question_bank_revision_lessons rl on rl.revision_id=r.id
      where rs.content_source_asset_id=${sourceId}
      order by r.id,rl.lesson_id nulls first
    `;
    assert(revisions.length===page.questions.length,`page ${page.page} revision/link rows=${revisions.length}, expected=${page.questions.length}`);
    assert(new Set(revisions.map(x=>x.id)).size===page.questions.length,`page ${page.page} has duplicate/multiple lesson links`);
    assert(revisions.every(x=>x.status==='draft'&&x.published_at===null),`page ${page.page} published/non-draft revision`);

    const targetLessonId=targetByKey[page.target].id;
    const legacyLesson=legacyBySlug.get(`legacy-sb-${page.candidate}`);
    assert(legacyLesson,`page ${page.page} legacy lesson missing`);
    const matched=[];
    for(const spec of page.questions){
      const [oldPrompt,options,index,newPrompt]=spec;
      const valid=newPrompt?[oldPrompt,newPrompt]:[oldPrompt];
      const rows=revisions.filter(x=>valid.includes(x.prompt));
      assert(rows.length===1,`page ${page.page} prompt locator ${oldPrompt}`);
      const row=rows[0];
      assert(same(row.options,options),`page ${page.page} options drift ${row.prompt}`);
      assert(row.correct_option_index===index,`page ${page.page} answer index drift ${row.prompt}`);
      matched.push({...row,oldPrompt,newPrompt:newPrompt??null,targetLessonId,legacyLessonId:legacyLesson.id,expectedInitialLink:page.initialLink});
    }
    resultPages.push({...page,sourceId,targetLessonId,legacyLessonId:legacyLesson.id,revisions:matched});
  }
  const all=resultPages.flatMap(p=>p.revisions);
  assert(all.length===19 && new Set(all.map(x=>x.id)).size===19,`global revisions=${all.length}`);
  const qrs=await q`select revision_id,content_source_asset_id from question_bank_revision_sources where revision_id in ${q(all.map(x=>x.id))} order by revision_id,content_source_asset_id`;
  assert(qrs.length===19 && new Set(qrs.map(x=>x.revision_id)).size===19,`provenance rows=${qrs.length}`);
  const [linkCount]=await q`select count(*)::int c from question_bank_revision_lessons`;
  return {classId,subjectId,targetByKey,resultPages,all,qrs,totalLinkRows:linkCount.c};
}

function classify(state){
  let none=0,legacy=0,target=0,wrong=0;
  for(const r of state.all){
    if(r.lesson_id===null) none++;
    else if(r.lesson_id===r.targetLessonId) target++;
    else if(r.lesson_id===r.legacyLessonId) legacy++;
    else wrong++;
  }
  const corrected=state.all.find(x=>x.newPrompt);
  assert(corrected,'corrected question not found');
  const prompt=corrected.prompt===corrected.oldPrompt?'legacy':corrected.prompt===corrected.newPrompt?'corrected':'drift';
  if(none===0&&legacy===0&&target===19&&wrong===0&&prompt==='corrected') return {mode:'applied',none,legacy,target,wrong,prompt};
  if(none===12&&legacy===7&&target===0&&wrong===0&&prompt==='legacy') return {mode:'legacy',none,legacy,target,wrong,prompt};
  return {mode:'mixed',none,legacy,target,wrong,prompt};
}

function assertExpectedInitialLinks(state){
  for(const r of state.all){
    if(r.expectedInitialLink==='none') assert(r.lesson_id===null,`revision ${r.id} expected no initial link`);
    else assert(r.lesson_id===r.legacyLessonId,`revision ${r.id} expected legacy link`);
  }
}

async function mutateLinks(q,state){
  let inserts=0,updates=0;
  for(const r of state.all){
    if(r.lesson_id===null){
      const added=await q`insert into question_bank_revision_lessons(revision_id,lesson_id) values(${r.id},${r.targetLessonId}) returning revision_id`;
      assert(added.length===1,`insert link revision=${r.id}`); inserts++;
    }else{
      const moved=await q`update question_bank_revision_lessons set lesson_id=${r.targetLessonId} where revision_id=${r.id} and lesson_id=${r.legacyLessonId} returning revision_id`;
      assert(moved.length===1,`update link revision=${r.id}`); updates++;
    }
  }
  assert(inserts===12&&updates===7,`link mutation inserts=${inserts}, updates=${updates}`);
  return {inserts,updates};
}

async function mutatePrompt(q,state){
  const r=state.all.find(x=>x.newPrompt);
  if(r.prompt===r.newPrompt) return 0;
  const changed=await q`update question_bank_revisions set prompt=${r.newPrompt} where id=${r.id} and prompt=${r.oldPrompt} and status='draft' and published_at is null returning id`;
  assert(changed.length===1,'corrected prompt update count');
  return 1;
}

async function verifyApplied(q,beforeProvenance){
  const s=await resolve(q);
  const c=classify(s);
  assert(c.mode==='applied',`verified state=${JSON.stringify(c)}`);
  assert(s.all.filter(x=>x.lesson_id===s.targetByKey.describing.id).length===12,'describing links !=12');
  assert(s.all.filter(x=>x.lesson_id===s.targetByKey.time.id).length===7,'time links !=7');
  assert(s.all.every(x=>x.status==='draft'&&x.published_at===null),'publication/status drift');
  assert(same(s.qrs,beforeProvenance),'provenance changed');
  return s;
}

const initial=await resolve(sql);
const ic=classify(initial);
if(ic.mode==='applied'){
  await verifyApplied(sql,initial.qrs);
  console.log('G9_U2_QUESTION_MIGRATION_ALREADY_VERIFIED',JSON.stringify({reviewed:19,approvedUnchanged:18,corrected:1,linkInserts:12,linkUpdates:7,describingLinks:12,timeLinks:7,publicationChanges:0,provenanceChanges:0}));
  console.log('G9_U2_QUESTION_MIGRATION_FULL_PASS',JSON.stringify({status:'COMMITTED_STATE_VERIFIED'}));
  await sql.end({timeout:1}); process.exit(0);
}
assert(ic.mode==='legacy',`initial state=${JSON.stringify(ic)}`);
assertExpectedInitialLinks(initial);
const snapshot={qrs:initial.qrs,totalLinkRows:initial.totalLinkRows,links:initial.all.map(x=>[x.id,x.lesson_id]).sort(),prompt:initial.all.find(x=>x.newPrompt).prompt};

let gate;
try{
  await sql.begin(async tx=>{
    await tx`set local lock_timeout='5s'`; await tx`set local statement_timeout='60s'`;
    const state=await resolve(tx,{lock:true});
    assert(classify(state).mode==='legacy','gate input drift'); assertExpectedInitialLinks(state);
    const links=await mutateLinks(tx,state);
    const promptUpdates=await mutatePrompt(tx,state);
    const inside=await resolve(tx);
    const cc=classify(inside); assert(cc.mode==='applied',`gate post mutation=${JSON.stringify(cc)}`);
    assert(inside.totalLinkRows===state.totalLinkRows+12,`gate link row delta=${inside.totalLinkRows-state.totalLinkRows}`);
    assert(same(inside.qrs,state.qrs),'gate provenance changed');
    gate={...links,promptUpdates,reviewed:19,approvedUnchanged:18,corrected:1,publicationChanges:0,provenanceChanges:0,rawMutations:0,mediaMutations:0};
    throw new Error(ROLLBACK);
  });
}catch(e){
  if(e?.message!==ROLLBACK){ console.error(e?.stack||e); await sql.end({timeout:1}); process.exit(1); }
}

const rb=await resolve(sql); const rbc=classify(rb);
assert(rbc.mode==='legacy',`rollback state=${JSON.stringify(rbc)}`); assertExpectedInitialLinks(rb);
assert(rb.totalLinkRows===snapshot.totalLinkRows,'rollback total link rows drift');
assert(same(rb.qrs,snapshot.qrs),'rollback provenance drift');
assert(rb.all.find(x=>x.newPrompt).prompt===snapshot.prompt,'rollback prompt drift');
console.log('G9_U2_QUESTION_TRANSACTION_GATE_PASS',JSON.stringify({...gate,rollbackVerified:true,committedBusinessWrites:0}));

await sql.begin(async tx=>{
  await tx`set local lock_timeout='5s'`; await tx`set local statement_timeout='60s'`;
  const state=await resolve(tx,{lock:true}); const c=classify(state);
  if(c.mode==='applied') return;
  assert(c.mode==='legacy',`apply input=${JSON.stringify(c)}`); assertExpectedInitialLinks(state);
  await mutateLinks(tx,state); await mutatePrompt(tx,state);
  const inside=await resolve(tx); assert(classify(inside).mode==='applied','apply in-transaction verify');
  assert(inside.totalLinkRows===state.totalLinkRows+12,'apply link row delta');
});
console.log('G9_U2_QUESTION_APPLY_PASS',JSON.stringify({reviewed:19,approvedUnchanged:18,corrected:1,linkInserts:12,linkUpdates:7,revisionTextUpdates:1,publicationChanges:0,provenanceChanges:0}));

const verified=await verifyApplied(sql,snapshot.qrs);
assert(verified.totalLinkRows===snapshot.totalLinkRows+12,`final link row delta=${verified.totalLinkRows-snapshot.totalLinkRows}`);
const corrected=verified.all.find(x=>x.newPrompt);
console.log('G9_U2_QUESTION_VERIFY_PASS',JSON.stringify({reviewed:19,approvedUnchanged:18,corrected:1,correctedRevisionId:corrected.id,correctedPrompt:corrected.prompt,linkInserts:12,linkUpdates:7,describingLinks:12,timeLinks:7,sourceProvenanceRows:19,publishedRevisions:0,publicationChanges:0,rawMutations:0,mediaMutations:0}));
console.log('G9_U2_QUESTION_MIGRATION_FULL_PASS',JSON.stringify({status:'COMMITTED_STATE_VERIFIED'}));
await sql.end({timeout:1});
