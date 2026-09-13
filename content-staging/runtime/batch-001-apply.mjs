import postgres from 'postgres';
const sql=postgres(process.env.DATABASE_URL,{max:1,connect_timeout:15,idle_timeout:5,prepare:false});
const lessons=[
['legacy-sb-2d53aec17e54f46db304','curated-english9-pb3-u1-p001-presents-from-london','Presents from London',0,'public.lessons/2d98475c-91bf-4000-bfbc-79f7a6a854f9/image/0','ae3e89be65d1c9ec5f70e361a5e78ea903d6e305f22d399e2c88bf864f6c3a4f'],
['legacy-sb-908a58f8e7b25f82c787','curated-english9-pb3-u1-p002-whats-my-job',"What's my job?",1,'public.lessons/5e207993-508f-426b-ae71-f00aa4f782df/image/0','1df05a27195e28e5543747c1f827a4d32c2bf937476c91ae69b0f4fe8b61b413'],
['legacy-sb-4e1131b5222334610174','curated-english9-pb3-u1-p003-the-holidays','The holidays',2,'public.lessons/dc1d6249-c0cb-4982-9711-092b1dcffee3/image/0','78741ebd493e6b7dbbc05115472fec173edbeab9e05079b806a61acd1d7d13ac'],
['legacy-sb-840f23a0e0a98aaa674e','curated-english9-pb3-u1-p004-a-postcard-from-london','A postcard from London',3,'public.lessons/f2947d7f-5697-4bdc-b561-ad880a1afdf1/image/0','86d655468bfbc73248da92e0d16d4b4dcccc0217df241e69bac94f6cee6cf321']];
const fixes=[
['What does Mr Al Sabri want to buy for Saleh?','What does Mr Al Sabri suggest Taha buy for Saleh?','multiple_choice',['a pair of shorts','a school uniform','a bicycle','a camera'],0],
['Taha works in a clinic.','The dentist works in a clinic.','true_false',null,null],
["What is Taha's job?","What is the job of the person who takes care of people's teeth?",'multiple_choice',['a dentist','a teacher','a doctor','a police officer'],0],
['Where does the doctor work?','Where does the dentist work?','multiple_choice',['in a clinic','in an office','in a hospital','in a school'],0],
['The family went to London for the holidays.','One speaker went to a village by the sea in the holidays.','true_false',null,null],
['What did Amna do every day?','What did the first speaker do every day?','multiple_choice',['went swimming and fishing','stayed at home','went shopping','worked on a farm'],0],
['Where did Mr Al Sabri and his family go on holiday?','Where did the first speaker go in the holidays?','multiple_choice',['a village by the sea','London','Paris',"Sana'a"],0]];
function ok(c,m){if(!c)throw new Error('BATCH001_APPLY_FAIL: '+m)}
let summary;
try{
 await sql.begin(async tx=>{
  await tx`set local lock_timeout='5s'`; await tx`set local statement_timeout='60s'`;
  const scope=await tx`select c.id class_id,s.id subject_id from classes c join subjects s on s.slug='english' join subject_class_links x on x.class_id=c.id and x.subject_id=s.id where c.slug='grade-9' and c.status='active' and s.status='active' and x.status='active' for update of x`;
  ok(scope.length===1,'scope drift'); const {class_id,subject_id}=scope[0];
  const preCounts={}; for(const t of ['curriculum_sections','lessons','lesson_assets','media_assets','content_source_assets','question_bank_items','question_bank_revisions','question_bank_revision_lessons','question_bank_revision_sources']){const [r]=await tx.unsafe(`select count(*)::int c from ${t}`);preCounts[t]=r.c}
  const resolved=[];
  for(const [legacySlug,targetSlug,title,position,path,sha] of lessons){const r=await tx`select l.id,csa.id source_asset_id,la.publication_status,l.published_at from content_source_assets csa join media_assets ma on ma.content_source_asset_id=csa.id join lesson_assets la on la.media_asset_id=ma.id join lessons l on l.id=la.lesson_id where csa.is_present=true and csa.source_path=${path} and csa.checksum_sha256=${sha} and ma.source_checksum_sha256=${sha} and ma.status='ready' and la.publication_status='draft' and la.asset_published_at is null and l.class_id=${class_id} and l.subject_id=${subject_id} and l.slug=${legacySlug} and l.status='active' and l.published_at is null for update of l`;ok(r.length===1,'lesson identity drift '+path);resolved.push({id:r[0].id,targetSlug,title,position})}
  ok(new Set(resolved.map(x=>x.id)).size===4,'lesson uniqueness drift');
  const existing=await tx`select id from curriculum_sections where class_id=${class_id} and subject_id=${subject_id} and slug='curated-english9-pb3-unit-1-revision'`;ok(existing.length===0,'section already exists');
  const ids=resolved.map(x=>x.id); const drafts=await tx`select r.id,r.prompt,r.status,r.published_at,rl.lesson_id from question_bank_revisions r join question_bank_revision_lessons rl on rl.revision_id=r.id where rl.lesson_id in ${tx(ids)} and r.status='draft' and r.published_at is null for update of r`;ok(drafts.length===13,'question draft count '+drafts.length);
  const target=[]; for(const f of fixes){const m=drafts.filter(r=>r.prompt===f[0]);ok(m.length===1,'question locator '+f[0]);target.push({id:m[0].id,f})} ok(new Set(target.map(x=>x.id)).size===7,'question uniqueness drift');
  const [section]=await tx`insert into curriculum_sections(class_id,subject_id,slug,title,position,status) values(${class_id},${subject_id},'curated-english9-pb3-unit-1-revision','Unit 1 - Revision',1,'active') returning id`;
  for(const x of resolved) await tx`update lessons set section_id=${section.id},slug=${x.targetSlug},title=${x.title},position=${x.position} where id=${x.id}`;
  for(const x of target){const [old,prompt,type,opts,idx]=x.f;if(opts){await tx`update question_bank_revisions set type=${type}::question_bank_question_type,prompt=${prompt},options=${tx.json(opts)},correct_option_index=${idx},answer_text=${opts[idx]} where id=${x.id}`}else{await tx`update question_bank_revisions set type=${type}::question_bank_question_type,prompt=${prompt} where id=${x.id}`}}
  const postLessons=await tx`select count(*)::int c from lessons where id in ${tx(ids)} and section_id=${section.id} and published_at is null`;ok(postLessons[0].c===4,'post lessons');
  const postQ=await tx`select count(*)::int c from question_bank_revisions where id in ${tx(target.map(x=>x.id))} and status='draft' and published_at is null`;ok(postQ[0].c===7,'post questions publication');
  const pubAssets=await tx`select count(*)::int c from lesson_assets where lesson_id in ${tx(ids)} and (publication_status<>'draft' or asset_published_at is not null)`;ok(pubAssets[0].c===0,'asset publication changed');
  const postCounts={}; for(const t of Object.keys(preCounts)){const [r]=await tx.unsafe(`select count(*)::int c from ${t}`);postCounts[t]=r.c} for(const t of Object.keys(preCounts)) ok(postCounts[t]===preCounts[t]+(t==='curriculum_sections'?1:0),'row-count invariant '+t);
  summary={sectionId:section.id,lessonIds:ids,questionRevisionIds:target.map(x=>x.id),sectionInserts:1,lessonUpdates:4,questionUpdates:7,publicationChanges:0,rawMediaMutations:0,preCounts,postCounts};
 });
 console.log('BATCH001_APPLY_COMMIT_PASS',JSON.stringify(summary));
}catch(e){console.error('BATCH001_APPLY_FAIL',e?.stack||e);await sql.end({timeout:1});process.exit(1)}
await sql.end({timeout:1});