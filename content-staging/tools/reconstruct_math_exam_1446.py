#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
SID='85c13f3f-fe85-47c3-affb-fb437d10d908'
SD=ROOT/'content-staging/raw/legacy-supabase/subjects'/SID
OUT=ROOT/'content-staging/reconstruction/exams/source-groups'/f'{SID}.json'
TECH=ROOT/'content-staging/reconstruction/technical'/f'{SID}.json'
META=ROOT/'content-staging/reconstruction/exams/source-groups'/f'{SID}-metadata-evidence.json'
VIS=ROOT/'content-staging/reconstruction/exams/source-groups'/f'{SID}-visual-review.json'

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
    visual=json.loads(VIS.read_text(encoding='utf-8'))
    pages=load_pages(); byid={p.get('id'):p for p in pages if isinstance(p,dict) and p.get('id')}
    rows=meta['source_records']
    assert manifest['counts']['pages']==39 and manifest['counts']['images_downloaded']==39 and manifest['counts']['questions']==25 and manifest['counts']['image_download_failures']==0
    assert manifest['anomalies']['duplicate_page_numbers']==[16,29]
    assert tech['all_images_technically_verified'] and tech['checks']['failures']==0
    assert all(tech['checks'][k]==39 for k in ('existing_files','readable_images','sha256_matches','byte_size_matches','mime_matches'))
    assert not tech['duplicate_sha256_groups_within_subject']
    assert len(rows)==39 and meta['duplicate_page_number_occurrences']=={'16':[15,16],'29':[28,29]}
    assert visual['visual_findings']['verified_complete_model_count']==13 and visual['visual_findings']['all_occurrences_accounted_for']
    bytitle={}
    for r in rows:
        t=(r.get('title') or '').strip(); assert t and t not in bytitle, f'duplicate title: {t}'; bytitle[t]=r
    models=[]; used=[]
    for m in range(1,14):
        titles=[f'النموذج {m} الورقة 1',f'النموذج {m} الورقة 2',f'نموذج التصحيح النموذج {m}']
        rs=[bytitle[t] for t in titles]
        ords=[r['source_record_ordinal'] for r in rs]; nums=[r['page_number'] for r in rs]; used += ords
        models.append({
          'id':f'math-1446-exam-{m:02d}','internal_ordinal':m,'source_model_label':f'النموذج {m}',
          'official_model_code':'NOT VERIFIED','term':'NOT VERIFIED','exam_type':'وزاري',
          'ordered_source_record_ordinals':ords,'ordered_page_numbers':nums,
          'ordered_legacy_page_ids':[r['legacy_page_id'] for r in rs],
          'raw_paths':[r['raw_path'] for r in rs],'sha256':[r['sha256'] for r in rs],
          'question_source_record_ordinals':ords[:2],'correction_sheet_candidate_source_record_ordinal':ords[2],
          'boundary_status':'verified_from_explicit_source_titles_and_full_visual_review',
          'answer_key_status':'NOT VERIFIED'
        })
    assert sorted(used)==list(range(1,40)) and len(set(used))==39
    qrecords=[]; qtotal=0
    for model in models:
        for ordn,pid in zip(model['question_source_record_ordinals'],model['ordered_legacy_page_ids'][:2]):
            qs=(byid.get(pid) or {}).get('ai_questions') or []
            qtotal += len(qs)
            for idx,q in enumerate(qs,1):
                qrecords.append({'source_record_ordinal':ordn,'page_number':next(r['page_number'] for r in rows if r['source_record_ordinal']==ordn),'legacy_page_id':pid,'question_ordinal_on_page':idx,'source_reference':q.get('source_reference') if isinstance(q,dict) else None,'mapping_status':'exam_linked_structural','individual_exam_model_id':model['id']})
    assert qtotal==25 and len(qrecords)==25
    out={
      'schema_version':1,'source_group_id':SID,'source_group_name':'الرياضيات نماذج وزارية 1446','classification':'exam_source_group','academic_year_hijri':'1446',
      'source_pages':39,'source_questions':25,'source_records_reviewed':39,'verified_source_occurrence_count':13,'review_required_block_count':0,
      'individual_exam_model_count':13,'finalized_exam_page_count':39,'review_required_page_count':0,'correction_sheet_candidate_count':13,'verified_answer_key_count':0,'duplicate_sha256_groups_within_source':0,
      'source_numbering_anomalies':{'duplicate_page_numbers':[16,29],'normalization_performed':False,'identity_key':'legacy_page_id + source_record_ordinal'},
      'models':models,
      'question_mapping':{'exam_linked_structural':25,'review_required':0,'unassigned_within_source':0,'semantic_correctness':'NOT VERIFIED','records':qrecords},
      'evidence':{'technical_report':f'content-staging/reconstruction/technical/{SID}.json','metadata_evidence':f'content-staging/reconstruction/exams/source-groups/{SID}-metadata-evidence.json','visual_review':f'content-staging/reconstruction/exams/source-groups/{SID}-visual-review.json','visual_contact_sheets_generated':True,'raw_mutations':0},
      'status':'processed_boundary_verified_numbering_anomalies_preserved_answer_keys_not_verified'
    }
    OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'models':13,'finalized_exam_pages':39,'review_required_pages':0,'exam_linked':25,'duplicate_page_numbers':[16,29],'raw_mutations':0},ensure_ascii=False))
if __name__=='__main__': main()
