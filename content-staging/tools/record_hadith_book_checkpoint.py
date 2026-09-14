#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SID='cae82d8f-64f9-4d2a-984f-6e6fd19fac5c'
RECON=ROOT/'content-staging/reconstruction/educational'/f'{SID}.json'
MASTER=ROOT/'content-staging/manifests/MASTER_CONTENT_MANIFEST.json'
MARK='HADITH_BOOK_CHECKPOINT'; START=f'<!-- {MARK}_START -->'; END=f'<!-- {MARK}_END -->'
def replace_block(path,body):
    text=path.read_text(encoding='utf-8'); block=f'{START}\n{body.rstrip()}\n{END}'
    if START in text and END in text:
        before=text.split(START,1)[0].rstrip(); after=text.split(END,1)[1].lstrip(); text=before+'\n\n'+block+('\n\n'+after if after else '\n')
    else: text=text.rstrip()+'\n\n'+block+'\n'
    path.write_text(text,encoding='utf-8')
r=json.loads(RECON.read_text()); book=r['reconstructed_book']
assert r['status']=='reconstructed_verified_exact_sha_lesson_membership'
assert r['source_identity']['exact_sha_matches']==62 and book['lesson_count']==10 and book['lesson_member_page_count']==62
assert r['questions']['legacy_questions']==1483 and r['questions']['structurally_lesson_linked_questions']==1483
p=json.loads(MASTER.read_text()); progress=p['reconstruction_progress']
expected={'sources_completed':17,'educational_sources_completed':7,'verified_books':7,'source_images_technically_verified':1332,'lesson_linked_structural':3350,'exam_linked_to_individual_model':967,'review_required':351,'unclassified':21087}
for k,v in expected.items():
    if progress.get(k)!=v: raise SystemExit(f'progress drift {k}={progress.get(k)} expected={v}')
i=next(i for i,x in enumerate(p['sources']) if x['id']==SID); s=p['sources'][i]
if s.get('review_status') not in (None,'inventory_only','NOT VERIFIED','not_verified','review_needed'): raise SystemExit(f'already finalized: {s.get("review_status")}')
next_source=p['sources'][i+1] if i+1<len(p['sources']) else None; next_id=next_source['id'] if next_source else 'NOT YET RESOLVED'; next_name=next_source['legacy_source']['name'] if next_source else 'NOT YET RESOLVED'
s['classification']='educational_book_source'; s['classification_evidence']='62/62 exact RAW/master SHA identity; every retained master filename explicitly labels one of 10 lessons'
s['review_status']='reconstructed_verified_exact_sha_lesson_membership'
s['technical_verification']={'status':'verified','report_path':f'content-staging/reconstruction/technical/{SID}.json','images_verified':62,'readable':62,'sha256_match_manifest':62,'mime_match_manifest':62}
s['reconstruction']={'status':'verified','path':f'content-staging/reconstruction/educational/{SID}.json','book_title':'كتاب الحديث والتهذيب','retained_page_range':[9,70],'retained_pages':62,'units':0,'unit_status':'NOT VERIFIED','lessons':10,'lesson_pages':62,'page_subtype_review_boundaries':'NOT VERIFIED','legacy_questions':1483,'structurally_lesson_linked_questions':1483,'review_required_questions':0,'semantic_question_review':'NOT VERIFIED','raw_mutations':0}
new=dict(progress); new.update({'sources_completed':18,'educational_sources_completed':8,'verified_books':8,'verified_lessons':progress['verified_lessons']+10,'verified_lesson_pages':progress['verified_lesson_pages']+62,'source_images_technically_verified':1394,'lesson_linked_structural':4833,'unclassified':19604})
assert new['lesson_linked_structural']+new['exam_linked_to_individual_model']+new['review_required']+new['unclassified']==25755
assert new['raw_mutations']==0 and new['unrelated_mutations']==0 and new['new_imports']==0 and new['new_publications']==0
p['reconstruction_progress']=new; MASTER.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
summary=f'''## Reconstruction checkpoint — Hadith and Refinement Book\n\n- Sources processed: **18/58**; Educational: **8/26**; Exam Source Groups: **10/32**.\n- Books / Units / Lessons / Lesson pages: **8 / {new['verified_units']} / {new['verified_lessons']} / {new['verified_lesson_pages']}**.\n- Hadith source: **62/62** technically verified + exact SHA-identical to `master/التربية الاسلاميه ثالث ثانوي/كتاب الحديث والتهذيب/الصور`.\n- Exact filename evidence establishes **10 lessons** and assigns **62/62 retained pages** to one lesson; no unit layer was asserted (`NOT VERIFIED`).\n- Questions: **1,483/1,483 structurally lesson-linked** by exact page membership; semantic correctness remains `NOT VERIFIED`.\n- Global question invariant: **4,833 + 967 + 351 + 19,604 = 25,755**.\n- Source images technical **1,394/5,273**. RAW/unrelated/import/publication mutations **0/0/0/0**.\n- Next: `{next_id} — {next_name}`.\n'''
for name in ['CONTENT_REBUILD_EXECUTION_STATUS.md','CONTENT_REBUILD_HANDOFF.md','CONTENT_INVENTORY.md','CONTENT_VALIDATION_REPORT.md','CONTENT_IMPORT_REPORT.md','CONTENT_REBUILD_CONTINUATION_2026-09-14.md']:
    fp=ROOT/'content-staging'/name
    if fp.exists(): replace_block(fp,summary)
print(json.dumps({'sources':18,'educational':8,'books':8,'units':new['verified_units'],'lessons':new['verified_lessons'],'lesson_pages':new['verified_lesson_pages'],'images_verified':1394,'lesson_linked':4833,'unclassified':19604,'next_source_id':next_id,'next_source_name':next_name},ensure_ascii=False))
