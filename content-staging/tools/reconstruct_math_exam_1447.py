#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SID='fef5e58f-21df-42e3-81ae-6966cd7bad10'
SD=ROOT/'content-staging/raw/legacy-supabase/subjects'/SID
OUT=ROOT/'content-staging/reconstruction/exams/source-groups'/f'{SID}.json'
TECH=ROOT/'content-staging/reconstruction/technical'/f'{SID}.json'
META=ROOT/'content-staging/reconstruction/exams/source-groups'/f'{SID}-metadata-evidence.json'

def load_pages():
    x=json.loads((SD/'pages.json').read_text(encoding='utf-8'))
    if isinstance(x,list): return x
    for k in ('pages','records','items','data'):
        if isinstance(x.get(k),list): return x[k]
    raise SystemExit('unsupported pages shape')

def main():
    manifest=json.loads((SD/'manifest.json').read_text(encoding='utf-8'))
    tech=json.loads(TECH.read_text(encoding='utf-8'))
    meta=json.loads(META.read_text(encoding='utf-8'))
    pages=load_pages(); byid={p.get('id'):p for p in pages if isinstance(p,dict) and p.get('id')}
    rows=meta['source_records']
    assert manifest['counts']=={'image_download_failures':0,'image_references':42,'images_downloaded':42,'pages':42,'questions':112}
    assert not any(manifest['anomalies'].values())
    assert tech['all_images_technically_verified'] and tech['checks']['failures']==0
    assert all(tech['checks'][k]==42 for k in ('existing_files','readable_images','sha256_matches','byte_size_matches','mime_matches'))
    assert not tech['duplicate_sha256_groups_within_subject']
    assert len(rows)==42 and meta['duplicate_page_number_occurrences']=={} and meta['duplicate_sha256_ordinal_groups']==[]
    bytitle={}
    for r in rows:
        t=(r.get('title') or '').strip(); assert t and t not in bytitle; bytitle[t]=r
    models=[]; used=[]
    for m in range(1,15):
        rs=[bytitle[f'النموذج {m} الورقة 1'],bytitle[f'النموذج {m} الورقة 2'],bytitle[f'نموذج التصحيح النموذج {m}']]
        ords=[r['source_record_ordinal'] for r in rs]; nums=[r['page_number'] for r in rs]; used+=ords
        assert nums==[3*m-2,3*m-1,3*m]
        models.append({'id':f'math-1447-exam-{m:02d}','internal_ordinal':m,'source_model_label':f'النموذج {m}','official_model_code':'NOT VERIFIED','term':'NOT VERIFIED','exam_type':'وزاري','ordered_source_record_ordinals':ords,'ordered_page_numbers':nums,'ordered_legacy_page_ids':[r['legacy_page_id'] for r in rs],'raw_paths':[r['raw_path'] for r in rs],'sha256':[r['sha256'] for r in rs],'question_source_record_ordinals':ords[:2],'correction_sheet_candidate_source_record_ordinal':ords[2],'boundary_status':'verified_from_explicit_unique_source_titles_and_contiguous_source_sequence','visual_semantic_review_status':'NOT VERIFIED','answer_key_status':'NOT VERIFIED'})
    assert sorted(used)==list(range(1,43)) and len(set(used))==42
    row_by_ord={r['source_record_ordinal']:r for r in rows}; qrecords=[]; qtotal=0
    for model in models:
        for ordn,pid in zip(model['question_source_record_ordinals'],model['ordered_legacy_page_ids'][:2]):
            qs=(byid.get(pid) or {}).get('ai_questions') or []; qtotal+=len(qs)
            for idx,q in enumerate(qs,1): qrecords.append({'source_record_ordinal':ordn,'page_number':row_by_ord[ordn]['page_number'],'legacy_page_id':pid,'question_ordinal_on_page':idx,'source_reference':q.get('source_reference') if isinstance(q,dict) else None,'mapping_status':'exam_linked_structural','individual_exam_model_id':model['id']})
    assert qtotal==112 and len(qrecords)==112
    out={'schema_version':1,'source_group_id':SID,'source_group_name':'الرياضيات نماذج وزارية 1447','classification':'exam_source_group','academic_year_hijri':'1447','source_pages':42,'source_questions':112,'source_records_reviewed':42,'verified_source_occurrence_count':14,'review_required_block_count':0,'individual_exam_model_count':14,'finalized_exam_page_count':42,'review_required_page_count':0,'correction_sheet_candidate_count':14,'verified_answer_key_count':0,'duplicate_sha256_groups_within_source':0,'source_numbering_anomalies':{'duplicate_page_numbers':[],'missing_page_numbers':[],'normalization_performed':False,'identity_key':'legacy_page_id + source_record_ordinal'},'models':models,'question_mapping':{'exam_linked_structural':112,'review_required':0,'unassigned_within_source':0,'semantic_correctness':'NOT VERIFIED','records':qrecords},'evidence':{'technical_report':f'content-staging/reconstruction/technical/{SID}.json','metadata_evidence':f'content-staging/reconstruction/exams/source-groups/{SID}-metadata-evidence.json','github_actions_discovery_run':34859563356,'visual_contact_sheets_generated':True,'visual_semantic_review':'NOT VERIFIED','raw_mutations':0},'status':'processed_boundary_verified_from_explicit_titles_visual_semantics_not_verified_answer_keys_not_verified'}
    OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'models':14,'finalized_exam_pages':42,'exam_linked':112,'visual_semantic_review':'NOT VERIFIED'},ensure_ascii=False))
if __name__=='__main__': main()
