# CONTENT IMPORT REPORT

Current checkpoint: metadata inventory only.

New inserts/updates/publications: 0. Dry Run, Transaction Gate, Apply and current read-only PostgreSQL verifier: NOT RUN.

Historical Grade 9 English reports record 69 imported pages/images, 8 units and 104 Question Revisions, with later explicitly authorized publication of 2 Lessons, 6 Lesson Assets and 19 revisions. These are historical evidence, not a fresh runtime result. Do not rerun import or reset publication to zero.

Blocking gates: byte-level source verification, actual exam boundaries, answer-key evidence, current schema and runtime mapping. No candidate collection may be imported as a Lesson or Quiz.

<!-- CHEMISTRY_RECONSTRUCTION_CHECKPOINT_START -->
## Reconstruction checkpoint — no import performed

Chemistry textbook reconstruction is verified, but the corpus is **not import-ready yet**.

- Reconstruction artifact: `content-staging/reconstruction/educational/f0c5228c-7d5b-4ec2-85ed-ce59139ce0a4.json`.
- Technical artifact: `content-staging/reconstruction/technical/f0c5228c-7d5b-4ec2-85ed-ce59139ce0a4.json`.
- New imports: **0**.
- New publications: **0**.
- Production mutations: **0**.
- RAW mutations: **0**.
- PostgreSQL import contract review remains deferred until corpus Reconstruction and Exam Boundary Discovery are complete, per the execution gate.
<!-- CHEMISTRY_RECONSTRUCTION_CHECKPOINT_END -->

<!-- CHEMISTRY_EXAM_1445_CHECKPOINT_START -->
## Chemistry 1445 exam checkpoint — no import performed

- Reconstruction artifact: `content-staging/reconstruction/exams/source-groups/e101d097-7a14-44e5-b242-cdeb9a312b77.json`.
- Technical artifact: `content-staging/reconstruction/technical/e101d097-7a14-44e5-b242-cdeb9a312b77.json`.
- Discovered: **20 Individual Exam Models / 60 exam pages / 20 correction-sheet candidates / 0 verified Answer Keys**.
- New imports / publications / production mutations / RAW mutations: **0 / 0 / 0 / 0**.
- Import Readiness is still gated on completion of corpus reconstruction and remaining Exam Source Groups.
<!-- CHEMISTRY_EXAM_1445_CHECKPOINT_END -->

<!-- CHEMISTRY_EXAM_1446_CHECKPOINT_START -->
## Chemistry 1446 exam checkpoint — no import performed

- Final artifact: `content-staging/reconstruction/exams/source-groups/c09ce569-ea42-4f0b-997f-95b029a7e6ea.json`.
- Finalized: **60 pages / 15 source occurrences / 14 unique Individual Exam Models / 15 correction reports / 0 verified standalone Answer Keys**.
- Repeated `P.41` occurrence remains preserved with provenance; no automatic deletion or merge.
- New imports / publications / production / RAW mutations: **0 / 0 / 0 / 0**. Import Readiness remains gated on remaining reconstruction.
<!-- CHEMISTRY_EXAM_1446_CHECKPOINT_END -->

<!-- CHEMISTRY_EXAM_1447_CHECKPOINT_START -->
## Chemistry 1447 exam checkpoint — no import performed

- Final artifact: `content-staging/reconstruction/exams/source-groups/e7c8291c-e904-4e8c-9cd8-2753818cedf3.json`.
- Finalized: **28 unique Individual Exam Models / 116 model pages** from **29** verified occurrences; **8** source pages isolated in two `review_required` blocks.
- Questions: **226** structurally exam-linked; **0** review-required; semantic correctness `NOT VERIFIED`.
- Correction-report candidates: **31**; verified standalone Answer Keys: **0**.
- New imports / publications / production / RAW mutations: **0 / 0 / 0 / 0**. Import Readiness remains gated on remaining reconstruction.
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
## Science Part 1 reconstruction checkpoint — no import performed

The reconstruction artifact is verified, but the corpus remains `RECONSTRUCTION_IN_PROGRESS_NOT_IMPORT_READY`.

- New imports: **0**; new publications: **0**; production mutations: **0**; RAW mutations: **0**.
- Import readiness remains deferred until corpus reconstruction/boundary discovery is complete.
<!-- SCIENCE_BOOK_PART1_CHECKPOINT_END -->
