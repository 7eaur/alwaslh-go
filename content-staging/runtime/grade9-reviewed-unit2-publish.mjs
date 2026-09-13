import postgres from 'postgres';

const databaseUrl = process.env.DATABASE_URL;
if (!databaseUrl) throw new Error('DATABASE_URL is required');
const sql = postgres(databaseUrl,{max:1,connect_timeout:15,idle_timeout:5,prepare:false});
const ROLLBACK='G9_U2_PUBLISH_EXPECTED_ROLLBACK';

const targets={
 describing:{slug:'curated-english9-pb3-u2-describing-people-and-animals',assetCount:4,questionCount:12},
 time:{slug:'curated-english9-pb3-u2-time-and-meeting',assetCount:2,questionCount:7},
};
const pages=[
 {page:5,key:'describing',legacy:'706771c2-2145-4682-9bdd-4e7df5c69bf9',prompts:['The first person described weighs 79 kilos.','What colour are his eyes?','What is the weight of the tall, slim person described first?']},
 {page:6,key:'describing',legacy:'71ba9a99-e009-401f-b65f-8a956218a633',prompts:['Which person has a bad memory?']},
 {page:7,key:'describing',legacy:'710cb3d4-e2c1-4d05-a1ef-2c0a1bbede2b',prompts:['Ali weighs 27 kilos.',"Hassan's favourite bird is the black stork.",'How much does Ali weigh?',"What is Fatma's hair like?","What is Hassan's favourite bird?"]},
 {page:8,key:'describing',legacy:'4b6090c2-744e-4fc6-8908-87c211a8713b',prompts:['The animal described has a long tail.','What colour is the animal described?','What does the animal eat?']},
 {page:9,key:'time',legacy:'b2449f0f-71f1-4e36-a739-cf64340f9c90',prompts:["How is 12:15 expressed in the lesson?",'How many minutes are there in an hour?','How many minutes are there in half an hour?','There are sixty minutes in an hour.']},
 {page:10,key:'time',legacy:'75616176-b12d-47bb-bb6e-34cc3f902901',prompts:['Football is scheduled at 5.15.','What time is the football activity on the schedule?','When is Rashid meeting mentioned in the dialogue?'],corrected:['When is Rashid meeting mentioned in the dialogue?','When is Fuad helping Dad on Saturday?']},
];
function ok(c,m){if(!c)throw new Error('G9_U2_PUBLISH_FAIL: '+m)}

async function scopeCounts(q,classId,subjectId){
 const [l]=await q`select count(*)::int c from lessons where class_id=${classId} and subject_id=${subjectId} and published_at is not null`;
 const [a]=await q`select count(*)::int c from lesson_assets la join lessons l on l.id=la.lesson_id where l.class_id=${classId} and l.subject_id=${subjectId} and la.publication_status='published'`;
 const [r]=await q`select count(*)::int c from question_bank_revisions r join question_bank_items i on i.id=r.item_id where i.class_id=${classId} and i.subject_id=${subjectId} and r.status='published'`;
 return {lessons:l.c,assets:a.c,questions:r.c};
}

