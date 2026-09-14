#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SID='b80cbba1-410a-4346-9446-c3f01c4f9e56'
RECON=ROOT/'content-staging/reconstruction/educational'/f'{SID}.json'
MASTER=ROOT/'content-staging/manifests/MASTER_CONTENT_MANIFEST.json'
MARK='MATH_BOOK_PART2_CHECKPOINT'; START=f'<!-- {MARK}_START -->'; END=f'<!-- {MARK}_END -->'
def replace_block(path,body):
    text=path.read_text(encoding='utf-8'); block=f'{START}\n{body.rstrip()}\n{END}'
    if START in text and END in text:
        before=text.split(START,1)[0].rstrip(); after=text.split(END,1)[1].lstrip(); text=before+'\n\n'+block+('\n\n'+after if after else '\n')
    else: text=text.rstrip()+'\n\n'+block+'\n'
    path.write_text(text,encoding='utf-8')
r=json.loads(RECON.read_text(encoding='utf-8')); book=r['reconstructed_book']; q=r['questions']
assert r['status']=='reconstructed_verified_source_local_visual_structure'
assert book['unit_count']==3 and book['lesson_count']==19 and book['lesson_member_page_count']==122 and book['nonlesson_page_count']==13
assert q['legacy_questions']==0 and q['structurally_lesson_linked_questions']==0 and q['review_required_questions']==0 and q['unclassified_questions']==0
p=json.loads(MASTER.read_text(encoding='utf-8')); progress=p['reconstruction_progress']
expected={'sources_completed':24,'educational_sources_completed':11,'verified_books':11,'verified_units':37,'verified_lessons':217,'verified_lesson_pages':1039,'source_images_technically_verified':1851,'lesson_linked_structural':7511,'exam_linked_to_individual_model':1132,'review_required':448,'unclassified':16664}
for k,v in expected.items():
    if progress.get(k)!=v: raise SystemExit(f'progress drift {k}={progress.get(k)} expected={v}')
i=next(i for i,x in enumerate(p['sources']) if x['id']==SID); s=p['sources'][i]
if s.get('review_status') not in (None,'inventory_only','NOT VERIFIED','not_verified','review_needed'):
    raise SystemExit(f'already finalized: {s.get("review_status")}')
next_source=p['sources'][i+1] if i+1<len(p['sources']) else None
next_id=next_source['id'] if next_source else 'NOT YET RESOLVED'; next_name=next_source['legacy_source']['name'] if next_source else 'NOT YET RESOLVED'
s['classification']='educational_book_source'
s['classification_evidence']='135/135 technical RAW verification + source-local pages.json title continuity + complete contact-sheet visual review of every retained page; no Part 1 structure inherited'
s['review_status']='reconstructed_verified_source_local_visual_structure'
s['technical_verification']={'status':'verified','report_path':f'content-staging/reconstruction/technical/{SID}.json','images_verified':135,'readable':135,'sha256_match_manifest':135,'mime_match_manifest':135,'duplicate_sha_groups_within_source':0}
s['reconstruction']={'status':'verified','path':f'content-staging/reconstruction/educational/{SID}.json','book_title':'كتاب الرياضيات - الجزء الثاني','retained_page_range':[7,141],'retained_pages':135,'units':3,'lessons':19,'lesson_pages':122,'nonlesson_pages':13,'review_pages':0,'general_exercise_pages':7,'unit_test_pages':6,'legacy_questions':0,'structurally_lesson_linked_questions':0,'review_required_questions':0,'semantic_question_review':'NOT APPLICABLE — source has zero legacy questions','raw_mutations':0}
new=dict(progress); new.update({'sources_completed':25,'educational_sources_completed':12,'verified_books':12,'verified_units':40,'verified_lessons':236,'verified_lesson_pages':1161,'source_images_technically_verified':1986})
assert new['lesson_linked_structural']+new['exam_linked_to_individual_model']+new['review_required']+new['unclassified']==25755
assert new['raw_mutations']==0 and new['unrelated_mutations']==0 and new['new_imports']==0 and new['new_publications']==0
p['reconstruction_progress']=new; MASTER.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary=f'''## Reconstruction checkpoint — Math Book Part 2\n\n- Sources processed: **25/58**; Educational: **12/26**; Exam Source Groups: **{new['exam_source_groups_completed']}/32**.\n- Books / Units / Lessons / Lesson pages: **12 / 40 / 236 / 1,161**.\n- Math Part 2: **135/135** RAW images technically verified; complete visual review establishes **3 units / 19 lessons / 122 lesson pages / 13 non-lesson pages**.\n- Verified unit banners: **الوحدة الخامسة — الهندسة**; **الوحدة السادسة — الهندسة الإحداثية والتحويلات**; **الوحدة السابعة — الإحصاء**.\n- Non-lesson pages: **7 general-exercise + 6 unit-test pages**.\n- Questions: this source contains **0 legacy questions**; no question mappings invented.\n- Global invariant: **7,511 + 1,132 + 448 + 16,664 = 25,755**.\n- Source images technical **1,986/5,273**. RAW/unrelated/import/publication mutations **0/0/0/0**.\n- Next: `{next_id} — {next_name}`.\n'''
for name in ['CONTENT_REBUILD_EXECUTION_STATUS.md','CONTENT_REBUILD_HANDOFF.md','CONTENT_INVENTORY.md','CONTENT_VALIDATION_REPORT.md','CONTENT_IMPORT_REPORT.md','CONTENT_REBUILD_CONTINUATION_2026-09-14.md']:
    fp=ROOT/'content-staging'/name
    if fp.exists(): replace_block(fp,summary)
print(json.dumps({'sources':25,'educational':12,'books':12,'units':40,'lessons':236,'lesson_pages':1161,'images_verified':1986,'lesson_linked':new['lesson_linked_structural'],'exam_linked':new['exam_linked_to_individual_model'],'review_required':new['review_required'],'unclassified':new['unclassified'],'next_source_id':next_id,'next_source_name':next_name},ensure_ascii=False))
