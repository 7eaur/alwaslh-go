#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SOURCE_ID='0b28dc73-7e43-45f1-99c8-14825dcf3ded'
RECON_PATH=ROOT/'content-staging/reconstruction/exams/source-groups'/f'{SOURCE_ID}.json'
MASTER_PATH=ROOT/'content-staging/manifests/MASTER_CONTENT_MANIFEST.json'
START='<!-- PHYSICS_EXAM_1446_CHECKPOINT_START -->'; END='<!-- PHYSICS_EXAM_1446_CHECKPOINT_END -->'

def replace_block(path,body):
    text=path.read_text(encoding='utf-8'); block=f'{START}\n{body.rstrip()}\n{END}'
    if START in text and END in text:
        before=text.split(START,1)[0].rstrip(); after=text.split(END,1)[1].lstrip(); text=before+'\n\n'+block+('\n\n'+after if after else '\n')
    else: text=text.rstrip()+'\n\n'+block+'\n'
    path.write_text(text,encoding='utf-8')

def is_processed(s):
    status=str(s.get('review_status') or '')
    return status.startswith('processed_') or status in {'reconstructed_verified','verified_empty_retained_source'}
def next_unprocessed(master,idx):
    ss=master.get('sources') or []
    for item in ss[idx+1:]+ss[:idx]:
        if not is_processed(item): return item
    return None
def source_name(item):
    if not item:return 'NONE'
    return (item.get('legacy_source') or {}).get('name') or item.get('name') or 'UNKNOWN'