async function resolve(q){
 const scope=await q`select c.id class_id,s.id subject_id from classes c join subject_class_links x on x.class_id=c.id join subjects s on s.id=x.subject_id where c.slug='grade-9' and s.slug='english' and c.status='active' and s.status='active' and x.status='active'`;
 ok(scope.length===1,'grade-9/english scope'); const {class_id:classId,subject_id:subjectId}=scope[0];
 const lessonRows=await q`select l.id,l.slug,l.title,l.content_revision,l.published_at,l.status,cs.status section_status from lessons l left join curriculum_sections cs on cs.id=l.section_id where l.class_id=${classId} and l.subject_id=${subjectId} and (l.slug=${targets.describing.slug} or l.slug=${targets.time.slug}) order by l.slug`;
 ok(lessonRows.length===2,'target lesson count '+lessonRows.length); const target={};
 for(const [key,t] of Object.entries(targets)){const l=lessonRows.find(x=>x.slug===t.slug);ok(l&&l.status==='active'&&l.section_status==='active','target lesson '+key);target[key]=l;}
 const assetRows=[];
 for(const [key,t] of Object.entries(targets)){
  const rows=await q`select la.id,la.lesson_id,la.position,la.publication_status::text publication_status,la.submitted_for_review_by_profile_id,la.submitted_for_review_at,la.published_by_profile_id,la.asset_published_at,la.checksum_sha256,ma.status::text media_status,csa.source_path,csa.checksum_sha256 source_checksum,csa.is_present from lesson_assets la join media_assets ma on ma.id=la.media_asset_id join content_source_assets csa on csa.id=ma.content_source_asset_id where la.lesson_id=${target[key].id} order by la.position,la.id`;
  ok(rows.length===t.assetCount,`${key} asset count ${rows.length}`);ok(rows.every(x=>x.media_status==='ready'&&x.is_present===true&&x.checksum_sha256&&x.source_checksum),`${key} asset readiness/provenance`);assetRows.push(...rows.map(x=>({...x,targetKey:key})));
 }
 ok(assetRows.length===6,'global asset count');
 const revisions=[];
 for(const p of pages){
  const path=`public.lessons/${p.legacy}/image/0`;
  const sources=await q`select id,checksum_sha256,is_present from content_source_assets where source_path=${path}`;ok(sources.length===1&&sources[0].is_present===true,`page ${p.page} source`);
  const rows=await q`select r.id,r.item_id,r.prompt,r.type::text type,r.options,r.correct_option_index,r.answer_text,r.answer_status::text answer_status,r.status::text status,r.created_by_profile_id,r.submitted_for_review_by_profile_id,r.submitted_for_review_at,r.published_by_profile_id,r.published_at,i.archived_at,coalesce(array_agg(rl.lesson_id order by rl.position) filter(where rl.lesson_id is not null),'{}') lesson_ids from question_bank_revision_sources rs join question_bank_revisions r on r.id=rs.revision_id join question_bank_items i on i.id=r.item_id left join question_bank_revision_lessons rl on rl.revision_id=r.id where rs.content_source_asset_id=${sources[0].id} group by r.id,i.archived_at order by r.id`;
  ok(rows.length===p.prompts.length,`page ${p.page} revision count ${rows.length}`);ok(rows.every(x=>x.answer_status==='known'&&x.archived_at===null&&x.lesson_ids.length===1),`page ${p.page} question eligibility`);
  const used=new Set();
  for(const prompt of p.prompts){const allowed=p.corrected&&prompt===p.corrected[0]?[p.corrected[0],p.corrected[1]]:[prompt];const matches=rows.filter(x=>allowed.includes(x.prompt)&&!used.has(x.id));ok(matches.length===1,`page ${p.page} prompt ${prompt}`);used.add(matches[0].id);revisions.push({...matches[0],page:p.page,targetKey:p.key,sourceId:sources[0].id,oldPrompt:prompt,newPrompt:p.corrected&&prompt===p.corrected[0]?p.corrected[1]:null});}
 }
 ok(revisions.length===19&&new Set(revisions.map(x=>x.id)).size===19,'global question uniqueness');
 const creators=[...new Set(revisions.map(x=>x.created_by_profile_id))];let actor=null;
 if(creators.length===1){const p=await q`select id from profiles where id=${creators[0]} and role='admin' and status='active'`;if(p.length===1)actor=p[0].id;}
 if(!actor){const admins=await q`select id from profiles where role='admin' and status='active' order by created_at,id`;ok(admins.length===1,`publisher actor ambiguous active_admins=${admins.length} creators=${creators.length}`);actor=admins[0].id;}
 const publishedForItems=[];for(const r of revisions){const rows=await q`select id from question_bank_revisions where item_id=${r.item_id} and status='published' and id<>${r.id}`;publishedForItems.push(...rows);}ok(publishedForItems.length===0,'existing published revisions for target items');
 return {classId,subjectId,target,assetRows,revisions,actor};
}

