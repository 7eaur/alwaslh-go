#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
SID='a7f1e94f-82d1-4146-af5b-4e9b51363f0b'
RECON=ROOT/'content-staging/reconstruction/educational'/f'{SID}.json'
MASTER=ROOT/'content-staging/manifests/MASTER_CONTENT_MANIFEST.json'
MARK='GEOGRAPHY_BOOK_CHECKPOINT'; START=f'<!-- {MARK}_START -->'; END=f'<!-- {MARK}_END -->'

def replace_block(path, body):
    text=path.read_text(encoding='utf-8'); block=f'{START}\n{body.rstrip()}\n{END}'
    if START in text and END in text:
        before=text.split(START,1)[0].rstrip(); after=text.split(END,1)[1].lstrip(); text=before+'\n\n'+block+('\n\n'+after if after else '\n')
    else: text=text.rstrip()+'\n\n'+block+'\n'
    path.write_text(text,encoding='utf-8')

r=json.loads(RECON.read_text(encoding='utf-8'))
if r.get('status')!='reconstructed_verified': raise SystemExit('geography reconstruction not verified')
book=r['reconstructed_book']
if r['source_identity']['raw_master_exact_sha_matches']!=104 or book['retained_pages']!=104: raise SystemExit('geography identity/page gate failed')
if r['questions']['legacy_questions']!=0: raise SystemExit('geography question count drift')
p=json.loads(MASTER.read_text(encoding='utf-8')); progress=p['reconstruction_progress']
expected={'sources_completed':14,'educational_sources_completed':5,'verified_books':5,'source_images_technically_verified':1070,'lesson_linked_structural':2374,'exam_linked_to_individual_model':967,'review_required':351,'unclassified':22063}
for k,v in expected.items():
    if progress.get(k)!=v: raise SystemExit(f'live progress drift before geography finalization: {k}={progress.get(k)} expected={v}')
i=next(i for i,x in enumerate(p['sources']) if x['id']==SID); s=p['sources'][i]
if s.get('review_status') not in (None,'inventory_only','NOT VERIFIED','not_verified','review_needed'): raise SystemExit(f'geography source already appears finalized: {s.get("review_status")}')
for key in ('technical_verification','reconstruction'):
    value=s.get(key)
    if isinstance(value,dict) and value.get('status') in ('verified','reconstructed_verified'): raise SystemExit(f'geography already has verified {key}; fail closed')
next_source=p['sources'][i+1] if i+1<len(p['sources']) else None; next_id=next_source['id'] if next_source else 'NOT YET RESOLVED'; next_name=next_source['legacy_source']['name'] if next_source else 'NOT YET RESOLVED'
s['classification']='educational_book_source'; s['classification_evidence']='104/104 unique exact RAW/master SHA identity + exact master section/title runs'; s['review_status']='reconstructed_verified'
s['technical_verification']={'status':'verified','report_path':f'content-staging/reconstruction/technical/{SID}.json','images_verified':104,'readable':104,'sha256_match_manifest':104,'mime_match_manifest':104,'duplicate_sha_groups_within_source':0}
s['reconstruction']={'status':'verified','path':f'content-staging/reconstruction/educational/{SID}.json','book_title':'كتاب الجغرافيا','retained_page_range':r['source_identity']['stored_page_range'],'source_reference_page_range':r['source_identity']['source_reference_page_range'],'retained_pages':104,'units':book['unit_count'],'lessons':book['lesson_count'],'lesson_pages':book['lesson_page_count'],'unit_cover_pages':book['unit_cover_page_count'],'unit_review_pages':book['unit_review_page_count'],'non_lesson_pages':book['non_lesson_page_count'],'legacy_questions':0,'structurally_lesson_linked_questions':0,'review_required_questions':0,'semantic_question_review':'NOT APPLICABLE','raw_mutations':0}
new=dict(progress); new.update({'sources_completed':15,'educational_sources_completed':6,'verified_books':6,'verified_units':progress['verified_units']+book['unit_count'],'verified_lessons':progress['verified_lessons']+book['lesson_count'],'verified_lesson_pages':progress['verified_lesson_pages']+book['lesson_page_count'],'source_images_technically_verified':1174})
assert new['lesson_linked_structural']+new['exam_linked_to_individual_model']+new['review_required']+new['unclassified']==25755
p['status']='RECONSTRUCTION_IN_PROGRESS_NOT_IMPORT_READY'; p['reconstruction_progress']=new; MASTER.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=f'''## Reconstruction checkpoint — Grade 9 Geography\n\n- Sources processed: **15/58**; Educational: **6/26**; Exam Source Groups: **9/32**.\n- Books / Units / Lessons / Lesson pages: **6 / {new['verified_units']} / {new['verified_lessons']} / {new['verified_lesson_pages']}**.\n- Geography: **104/104** technically verified and unique exact RAW/master SHA identities.\n- Reconstructed: **{book['unit_count']} Units, {book['lesson_count']} Lessons, {book['lesson_page_count']} Lesson pages, {book['unit_cover_page_count']} covers, {book['unit_review_page_count']} reviews, {book['non_lesson_page_count']} non-lesson pages**.\n- Questions unchanged: **2,374 + 967 + 351 + 22,063 = 25,755**.\n- Source images technical **1,174/5,273**. RAW/unrelated/import/publication mutations **0/0/0/0**.\n- Next: `{next_id} — {next_name}`.\n'''
for path in ['CONTENT_REBUILD_EXECUTION_STATUS.md','CONTENT_REBUILD_HANDOFF.md','CONTENT_INVENTORY.md','CONTENT_VALIDATION_REPORT.md','CONTENT_IMPORT_REPORT.md','CONTENT_REBUILD_CONTINUATION_2026-09-14.md']:
    fp=ROOT/'content-staging'/path
    if fp.exists(): replace_block(fp,summary)
print(json.dumps({'sources':15,'educational':6,'books':6,'units':new['verified_units'],'lessons':new['verified_lessons'],'lesson_pages':new['verified_lesson_pages'],'images_verified':1174,'next_source_id':next_id,'next_source_name':next_name,'invariant':25755},ensure_ascii=False))
