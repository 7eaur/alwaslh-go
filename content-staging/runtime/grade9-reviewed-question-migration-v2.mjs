import postgres from 'postgres';

const databaseUrl = process.env.DATABASE_URL;
if (!databaseUrl) throw new Error('DATABASE_URL is required');
const sql = postgres(databaseUrl,{max:1,connect_timeout:15,idle_timeout:5,prepare:false});
const ROLLBACK='G9_U2_Q_V2_EXPECTED_ROLLBACK';

const targets={
 describing:'curated-english9-pb3-u2-describing-people-and-animals',
 time:'curated-english9-pb3-u2-time-and-meeting'
};
const rows=[
 ['b04c9ed1-c951-479e-90c3-fd4b9bde1173','describing','The first person described weighs 79 kilos.'],
 ['78c6c40a-728d-43c3-9ac9-41e747b87133','describing','What colour are his eyes?'],
 ['50f0c143-91b2-4fa0-b716-754dae907861','describing','What is the weight of the tall, slim person described first?'],
 ['207aed25-3dbd-4efd-955a-1e6a6cc4d530','describing','Which person has a bad memory?'],
 ['2395e589-2abd-478c-9ef6-8f67bc6c8c68','describing','Ali weighs 27 kilos.'],
 ['3ca8e849-caee-4a92-8bd1-53faccf28072','describing',"Hassan's favourite bird is the black stork."],
 ['692934dd-17b9-40a4-aa1c-f2527255761e','describing','How much does Ali weigh?'],
 ['1241aa5b-c986-4f89-aa6e-eba8ac85e79a','describing',"What is Fatma's hair like?"],
 ['b0f522e3-8259-441b-90e0-e22c71977792','describing',"What is Hassan's favourite bird?"],
 ['c7fc2878-635a-446b-a912-03e6eb842cde','describing','The animal described has a long tail.'],
 ['80312676-ffd1-4904-a983-ade62770f551','describing','What colour is the animal described?'],
 ['8ebbdd77-f69d-4ec7-ac61-d784c36daa6a','describing','What does the animal eat?'],
 ['e6e52fd0-ab4b-4b4c-a020-3339da465bbb','time',"How is 12:15 expressed in the lesson?"],
 ['1b5ac35b-b790-43ab-8904-36c2ab099376','time','How many minutes are there in an hour?'],
 ['50d61a93-5d05-4101-a9c2-85aa143c678f','time','How many minutes are there in half an hour?'],
 ['f9d9858e-adb4-46d8-9b44-4b8dd31aa8ed','time','There are sixty minutes in an hour.'],
 ['b14c06e0-88e4-4909-9da3-fb545bfdd6dd','time','Football is scheduled at 5.15.'],
 ['7a061954-1022-4362-aa98-b7999a9d5e0d','time','What time is the football activity on the schedule?'],
 ['c435569f-befc-4a81-8814-63755abab185','time','When is Rashid meeting mentioned in the dialogue?','When is Fuad helping Dad on Saturday?']
];
function ok(c,m){if(!c)throw new Error('G9_U2_Q_V2_FAIL: '+m)}