function classify(s){
 const lessonPublished=Object.values(s.target).filter(x=>x.published_at!==null).length;
 const assetPublished=s.assetRows.filter(x=>x.publication_status==='published').length;
 const assetDraft=s.assetRows.filter(x=>x.publication_status==='draft').length;
 const qPublished=s.revisions.filter(x=>x.status==='published').length;
 const qDraft=s.revisions.filter(x=>x.status==='draft').length;
 let targetLinks=0;for(const r of s.revisions)if(r.lesson_ids[0]===s.target[r.targetKey].id)targetLinks++;
 const corrected=s.revisions.find(x=>x.newPrompt);ok(corrected,'corrected question missing');const prompt=corrected.prompt===corrected.newPrompt?'corrected':corrected.prompt===corrected.oldPrompt?'legacy':'drift';
 if(lessonPublished===2&&assetPublished===6&&qPublished===19&&targetLinks===19&&prompt==='corrected')return'published';
 if(lessonPublished===0&&assetDraft===6&&qDraft===19&&(targetLinks===0||targetLinks===19)&&(prompt==='legacy'||prompt==='corrected'))return'ready';
 return`mixed lessons=${lessonPublished} assetsPub=${assetPublished} assetsDraft=${assetDraft} qPub=${qPublished} qDraft=${qDraft} links=${targetLinks} prompt=${prompt}`;
}

async function lockTarget(q,s){
 await q`select class_id from subject_class_links where class_id=${s.classId} and subject_id=${s.subjectId} for update`;
 for(const l of Object.values(s.target))await q`select id from lessons where id=${l.id} for update`;
 for(const a of s.assetRows)await q`select id from lesson_assets where id=${a.id} for update`;
 for(const r of s.revisions){await q`select id from question_bank_revisions where id=${r.id} for update`;await q`select revision_id from question_bank_revision_lessons where revision_id=${r.id} for update`;}
}

async function mutate(q,s){
 const actor=s.actor;
 for(const r of s.revisions){const targetId=s.target[r.targetKey].id;if(r.lesson_ids[0]!==targetId){const moved=await q`update question_bank_revision_lessons set lesson_id=${targetId} where revision_id=${r.id} and lesson_id=${r.lesson_ids[0]} returning revision_id`;ok(moved.length===1,'question link '+r.id);}}
 const corrected=s.revisions.find(x=>x.newPrompt);if(corrected.prompt===corrected.oldPrompt){const u=await q`update question_bank_revisions set prompt=${corrected.newPrompt} where id=${corrected.id} and prompt=${corrected.oldPrompt} returning id`;ok(u.length===1,'corrected prompt');}
 for(const a of s.assetRows){ok(a.publication_status==='draft','asset input '+a.id);await q`update lesson_assets set publication_status='review',submitted_for_review_by_profile_id=${actor},submitted_for_review_at=now() where id=${a.id}`;}
 for(const r of s.revisions){ok(r.status==='draft','question input '+r.id);await q`update question_bank_revisions set status='review',submitted_for_review_by_profile_id=${actor},submitted_for_review_at=now() where id=${r.id}`;await q`insert into question_bank_events(item_id,revision_id,action,actor_profile_id,note) values(${r.item_id},${r.id},'submit_review',${actor},'Reviewed Grade 9 Unit 2 content publication')`;}
 for(const [key,l] of Object.entries(s.target))await q`insert into curriculum_events(actor_profile_id,resource_type,resource_key,event_type,metadata) values(${actor},'lesson',${l.id},'lesson_content_submitted_for_review',${q.json({source:'reviewed-grade9-unit2',assetCount:targets[key].assetCount})})`;
 for(const a of s.assetRows)await q`update lesson_assets set publication_status='published',published_by_profile_id=${actor},asset_published_at=now() where id=${a.id} and publication_status='review'`;
 for(const l of Object.values(s.target))await q`update lessons set content_revision=content_revision+1,published_at=now() where id=${l.id} and published_at is null`;
 for(const r of s.revisions){await q`update question_bank_revisions set status='published',published_by_profile_id=${actor},published_at=now() where id=${r.id} and status='review'`;await q`insert into question_bank_events(item_id,revision_id,action,actor_profile_id,note) values(${r.item_id},${r.id},'publish',${actor},'Published after reviewed Grade 9 Unit 2 verification')`;}
 for(const [key,l] of Object.entries(s.target))await q`insert into curriculum_events(actor_profile_id,resource_type,resource_key,event_type,metadata) values(${actor},'lesson',${l.id},'lesson_content_published',${q.json({source:'reviewed-grade9-unit2',assetCount:targets[key].assetCount})})`;
}

