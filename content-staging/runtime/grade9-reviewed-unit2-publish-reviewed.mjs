import postgres from 'postgres';

const databaseUrl = process.env.DATABASE_URL;
if (!databaseUrl) throw new Error('DATABASE_URL is required');
const sql = postgres(databaseUrl,{max:1,connect_timeout:15,idle_timeout:5,prepare:false});
const ROLLBACK='G9_U2_REVIEWED_Q_FIX_EXPECTED_ROLLBACK';
const sourcePath='public.lessons/75616176-b12d-47bb-bb6e-34cc3f902901/image/0';
const oldPrompt='When is Rashid meeting mentioned in the dialogue?';
const newPrompt='When is Fuad helping Dad on Saturday?';
const newExplanation="Fuad says he is helping Dad at six o'clock.";

function ok(c,m){if(!c)throw new Error('G9_U2_REVIEWED_Q_FIX_FAIL: '+m)}
async function read(q){
 const source=await q`select id,is_present from content_source_assets where source_path=${sourcePath}`;
 ok(source.length===1&&source[0].is_present===true,'source identity');
 const rows=await q`select r.id,r.prompt,r.explanation,r.options,r.correct_option_index,r.answer_text,r.answer_status::text answer_status,r.status::text status,r.published_at
 from question_bank_revision_sources rs join question_bank_revisions r on r.id=rs.revision_id
 where rs.content_source_asset_id=${source[0].id} and (r.prompt=${oldPrompt} or r.prompt=${newPrompt})`;
 ok(rows.length===1,'question identity count '+rows.length);const r=rows[0];
 ok(r.status==='draft'&&r.published_at===null&&r.answer_status==='known','question state');
 ok(JSON.stringify(r.options)===JSON.stringify(["at six o'clock","at five o'clock","at seven o'clock","at eight o'clock"]),'options drift');
 ok(r.correct_option_index===0&&r.answer_text==="at six o'clock",'answer drift');
 return r;
}
async function apply(q,r){
 if(r.prompt===newPrompt&&r.explanation===newExplanation)return 0;
 const changed=await q`update question_bank_revisions set prompt=${newPrompt},explanation=${newExplanation}
 where id=${r.id} and status='draft' and published_at is null returning id`;
 ok(changed.length===1,'correction update');return 1;
}

const before=await read(sql);
if(!(before.prompt===newPrompt&&before.explanation===newExplanation)){
 try{await sql.begin(async tx=>{const r=await read(tx);const n=await apply(tx,r);ok(n===1,'gate expected update');const inside=await read(tx);ok(inside.prompt===newPrompt&&inside.explanation===newExplanation,'gate verification');console.log('G9_U2_REVIEWED_Q_FIX_GATE_PASS',JSON.stringify({questionCorrections:1}));throw new Error(ROLLBACK);});}catch(e){if(e.message!==ROLLBACK){console.error(e?.stack||e);await sql.end({timeout:1});process.exit(1);}}
 const restored=await read(sql);ok(restored.prompt===before.prompt&&restored.explanation===before.explanation,'rollback restore');console.log('G9_U2_REVIEWED_Q_FIX_ROLLBACK_VERIFIED');
 await sql.begin(async tx=>{const r=await read(tx);await apply(tx,r);});
}
const final=await read(sql);ok(final.prompt===newPrompt&&final.explanation===newExplanation,'final correction');console.log('G9_U2_REVIEWED_Q_FIX_APPLY_PASS',JSON.stringify({prompt:newPrompt,answerText:final.answer_text,status:final.status}));
await sql.end({timeout:1});
await import('./grade9-reviewed-unit2-publish.mjs');