async function readState(q,lock=false){
 const scope=await q`select c.id class_id,s.id subject_id from classes c join subject_class_links x on x.class_id=c.id join subjects s on s.id=x.subject_id where c.slug='grade-9' and s.slug='english' and c.status='active' and s.status='active' and x.status='active' ${lock?q`for update of x`:q``}`;
 ok(scope.length===1,'scope'); const {class_id,subject_id}=scope[0];
 const ls=await q`select id,slug,published_at,status from lessons where class_id=${class_id} and subject_id=${subject_id} and slug in ${q(Object.values(targets))}`;
 ok(ls.length===2,'target lessons'); const ids={}; for(const [k,slug] of Object.entries(targets)){const l=ls.find(x=>x.slug===slug);ok(l&&l.status==='active'&&l.published_at===null,'target '+k);ids[k]=l.id;}
 const revIds=rows.map(x=>x[0]);
 const revs=await q`select r.id,r.prompt,r.type::text type,r.options,r.correct_option_index,r.answer_text,r.status::text status,r.published_at,coalesce(array_agg(rl.lesson_id) filter(where rl.lesson_id is not null),'{}') lesson_ids from question_bank_revisions r left join question_bank_revision_lessons rl on rl.revision_id=r.id where r.id in ${q(revIds)} group by r.id order by r.id`;
 ok(revs.length===19,'revision count '+revs.length); ok(revs.every(r=>r.status==='draft'&&r.published_at===null),'revision publication drift');
 const byId=new Map(revs.map(r=>[r.id,r]));
 for(const spec of rows){const r=byId.get(spec[0]);ok(r,'missing '+spec[0]);const allowed=spec[3]?[spec[2],spec[3]]:[spec[2]];ok(allowed.includes(r.prompt),'prompt drift '+spec[0]);ok(r.lesson_ids.length===1,'link count '+spec[0]);}
 const [prov]=await q`select count(*)::int c from question_bank_revision_sources where revision_id in ${q(revIds)}`;ok(prov.c===19,'provenance rows '+prov.c);
 return {ids,revs,byId};
}
function mode(s){let legacy=0,target=0,wrong=0;for(const spec of rows){const r=s.byId.get(spec[0]);const tid=s.ids[spec[1]];if(r.lesson_ids[0]===tid)target++;else legacy++;if(spec[3]&&![spec[2],spec[3]].includes(r.prompt))wrong++;}const corrected=s.byId.get(rows[18][0]);const p=corrected.prompt===rows[18][3]?'corrected':corrected.prompt===rows[18][2]?'legacy':'drift';if(target===19&&legacy===0&&p==='corrected')return'applied';if(target===0&&legacy===19&&p==='legacy')return'legacy';return`mixed target=${target} legacy=${legacy} prompt=${p} wrong=${wrong}`;}
async function mutate(q,s){for(const spec of rows){const r=s.byId.get(spec[0]);const tid=s.ids[spec[1]];const old=r.lesson_ids[0];const u=await q`update question_bank_revision_lessons set lesson_id=${tid} where revision_id=${r.id} and lesson_id=${old} returning revision_id`;ok(u.length===1,'link '+r.id);}const c=rows[18];const u=await q`update question_bank_revisions set prompt=${c[3]} where id=${c[0]} and prompt=${c[2]} and status='draft' and published_at is null returning id`;ok(u.length===1,'prompt correction');}

const initial=await readState(sql);const im=mode(initial);if(im==='applied'){console.log('G9_U2_Q_V2_FULL_PASS',JSON.stringify({status:'COMMITTED_STATE_VERIFIED',links:19,corrected:1}));await sql.end({timeout:1});process.exit(0);}ok(im==='legacy','initial '+im);
try{await sql.begin(async tx=>{await tx`set local lock_timeout='5s'`;await tx`set local statement_timeout='60s'`;const s=await readState(tx,true);ok(mode(s)==='legacy','gate input');await mutate(tx,s);const inside=await readState(tx);ok(mode(inside)==='applied','gate inside '+mode(inside));console.log('G9_U2_Q_V2_GATE_PASS',JSON.stringify({linkUpdates:19,promptUpdates:1,publicationChanges:0,provenanceChanges:0}));throw new Error(ROLLBACK);});}catch(e){if(e.message!==ROLLBACK)throw e;}
const afterRollback=await readState(sql);ok(mode(afterRollback)==='legacy','rollback not restored');console.log('G9_U2_Q_V2_ROLLBACK_VERIFIED');
await sql.begin(async tx=>{await tx`set local lock_timeout='5s'`;await tx`set local statement_timeout='60s'`;const s=await readState(tx,true);ok(mode(s)==='legacy','apply input');await mutate(tx,s);});
const final=await readState(sql);ok(mode(final)==='applied','final '+mode(final));ok(final.revs.filter(r=>r.lesson_ids[0]===final.ids.describing).length===12,'describing 12');ok(final.revs.filter(r=>r.lesson_ids[0]===final.ids.time).length===7,'time 7');
console.log('G9_U2_Q_V2_APPLY_PASS',JSON.stringify({describingLinks:12,timeLinks:7,corrected:1,publicationChanges:0}));console.log('G9_U2_Q_V2_FULL_PASS',JSON.stringify({status:'COMMITTED_STATE_VERIFIED'}));await sql.end({timeout:1});