#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SID='fef5e58f-21df-42e3-81ae-6966cd7bad10'
RP=ROOT/'content-staging/reconstruction/exams/source-groups'/f'{SID}.json'
MP=ROOT/'content-staging/manifests/MASTER_CONTENT_MANIFEST.json'
START='<!-- MATH_EXAM_1447_CHECKPOINT_START -->'; END='<!-- MATH_EXAM_1447_CHECKPOINT_END -->'

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
    assert r['individual_exam_model_count']==14 and r['finalized_exam_page_count']==42 and r['review_required_page_count']==0
    assert r['question_mapping']['exam_linked_structural']==112 and r['question_mapping']['unassigned_within_source']==0
    assert r['evidence']['visual_semantic_review']=='NOT VERIFIED'
    i=next(i for i,s in enumerate(sources) if s['id']==SID); s=sources[i]; was=processed(s)
    oe=s.get('exam_reconstruction') if isinstance(s.get('exam_reconstruction'),dict) else {}; ot=s.get('technical_verification') if isinstance(s.get('technical_verification'),dict) else {}
    old_models=int(oe.get('individual_exam_models') or 0); old_pages=int(oe.get('finalized_exam_pages') or oe.get('exam_pages') or 0); old_corr=int(oe.get('correction_sheet_candidates') or 0); old_link=int(oe.get('exam_linked_questions') or 0); old_rq=int(oe.get('review_required_questions') or 0); old_imgs=int(ot.get('images_verified') or 0)
    s.update({'classification':'exam_source_group','classification_evidence':'42/42 technical verification + explicit unique source-local titles covering models 1..14 in exact 3-page sequences; contact sheets generated; visual semantic inspection NOT VERIFIED','review_status':'processed_boundary_verified_explicit_titles_visual_semantics_not_verified_answer_keys_not_verified','exam_models':14,'answer_keys':'NOT VERIFIED','technical_verification':{'status':'verified','report_path':f'content-staging/reconstruction/technical/{SID}.json','images_verified':42,'readable':42,'sha256_match_manifest':42,'mime_match_manifest':42,'duplicate_sha_groups_within_source':0},'exam_reconstruction':{'status':r['status'],'path':f'content-staging/reconstruction/exams/source-groups/{SID}.json','source_records_reviewed':42,'verified_source_occurrences':14,'review_required_blocks':0,'individual_exam_models':14,'source_pages':42,'finalized_exam_pages':42,'review_required_pages':0,'correction_sheet_candidates':14,'verified_answer_keys':0,'answer_key_status':'NOT VERIFIED','visual_semantic_review':'NOT VERIFIED','exam_linked_questions':112,'review_required_questions':0,'associated_legacy_questions':112,'semantic_question_correctness':'NOT VERIFIED','raw_mutations':0}})
    p=m.setdefault('reconstruction_progress',{})
    p['sources_completed']=int(p.get('sources_completed') or 0)+(0 if was else 1); p['exam_source_groups_completed']=int(p.get('exam_source_groups_completed') or 0)+(0 if was else 1); p['individual_exam_models']=int(p.get('individual_exam_models') or 0)+(14-old_models); p['exam_pages_completed']=int(p.get('exam_pages_completed') or 0)+(42-old_pages); p['correction_sheet_candidates']=int(p.get('correction_sheet_candidates') or 0)+(14-old_corr); p['source_images_technically_verified']=int(p.get('source_images_technically_verified') or 0)+(42-old_imgs); p['exam_linked_to_individual_model']=int(p.get('exam_linked_to_individual_model') or 0)+(112-old_link); p['review_required']=int(p.get('review_required') or 0)+(0-old_rq); p['unclassified']=int(p.get('unclassified') or 0)-((112+0)-(old_link+old_rq))
    for k,v in {'sources_total':58,'educational_sources_total':26,'exam_source_groups_total':32,'exam_pages_total':2286,'source_images_total':5273,'legacy_questions_total':25755,'duplicate_fingerprint_groups_total':99,'raw_mutations':0,'unrelated_mutations':0,'new_imports':0,'new_publications':0}.items(): p[k]=v
    inv=int(p.get('lesson_linked_structural') or 0)+int(p.get('exam_linked_to_individual_model') or 0)+int(p.get('review_required') or 0)+int(p.get('unclassified') or 0)
    assert inv==25755 and p['unclassified']>=0 and p['source_images_technically_verified']<=5273
    m['status']='RECONSTRUCTION_IN_PROGRESS_NOT_IMPORT_READY'
    nxt=None
    for x in sources[i+1:]+sources[:i]:
        if not processed(x): nxt=x; break
    MP.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    nid=nxt['id'] if nxt else 'NONE'; nn=(nxt.get('legacy_source') or {}).get('name') if nxt else 'NONE'
    body=f'''## Reconstruction checkpoint — Mathematics Ministry Exams 1447\n\n- Source `{SID}` — `الرياضيات نماذج وزارية 1447` safely processed.\n- Technical verification: **42/42** immutable images; duplicate SHA groups **0**; page sequence **1..42** complete.\n- Boundary evidence: explicit unique source-local titles prove **14** three-page model sequences (question sheet 1, question sheet 2, correction-sheet candidate).\n- Visual contact sheets were generated in GitHub Actions run `34859563356`; semantic visual inspection remains **NOT VERIFIED** and was not claimed.\n- Finalized exam pages: **42**; correction candidates: **14**; verified standalone Answer Keys: **0 / NOT VERIFIED**.\n- Questions: **112/112** structurally linked by legacy-page membership; semantic correctness **NOT VERIFIED**.\n- Progress: Sources **{p['sources_completed']}/58**; Educational **{p.get('educational_sources_completed',0)}/26**; Exam Groups **{p['exam_source_groups_completed']}/32**; Individual Exam Models **{p['individual_exam_models']}**; Exam Pages **{p['exam_pages_completed']}/2,286**; source images technical **{p['source_images_technically_verified']}/5,273**.\n- Global questions: Lesson-linked **{p.get('lesson_linked_structural',0)}**; Exam-linked **{p.get('exam_linked_to_individual_model',0)}**; Review-required **{p.get('review_required',0)}**; Unclassified **{p.get('unclassified',0)}**; invariant **PASS = 25,755**.\n- RAW/unrelated/import/publication mutations: **0/0/0/0**.\n- Next source: `{nid}` — `{nn}`.\n'''
    for fn in ('CONTENT_REBUILD_EXECUTION_STATUS.md','CONTENT_REBUILD_HANDOFF.md','CONTENT_INVENTORY.md','CONTENT_VALIDATION_REPORT.md','CONTENT_IMPORT_REPORT.md','CONTENT_REBUILD_CONTINUATION_2026-09-14.md'):
        path=ROOT/'content-staging'/fn
        if path.exists(): replace(path,body)
    print(json.dumps({'progress':p,'next_source_id':nid,'next_source_name':nn,'invariant':inv},ensure_ascii=False))
if __name__=='__main__': main()
