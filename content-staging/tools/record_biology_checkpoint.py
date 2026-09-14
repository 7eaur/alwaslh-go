#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
SID='67d4ffae-68e1-42e8-9c3b-72329973c93d'
RECON=ROOT/'content-staging/reconstruction/educational'/f'{SID}.json'
MASTER=ROOT/'content-staging/manifests/MASTER_CONTENT_MANIFEST.json'
START='<!-- BIOLOGY_BOOK_CHECKPOINT_START -->'; END='<!-- BIOLOGY_BOOK_CHECKPOINT_END -->'

def replace_block(path,body):
    text=path.read_text(encoding='utf-8')
    block=f'{START}\n{body.rstrip()}\n{END}'
    if START in text and END in text:
        before=text.split(START,1)[0].rstrip(); after=text.split(END,1)[1].lstrip()
        text=before+'\n\n'+block+('\n\n'+after if after else '\n')
    else:
        text=text.rstrip()+'\n\n'+block+'\n'
    path.write_text(text,encoding='utf-8')

r=json.loads(RECON.read_text(encoding='utf-8'))
if r.get('status')!='reconstructed_verified': raise SystemExit('biology reconstruction not verified')
ql=r['questions']['structurally_lesson_linked_questions']; qr=r['questions']['review_required_questions']
if ql+qr!=3304: raise SystemExit(f'biology question accounting mismatch {ql}+{qr}')

m=json.loads(MASTER.read_text(encoding='utf-8'))
s=next(x for x in m['sources'] if x['id']==SID)
progress=m['reconstruction_progress']
already=s.get('review_status')=='reconstructed_verified'
if not already:
    progress['sources_completed']+=1
    progress['educational_sources_completed']+=1
    progress['verified_books']+=1
    progress['verified_units']+=8
    progress['verified_lessons']+=47
    progress['verified_lesson_pages']+=193
    progress['source_images_technically_verified']+=214
    progress['lesson_linked_structural']+=ql
    progress['review_required']+=qr
    progress['unclassified']-=3304

s['classification']='educational_book_source'
s['classification_evidence']='214/214 exact RAW/master SHA identity in one canonical biology directory + exact master filename title runs'
s['review_status']='reconstructed_verified'
s['technical_verification']={'status':'verified','report_path':f'content-staging/reconstruction/technical/{SID}.json','images_verified':214,'readable':214,'sha256_match_manifest':214,'mime_match_manifest':214,'duplicate_sha_groups_within_source':0}
s['reconstruction']={'status':'verified','path':f'content-staging/reconstruction/educational/{SID}.json','book_title':'الأحياء الكتاب المدرسي','retained_page_range':[8,221],'retained_pages':214,'units':8,'lessons':47,'lesson_pages':193,'unit_cover_pages':8,'unit_review_pages':13,'appendix_pages':0,'legacy_questions':3304,'structurally_lesson_linked_questions':ql,'review_required_questions':qr,'semantic_question_review':'NOT VERIFIED','raw_mutations':0}
m['status']='RECONSTRUCTION_IN_PROGRESS_NOT_IMPORT_READY'
if progress['lesson_linked_structural']+progress['exam_linked_to_individual_model']+progress['review_required']+progress['unclassified']!=25755:
    raise SystemExit('global legacy-question invariant failed')
for k in ('raw_mutations','unrelated_mutations','new_imports','new_publications'):
    if progress[k]!=0: raise SystemExit(f'forbidden mutation counter nonzero: {k}={progress[k]}')
MASTER.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Select the next unresolved source after Biology in manifest order, wrapping once if necessary.
sources=m['sources']; idx=next(i for i,x in enumerate(sources) if x['id']==SID)
def done(x):
    rs=str(x.get('review_status','')).lower(); rec=(x.get('reconstruction') or {}).get('status')
    return rec=='verified' or 'verified_empty' in rs or 'reconstructed_verified' in rs
next_source=None
for x in sources[idx+1:]+sources[:idx]:
    if not done(x): next_source=x; break
next_id=next_source['id'] if next_source else 'NONE'
next_name=next_source.get('name') or next_source.get('source_name') or next_source.get('title') or 'UNKNOWN'

