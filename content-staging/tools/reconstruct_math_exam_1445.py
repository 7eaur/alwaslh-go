#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
SID='0d4fa9fd-a93c-4d18-9dea-6dd22eb2e199'
SD=ROOT/'content-staging/raw/legacy-supabase/subjects'/SID
OUT=ROOT/'content-staging/reconstruction/exams/source-groups'/f'{SID}.json'
TECH=ROOT/'content-staging/reconstruction/technical'/f'{SID}.json'
REP=ROOT/'content-staging/reconstruction/exams/source-groups'/f'{SID}-repeated-label-evidence.json'

def load_pages():
    x=json.loads((SD/'pages.json').read_text(encoding='utf-8'))
    if isinstance(x,list): return x
    for k in ('pages','records','items','data'):
        if isinstance(x.get(k),list): return x[k]
    raise SystemExit('unsupported pages shape')

def main():
    manifest=json.loads((SD/'manifest.json').read_text(encoding='utf-8'))
    tech=json.loads(TECH.read_text(encoding='utf-8'))
    repeated=json.loads(REP.read_text(encoding='utf-8'))
    pages=load_pages(); byp={int(p['page_number']):p for p in pages}; imgs={int(i['page_number']):i for i in manifest['images']}
    assert tech['all_images_technically_verified'] and tech['checks']['failures']==0
    assert all(tech['checks'][k]==42 for k in ('existing_files','readable_images','sha256_matches','byte_size_matches','mime_matches'))
    assert sorted(imgs)==list(range(1,43)) and sorted(byp)==list(range(1,43))
    assert not tech['duplicate_sha256_groups_within_subject']
    assert manifest['counts']['pages']==42 and manifest['counts']['questions']==28
    titles={n:(byp[n].get('title') or '').strip() for n in byp}
    for m in range(1,14):
        a=(m-1)*3+1
        assert titles[a]==f'النموذج {m} الورقة 1'
        assert titles[a+1]==f'النموذج {m} الورقة 2'
        assert titles[a+2]==f'نموذج التصحيح النموذج {m}'
    assert [titles[n] for n in (40,41,42)]==['النموذج 12 الورقة 1','النموذج 12 الورقة 2','نموذج التصحيح النموذج 12']
    assert repeated['semantic_identity_relation']=='NOT VERIFIED'
    qcounts={n:len(byp[n].get('ai_questions') or []) for n in byp}
    assert sum(qcounts.values())==28 and qcounts[1]==28 and all(qcounts[n]==0 for n in range(2,43))
    models=[]
    for m in range(1,14):
        a=(m-1)*3+1; nums=[a,a+1,a+2]
        models.append({'id':f'math-1445-exam-{m:02d}','internal_ordinal':m,'source_model_label':f'النموذج {m}','official_model_code':'NOT VERIFIED','term':'NOT VERIFIED','exam_type':'وزاري','ordered_page_numbers':nums,'ordered_legacy_page_ids':[imgs[n]['legacy_page_id'] for n in nums],'raw_paths':[imgs[n]['raw_path'] for n in nums],'sha256':[imgs[n]['sha256'] for n in nums],'question_pages':nums[:2],'correction_sheet_candidate_page':nums[2],'boundary_status':'verified_from_source_metadata_and_sequence','answer_key_status':'NOT VERIFIED'})
    maps=[]
    for idx,q in enumerate(byp[1].get('ai_questions') or [],1):
        maps.append({'page_number':1,'legacy_page_id':byp[1].get('id'),'question_ordinal_on_page':idx,'source_reference':q.get('source_reference') if isinstance(q,dict) else None,'mapping_status':'exam_linked_structural','individual_exam_model_id':'math-1445-exam-01'})
    out={'schema_version':1,'source_group_id':SID,'source_group_name':'الرياضيات نماذج وزارية 1445','classification':'exam_source_group','academic_year_hijri':'1445','source_pages':42,'source_questions':28,'source_blocks_reviewed':14,'verified_source_occurrence_count':13,'review_required_block_count':1,'individual_exam_model_count':13,'finalized_exam_page_count':39,'review_required_page_count':3,'correction_sheet_candidate_count':13,'verified_answer_key_count':0,'duplicate_sha256_groups_within_source':0,'models':models,'review_required_blocks':[{'ordered_page_numbers':[40,41,42],'source_label':'النموذج 12','reason':'A second distinct-binary three-page occurrence repeats the model-12 labels. Pixel similarity supports related layout/content but does not prove whether this is the same semantic model, an alternate version, or mislabeled separate model. Relation is NOT VERIFIED; pages are quarantined rather than merged or renumbered.','evidence_path':f'content-staging/reconstruction/exams/source-groups/{SID}-repeated-label-evidence.json'}],'question_mapping':{'exam_linked_structural':28,'review_required':0,'unassigned_within_source':0,'semantic_correctness':'NOT VERIFIED','records':maps},'evidence':{'technical_report':f'content-staging/reconstruction/technical/{SID}.json','discovery_report':f'content-staging/reconstruction/exams/source-groups/{SID}-discovery.json','metadata_evidence':f'content-staging/reconstruction/exams/source-groups/{SID}-metadata-evidence.json','repeated_label_evidence':f'content-staging/reconstruction/exams/source-groups/{SID}-repeated-label-evidence.json','visual_contact_sheets_generated':True,'visual_semantic_adjudication':'NOT VERIFIED','raw_mutations':0},'status':'processed_partial_boundary_verified_repeated_model12_occurrence_review_required'}
    OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'models':13,'finalized_exam_pages':39,'review_required_pages':3,'exam_linked':28,'raw_mutations':0},ensure_ascii=False))
if __name__=='__main__': main()
