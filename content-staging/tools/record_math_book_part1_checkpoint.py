#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SID='1933807f-4cb0-40c9-9b29-3ef3d32c98dc'
RECON=ROOT/'content-staging/reconstruction/educational'/f'{SID}.json'
MASTER=ROOT/'content-staging/manifests/MASTER_CONTENT_MANIFEST.json'
MARK='MATH_BOOK_PART1_CHECKPOINT'; START=f'<!-- {MARK}_START -->'; END=f'<!-- {MARK}_END -->'
def replace_block(path,body):
    text=path.read_text(encoding='utf-8'); block=f'{START}\n{body.rstrip()}\n{END}'
    if START in text and END in text:
        before=text.split(START,1)[0].rstrip(); after=text.split(END,1)[1].lstrip(); text=before+'\n\n'+block+('\n\n'+after if after else '\n')
    else: text=text.rstrip()+'\n\n'+block+'\n'
    path.write_text(text,encoding='utf-8')
r=json.loads(RECON.read_text(encoding='utf-8')); book=r['reconstructed_book']; q=r['questions']
assert r['status']=='reconstructed_verified_source_local_visual_structure'
assert book['unit_count']==4 and book['lesson_count']==21 and book['lesson_member_page_count']==162 and book['nonlesson_page_count']==24
assert q['legacy_questions']==717 and q['structurally_lesson_linked_questions']==620 and q['review_required_questions']==97 and q['unclassified_questions']==0
p=json.loads(MASTER.read_text(encoding='utf-8')); progress=p['reconstruction_progress']
expected={'sources_completed':23,'educational_sources_completed':10,'verified_books':10,'verified_units':33,'verified_lessons':196,'verified_lesson_pages':877,'source_images_technically_verified':1665,'lesson_linked_structural':6891,'exam_linked_to_individual_model':1132,'review_required':351,'unclassified':17381}
for k,v in expected.items():
    if progress.get(k)!=v: raise SystemExit(f'progress drift {k}={progress.get(k)} expected={v}')
i=next(i for i,x in enumerate(p['sources']) if x['id']==SID); s=p['sources'][i]
if s.get('review_status') not in (None,'inventory_only','NOT VERIFIED','not_verified','review_needed'):
    raise SystemExit(f'already finalized: {s.get("review_status")}')
next_source=p['sources'][i+1] if i+1<len(p['sources']) else None
next_id=next_source['id'] if next_source else 'NOT YET RESOLVED'; next_name=next_source['legacy_source']['name'] if next_source else 'NOT YET RESOLVED'
s['classification']='educational_book_source'
s['classification_evidence']='186/186 technical RAW verification + source-local pages.json title continuity + complete direct RAW visual review; rejected master reference not used for structure'
s['review_status']='reconstructed_verified_source_local_visual_structure'
s['technical_verification']={'status':'verified','report_path':f'content-staging/reconstruction/technical/{SID}.json','images_verified':186,'readable':186,'sha256_match_manifest':186,'mime_match_manifest':186,'duplicate_sha_groups_within_source':0}
s['reconstruction']={'status':'verified','path':f'content-staging/reconstruction/educational/{SID}.json','book_title':'كتاب الرياضيات - الجزء الأول','retained_page_range':[7,192],'retained_pages':186,'units':4,'lessons':21,'lesson_pages':162,'nonlesson_pages':24,'review_pages':2,'general_exercise_pages':18,'unit_test_pages':4,'legacy_questions':717,'structurally_lesson_linked_questions':620,'review_required_questions':97,'semantic_question_review':'NOT VERIFIED','rejected_master_reference':'الرياضيات ثالث ثانوي/02_الرياضيات_ثالث_ثانوي','raw_mutations':0}
new=dict(progress); new.update({'sources_completed':24,'educational_sources_completed':11,'verified_books':11,'verified_units':37,'verified_lessons':217,'verified_lesson_pages':1039,'source_images_technically_verified':1851,'lesson_linked_structural':7511,'review_required':448,'unclassified':16664})
assert new['lesson_linked_structural']+new['exam_linked_to_individual_model']+new['review_required']+new['unclassified']==25755
assert new['raw_mutations']==0 and new['unrelated_mutations']==0 and new['new_imports']==0 and new['new_publications']==0
p['reconstruction_progress']=new; MASTER.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=f'''## Reconstruction checkpoint — Math Book Part 1\n\n- Sources processed: **24/58**; Educational: **11/26**; Exam Source Groups: **{new['exam_source_groups_completed']}/32**.\n- Books / Units / Lessons / Lesson pages: **11 / 37 / 217 / 1,039**.\n- Math Part 1: **186/186** RAW images technically verified; complete direct RAW visual review establishes **4 units / 21 lessons / 162 lesson pages / 24 non-lesson pages**.\n- The apparent master reference `الرياضيات ثالث ثانوي/02_الرياضيات_ثالث_ثانوي` remains explicitly rejected (0/186 SHA identity; no structure transferred).\n- Non-lesson pages: **2 review + 18 general exercise + 4 unit-test pages**.\n- Questions: **620 lesson-linked + 97 review_required = 717**, semantic correctness `NOT VERIFIED`.\n- Global invariant: **7,511 + 1,132 + 448 + 16,664 = 25,755**.\n- Source images technical **1,851/5,273**. RAW/unrelated/import/publication mutations **0/0/0/0**.\n- Next: `{next_id} — {next_name}`.\n'''
for name in ['CONTENT_REBUILD_EXECUTION_STATUS.md','CONTENT_REBUILD_HANDOFF.md','CONTENT_INVENTORY.md','CONTENT_VALIDATION_REPORT.md','CONTENT_IMPORT_REPORT.md','CONTENT_REBUILD_CONTINUATION_2026-09-14.md']:
    fp=ROOT/'content-staging'/name
    if fp.exists(): replace_block(fp,summary)
print(json.dumps({'sources':24,'educational':11,'books':11,'units':37,'lessons':217,'lesson_pages':1039,'images_verified':1851,'lesson_linked':7511,'review_required':448,'unclassified':16664,'next_source_id':next_id,'next_source_name':next_name},ensure_ascii=False))
