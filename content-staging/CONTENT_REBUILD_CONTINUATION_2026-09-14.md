# Alwaslh Content Reconstruction — Exact Continuation Checkpoint

Date: 2026-09-14
Repository: `7eaur/alwaslh-go`
Working branch: `content/corpus-inventory-20260914`
Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`

> This file is an execution-continuation checkpoint. Always verify the live branch HEAD before doing work; repository evidence newer than this file wins.

## Live checkpoint used to build this document

The live branch was verified immediately before this checkpoint at:

`cb05664e6ee7e7c4bdc3555d463b9a1232ca2788`

Commit message:

`content: discover chemistry 1446 exam boundary candidates [skip ci]`

This documentation commit will advance the branch HEAD. A new conversation must therefore resolve the live HEAD first rather than assuming the SHA above is still current.

## Source-of-truth order

1. Actual original/RAW files.
2. RAW checksums, immutable legacy IDs, byte sizes and provenance.
3. Live reconstruction/technical manifests.
4. Source images and selective visual evidence.
5. `master` only when the exact book/source identity is proven equivalent.
6. PostgreSQL schema/migrations/entities/import contracts when Import Readiness begins.
7. Runtime verification.
8. Documentation.

Unknown or insufficiently evidenced facts must remain `NOT VERIFIED`.

## Fixed safety/execution rules

- Never mutate, recompress, delete or reformat legacy RAW in place.
- Never silently correct source data.
- No corpus-wide auto-publication.
- No new import during the current Reconstruction phase.
- Exams are not Lessons and an Exam Source Group is not automatically one Individual Exam Model.
- Never infer Answer Keys without direct evidence.
- Never equate a page with a Lesson.
- Never auto-delete/merge duplicate SHA/fingerprint groups.
- Ambiguous evidence becomes `review_required` and execution continues to the next evidence-backed step.
- Grade 9 English prior import/publication work is closed and must not be rerun without fresh drift evidence.

## Baseline inventory — already completed; DO NOT redo

- Legacy sources/manifests: **58**
- Legacy class/subject groups: **15**
- Source image/page references: **5,273**
- Recorded path + byte-size matches from inventory: **5,273/5,273**
- Missing referenced paths at inventory: **0**
- Legacy questions: **25,755**
- Candidate non-exam educational sources: **26**
- Candidate Exam Source Groups: **32**
- Exam-source pages: **2,286**
- Legacy questions associated with Exam Source Groups: **2,715**
- Recorded duplicate fingerprint groups: **99**
- The **32** count is Exam Source Groups, NOT Individual Exam Models.
- Classes / Subjects / Books / Units / Lessons / Individual Exam Models / Answer Keys were not globally fixed by inventory alone.

## Closed historical scope — Grade 9 English

Do not redo the previous Grade 9 English work.

Known closed state retained in the existing handoff/status files:

- 69 RAW-backed pages and 69 RAW images imported in the prior Grade 9 English pipeline.
- 104 Question Revisions.
- 8 recovered Units/Sections.
- page 70 remains manifest-only/evidence-only because no RAW identity exists.
- Only 2 reviewed Lessons, 6 Lesson Assets and 19 reviewed Question Revisions from Unit 2 pages 5..10 were explicitly published.
- Everything else in that prior Grade 9 English scope remains draft/unpublished per the recorded gate.
- Do not reintroduce the old `69 -> 62 lessons` heuristic.

## Reconstruction completed in the current corpus-wide phase

### 1) Third Secondary Chemistry textbook — COMPLETE

Legacy source group:

`f0c5228c-7d5b-4ec2-85ed-ce59139ce0a4`

Name:

`الكيمياء الكتاب المدرسي`

Verified result:

- source pages/images technically verified: **178/178**
- page range: **11..188**, contiguous
- exists/readable/byte-size/SHA-256/MIME checks: **178/178**
- within-source duplicate SHA groups: **0**
- reconstructed Books: **1**
- Units: **9**
- Lessons: **57**
- Lesson pages: **149**
- review pages: **14**
- glossary pages: **5**
- structurally lesson-linked legacy questions: **2,225**
- Chemistry questions requiring review because they are on covers/reviews/non-lesson structures: **351**
- semantic correctness of those question links: **NOT VERIFIED**
- WebP derivative optimization for this source: **not executed**; do not claim it was.

Important evidence resolution:

An earlier apparent page-count conflict existed between the 178-page legacy source and a larger `master` reference. The completed reconstruction resolved the source using exact RAW/master identity for the verified matching range plus trusted TOC and selective visual boundary evidence. Do not reopen that work unless new evidence shows drift.

### 2) Chemistry Ministry Exams 1445 — COMPLETE

Legacy Exam Source Group:

`e101d097-7a14-44e5-b242-cdeb9a312b77`

Name:

`الكيمياء نماذج وزاريه 1445`

Verified result:

- pages/images technically verified: **60/60**
- exists/readable/byte-size/SHA-256/MIME checks: **60/60**
- page sequence: **1..60**, contiguous
- verified Individual Exam Models: **20**
- verified page grouping: **3 pages/model** for this source only
- full source-group visual review was completed
- correction/electronic-answer-sheet candidates: **20**
- verified official Answer Keys: **0**
- official model codes/titles/term and official Answer Key status remain `NOT VERIFIED` wherever evidence was insufficient
- do NOT generalize the 3-pages/model pattern to another source without visual evidence

## Current active source — Chemistry Ministry Exams 1446 — IN PROGRESS

Legacy Exam Source Group:

`c09ce569-ea42-4f0b-997f-95b029a7e6ea`

Name:

`الكيمياء نماذج وزاريه 1446`

Latest generated evidence files:

- `content-staging/reconstruction/exams/source-groups/c09ce569-ea42-4f0b-997f-95b029a7e6ea-discovery.json`
- `content-staging/reconstruction/technical/c09ce569-ea42-4f0b-997f-95b029a7e6ea.json`

Technical verification already completed for this source:

- manifest image references: **60**
- existing files: **60/60**
- readable images: **60/60**
- byte-size matches: **60/60**
- SHA-256 matches: **60/60**
- MIME matches: **60/60**
- failures: **0**
- page sequence: **1..60**, contiguous
- images downloaded by the reconstruction probe: **60/60**
- legacy questions recorded in this source discovery: **0**
- RAW mutations: **0**

Current boundary status:

- `individual_exam_models`: **NOT VERIFIED**
- `answer_keys`: **NOT VERIFIED**
- metadata/storage currently exposes one 1..60 run only.
- That 1..60 run is explicitly only a `boundary_candidate_not_yet_individual_exam_model`; it MUST NOT be treated as one exam.

Important duplicate evidence inside Chemistry 1446:

Three exact within-source SHA-256 duplicate pairs were detected:

- page **29 == page 41** by SHA-256
- page **30 == page 42** by SHA-256
- page **31 == page 43** by SHA-256

This strongly indicates an exact repeated 3-page block candidate, but its meaning is still `NOT VERIFIED`. Do not delete or merge it automatically. During visual boundary review classify it as one of: legitimate repeated exam/model, duplicate source import, reused context, accidental duplicate, or `review_required`.

## Exact progress at this checkpoint

Count a source/group as processed only after its reconstruction/boundaries are finalized. Chemistry 1446 has technical verification but is NOT yet a completed Exam Source Group.

- Sources fully processed: **2/58**
- Educational sources fully processed: **1/26**
- Verified Books / Units / Lessons / Lesson pages: **1 / 9 / 57 / 149**
- Exam Source Groups fully processed: **1/32**
- Verified Individual Exam Models: **20**
- Finalized Exam pages: **60/2,286**
- Verified Answer Keys: **0**
- Source images technically verified by reconstruction: **298/5,273**
  - 178 Chemistry textbook
  - 60 Chemistry 1445 exams
  - 60 Chemistry 1446 exams
- WebP generated / accepted / rejected in the current corpus-wide run: **0 / 0 / 0**
- Legacy questions baseline: **25,755**
- Structurally lesson-linked: **2,225**
- Review-required from completed Chemistry textbook mapping: **351**
- Exam-linked to finalized Individual Exam Models: **0** at the latest documented classification checkpoint
- Remaining unclassified by that checkpoint: **23,179**
- Global duplicate fingerprint groups classified: **0/99**
- RAW mutations / unrelated mutations / new imports / new publications: **0 / 0 / 0 / 0**

Do not count the three Chemistry 1446 within-source duplicate pairs as globally classified duplicate fingerprint groups until the global duplicate report/mapping proves their relationship to the recorded 99 groups and assigns a classification.

## Exact next operation — resume here

Continue **Chemistry 1446**; do not select another source yet.

1. Resolve the live branch HEAD and confirm no newer Chemistry 1446 finalization already exists.
2. Read the two Chemistry 1446 evidence JSON files listed above.
3. Locate the runner/workflow/scripts that produced the technical/discovery evidence and any generated contact sheets/visual artifacts.
4. Perform visual boundary discovery across all 60 pages, using contact sheets/full-source review where available. Inspect starts, ends, transitions, repeated headers, correction-sheet candidates and ambiguous pages.
5. Do **not** assume the Chemistry 1445 pattern of 3 pages/model. Derive 1446 boundaries from 1446 evidence only.
6. Explicitly resolve pages 29..31 versus 41..43 because they are exact SHA duplicates.
7. Produce the finalized list of Individual Exam Models with ordered page IDs/paths and provenance.
8. Identify correction-sheet/Answer-Key relations only where visual/source evidence proves them; otherwise record `NOT VERIFIED`.
9. Validate each model using first/last/middle evidence and continuity checks.
10. Update the exam reconstruction artifact, master manifest and the required documentation/checkpoint files.
11. Make a small logical commit such as `content: finalize chemistry 1446 exam reconstruction`.
12. Only then increment Sources processed / Exam Source Groups processed / Individual Exam Models / Exam pages and move to the next source automatically.

## Existing workflow note

`.github/workflows/content-media-001-probe.yml` was inspected. It has `workflow_dispatch`, `contents: read`, checks out the active ref, installs Pillow 11.3.0, runs `content-staging/tools/media_001_probe.py`, and uploads `content-staging/runtime/media-001/` as an artifact. Its push trigger is tied to the older `content/legacy-staging-rebuild` branch, so do not assume a push on the current corpus branch invokes it; manual dispatch is available if that probe is relevant.

Use existing repository-side runners/workflows for binary inspection when local/container GitHub binary access is unavailable. Do not claim visual/SHA/WebP work without runner evidence.

## Mandatory documentation to keep synchronized as work advances

- `content-staging/CONTENT_REBUILD_EXECUTION_STATUS.md`
- `content-staging/CONTENT_REBUILD_HANDOFF.md`
- `content-staging/CONTENT_INVENTORY.md`
- `content-staging/CONTENT_VALIDATION_REPORT.md`
- `content-staging/CONTENT_IMPORT_REPORT.md`
- `content-staging/manifests/MASTER_CONTENT_MANIFEST.json`
- specialized reconstruction/technical reports under `content-staging/reconstruction/`

## Import boundary

Do not inspect or modify the main application database schema merely because Reconstruction is in progress. Only after Reconstruction and Validation reach Import Readiness, inspect `7eaur/alwaslh@main` PostgreSQL migrations/schema/entities/import contracts, then proceed through Dry Run -> Transaction Gate -> Apply -> Runtime Verify. No production mutation is authorized at this checkpoint.

## Completion condition for this corpus-wide phase

Do not call the phase complete until all 58 sources are either reconstructed or explicitly unresolved with evidence, all 32 Exam Source Groups are processed, Individual Exam Models/pages/Answer Keys are established where evidence permits, all 5,273 images have technical verification, WebP decisions are completed, all 25,755 questions have structural classifications, the 99 duplicate fingerprint groups are classified, master manifests/docs are synchronized, and RAW/unrelated/import/publication mutations remain controlled at zero unless a later explicit import gate authorizes otherwise.

<!-- CHEMISTRY_EXAM_1446_CHECKPOINT_START -->
## Superseding exact continuation — Chemistry 1446 finalized

The earlier 1446 IN PROGRESS section is superseded by this evidence-backed checkpoint.

- Chemistry 1446 is **COMPLETE** for current Reconstruction/Boundary scope: **60/60** technical checks green and all **60** pages visually reviewed.
- Final: **15** four-page source occurrences, **14** unique Individual Exam Models, **60** finalized source pages, **15** correction-report candidates, **0** verified standalone Answer Keys.
- Repeated `P.41`: pages 29..31 == 41..43 by exact SHA; pages 32/44 are distinct candidate correction reports. Classification `legitimate_repeated_exam_model_occurrence`; preserve all pages.
- Progress: Sources **3/58**; Educational **1/26**; Books/Units/Lessons/Lesson Pages **1/9/57/149**; Exam Source Groups **2/32**; Individual Exam Models **34**; Exam Pages **120/2,286**; images verified **298/5,273**.
- Questions: **25,755** total; lesson-linked **2,225**; exam-linked **0**; review-required **351**; unclassified **23,179**; duplicate fingerprint groups classified **0/99**.
- RAW/unrelated/import/publication mutations **0/0/0/0**.
- Next source: `e7c8291c-e904-4e8c-9cd8-2753818cedf3` — `الكيمياء نماذج وزاريه 1447`; start technical verification + source-local visual boundary discovery. Do not assume 3 or 4 pages/model.
<!-- CHEMISTRY_EXAM_1446_CHECKPOINT_END -->

<!-- CHEMISTRY_EXAM_1447_CHECKPOINT_START -->
## Superseding continuation — Chemistry 1447 finalized

- Chemistry 1447 is closed for the current Reconstruction/Boundary scope with isolated review-required anomalies rather than guessed repairs.
- **124/124** technical verification; full visual review of **124** pages; **31** source blocks; **29** verified model-matched occurrences; **28** unique models; **116** finalized exam pages; **8** review-required pages; **31** correction-report candidates; **0** verified standalone Answer Keys.
- Mismatches retained: `37..40` = `P.61` questions / `P.31` correction; `45..48` = `P.28` questions / `P.88` correction. `P.8` repeat is legitimate and preserved.
- Source questions: **226/226** structurally accounted for (**226** exam-linked, **0** review-required); semantic correctness `NOT VERIFIED`.
- Global progress: Sources **4/58**; Educational **1/26**; Books/Units/Lessons/Lesson Pages **1/9/57/149**; Exam Groups **3/32**; Models **62**; Exam Pages **236/2,286**; images **422/5,273**.
- Legacy Questions **25,755**; Lesson-linked **2225**; Exam-linked **226**; Review-required **351**; Unclassified **22953**; duplicate fingerprint groups classified **0/99**.
- RAW/unrelated/import/publication mutations **0/0/0/0**.
- Next source: `ef408805-c337-44dd-b903-7838030e6de0` — `العلوم نماذج وزارية 1445`. Continue source-local technical verification → visual boundary discovery → reconstruction.
<!-- CHEMISTRY_EXAM_1447_CHECKPOINT_END -->

<!-- SCIENCE_EXAM_1445_CHECKPOINT_START -->
## Reconstruction checkpoint — Grade 9 Science Ministry Exams 1445

- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Source `ef408805-c337-44dd-b903-7838030e6de0` — `العلوم نماذج وزارية 1445` completed from source-local evidence.
- Technical verification: **30/30** images exist, readable, byte-size/SHA-256/MIME match; sequence **1..30** contiguous; duplicate SHA groups **0**.
- Full visual review + explicit page titles resolve **10** verified source occurrences / **10** unique Individual Exam Models; each occurrence is two question pages + one correction-model page.
- Finalized Exam Pages: **30**; review-required pages: **0**; correction-sheet candidates: **10**; verified standalone Answer Keys: **0 / NOT VERIFIED**.
- Source legacy questions: **215/215** structurally linked to the ten verified models; semantic correctness remains `NOT VERIFIED`.
- Progress: Sources **5/58**; Educational **1/26**; Exam Groups **4/32**; Individual Exam Models **72**; Exam Pages **266/2,286**; source images technical **452/5,273**.
- Global questions: Lesson-linked **2225**; Exam-linked **441**; Review-required **351**; Unclassified **22738**; invariant **PASS = 25,755**.
- RAW/unrelated/import/publication mutations: **0/0/0/0**.
- Next source: `004c02be-3f55-49e1-bbdc-b0824491bd68` — `العلوم نماذج وزارية 1446`.
<!-- SCIENCE_EXAM_1445_CHECKPOINT_END -->

<!-- SCIENCE_EXAM_1446_CHECKPOINT_START -->
## Reconstruction checkpoint — Grade 9 Science Ministry Exams 1446

- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Source `004c02be-3f55-49e1-bbdc-b0824491bd68` — `العلوم نماذج وزارية 1446` completed from source-local evidence.
- Technical verification: **39/39** images exist, readable, byte-size/SHA-256/MIME match; sequence **1..39** contiguous; duplicate SHA groups **0**.
- Full visual review + explicit page titles resolve **13** verified source occurrences / **13** unique Individual Exam Models; each occurrence is two question pages + one electronic correction/result sheet.
- Finalized Exam Pages: **39**; review-required pages: **0**; correction-sheet candidates: **13**; verified standalone Answer Keys: **0 / NOT VERIFIED**.
- Source legacy questions: **30/30** structurally linked to the thirteen verified models; semantic correctness remains `NOT VERIFIED`.
- Progress: Sources **6/58**; Educational **1/26**; Exam Groups **5/32**; Individual Exam Models **85**; Exam Pages **305/2,286**; source images technical **491/5,273**.
- Global questions: Lesson-linked **2225**; Exam-linked **471**; Review-required **351**; Unclassified **22708**; invariant **PASS = 25,755**.
- RAW/unrelated/import/publication mutations: **0/0/0/0**.
- Next source: `14ef15e0-5524-473a-bbdb-996df35ba535` — `العلوم نماذج وزارية 1447`.
<!-- SCIENCE_EXAM_1446_CHECKPOINT_END -->

<!-- SCIENCE_EXAM_1447_CHECKPOINT_START -->
## Reconstruction checkpoint — Grade 9 Science Ministry Exams 1447

- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Source `14ef15e0-5524-473a-bbdb-996df35ba535` — `العلوم نماذج وزارية 1447` completed from source-local evidence.
- Technical verification: **42/42** images exist, readable, byte-size/SHA-256/MIME match; duplicate SHA groups **0**.
- Stored page numbering anomaly is preserved exactly: missing stored number **35**, duplicate stored number **36**; no RAW/metadata rewrite and no fabricated page 35.
- Full visual review + source-record identity/order resolves **14** verified source occurrences / **14** Individual Exam Models, including model 12 whose second question-form image and correction image are distinct page-36 records.
- Finalized source image records counted as Exam Pages: **42**; review-required pages: **0**; correction-sheet candidates: **14**; verified standalone Answer Keys: **0 / NOT VERIFIED**.
- Source legacy questions: **262/262** structurally linked to the fourteen verified models; semantic correctness remains `NOT VERIFIED`.
- Progress: Sources **7/58**; Educational **1/26**; Exam Groups **6/32**; Individual Exam Models **99**; Exam Pages **347/2,286**; source images technical **533/5,273**.
- Global questions: Lesson-linked **2225**; Exam-linked **733**; Review-required **351**; Unclassified **22446**; invariant **PASS = 25,755**.
- RAW/unrelated/import/publication mutations: **0/0/0/0**.
- Next source: `f4b6708c-027f-4883-9e85-e6e7acb52ecc` — `كتاب العلوم - الجزء الأول`.
<!-- SCIENCE_EXAM_1447_CHECKPOINT_END -->

<!-- SCIENCE_BOOK_PART1_CHECKPOINT_START -->
## Continuation checkpoint — Science Part 1 complete

Continue with `81e99fe6-1421-462b-9562-1c0c5053a809 — كتاب العلوم - الجزء الثاني`; do not rerun Science Part 1 absent new drift evidence. Current verified global progress: **8/58 sources; 2/26 educational; 6/32 exam groups; 694/5,273 technical images; 2,236 lesson-linked; 733 exam-linked; 351 review-required; 22,435 unclassified**.
<!-- SCIENCE_BOOK_PART1_CHECKPOINT_END -->

<!-- SCIENCE_BOOK_PART2_CHECKPOINT_START -->
## Continuation checkpoint — Science Part 2 complete

Continue with `8489a487-91d9-47fb-80b8-35d0e7a074a4 — الانجليزي نماذج وزارية 1445`; do not rerun Science Part 2 absent new drift evidence. Current verified global progress: **9/58 sources; 3/26 educational; 6/32 exam groups; 839/5,273 technical images; 2,236 lesson-linked; 733 exam-linked; 351 review-required; 22,435 unclassified**.
<!-- SCIENCE_BOOK_PART2_CHECKPOINT_END -->

<!-- ENGLISH_EXAM_1445_CHECKPOINT_START -->
## Reconstruction checkpoint — Grade 9 English Ministry Exams 1445

- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Source `8489a487-91d9-47fb-80b8-35d0e7a074a4` — `الانجليزي نماذج وزارية 1445` completed from source-local evidence.
- Technical verification: **30/30** images exist, readable, byte-size/SHA-256/MIME match; sequence **1..30** contiguous; duplicate SHA groups **0**.
- Full visual review + explicit page titles resolve **10** verified source occurrences / **10** unique Individual Exam Models; each occurrence is two question pages + one correction/result page.
- Finalized Exam Pages: **30**; review-required pages: **0**; correction-sheet candidates: **10**; verified standalone Answer Keys: **0 / NOT VERIFIED**.
- Source legacy questions: **0**; no questions were fabricated or mapped.
- Progress: Sources **10/58**; Educational **3/26**; Exam Groups **7/32**; Individual Exam Models **109**; Exam Pages **377/2,286**; source images technical **869/5,273**.
- Global questions: Lesson-linked **2236**; Exam-linked **733**; Review-required **351**; Unclassified **22435**; invariant **PASS = 25,755**.
- RAW/unrelated/import/publication mutations: **0/0/0/0**.
- Next source: `062f0aa0-ae21-454e-ad9a-c390df6e4a08` — `الانجليزي نماذج وزارية 1446`.
<!-- ENGLISH_EXAM_1445_CHECKPOINT_END -->

<!-- ENGLISH_EXAM_1446_CHECKPOINT_START -->
## Reconstruction checkpoint — Grade 9 English Ministry Exams 1446

- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Source `062f0aa0-ae21-454e-ad9a-c390df6e4a08` — `الانجليزي نماذج وزارية 1446` completed from source-local evidence.
- Technical verification: **39/39** images exist, readable, byte-size/SHA-256/MIME match; sequence **1..39** contiguous; duplicate SHA groups **0**.
- Full visual review + explicit page titles resolve **13** verified source occurrences / **13** unique Individual Exam Models; each occurrence is two question pages + one correction/result page.
- Finalized Exam Pages: **39**; review-required pages: **0**; correction-sheet candidates: **13**; verified standalone Answer Keys: **0 / NOT VERIFIED**.
- Source legacy questions: **0**; no questions were fabricated or mapped.
- Progress: Sources **11/58**; Educational **3/26**; Exam Groups **8/32**; Individual Exam Models **122**; Exam Pages **416/2,286**; source images technical **908/5,273**.
- Global questions: Lesson-linked **2236**; Exam-linked **733**; Review-required **351**; Unclassified **22435**; invariant **PASS = 25,755**.
- RAW/unrelated/import/publication mutations: **0/0/0/0**.
- Next source: `da6fc228-1ada-4627-8306-80d9d3401490` — `الانجليزي نماذج وزارية 1447`.
<!-- ENGLISH_EXAM_1446_CHECKPOINT_END -->

<!-- ENGLISH_EXAM_1447_CHECKPOINT_START -->
## Reconstruction checkpoint — Grade 9 English Ministry Exams 1447

- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Source `da6fc228-1ada-4627-8306-80d9d3401490` — `الانجليزي نماذج وزارية 1447` completed with source anomalies preserved rather than normalized.
- Technical verification: **42/42** images exist, readable, byte-size/SHA-256/MIME match; duplicate SHA groups **0**.
- Preserved numbering anomaly: missing numeric labels **12, 26, 37**; duplicate numeric labels **18, 27, 29**; RAW/metadata normalization **0**.
- Full visual review resolves **13** complete Individual Exam Models / **39** finalized Exam Pages. Three records remain page-level `review_required`: one unmatched extra paper-2 record and the incomplete model-13 paper-2 + correction pair whose paper 1 is `NOT VERIFIED`.
- Correction/result candidates: **14** total; **13** model-matched to finalized models; verified standalone Answer Keys: **0 / NOT VERIFIED**.
- All **234/234** legacy questions occur on question records that belong to finalized models and are structurally exam-linked; semantic correctness remains `NOT VERIFIED`.
- Progress: Sources **12/58**; Educational **3/26**; Exam Groups **9/32**; Individual Exam Models **135**; Exam Pages **455/2,286**; source images technical **950/5,273**.
- Global questions: Lesson-linked **2236**; Exam-linked **967**; Review-required **351**; Unclassified **22201**; invariant **PASS = 25,755**.
- RAW/unrelated/import/publication mutations: **0/0/0/0**.
- Next source: `1794eea5-4772-4c94-bd2b-b08e5815e733` — `انجليزي الكتاب `.
<!-- ENGLISH_EXAM_1447_CHECKPOINT_END -->

<!-- HISTORY_SOURCE_LOCAL_CHECKPOINT_START -->
## Continuation checkpoint — History source-local reconstruction complete

Continue with `7f02b242-5164-46d1-a82d-7f1023cfa8c9 — التربية الوطنية`; do not rerun History absent fresh drift evidence. Current verified global progress: **13/58 sources; 4/26 educational; 9/32 exam groups; 1,011/5,273 technical images; 2,374 lesson-linked; 967 exam-linked; 351 review-required; 22,063 unclassified**. History master equivalence remains `NOT VERIFIED`, but source-local structure is independently verified from immutable RAW evidence.
<!-- HISTORY_SOURCE_LOCAL_CHECKPOINT_END -->

<!-- CIVICS_BOOK_CHECKPOINT_START -->
## Continuation checkpoint — Civics complete

Continue with `a7f1e94f-82d1-4146-af5b-4e9b51363f0b — كتاب الجغرافيا`; do not rerun Civics absent new drift evidence. Current verified global progress: **14/58 sources; 5/26 educational; 9/32 exam groups; 1,070/5,273 technical images; 2,374 lesson-linked; 967 exam-linked; 351 review-required; 22,063 unclassified**.
<!-- CIVICS_BOOK_CHECKPOINT_END -->

<!-- GEOGRAPHY_BOOK_CHECKPOINT_START -->
## Reconstruction checkpoint — Grade 9 Geography

- Sources processed: **15/58**; Educational: **6/26**; Exam Source Groups: **9/32**.
- Books / Units / Lessons / Lesson pages: **6 / 33 / 151 / 602**.
- Geography: **104/104** technically verified and unique exact RAW/master SHA identities.
- Reconstructed: **4 Units, 18 Lessons, 94 Lesson pages, 4 covers, 6 reviews, 0 non-lesson pages**.
- Questions unchanged: **2,374 + 967 + 351 + 22,063 = 25,755**.
- Source images technical **1,174/5,273**. RAW/unrelated/import/publication mutations **0/0/0/0**.
- Next: `516f1c1d-acc0-4b1c-8e50-8f92a7c737e0 — الإيمان الكتاب المدرسي`.
<!-- GEOGRAPHY_BOOK_CHECKPOINT_END -->
