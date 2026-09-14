#!/usr/bin/env python3
import json
from collections import OrderedDict, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
SID='3df6f57e-26cb-414e-97c5-ef6bd2ff4487'
SUBJ=ROOT/'content-staging/raw/legacy-supabase/subjects'/SID
TECH=ROOT/'content-staging/reconstruction/technical'/f'{SID}.json'
DISC=ROOT/'content-staging/reconstruction/exams/source-groups'/f'{SID}-discovery.json'
OUT=ROOT/'content-staging/reconstruction/exams/source-groups'/f'{SID}.json'
MASTER=ROOT/'content-staging/manifests/MASTER_CONTENT_MANIFEST.json'
START='<!-- BIOLOGY_EXAM_1447_CHECKPOINT_START -->'; END='<!-- BIOLOGY_EXAM_1447_CHECKPOINT_END -->'

# Source-local visual review. Question blocks are three pages followed by a correction/result sheet.
BLOCKS=[
(1,'P.28','P.28','verified'),(5,'P.63','P.63','verified'),(9,'P.10','P.10','verified'),(13,'P.2','P.2','verified'),
(17,'P.84','P.84','verified'),(21,'P.23','P.23','verified'),(25,'P.97','P.97','verified'),(29,'P.55','P.55','verified'),
(33,'P.30','P.30','verified'),(37,'P.61','P.31','review_required'),(41,'P.7','P.7','verified'),(45,'P.28','P.88','review_required'),
(49,'P.8','P.8','verified'),(53,'P.45','P.45','verified'),(57,'P.8','P.8','verified'),(61,'P.80','P.80','verified'),
(65,'P.61','P.61','verified'),(69,'P.71','P.71','verified'),(73,'P.6','P.6','verified'),(77,'P.44','P.44','verified'),
(81,'P.57','P.57','verified'),(85,'P.106','P.106','verified'),(89,'P.89','P.89','verified'),(93,'P.77','P.77','verified'),
(97,'P.19','P.19','verified'),(101,'P.18','P.18','verified'),(105,'P.21','P.21','verified'),(109,'P.64','P.64','verified'),
(113,'P.56','P.56','verified'),(117,'P.12','P.12','verified'),(121,'P.9','P.9','verified')]
EXPECTED={(1,45),(2,46),(3,47),(37,65),(38,66),(39,67),(49,57),(50,58),(51,59)}

def rep(path,body):
    text=path.read_text(encoding='utf-8'); block=f'{START}\n{body.rstrip()}\n{END}'
    if START in text and END in text:
        text=text.split(START,1)[0].rstrip()+'\n\n'+block+'\n\n'+text.split(END,1)[1].lstrip()
    else: text=text.rstrip()+'\n\n'+block+'\n'
    path.write_text(text,encoding='utf-8')

def processed(s):
    st=str(s.get('review_status') or '')
    return st.startswith('processed_') or st=='reconstructed_verified'

def next_source(master,idx):
    src=master['sources']
    for x in src[idx+1:]+src[:idx]:
        if not processed(x): return x
    return None

def mid(code): return 'biology-1447-model-'+code.lower().replace('.','-')