async function verifyPublished(q,baseline){
 const s=await resolve(q);ok(classify(s)==='published','post state '+classify(s));
 ok(s.revisions.filter(x=>x.lesson_ids[0]===s.target.describing.id).length===12,'describing question links');ok(s.revisions.filter(x=>x.lesson_ids[0]===s.target.time.id).length===7,'time question links');
 const counts=await scopeCounts(q,s.classId,s.subjectId);ok(counts.lessons===baseline.lessons+2,`lesson publication delta ${counts.lessons-baseline.lessons}`);ok(counts.assets===baseline.assets+6,`asset publication delta ${counts.assets-baseline.assets}`);ok(counts.questions===baseline.questions+19,`question publication delta ${counts.questions-baseline.questions}`);
 const [reader]=await q`select count(*)::int lessons,count(la.id)::int assets from lessons l join curriculum_sections cs on cs.id=l.section_id and cs.status='active' left join lesson_assets la on la.lesson_id=l.id and la.publication_status='published' join media_assets ma on ma.id=la.media_asset_id and ma.status='ready' where (l.id=${s.target.describing.id} or l.id=${s.target.time.id}) and l.status='active' and l.published_at is not null and l.published_at<=now()`;ok(reader.lessons===6&&reader.assets===6,'reader asset eligibility');
 const [quiz]=await q`select count(*)::int c from question_bank_revisions r join question_bank_items i on i.id=r.item_id join question_bank_revision_lessons rl on rl.revision_id=r.id where (rl.lesson_id=${s.target.describing.id} or rl.lesson_id=${s.target.time.id}) and i.archived_at is null and r.status='published' and r.answer_status='known'`;ok(quiz.c===19,'quiz-builder eligibility '+quiz.c);
 return {state:s,counts,readerAssets:reader.assets,quizQuestions:quiz.c};
}

const initial=await resolve(sql);const initialMode=classify(initial);if(initialMode==='published'){console.log('G9_U2_PUBLISH_FULL_PASS',JSON.stringify({status:'COMMITTED_STATE_VERIFIED',lessons:2,assets:6,questions:19}));await sql.end({timeout:1});process.exit(0);}ok(initialMode==='ready','initial '+initialMode);const baseline=await scopeCounts(sql,initial.classId,initial.subjectId);const eventBaseline=(await sql`select count(*)::int c from question_bank_events`)[0].c;const curriculumEventBaseline=(await sql`select count(*)::int c from curriculum_events`)[0].c;
try{await sql.begin(async tx=>{const s=await resolve(tx);await lockTarget(tx,s);ok(classify(await resolve(tx))==='ready','gate locked input');await mutate(tx,s);await verifyPublished(tx,baseline);console.log('G9_U2_PUBLISH_GATE_PASS',JSON.stringify({lessons:2,assets:6,questions:19,questionLinkMoves:s.revisions.filter(r=>r.lesson_ids[0]!==s.target[r.targetKey].id).length,questionCorrections:s.revisions.filter(r=>r.newPrompt&&r.prompt===r.oldPrompt).length,actorProfileResolved:true}));throw new Error(ROLLBACK);});}catch(e){if(e.message!==ROLLBACK){console.error(e?.stack||e);await sql.end({timeout:1});process.exit(1);}}
const restored=await resolve(sql);ok(classify(restored)==='ready','rollback state '+classify(restored));ok((await sql`select count(*)::int c from question_bank_events`)[0].c===eventBaseline,'question events rollback');ok((await sql`select count(*)::int c from curriculum_events`)[0].c===curriculumEventBaseline,'curriculum events rollback');const restoredCounts=await scopeCounts(sql,restored.classId,restored.subjectId);ok(JSON.stringify(restoredCounts)===JSON.stringify(baseline),'publication counts rollback');console.log('G9_U2_PUBLISH_ROLLBACK_VERIFIED',JSON.stringify(baseline));
await sql.begin(async tx=>{const s=await resolve(tx);await lockTarget(tx,s);ok(classify(await resolve(tx))==='ready','apply locked input');await mutate(tx,s);});
const final=await verifyPublished(sql,baseline);console.log('G9_U2_PUBLISH_APPLY_PASS',JSON.stringify({lessons:2,assets:6,questions:19,readerAssets:final.readerAssets,quizQuestions:final.quizQuestions,publicationCounts:final.counts}));console.log('G9_U2_PUBLISH_FULL_PASS',JSON.stringify({status:'COMMITTED_STATE_VERIFIED_AND_PUBLISHED',lessons:2,assets:6,questions:19}));await sql.end({timeout:1});