#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SID='f4b6708c-027f-4883-9e85-e6e7acb52ecc'
RECON=ROOT/'content-staging/reconstruction/educational'/f'{SID}.json'
MASTER=ROOT/'content-staging/manifests/MASTER_CONTENT_MANIFEST.json'
START='<!-- SCIENCE_BOOK_PART1_CHECKPOINT_START -->'; END='<!-- SCIENCE_BOOK_PART1_CHECKPOINT_END -->'
def replace_block(path,body):
 text=path.read_text(encoding='utf-8'); block=f'{START}\n{body.rstrip()}\n{END}'
 if START in text and END in text:
  before=text.split(START,1)[0].rstrip(); after=text.split(END,1)[1].lstrip(); text=before+'\n\n'+block+('\n\n'+after if after else '\n')
 else: text=text.rstrip()+'\n\n'+block+'\n'
 path.write_text(text,encoding='utf-8')
r=json.loads(RECON.read_text(encoding='utf-8'))
if r.get('status')!='reconstructed_verified': raise SystemExit('science part1 reconstruction not verified')
p=json.loads(MASTER.read_text(encoding='utf-8')); s=next(x for x in p['sources'] if x['id']==SID)
s['classification']='educational_book_source'
s['classification_evidence']='161/161 exact RAW/master SHA identity + exact master page-by-page section/title runs'
s['review_status']='reconstructed_verified'
s['technical_verification']={'status':'verified','report_path':f'content-staging/reconstruction/technical/{SID}.json','images_verified':161,'readable':161,'sha256_match_manifest':161,'mime_match_manifest':161,'duplicate_sha_groups_within_source':0}
s['reconstruction']={'status':'verified','path':f'content-staging/reconstruction/educational/{SID}.json','book_title':'كتاب العلوم - الجزء الأول','retained_page_range':[7,167],'source_reference_page_range':[8,168],'retained_pages':161,'units':8,'lessons':22,'lesson_pages':138,'unit_cover_pages':8,'unit_review_pages':15,'appendix_pages':0,'legacy_questions':11,'structurally_lesson_linked_questions':11,'review_required_questions':0,'semantic_question_review':'NOT VERIFIED','raw_mutations':0}
p['status']='RECONSTRUCTION_IN_PROGRESS_NOT_IMPORT_READY'
p['reconstruction_progress']={'sources_completed':8,'sources_total':58,'educational_sources_completed':2,'educational_sources_total':26,'verified_books':2,'verified_units':17,'verified_lessons':79,'verified_lesson_pages':287,'exam_source_groups_completed':6,'exam_source_groups_total':32,'individual_exam_models':99,'exam_pages_completed':347,'exam_pages_total':2286,'answer_keys':0,'source_images_technically_verified':694,'source_images_total':5273,'webp_derivatives_generated':0,'webp_derivatives_accepted':0,'webp_derivatives_rejected':0,'legacy_questions_total':25755,'lesson_linked_structural':2236,'exam_linked_to_individual_model':733,'review_required':351,'unclassified':22435,'duplicate_fingerprint_groups_classified':0,'duplicate_fingerprint_groups_total':99,'raw_mutations':0,'unrelated_mutations':0,'new_imports':0,'new_publications':0}
assert 2236+733+351+22435==25755
MASTER.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
status='''## Reconstruction checkpoint — Grade 9 Science Part 1

- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Sources processed: **8/58**; Educational: **2/26**; Exam Source Groups: **6/32**.
- Books / Units / Lessons / Lesson pages: **2 / 17 / 79 / 287**.
- Science Part 1: **161/161** technically verified images and **161/161** exact RAW/master SHA identities; retained stored pages **7..167**, exact master source pages **8..168**.
- Reconstructed source: **1 Book, 8 Units, 22 Lessons, 138 Lesson pages, 8 Unit-cover pages, 15 Unit-review pages, 0 appendices**.
- Questions: **11/11** structurally lesson-linked to `المحلول ومكوناته`; semantic correctness `NOT VERIFIED`; source review-required questions **0**.
- Global questions: Lesson-linked **2,236**; Exam-linked **733**; Review-required **351**; Unclassified **22,435** = **25,755**.
- Individual Exam Models **99**; Exam Pages **347/2,286**; Verified Answer Keys **0**.
- Source images technical **694/5,273**; WebP **0/0/0**; Duplicate groups **0/99**.
- RAW / unrelated / imports / publications: **0/0/0/0**.
- Last completed: `f4b6708c-027f-4883-9e85-e6e7acb52ecc — كتاب العلوم - الجزء الأول`.
- Next: `81e99fe6-1421-462b-9562-1c0c5053a809 — كتاب العلوم - الجزء الثاني`.
'''
replace_block(ROOT/'content-staging/CONTENT_REBUILD_EXECUTION_STATUS.md',status)
replace_block(ROOT/'content-staging/CONTENT_REBUILD_HANDOFF.md','''## Active reconstruction handoff — Science Part 1 complete

- Last completed: `f4b6708c-027f-4883-9e85-e6e7acb52ecc — كتاب العلوم - الجزء الأول`.
- Verified: **161/161** technical + exact master SHA identity; **8 Units / 22 Lessons / 138 Lesson pages / 8 covers / 15 reviews**.
- Questions: **11 lesson-linked; 0 source review-required; semantic correctness NOT VERIFIED**.
- Current/next: `81e99fe6-1421-462b-9562-1c0c5053a809 — كتاب العلوم - الجزء الثاني` (145 images/pages; 0 questions in current manifest).
- Exact next operation: technically verify all 145 images; establish exact identity against `master/تاسع علوم/علوم_تاسع_الجزء_الثاني`; reconstruct its own units/lessons/reviews; assert invariant; checkpoint.
- RAW/unrelated/import/publication mutations remain **0/0/0/0**.
''')
replace_block(ROOT/'content-staging/CONTENT_INVENTORY.md','''## Verified reconstruction checkpoint — Grade 9 Science Part 1

- Legacy source `f4b6708c-027f-4883-9e85-e6e7acb52ecc` is exactly identified as `master/تاسع علوم/علوم_تاسع_الجزء_الأول` for all **161 retained images** by SHA-256.
- Retained stored pages **7..167** correspond to exact master source pages **8..168**; master-only pages outside the retained slice remain reference-only and were not fabricated.
- Reconstructed structure: **8 Units, 22 Lessons, 138 Lesson pages, 8 Unit covers, 15 Unit reviews**.
- **11/11** source questions are structurally linked to the verified `المحلول ومكوناته` lesson; semantic correctness remains `NOT VERIFIED`.
''')
replace_block(ROOT/'content-staging/CONTENT_VALIDATION_REPORT.md','''## Grade 9 Science Part 1 reconstruction validation

- Technical verification: **161/161** files exist, readable, size/SHA/MIME match.
- Exact reference identity: **161/161** RAW images equal the corresponding master images by SHA-256.
- Exact retained reference range: source pages **8..168**; no retained identity failure.
- Structure: **8 Units / 22 Lessons / 138 Lesson pages / 8 covers / 15 reviews**; every one of the 161 retained pages is classified exactly once.
- Questions: **11/11** structurally linked by verified page membership; semantic correctness `NOT VERIFIED`.
- RAW mutations: **0**.
''')
replace_block(ROOT/'content-staging/CONTENT_IMPORT_REPORT.md','''## Science Part 1 reconstruction checkpoint — no import performed

The reconstruction artifact is verified, but the corpus remains `RECONSTRUCTION_IN_PROGRESS_NOT_IMPORT_READY`.

- New imports: **0**; new publications: **0**; production mutations: **0**; RAW mutations: **0**.
- Import readiness remains deferred until corpus reconstruction/boundary discovery is complete.
''')
cont=ROOT/'content-staging/CONTENT_REBUILD_CONTINUATION_2026-09-14.md'
if cont.exists(): replace_block(cont,'''## Continuation checkpoint — Science Part 1 complete

Continue with `81e99fe6-1421-462b-9562-1c0c5053a809 — كتاب العلوم - الجزء الثاني`; do not rerun Science Part 1 absent new drift evidence. Current verified global progress: **8/58 sources; 2/26 educational; 6/32 exam groups; 694/5,273 technical images; 2,236 lesson-linked; 733 exam-linked; 351 review-required; 22,435 unclassified**.
''')
print(json.dumps({'checkpoint':'SCIENCE_BOOK_PART1','sources':8,'educational':2,'books':2,'units':17,'lessons':79,'lesson_pages':287,'images_verified':694,'lesson_linked':2236,'unclassified':22435,'invariant':25755,'next_source':'81e99fe6-1421-462b-9562-1c0c5053a809','raw_mutations':0}))