def main():
    subject=json.loads((SUBJ/'subject.json').read_text(encoding='utf-8'))
    manifest=json.loads((SUBJ/'manifest.json').read_text(encoding='utf-8'))
    pages=json.loads((SUBJ/'pages.json').read_text(encoding='utf-8'))
    tech=json.loads(TECH.read_text(encoding='utf-8')); disc=json.loads(DISC.read_text(encoding='utf-8'))
    c=tech['checks']
    assert tech['all_images_technically_verified'] is True
    assert all(c[k]==124 for k in ('manifest_image_count','existing_files','readable_images','sha256_matches','byte_size_matches','mime_matches'))
    assert c['failures']==0 and tech['raw_mutations']==0
    seq=tech['page_sequence']; assert seq['first_page_number']==1 and seq['last_page_number']==124 and not seq['missing_page_numbers'] and not seq['duplicate_page_numbers']
    assert manifest['counts']['pages']==124 and manifest['counts']['images_downloaded']==124 and manifest['counts']['questions']==50 and manifest['counts']['image_download_failures']==0
    assert disc['page_sequence']['count']==124 and disc['page_sequence']['contiguous']
    assert isinstance(pages,list) and len(pages)==124
    byp={int(p['page_number']):p for p in pages}; assert sorted(byp)==list(range(1,125))
    imgs={int(x['page_number']):x for x in manifest['images']}; assert sorted(imgs)==list(range(1,125))
    sha=defaultdict(list)
    for n,x in imgs.items(): sha[x['sha256']].append(n)
    pairs={tuple(sorted(v)) for v in sha.values() if len(v)>1}
    assert pairs==EXPECTED and len(tech.get('duplicate_sha256_groups_within_subject') or [])==9

    qcounts={n:len(byp[n].get('ai_questions') or []) for n in range(1,125)}; assert sum(qcounts.values())==50
    valid=OrderedDict(); reviews=[]; p2m={}; review_pages=set(); occ=[]
    for ordinal,(first,qcode,ccode,status) in enumerate(BLOCKS,1):
        nums=list(range(first,first+4)); qn=sum(qcounts[n] for n in nums)
        row={'source_block_ordinal':ordinal,'first_page':first,'last_page':first+3,'ordered_page_numbers':nums,'question_pages':nums[:3],'correction_sheet_candidate_page':nums[3],'question_model_code':qcode,'correction_report_model_code':ccode,'source_block_question_count':qn,'status':status,'ordered_legacy_page_ids':[imgs[n]['legacy_page_id'] for n in nums],'raw_paths':[imgs[n]['raw_path'] for n in nums],'sha256':[imgs[n]['sha256'] for n in nums]}
        if status=='verified':
            assert qcode==ccode; valid.setdefault(qcode,[]).append(row); occ.append(row)
            for n in nums: p2m[n]=mid(qcode)
        else:
            assert qcode!=ccode; row['review_reason']='question_model_code_and_correction_report_model_code_do_not_match'; reviews.append(row); review_pages.update(nums)
    assert len(occ)==29 and len(valid)==28 and len(reviews)==2 and [x['first_page'] for x in reviews]==[37,45]
    assert len(valid['P.8'])==2

    models=[]
    for i,(code,os) in enumerate(valid.items(),1):
        can=os[0]
        model={'id':mid(code),'internal_ordinal':i,'official_model_code':code,'official_title':'اختبار الشهادة الثانوية العامة (القسم العلمي) - الأحياء','academic_year_hijri':'1447','academic_year_gregorian':'2025-2026','term':'NOT VERIFIED','exam_type':'وزاري','first_page':can['first_page'],'last_page':can['last_page'],'page_count':4,'ordered_page_numbers':can['ordered_page_numbers'],'question_pages':can['question_pages'],'correction_sheet_candidate_page':can['correction_sheet_candidate_page'],'source_occurrence_count':len(os),'source_occurrences':os,'associated_legacy_questions':sum(o['source_block_question_count'] for o in os),'boundary_status':'verified','answer_key':{'status':'NOT VERIFIED','reason':'Correction/result sheet is paired and model-coded, but source evidence does not establish a standalone official Answer Key.'},'review_status':'boundary_verified_correction_relation_verified_answer_key_unverified'}
        if code=='P.8': model['repeat_classification']={'classification':'legitimate_repeated_exam_model_occurrence','canonical_occurrence_pages':os[0]['ordered_page_numbers'],'repeated_occurrence_pages':[o['ordered_page_numbers'] for o in os[1:]],'reason':'Question pages 49..51 and 57..59 are exact-SHA duplicates with matching P.8 correction reports 52 and 60.'}
        models.append(model)
    linked=sum(qcounts[n] for n in p2m); reviewq=sum(qcounts[n] for n in review_pages); assert linked+reviewq==50
    maps=[]
    for n in range(1,125):
        for qi,_ in enumerate(byp[n].get('ai_questions') or [],1):
            maps.append({'page_number':n,'legacy_page_id':byp[n].get('id'),'question_ordinal_on_page':qi,'mapping_status':'exam_linked_structural' if n in p2m else 'review_required','individual_exam_model_id':p2m.get(n,'NOT VERIFIED'),'semantic_correctness':'NOT VERIFIED'})
    assert len(maps)==50
    recon={'schema_version':1,'source_group_id':SID,'source_group_name':subject['subject']['name'],'class_id':subject['class']['id'],'class_name':subject['class']['name'].strip(),'subject':'الأحياء','classification':'exam_source_group','academic_year_hijri':'1447','academic_year_gregorian':'2025-2026','source_pages':124,'source_questions':50,'source_blocks_reviewed':31,'verified_source_occurrence_count':29,'review_required_block_count':2,'individual_exam_model_count':28,'finalized_exam_page_count':116,'review_required_page_count':8,'correction_sheet_candidate_count':29,'verified_answer_key_count':0,'duplicate_sha256_groups_within_source':9,'duplicate_sha256_groups':tech['duplicate_sha256_groups_within_subject'],'duplicate_disposition':'source_local_relation_resolved_where_evidence_sufficient_review_required_for_mismatched_correction_pairs','models':models,'review_required_blocks':reviews,'question_mapping':{'exam_linked_structural':linked,'review_required':reviewq,'unassigned_within_source':0,'semantic_correctness':'NOT VERIFIED','records':maps},'evidence':{'technical_report':f'content-staging/reconstruction/technical/{SID}.json','discovery_report':f'content-staging/reconstruction/exams/source-groups/{SID}-discovery.json','visual_review':'all 124 pages reviewed in contact sheets 001-012 through 121-124','visual_discovery_workflow_run':34893245344,'visual_discovery_artifact_id':10368161081,'raw_mutations':0},'status':'boundary_verified_with_two_review_required_mismatched_blocks'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(recon,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    master=json.loads(MASTER.read_text(encoding='utf-8')); src=master['sources']; idx=next(i for i,s in enumerate(src) if s['id']==SID); s=src[idx]
    oldp=processed(s); olde=s.get('exam_reconstruction') if isinstance(s.get('exam_reconstruction'),dict) else {}; oldt=s.get('technical_verification') if isinstance(s.get('technical_verification'),dict) else {}
    oldmodels=int(olde.get('individual_exam_models') or 0); oldpages=int(olde.get('finalized_exam_pages') or 0); oldcorr=int(olde.get('correction_sheet_candidates') or 0); oldlink=int(olde.get('exam_linked_questions') or 0); oldrev=int(olde.get('review_required_questions') or 0); oldimg=int(oldt.get('images_verified') or 0)
    s.update({'classification':'exam_source_group','classification_evidence':'legacy exam label + 124/124 technical verification + complete source-local visual review of 31 four-page blocks','review_status':'processed_boundary_verified_with_review_required_mismatched_blocks','exam_models':28,'answer_keys':'NOT VERIFIED','technical_verification':{'status':'verified','report_path':f'content-staging/reconstruction/technical/{SID}.json','images_verified':124,'readable':124,'sha256_match_manifest':124,'mime_match_manifest':124,'duplicate_sha_groups_within_source':9},'exam_reconstruction':{'status':recon['status'],'path':f'content-staging/reconstruction/exams/source-groups/{SID}.json','source_blocks_reviewed':31,'verified_source_occurrences':29,'review_required_blocks':2,'individual_exam_models':28,'source_pages':124,'finalized_exam_pages':116,'review_required_pages':8,'correction_sheet_candidates':29,'verified_answer_keys':0,'answer_key_status':'NOT VERIFIED','exam_linked_questions':linked,'review_required_questions':reviewq,'associated_legacy_questions':50,'semantic_question_correctness':'NOT VERIFIED','duplicate_sha_groups_within_source':9,'raw_mutations':0}})
    p=master['reconstruction_progress']; p['sources_completed']=int(p.get('sources_completed') or 0)+(0 if oldp else 1); p['exam_source_groups_completed']=int(p.get('exam_source_groups_completed') or 0)+(0 if oldp else 1); p['individual_exam_models']=int(p.get('individual_exam_models') or 0)+(28-oldmodels); p['exam_pages_completed']=int(p.get('exam_pages_completed') or 0)+(116-oldpages); p['correction_sheet_candidates']=int(p.get('correction_sheet_candidates') or 0)+(29-oldcorr); p['source_images_technically_verified']=int(p.get('source_images_technically_verified') or 0)+(124-oldimg); p['exam_linked_to_individual_model']=int(p.get('exam_linked_to_individual_model') or 0)+(linked-oldlink); p['review_required']=int(p.get('review_required') or 0)+(reviewq-oldrev); p['unclassified']=int(p.get('unclassified') or 0)-((linked-oldlink)+(reviewq-oldrev)); assert sum(int(p.get(k) or 0) for k in ('lesson_linked_structural','exam_linked_to_individual_model','review_required','unclassified'))==25755
    assert p['raw_mutations']==0 and p['unrelated_mutations']==0 and p['new_imports']==0 and p['new_publications']==0
    master['status']='RECONSTRUCTION_IN_PROGRESS_NOT_IMPORT_READY'; nxt=next_source(master,idx); MASTER.write_text(json.dumps(master,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    nid=nxt['id'] if nxt else 'NONE'; nname=(nxt.get('legacy_source') or {}).get('name') if nxt else 'NONE'
    body=f'''## Reconstruction checkpoint — Biology Ministry Exams 1447\n\n- Source `{SID}` completed from source-local evidence.\n- Technical verification: **124/124**; contiguous pages **1..124**; **9** within-source SHA duplicate groups preserved.\n- Visual review: **31** four-page blocks reviewed; **29** verified occurrences; **2** mismatched question/correction blocks isolated as `review_required`; **28** unique Individual Exam Models.\n- Finalized Exam Pages: **116**; review-required pages: **8**; correction candidates: **29**; verified standalone Answer Keys: **0 / NOT VERIFIED**.\n- Legacy questions: **{linked}** exam-linked structurally; **{reviewq}** review-required; semantic correctness `NOT VERIFIED`.\n- Global progress: Sources **{p['sources_completed']}/58**; Exam Groups **{p['exam_source_groups_completed']}/32**; Individual Models **{p['individual_exam_models']}**; Exam Pages **{p['exam_pages_completed']}/2,286**; source images **{p['source_images_technically_verified']}/5,273**.\n- Question invariant: PASS = 25,755. RAW/unrelated/import/publication mutations: **0/0/0/0**.\n- Next source: `{nid}` — `{nname}`.\n'''
    for fn in ('CONTENT_REBUILD_EXECUTION_STATUS.md','CONTENT_REBUILD_HANDOFF.md','CONTENT_INVENTORY.md','CONTENT_VALIDATION_REPORT.md','CONTENT_IMPORT_REPORT.md','CONTENT_REBUILD_CONTINUATION_2026-09-14.md'):
        path=ROOT/'content-staging'/fn
        if path.exists(): rep(path,body)
    print(json.dumps({'models':28,'verified_occurrences':29,'review_blocks':2,'exam_pages':116,'review_pages':8,'exam_linked':linked,'review_required_questions':reviewq,'next_source_id':nid,'next_source_name':nname,'progress':p},ensure_ascii=False))

if __name__=='__main__': main()