def main():
    r=json.loads(RECON_PATH.read_text(encoding='utf-8'))
    if r.get('individual_exam_model_count')!=26 or r.get('finalized_exam_page_count')!=104: raise SystemExit('Physics 1446 model/page count not finalized')
    q=r.get('question_mapping') or {}
    if (q.get('exam_linked_structural'),q.get('review_required'),q.get('unassigned_within_source'))!=(200,0,0): raise SystemExit('Physics 1446 question mapping not finalized')
    m=json.loads(MASTER_PATH.read_text(encoding='utf-8')); ss=m.get('sources') or []
    idx=next((i for i,s in enumerate(ss) if s.get('id')==SOURCE_ID),None)
    if idx is None: raise SystemExit('source missing from master')
    s=ss[idx]; old_processed=is_processed(s); oe=s.get('exam_reconstruction') if isinstance(s.get('exam_reconstruction'),dict) else {}; ot=s.get('technical_verification') if isinstance(s.get('technical_verification'),dict) else {}
    old_models=int(oe.get('individual_exam_models') or 0); old_pages=int(oe.get('finalized_exam_pages') or oe.get('exam_pages') or 0); old_corr=int(oe.get('correction_sheet_candidates') or 0); old_images=int(ot.get('images_verified') or 0); old_eq=int(oe.get('exam_linked_questions') or 0); old_rq=int(oe.get('review_required_questions') or 0)
    s.update({'classification':'exam_source_group','classification_evidence':'legacy exam label + 104/104 technical verification + complete source-local 104-page visual review resolving twenty-six four-page question/question/question/correction occurrences','review_status':'processed_boundary_verified_answer_keys_not_verified','exam_models':26,'answer_keys':'NOT VERIFIED','technical_verification':{'status':'verified','report_path':f'content-staging/reconstruction/technical/{SOURCE_ID}.json','images_verified':104,'readable':104,'sha256_match_manifest':104,'mime_match_manifest':104,'duplicate_sha_groups_within_source':6},'exam_reconstruction':{'status':r['status'],'path':f'content-staging/reconstruction/exams/source-groups/{SOURCE_ID}.json','source_blocks_reviewed':26,'verified_source_occurrences':26,'review_required_blocks':0,'individual_exam_models':26,'source_pages':104,'finalized_exam_pages':104,'review_required_pages':0,'pages_per_source_block':4,'question_pages_per_verified_occurrence':3,'correction_sheet_candidates':26,'verified_answer_keys':0,'answer_key_status':'NOT VERIFIED','exam_linked_questions':200,'review_required_questions':0,'associated_legacy_questions':200,'semantic_question_correctness':'NOT VERIFIED','raw_mutations':0}})
    p=m.setdefault('reconstruction_progress',{}); sd=0 if old_processed else 1; md=26-old_models; pd=104-old_pages; cd=26-old_corr; idelta=104-old_images; eqd=200-old_eq; rqd=0-old_rq
    if min(md,pd,cd,idelta,eqd)<0: raise SystemExit('existing counters exceed evidence; fail closed')
    p['sources_completed']=int(p.get('sources_completed') or 0)+sd; p['exam_source_groups_completed']=int(p.get('exam_source_groups_completed') or 0)+sd; p['individual_exam_models']=int(p.get('individual_exam_models') or 0)+md; p['exam_pages_completed']=int(p.get('exam_pages_completed') or 0)+pd; p['correction_sheet_candidates']=int(p.get('correction_sheet_candidates') or 0)+cd; p['source_images_technically_verified']=int(p.get('source_images_technically_verified') or 0)+idelta; p['exam_linked_to_individual_model']=int(p.get('exam_linked_to_individual_model') or 0)+eqd; p['review_required']=int(p.get('review_required') or 0)+rqd; p['unclassified']=int(p.get('unclassified') or 0)-eqd-rqd
    for k,v in {'sources_total':58,'educational_sources_total':26,'exam_source_groups_total':32,'exam_pages_total':2286,'source_images_total':5273,'legacy_questions_total':25755,'duplicate_fingerprint_groups_total':99,'raw_mutations':0,'unrelated_mutations':0,'new_imports':0,'new_publications':0}.items(): p[k]=v
    invariant=sum(int(p.get(k) or 0) for k in ('lesson_linked_structural','exam_linked_to_individual_model','review_required','unclassified'))
    if invariant!=25755: raise SystemExit(f'global invariant failed {invariant}')
    if int(p.get('source_images_technically_verified') or 0)>5273: raise SystemExit('image count exceeds total')
    if any(int(p.get(k) or 0)!=0 for k in ('raw_mutations','unrelated_mutations','new_imports','new_publications')): raise SystemExit('forbidden counter nonzero')
    m['status']='RECONSTRUCTION_IN_PROGRESS_NOT_IMPORT_READY'; nxt=next_unprocessed(m,idx); nid=nxt.get('id') if nxt else 'NONE'; nname=source_name(nxt); MASTER_PATH.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    body=f'''## Reconstruction checkpoint — Physics Ministry Exams 1446

- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Source `{SOURCE_ID}` — `الفيزياء نماذج وزاريه 1446` completed from source-local evidence.
- Technical verification: **104/104** images verified; sequence **1..104** contiguous; duplicate SHA groups **6**, preserved without merge or RAW mutation.
- Full visual review resolves **26** verified source occurrences; each has three question pages followed by one correction/result-sheet candidate; all **104** source pages finalized exactly once.
- Partial-page SHA duplication does not collapse occurrences because paired fourth-page correction/result sheets differ; official model codes remain `NOT VERIFIED`.
- Correction/result candidates: **26**; verified standalone official Answer Keys: **0 / NOT VERIFIED**.
- Source questions: **200/200 structurally exam-linked** by verified page membership; semantic correctness remains `NOT VERIFIED`.
- Progress: Sources **{p['sources_completed']}/58**; Educational **{p.get('educational_sources_completed',0)}/26**; Exam Groups **{p['exam_source_groups_completed']}/32**; Individual Exam Models **{p['individual_exam_models']}**; Exam Pages **{p['exam_pages_completed']}/2,286**; source images technical **{p['source_images_technically_verified']}/5,273**.
- Global questions: Lesson-linked **{p.get('lesson_linked_structural',0)}**; Exam-linked **{p.get('exam_linked_to_individual_model',0)}**; Review-required **{p.get('review_required',0)}**; Unclassified **{p.get('unclassified',0)}**; invariant **PASS = 25,755**.
- RAW/unrelated/import/publication mutations: **0/0/0/0**.
- Next source: `{nid}` — `{nname}`.
'''
    for fn in ('CONTENT_REBUILD_EXECUTION_STATUS.md','CONTENT_REBUILD_HANDOFF.md','CONTENT_INVENTORY.md','CONTENT_VALIDATION_REPORT.md','CONTENT_IMPORT_REPORT.md','CONTENT_REBUILD_CONTINUATION_2026-09-14.md'):
        path=ROOT/'content-staging'/fn
        if path.exists(): replace_block(path,body)
    print(json.dumps({'sources_completed':p['sources_completed'],'exam_source_groups_completed':p['exam_source_groups_completed'],'individual_exam_models':p['individual_exam_models'],'exam_pages_completed':p['exam_pages_completed'],'source_images_technically_verified':p['source_images_technically_verified'],'lesson_linked':p.get('lesson_linked_structural',0),'exam_linked':p.get('exam_linked_to_individual_model',0),'review_required':p.get('review_required',0),'unclassified':p.get('unclassified',0),'next_source_id':nid,'next_source_name':nname,'invariant':invariant},ensure_ascii=False))
if __name__=='__main__': main()
