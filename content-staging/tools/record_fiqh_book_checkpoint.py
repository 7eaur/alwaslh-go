#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SID='6a8ea7f2-1e77-4654-a28c-0ea1b82b4830'
RECON=ROOT/'content-staging/reconstruction/educational'/f'{SID}.json'
MASTER=ROOT/'content-staging/manifests/MASTER_CONTENT_MANIFEST.json'
MARK='FIQH_BOOK_CHECKPOINT'; START=f'<!-- {MARK}_START -->'; END=f'<!-- {MARK}_END -->'
def replace_block(path,body):
    text=path.read_text(encoding='utf-8'); block=f'{START}\n{body.rstrip()}\n{END}'
    if START in text and END in text:
        before=text.split(START,1)[0].rstrip(); after=text.split(END,1)[1].lstrip(); text=before+'\n\n'+block+('\n\n'+after if after else '\n')
    else: text=text.rstrip()+'\n\n'+block+'\n'
    path.write_text(text,encoding='utf-8')
r=json.loads(RECON.read_text()); book=r['reconstructed_book']
assert r['status']=='reconstructed_verified_exact_sha_lesson_membership'
assert r['source_identity']['exact_sha_matches']==67 and book['lesson_count']==13 and book['lesson_member_page_count']==67
assert r['questions']['legacy_questions']==906 and r['questions']['structurally_lesson_linked_questions']==906
p=json.loads(MASTER.read_text()); progress=p['reconstruction_progress']
expected={'sources_completed':19,'educational_sources_completed':9,'verified_books':9,'source_images_technically_verified':1475,'lesson_linked_structural':5985,'exam_linked_to_individual_model':967,'review_required':351,'unclassified':18452}
for k,v in expected.items():
    if progress.get(k)!=v: raise SystemExit(f'progress drift {k}={progress.get(k)} expected={v}')
i=next(i for i,x in enumerate(p['sources']) if x['id']==SID); s=p['sources'][i]
if s.get('review_status') not in (None,'inventory_only','NOT VERIFIED','not_verified','review_needed'): raise SystemExit(f'already finalized: {s.get("review_status")}')
next_source=p['sources'][i+1] if i+1<len(p['sources']) else None; next_id=next_source['id'] if next_source else 'NOT YET RESOLVED'; next_name=next_source['legacy_source']['name'] if next_source else 'NOT YET RESOLVED'
s['classification']='educational_book_source'; s['classification_evidence']='67/67 exact RAW/master SHA identity; every retained master filename explicitly labels one of 13 lessons'
s['review_status']='reconstructed_verified_exact_sha_lesson_membership'
s['technical_verification']={'status':'verified','report_path':f'content-staging/reconstruction/technical/{SID}.json','images_verified':67,'readable':67,'sha256_match_manifest':67,'mime_match_manifest':67}
s['reconstruction']={'status':'verified','path':f'content-staging/reconstruction/educational/{SID}.json','book_title':'كتاب الفقه','retained_page_range':[8,74],'retained_pages':67,'units':0,'unit_status':'NOT VERIFIED','lessons':13,'lesson_pages':67,'explicit_evaluation_or_conclusion_filename_pages':[],'other_page_subtype_review_boundaries':'NOT VERIFIED','legacy_questions':906,'structurally_lesson_linked_questions':906,'review_required_questions':0,'semantic_question_review':'NOT VERIFIED','raw_mutations':0}
new=dict(progress); new.update({'sources_completed':20,'educational_sources_completed':10,'verified_books':10,'verified_lessons':progress['verified_lessons']+13,'verified_lesson_pages':progress['verified_lesson_pages']+67,'source_images_technically_verified':1542,'lesson_linked_structural':6891,'unclassified':17546})
assert new['lesson_linked_structural']+new['exam_linked_to_individual_model']+new['review_required']+new['unclassified']==25755
assert new['raw_mutations']==0 and new['unrelated_mutations']==0 and new['new_imports']==0 and new['new_publications']==0
p['reconstruction_progress']=new; MASTER.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
summary=f'''## Reconstruction checkpoint — Fiqh Book\n\n- Sources processed: **20/58**; Educational: **10/26**; Exam Source Groups: **10/32**.\n- Books / Units / Lessons / Lesson pages: **10 / {new['verified_units']} / {new['verified_lessons']} / {new['verified_lesson_pages']}**.\n- Fiqh source: **67/67** technically verified + exact SHA-identical to `master/التربية الاسلاميه ثالث ثانوي/كتاب الفقه/الصور`.\n- Exact filename evidence establishes **13 lessons** and assigns **67/67 retained pages** to one lesson; no unit layer was asserted (`NOT VERIFIED`).\n- Independent page subtype/review boundaries remain `NOT VERIFIED`; no unsupported review page was invented.\n- Questions: **906/906 structurally lesson-linked** by exact page membership; semantic correctness remains `NOT VERIFIED`.\n- Global question invariant: **6,891 + 967 + 351 + 17,546 = 25,755**.\n- Source images technical **1,542/5,273**. RAW/unrelated/import/publication mutations **0/0/0/0**.\n- Next: `{next_id} — {next_name}`.\n'''
for name in ['CONTENT_REBUILD_EXECUTION_STATUS.md','CONTENT_REBUILD_HANDOFF.md','CONTENT_INVENTORY.md','CONTENT_VALIDATION_REPORT.md','CONTENT_IMPORT_REPORT.md','CONTENT_REBUILD_CONTINUATION_2026-09-14.md']:
    fp=ROOT/'content-staging'/name
    if fp.exists(): replace_block(fp,summary)
print(json.dumps({'sources':20,'educational':10,'books':10,'units':new['verified_units'],'lessons':new['verified_lessons'],'lesson_pages':new['verified_lesson_pages'],'images_verified':1542,'lesson_linked':6891,'unclassified':17546,'next_source_id':next_id,'next_source_name':next_name},ensure_ascii=False))
