#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SID='81e99fe6-1421-462b-9562-1c0c5053a809'
RECON=ROOT/'content-staging/reconstruction/educational'/f'{SID}.json'
MASTER=ROOT/'content-staging/manifests/MASTER_CONTENT_MANIFEST.json'
START='<!-- SCIENCE_BOOK_PART2_CHECKPOINT_START -->'; END='<!-- SCIENCE_BOOK_PART2_CHECKPOINT_END -->'
def replace_block(path,body):
 text=path.read_text(encoding='utf-8'); block=f'{START}\n{body.rstrip()}\n{END}'
 if START in text and END in text:
  before=text.split(START,1)[0].rstrip(); after=text.split(END,1)[1].lstrip(); text=before+'\n\n'+block+('\n\n'+after if after else '\n')
 else: text=text.rstrip()+'\n\n'+block+'\n'
 path.write_text(text,encoding='utf-8')
r=json.loads(RECON.read_text(encoding='utf-8'))
if r.get('status')!='reconstructed_verified': raise SystemExit('science part2 reconstruction not verified')
p=json.loads(MASTER.read_text(encoding='utf-8')); s=next(x for x in p['sources'] if x['id']==SID)
s['classification']='educational_book_source'
s['classification_evidence']='145/145 exact RAW/master SHA identity + exact master page-by-page section/title runs'
s['review_status']='reconstructed_verified'
s['technical_verification']={'status':'verified','report_path':f'content-staging/reconstruction/technical/{SID}.json','images_verified':145,'readable':145,'sha256_match_manifest':145,'mime_match_manifest':145,'duplicate_sha_groups_within_source':0}
s['reconstruction']={'status':'verified','path':f'content-staging/reconstruction/educational/{SID}.json','book_title':'كتاب العلوم - الجزء الثاني','retained_page_range':[7,151],'source_reference_page_range':[8,152],'retained_pages':145,'units':8,'lessons':31,'lesson_pages':126,'unit_cover_pages':8,'unit_review_pages':11,'appendix_pages':0,'legacy_questions':0,'structurally_lesson_linked_questions':0,'review_required_questions':0,'semantic_question_review':'NOT APPLICABLE','raw_mutations':0}
p['status']='RECONSTRUCTION_IN_PROGRESS_NOT_IMPORT_READY'
p['reconstruction_progress']={'sources_completed':9,'sources_total':58,'educational_sources_completed':3,'educational_sources_total':26,'verified_books':3,'verified_units':25,'verified_lessons':110,'verified_lesson_pages':413,'exam_source_groups_completed':6,'exam_source_groups_total':32,'individual_exam_models':99,'exam_pages_completed':347,'exam_pages_total':2286,'answer_keys':0,'source_images_technically_verified':839,'source_images_total':5273,'webp_derivatives_generated':0,'webp_derivatives_accepted':0,'webp_derivatives_rejected':0,'legacy_questions_total':25755,'lesson_linked_structural':2236,'exam_linked_to_individual_model':733,'review_required':351,'unclassified':22435,'duplicate_fingerprint_groups_classified':0,'duplicate_fingerprint_groups_total':99,'raw_mutations':0,'unrelated_mutations':0,'new_imports':0,'new_publications':0}
assert 2236+733+351+22435==25755
MASTER.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
status='''## Reconstruction checkpoint — Grade 9 Science Part 2

- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Sources processed: **9/58**; Educational: **3/26**; Exam Source Groups: **6/32**.
- Books / Units / Lessons / Lesson pages: **3 / 25 / 110 / 413**.
- Science Part 2: **145/145** technically verified images and **145/145** exact RAW/master SHA identities; retained stored pages **7..151**, exact master source pages **8..152**.
- Reconstructed source: **1 Book, 8 Units, 31 Lessons, 126 Lesson pages, 8 Unit-cover pages, 11 Unit-review pages, 0 appendices**.
- Questions: source manifest/pages contain **0** legacy questions; no question records fabricated.
- Global questions: Lesson-linked **2,236**; Exam-linked **733**; Review-required **351**; Unclassified **22,435** = **25,755**.
- Individual Exam Models **99**; Exam Pages **347/2,286**; Verified Answer Keys **0**.
- Source images technical **839/5,273**; WebP **0/0/0**; Duplicate groups **0/99**.
- RAW / unrelated / imports / publications: **0/0/0/0**.
- Last completed: `81e99fe6-1421-462b-9562-1c0c5053a809 — كتاب العلوم - الجزء الثاني`.
- Next: `8489a487-91d9-47fb-80b8-35d0e7a074a4 — الانجليزي نماذج وزارية 1445`.
'''
replace_block(ROOT/'content-staging/CONTENT_REBUILD_EXECUTION_STATUS.md',status)
replace_block(ROOT/'content-staging/CONTENT_REBUILD_HANDOFF.md','''## Active reconstruction handoff — Science Part 2 complete

- Last completed: `81e99fe6-1421-462b-9562-1c0c5053a809 — كتاب العلوم - الجزء الثاني`.
- Verified: **145/145** technical + exact master SHA identity; **8 Units / 31 Lessons / 126 Lesson pages / 8 covers / 11 reviews**.
- Questions: source contains **0 legacy questions**; no fabricated links; semantic question review `NOT APPLICABLE`.
- Current/next: `8489a487-91d9-47fb-80b8-35d0e7a074a4 — الانجليزي نماذج وزارية 1445`.
- Exact next operation: read the English 1445 live manifest/pages; verify all images; scan duplicates/sequence; derive exam model/correction boundaries only from that source's evidence; map questions; assert invariant; checkpoint.
- RAW/unrelated/import/publication mutations remain **0/0/0/0**.
''')
replace_block(ROOT/'content-staging/CONTENT_INVENTORY.md','''## Verified reconstruction checkpoint — Grade 9 Science Part 2

- Legacy source `81e99fe6-1421-462b-9562-1c0c5053a809` is exactly identified as `master/تاسع علوم/علوم_تاسع_الجزء_الثاني` for all **145 retained images** by SHA-256.
- Retained stored pages **7..151** correspond to exact master source pages **8..152**; master-only pages outside the retained slice remain reference-only and were not fabricated.
- Reconstructed structure: **8 Units, 31 Lessons, 126 Lesson pages, 8 Unit covers, 11 Unit reviews**.
- Source has **0** legacy questions in the verified manifest/pages dataset.
''')
replace_block(ROOT/'content-staging/CONTENT_VALIDATION_REPORT.md','''## Grade 9 Science Part 2 reconstruction validation

- Technical verification: **145/145** files exist, readable, size/SHA/MIME match.
- Exact reference identity: **145/145** RAW images equal the corresponding master images by SHA-256.
- Exact retained reference range: source pages **8..152**; no retained identity failure.
- Structure: **8 Units / 31 Lessons / 126 Lesson pages / 8 covers / 11 reviews**; every one of the 145 retained pages is classified exactly once.
- Questions: **0** source questions; no fabricated question links.
- RAW mutations: **0**.
''')
replace_block(ROOT/'content-staging/CONTENT_IMPORT_REPORT.md','''## Science Part 2 reconstruction checkpoint — no import performed

The reconstruction artifact is verified, but the corpus remains `RECONSTRUCTION_IN_PROGRESS_NOT_IMPORT_READY`.

- New imports: **0**; new publications: **0**; production mutations: **0**; RAW mutations: **0**.
- Import readiness remains deferred until corpus reconstruction/boundary discovery is complete.
''')
cont=ROOT/'content-staging/CONTENT_REBUILD_CONTINUATION_2026-09-14.md'
if cont.exists(): replace_block(cont,'''## Continuation checkpoint — Science Part 2 complete

Continue with `8489a487-91d9-47fb-80b8-35d0e7a074a4 — الانجليزي نماذج وزارية 1445`; do not rerun Science Part 2 absent new drift evidence. Current verified global progress: **9/58 sources; 3/26 educational; 6/32 exam groups; 839/5,273 technical images; 2,236 lesson-linked; 733 exam-linked; 351 review-required; 22,435 unclassified**.
''')
print(json.dumps({'checkpoint':'SCIENCE_BOOK_PART2','sources':9,'educational':3,'books':3,'units':25,'lessons':110,'lesson_pages':413,'images_verified':839,'lesson_linked':2236,'unclassified':22435,'invariant':25755,'next_source':'8489a487-91d9-47fb-80b8-35d0e7a074a4','raw_mutations':0}))
