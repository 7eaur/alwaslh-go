#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; SID='4863bbf6-6cf3-4238-9407-75825724292a'; RECON=ROOT/'content-staging/reconstruction/educational'/f'{SID}.json'; MASTER=ROOT/'content-staging/manifests/MASTER_CONTENT_MANIFEST.json'; START='<!-- PHYSICS_BOOK_CHECKPOINT_START -->'; END='<!-- PHYSICS_BOOK_CHECKPOINT_END -->'
def repl(path,body):
 text=path.read_text(encoding='utf-8'); block=f'{START}\n{body.rstrip()}\n{END}'
 if START in text and END in text: text=text.split(START,1)[0].rstrip()+'\n\n'+block+('\n\n'+text.split(END,1)[1].lstrip() if text.split(END,1)[1].strip() else '\n')
 else:text=text.rstrip()+'\n\n'+block+'\n'
 path.write_text(text,encoding='utf-8')
r=json.loads(RECON.read_text()); ql=r['questions']['structurally_lesson_linked_questions']; qr=r['questions']['review_required_questions']; assert ql+qr==3101
m=json.loads(MASTER.read_text()); s=next(x for x in m['sources'] if x['id']==SID); p=m['reconstruction_progress']; already=s.get('review_status')=='reconstructed_verified'
if not already:
 p['sources_completed']+=1;p['educational_sources_completed']+=1;p['verified_books']+=1;p['verified_units']+=9;p['verified_lessons']+=45;p['verified_lesson_pages']+=173;p['source_images_technically_verified']+=207;p['lesson_linked_structural']+=ql;p['review_required']+=qr;p['unclassified']-=3101
s['classification']='educational_book_source';s['classification_evidence']='207/207 exact RAW/master SHA identity in one canonical physics directory + exact master filename title runs';s['review_status']='reconstructed_verified';s['technical_verification']={'status':'verified','report_path':f'content-staging/reconstruction/technical/{SID}.json','images_verified':207,'readable':207,'sha256_match_manifest':207,'mime_match_manifest':207};s['reconstruction']={'status':'verified','path':f'content-staging/reconstruction/educational/{SID}.json','book_title':'الفيزياء الكتاب المدرسي','retained_page_range':[9,215],'retained_pages':207,'units':9,'lessons':45,'lesson_pages':173,'unit_cover_pages':9,'unit_review_pages':25,'legacy_questions':3101,'structurally_lesson_linked_questions':ql,'review_required_questions':qr,'semantic_question_review':'NOT VERIFIED','raw_mutations':0};m['status']='RECONSTRUCTION_IN_PROGRESS_NOT_IMPORT_READY'
assert p['lesson_linked_structural']+p['exam_linked_to_individual_model']+p['review_required']+p['unclassified']==25755
assert all(p[k]==0 for k in ('raw_mutations','unrelated_mutations','new_imports','new_publications'));MASTER.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
sources=m['sources'];idx=next(i for i,x in enumerate(sources) if x['id']==SID)
def done(x):
 rs=str(x.get('review_status','')).lower(); rec=(x.get('reconstruction') or {}).get('status'); return rec=='verified' or 'verified_empty' in rs or 'reconstructed_verified' in rs
n=next((x for x in sources[idx+1:]+sources[:idx] if not done(x)),None); nid=n['id'] if n else 'NONE'; nn=(n.get('name') or n.get('source_name') or n.get('title') or 'UNKNOWN') if n else 'NONE'
body=f'''## Reconstruction checkpoint — Physics textbook\n\n- Sources processed: **{p['sources_completed']}/{p['sources_total']}**; Educational: **{p['educational_sources_completed']}/{p['educational_sources_total']}**; Exam groups: **{p['exam_source_groups_completed']}/{p['exam_source_groups_total']}**.\n- Books / Units / Lessons / Lesson pages: **{p['verified_books']} / {p['verified_units']} / {p['verified_lessons']} / {p['verified_lesson_pages']}**.\n- Physics: **207/207** technical + exact SHA identity; pages **9..215**; **9 Units / 45 Lessons / 173 Lesson pages / 9 covers / 25 reviews**.\n- Questions: **{ql} lesson-linked; {qr} review_required; semantic correctness NOT VERIFIED**.\n- Global questions: **{p['lesson_linked_structural']} + {p['exam_linked_to_individual_model']} + {p['review_required']} + {p['unclassified']} = 25,755**.\n- Technical images: **{p['source_images_technically_verified']}/{p['source_images_total']}**. RAW/unrelated/import/publication mutations **0/0/0/0**.\n- Last completed: `{SID} — الفيزياء الكتاب المدرسي`. Next: `{nid} — {nn}`.\n'''
for f in ['CONTENT_REBUILD_EXECUTION_STATUS.md','CONTENT_REBUILD_HANDOFF.md','CONTENT_INVENTORY.md','CONTENT_VALIDATION_REPORT.md','CONTENT_IMPORT_REPORT.md','CONTENT_REBUILD_CONTINUATION_2026-09-14.md']:
 path=ROOT/'content-staging'/f
 if path.exists(): repl(path,body)
print(json.dumps({'already':already,'ql':ql,'qr':qr,'next_source_id':nid,'next_source_name':nn,'progress':p},ensure_ascii=False))