p=progress
status=f'''## Reconstruction checkpoint — Biology textbook\n\n- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`\n- Sources processed: **{p['sources_completed']}/{p['sources_total']}**; Educational: **{p['educational_sources_completed']}/{p['educational_sources_total']}**; Exam Source Groups: **{p['exam_source_groups_completed']}/{p['exam_source_groups_total']}**.\n- Books / Units / Lessons / Lesson pages: **{p['verified_books']} / {p['verified_units']} / {p['verified_lessons']} / {p['verified_lesson_pages']}**.\n- Biology: **214/214** technically verified and **214/214** exact RAW/master SHA identities in `الأحياء ثالث ثانوي/الاحياء الكتاب المدرسي/الصور`; retained pages **8..221**.\n- Reconstructed source: **1 Book, 8 Units, 47 Lessons, 193 Lesson pages, 8 Unit-cover pages, 13 Unit-review pages**.\n- Questions: **{ql}** structurally lesson-linked; **{qr}** `review_required` on non-lesson unit cover/review pages; semantic correctness `NOT VERIFIED`.\n- Global questions: Lesson-linked **{p['lesson_linked_structural']}**; Exam-linked **{p['exam_linked_to_individual_model']}**; Review-required **{p['review_required']}**; Unclassified **{p['unclassified']}** = **25,755**.\n- Individual Exam Models **{p['individual_exam_models']}**; Exam Pages **{p['exam_pages_completed']}/{p['exam_pages_total']}**; Verified Answer Keys **{p['answer_keys']}**.\n- Source images technical **{p['source_images_technically_verified']}/{p['source_images_total']}**; Duplicate groups **{p['duplicate_fingerprint_groups_classified']}/{p['duplicate_fingerprint_groups_total']}**.\n- RAW / unrelated / imports / publications: **0/0/0/0**.\n- Last completed: `{SID} — الأحياء الكتاب المدرسي`.\n- Next candidate: `{next_id} — {next_name}`; must be re-read from live manifest/baton before work.\n'''
replace_block(ROOT/'content-staging/CONTENT_REBUILD_EXECUTION_STATUS.md',status)
replace_block(ROOT/'content-staging/CONTENT_REBUILD_HANDOFF.md',f'''## Active reconstruction handoff — Biology complete\n\n- Last completed: `{SID} — الأحياء الكتاب المدرسي`.\n- Verified: **214/214** technical + exact SHA identity; **8 Units / 47 Lessons / 193 Lesson pages / 8 covers / 13 reviews**.\n- Questions: **{ql} lesson-linked; {qr} review-required; semantic correctness NOT VERIFIED**.\n- Current/next candidate: `{next_id} — {next_name}`.\n- Exact next operation: re-fetch live HEAD and shared baton, verify no active workflow for that source, then inspect its own manifest/RAW/reference evidence without inheriting Biology structure.\n- RAW/unrelated/import/publication mutations remain **0/0/0/0**.\n''')
replace_block(ROOT/'content-staging/CONTENT_INVENTORY.md',f'''## Verified reconstruction checkpoint — Biology textbook\n\n- Legacy source `{SID}` has **214/214** retained images byte-identical by SHA-256 to `master/الأحياء ثالث ثانوي/الاحياء الكتاب المدرسي/الصور`.\n- Reconstructed structure from exact-master filename/title runs: **8 Units, 47 Lessons, 193 Lesson pages, 8 Unit covers, 13 Unit reviews**.\n- **{ql}/3,304** questions are structurally lesson-linked; **{qr}/3,304** remain `review_required` because they reside on non-lesson unit cover/review pages; semantic correctness remains `NOT VERIFIED`.\n''')
replace_block(ROOT/'content-staging/CONTENT_VALIDATION_REPORT.md',f'''## Biology textbook reconstruction validation\n\n- Technical verification: **214/214** files exist, readable, and match manifest size/SHA/MIME.\n- Exact reference identity: **214/214** RAW images equal the single canonical master directory by SHA-256.\n- Structure: **8 Units / 47 Lessons / 193 Lesson pages / 8 covers / 13 reviews**; all 214 retained pages classified exactly once.\n- Questions: **{ql}** structurally linked; **{qr}** `review_required`; semantic correctness `NOT VERIFIED`.\n- RAW mutations: **0**.\n''')
replace_block(ROOT/'content-staging/CONTENT_IMPORT_REPORT.md','''## Biology reconstruction checkpoint — no import performed\n\nThe reconstruction artifact is verified, but the corpus remains `RECONSTRUCTION_IN_PROGRESS_NOT_IMPORT_READY`.\n\n- New imports: **0**; new publications: **0**; production mutations: **0**; RAW mutations: **0**.\n''')
cont=ROOT/'content-staging/CONTENT_REBUILD_CONTINUATION_2026-09-14.md'
if cont.exists():
    replace_block(cont,f'''## Continuation checkpoint — Biology complete\n\nContinue from `{next_id} — {next_name}` only after re-reading the live baton. Current verified global progress: **{p['sources_completed']}/{p['sources_total']} sources; {p['educational_sources_completed']}/{p['educational_sources_total']} educational; {p['exam_source_groups_completed']}/{p['exam_source_groups_total']} exam groups; {p['source_images_technically_verified']}/{p['source_images_total']} technical images; {p['lesson_linked_structural']} lesson-linked; {p['exam_linked_to_individual_model']} exam-linked; {p['review_required']} review-required; {p['unclassified']} unclassified**.\n''')
print(json.dumps({'checkpoint':'BIOLOGY_BOOK','already_recorded':already,'sources':p['sources_completed'],'educational':p['educational_sources_completed'],'books':p['verified_books'],'units':p['verified_units'],'lessons':p['verified_lessons'],'lesson_pages':p['verified_lesson_pages'],'images_verified':p['source_images_technically_verified'],'biology_lesson_linked':ql,'biology_review_required':qr,'global_lesson_linked':p['lesson_linked_structural'],'global_review_required':p['review_required'],'global_unclassified':p['unclassified'],'next_source_id':next_id,'next_source_name':next_name,'raw_mutations':0},ensure_ascii=False))
