#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SID='0d4fa9fd-a93c-4d18-9dea-6dd22eb2e199'
RP=ROOT/'content-staging/reconstruction/exams/source-groups'/f'{SID}.json'
MP=ROOT/'content-staging/manifests/MASTER_CONTENT_MANIFEST.json'
START='<!-- MATH_EXAM_1445_CHECKPOINT_START -->'; END='<!-- MATH_EXAM_1445_CHECKPOINT_END -->'

def processed(s):
    x=str(s.get('review_status') or '')
    return x.startswith('processed_') or x=='reconstructed_verified'
def replace(path,body):
    text=path.read_text(encoding='utf-8'); block=f'{START}\n{body.rstrip()}\n{END}'
    if START in text and END in text:
        text=text.split(START,1)[0].rstrip()+'\n\n'+block+'\n\n'+text.split(END,1)[1].lstrip()
    else: text=text.rstrip()+'\n\n'+block+'\n'
    path.write_text(text,encoding='utf-8')
def main():
    r=json.loads(RP.read_text(encoding='utf-8')); m=json.loads(MP.read_text(encoding='utf-8')); sources=m['sources']
    assert r['individual_exam_model_count']==13 and r['finalized_exam_page_count']==39 and r['review_required_page_count']==3
    assert r['question_mapping']['exam_linked_structural']==28 and r['question_mapping']['unassigned_within_source']==0
    i=next(i for i,s in enumerate(sources) if s['id']==SID); s=sources[i]; was=processed(s)
    oe=s.get('exam_reconstruction') if isinstance(s.get('exam_reconstruction'),dict) else {}; ot=s.get('technical_verification') if isinstance(s.get('technical_verification'),dict) else {}
    old_models=int(oe.get('individual_exam_models') or 0); old_pages=int(oe.get('finalized_exam_pages') or oe.get('exam_pages') or 0); old_corr=int(oe.get('correction_sheet_candidates') or 0); old_link=int(oe.get('exam_linked_questions') or 0); old_rq=int(oe.get('review_required_questions') or 0); old_imgs=int(ot.get('images_verified') or 0)
    s.update({'classification':'exam_source_group','classification_evidence':'42/42 technical verification + explicit source-local page titles for models 1..13; repeated second model-12 occurrence quarantined because semantic identity is NOT VERIFIED','review_status':'processed_partial_boundary_verified_repeated_model12_review_required','exam_models':13,'answer_keys':'NOT VERIFIED','technical_verification':{'status':'verified','report_path':f'content-staging/reconstruction/technical/{SID}.json','images_verified':42,'readable':42,'sha256_match_manifest':42,'mime_match_manifest':42,'duplicate_sha_groups_within_source':0},'exam_reconstruction':{'status':r['status'],'path':f'content-staging/reconstruction/exams/source-groups/{SID}.json','source_blocks_reviewed':14,'verified_source_occurrences':13,'review_required_blocks':1,'individual_exam_models':13,'source_pages':42,'finalized_exam_pages':39,'review_required_pages':3,'correction_sheet_candidates':13,'verified_answer_keys':0,'answer_key_status':'NOT VERIFIED','exam_linked_questions':28,'review_required_questions':0,'associated_legacy_questions':28,'semantic_question_correctness':'NOT VERIFIED','raw_mutations':0}})
    p=m.setdefault('reconstruction_progress',{})
    p['sources_completed']=int(p.get('sources_completed') or 0)+(0 if was else 1); p['exam_source_groups_completed']=int(p.get('exam_source_groups_completed') or 0)+(0 if was else 1); p['individual_exam_models']=int(p.get('individual_exam_models') or 0)+(13-old_models); p['exam_pages_completed']=int(p.get('exam_pages_completed') or 0)+(39-old_pages); p['correction_sheet_candidates']=int(p.get('correction_sheet_candidates') or 0)+(13-old_corr); p['source_images_technically_verified']=int(p.get('source_images_technically_verified') or 0)+(42-old_imgs); p['exam_linked_to_individual_model']=int(p.get('exam_linked_to_individual_model') or 0)+(28-old_link); p['review_required']=int(p.get('review_required') or 0)+(0-old_rq); p['unclassified']=int(p.get('unclassified') or 0)-((28+0)-(old_link+old_rq))
    for k,v in {'sources_total':58,'educational_sources_total':26,'exam_source_groups_total':32,'exam_pages_total':2286,'source_images_total':5273,'legacy_questions_total':25755,'duplicate_fingerprint_groups_total':99,'raw_mutations':0,'unrelated_mutations':0,'new_imports':0,'new_publications':0}.items(): p[k]=v
    inv=int(p.get('lesson_linked_structural') or 0)+int(p.get('exam_linked_to_individual_model') or 0)+int(p.get('review_required') or 0)+int(p.get('unclassified') or 0)
    assert inv==25755 and p['unclassified']>=0
    m['status']='RECONSTRUCTION_IN_PROGRESS_NOT_IMPORT_READY'
    nxt=None
    for x in sources[i+1:]+sources[:i]:
        if not processed(x): nxt=x; break
    MP.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    nid=nxt['id'] if nxt else 'NONE'; nn=(nxt.get('legacy_source') or {}).get('name') if nxt else 'NONE'
    body=f'''## Reconstruction checkpoint — Mathematics Ministry Exams 1445

- Source `{SID}` — `الرياضيات نماذج وزارية 1445` safely processed.
- Technical verification: **42/42** images; contiguous pages 1..42; duplicate SHA groups **0**.
- Verified models: **13** (pages 1..39); finalized exam pages: **39**; correction candidates: **13**; verified standalone Answer Keys: **0 / NOT VERIFIED**.
- Pages **40..42**: `review_required`; metadata repeats model 12 but binaries differ, and semantic identity versus pages 34..36 remains `NOT VERIFIED`; no merge/renumber performed.
- Questions: **28/28** structurally linked to verified model 1 from source page membership; semantic correctness `NOT VERIFIED`.
- Progress: Sources **{p['sources_completed']}/58**; Educational **{p.get('educational_sources_completed',0)}/26**; Exam Groups **{p['exam_source_groups_completed']}/32**; Individual Exam Models **{p['individual_exam_models']}**; Exam Pages **{p['exam_pages_completed']}/2,286**; source images technical **{p['source_images_technically_verified']}/5,273**.
- Global questions: Lesson-linked **{p.get('lesson_linked_structural',0)}**; Exam-linked **{p.get('exam_linked_to_individual_model',0)}**; Review-required **{p.get('review_required',0)}**; Unclassified **{p.get('unclassified',0)}**; invariant **PASS = 25,755**.
- RAW/unrelated/import/publication mutations: **0/0/0/0**.
- Next source: `{nid}` — `{nn}`.
'''
    for fn in ('CONTENT_REBUILD_EXECUTION_STATUS.md','CONTENT_REBUILD_HANDOFF.md','CONTENT_INVENTORY.md','CONTENT_VALIDATION_REPORT.md','CONTENT_IMPORT_REPORT.md','CONTENT_REBUILD_CONTINUATION_2026-09-14.md'):
        path=ROOT/'content-staging'/fn
        if path.exists(): replace(path,body)
    print(json.dumps({'progress':p,'next_source_id':nid,'next_source_name':nn,'invariant':inv},ensure_ascii=False))
if __name__=='__main__': main()
