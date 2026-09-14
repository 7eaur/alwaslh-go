# Alwaslh Content Rebuild — Shared Execution Status

## 2026-09-14 — Corpus-wide metadata inventory checkpoint

Current owner instruction supersedes the earlier Grade 9-only continuation: inventory and reconstruct all available sources and independent exam models; no new publication.

Working branch: `content/corpus-inventory-20260914`, based on `041cb0738f3a76600eebde29dfb0181ef7e76255`.
Read `CONTENT_INVENTORY.md`, `CONTENT_VALIDATION_REPORT.md`, `CONTENT_IMPORT_REPORT.md` and `manifests/MASTER_CONTENT_MANIFEST.json`.
58 legacy manifests read; 5273 image references matched Git paths and sizes; 25755 questions recorded. 32 candidate exam collections cover 2286 pages and 2715 legacy questions. Collection count is NOT individual Exam Model count. 99 recorded checksum duplicate groups retained.
New imports/publications: 0. Current PostgreSQL state and binary SHA-256 recalculation: NOT VERIFIED. No import-ready batch exists yet.
Next: verify source bytes, inspect actual exam boundaries and answer-key evidence, reconcile master against RAW, inspect modern schema/runtime, then run guarded import gates. Direct GitHub access from the execution environment timed out; connector text reads succeeded.
Preserve previously authorized Grade 9 publication; do not rerun prior import or publisher.


> اقرأ هذه النسخة + live heads قبل أي عمل. Code/DB/runtime evidence outrank stale prose.

Last synchronized: **2026-09-14 — reviewed Grade 9 English Unit 2 Lessons published and post-verified**.

## Fixed execution contract

`Legacy Supabase -> Immutable RAW -> Reviewed/Recovered Structure -> Dry Run -> Controlled Transaction -> Modern PostgreSQL -> Verification -> Explicit Publication`

- لا تستخدم heuristic القديم `69 -> 62` كحقيقة منهجية.
- RAW immutable.
- لا auto-publish لأي AI/legacy content غير مراجع.
- لا حذف anomalies أو تعديل بيانات غير مرتبطة لتجميل الأرقام.
- أي apply يفشل مغلقًا عند identity/count/provenance/publication drift.
- WebP لا يُقبل إلا بعد إثبات فائدة الحجم والوضوح.

## Current live checkpoint

Working repository/branch:

- `7eaur/alwaslh-go@content/legacy-staging-rebuild`
- full-bulk source commit: `9e58ab3e882b883bddd016099949881801eedc28`
- CURATION-002 verifier commit: `2575d399db03be62911a927d5ce15bb8614fa9e8`
- reviewed publication runner commit: `ea5a19b7086eb8779701be2b1f47fc073b38aa12`
- reviewed correction/final publication head: `7d17e19bef37835d500de492053e728f0cdb9f1b`
- publication report commit: `71a77cf3050bd5e1777a8fc387396edab9a93fd9`

Railway content service was returned to an idle start command after publication verification; later documentation commits must not replay publication logic.

## FULL-GRADE9-ENGLISH-BULK-IMPORT — DONE / FULL_ASSET_COVERAGE_VERIFIED

Authoritative reconstruction scope:

- Legacy subject ID: `1794eea5-4772-4c94-bd2b-b08e5815e733`
- RAW-backed pages: `69`
- RAW images: `69`
- Question revisions: `104`
- recovered Sections/Units: `8`
- source-manifest-only page: `1` (`Blank Final Page`, page 70), evidence-only because no RAW identity exists

Recovered units:

1. `Unit 1 - Revision`
2. `Unit 2 - Describing: Making plans`
3. `Unit 3 - Other countries`
4. `Unit 4 - Visiting Japan`
5. `Unit 5 - Safety`
6. `Unit 6 - Helping others`
7. `Unit 7 - Communications`
8. `Unit 8 - Winning medals`

Source clarification:

- `master` contains the original Grade 9 English reference under `تاسع انجليزي/الانجليزي_تاسع` (`manifest.json`, page-by-page guide and source images). It is valid structural/reference evidence and was used to cross-check page/unit/title layout.
- `master` also contains unrelated corpora, including Third Secondary/Pupil's Book 6; always resolve the exact Grade 9 path before using it.
- Immutable RAW + reconstruction manifest + modern PostgreSQL remain write/import authority; the original `master` corpus is reference evidence, not permission to overwrite modern state blindly.

### Bulk runtime evidence

Railway deployment:

`de7f9883-b2f0-483d-a7c1-ffbfb15ac30c` — `SUCCESS`

Verified runtime sequence:

- `BULK_G9_EN_INSPECT_PASS`
- `BULK_G9_EN_TRANSACTION_GATE_PASS`
- `BULK_G9_EN_APPLY_PASS`
- `BULK_G9_EN_VERIFY_PASS`
- `BULK_G9_EN_RUNNER_PASS`

Committed bulk state:

- pages verified `69/69`
- RAW images verified by SHA-256 `69/69`
- ready Media Assets `69/69`
- Lesson Assets `69/69`
- Sections `8/8`
- asset-owning Lesson identities at bulk checkpoint `59`
- Question Revisions preserved `104/104`
- page 70 preserved evidence-only `1`
- RAW/media-binary/question/unrelated mutations `0`

At the bulk checkpoint publication was intentionally `0/0/0`. Publication was later opened only for the explicitly reviewed two-Lesson Unit 2 slice documented below.

`59` was an observed bulk-checkpoint count, not a derived `69 -> 62` heuristic. Modern reviewed curation may group multiple source pages into one Lesson while preserving page/image provenance.

Detailed bulk evidence: `content-staging/BULK_GRADE9_ENGLISH_IMPORT_REPORT.md`.

## CURATION-001 — DONE / COMMITTED_STATE_VERIFIED / PUBLISHED

Reviewed Unit 2 pages `5..8` are one modern Lesson:

- slug: `curated-english9-pb3-u2-describing-people-and-animals`
- title: `Describing people and animals`
- Lesson Assets: `4`, exact ordered pages `5,6,7,8`
- reviewed Question Revisions: `12`
- Lesson: published
- all 4 Lesson Assets: published
- all 12 reviewed Question Revisions: published and linked to this modern Lesson

## CURATION-002 — DONE / COMMITTED_STATE_VERIFIED / PUBLISHED

Reviewed Unit 2 pages `9..10` are one modern Lesson:

- slug: `curated-english9-pb3-u2-time-and-meeting`
- title: `Telling time and arranging a meeting`
- Lesson Assets: `2`, exact ordered pages `9,10`
- provenance/SHA verified: `2/2`
- reviewed Question Revisions: `7`
- Lesson: published
- both Lesson Assets: published
- all 7 reviewed Question Revisions: published and linked to this modern Lesson

One page-10 legacy question was corrected before publication:

- old: `When is Rashid meeting mentioned in the dialogue?`
- reviewed: `When is Fuad helping Dad on Saturday?`
- answer: `at six o'clock`
- reviewed explanation: `Fuad says he is helping Dad at six o'clock.`

The other `18/19` reviewed questions were approved unchanged.

## REVIEWED-UNIT2-PUBLICATION — DONE / COMMITTED_STATE_VERIFIED_AND_PUBLISHED

User explicitly authorized publication only for the Lessons/questions that had completed review.

Final Railway deployment:

`5024b218-32e0-49fe-b9f8-20ee82c5bcd0` — `SUCCESS`

Post-commit runtime markers:

- `G9_U2_PUBLISH_APPLY_PASS`
- `G9_U2_PUBLISH_FULL_PASS`
- status: `COMMITTED_STATE_VERIFIED_AND_PUBLISHED`

Verified publication result:

- published Lessons in Grade 9 English after this gate: `2`
- published Lesson Assets after this gate: `6`
- published Question Revisions after this gate: `19`
- target Reader-eligible published assets: `6`
- target Question Bank revisions eligible for Quiz Builder: `19`
- question links: `12` to Describing + `7` to Time/Meeting
- RAW mutations: `0`
- media-binary mutations: `0`
- page 70 fabrication: `0`
- unrelated publication: `0`

The exact Grade 9 English publication totals `2 / 6 / 19` prove the rest of the imported book remains Draft/unpublished.

Student-delivery meaning:

- the two reviewed Lessons now satisfy Student Reader publication predicates, subject to normal auth/entitlement rules;
- the 19 reviewed questions are published Question Bank revisions with known answers and are available to Quiz Builder;
- this does **not** claim that a standalone student Quiz/version has been created or published. Quiz construction/publication is a separate product action if required.

Detailed publication evidence: `content-staging/GRADE9_UNIT2_REVIEWED_PUBLICATION_REPORT.md`.

## Prior closed checkpoints retained

- `BATCH-001` — DONE / COMMITTED_STATE_VERIFIED
- `STRUCTURE-001` — DONE / SECTION_BOUNDARY_VERIFIED
- `STRUCTURE-002` — DONE / SECTION_BOUNDARY_VERIFIED
- `CURATION-001` — DONE / COMMITTED_STATE_VERIFIED / PUBLISHED
- `CURATION-002` — DONE / COMMITTED_STATE_VERIFIED / PUBLISHED
- `CONTENT-GAPS-001` — DONE / GAP_INVENTORY_VERIFIED
- `MEDIA-001` — DONE / MEDIA_PROFILE_VERIFIED_PARTIAL_ACCEPTANCE
- `IMPORT-001` — DONE / COMMITTED_STATE_VERIFIED
- `VERIFY-001` — DONE / DELIVERY_ISOLATION_AND_PROVENANCE_VERIFIED
- `ROADMAP-RETURN` — DONE / STUDENT-016I_HANDOFF_VERIFIED
- `FULL-GRADE9-ENGLISH-BULK-IMPORT` — DONE / FULL_ASSET_COVERAGE_VERIFIED
- `REVIEWED-UNIT2-PUBLICATION` — DONE / COMMITTED_STATE_VERIFIED_AND_PUBLISHED

Do not repeat them unless fresh evidence invalidates their results.

## Exact next Content action

Do **not** rerun the Grade 9 English bulk import or republish the two reviewed Lessons.

The remaining Grade 9 English corpus is still imported but unpublished. Continue pedagogical review from the first unresolved evidence-backed boundary, then publish only future Lessons/questions that complete the same review + rollback-gate + post-verify standard.

Never delete provenance, fabricate page 70, mutate RAW, reintroduce the `69 -> 62` heuristic, or auto-publish unreviewed legacy/AI content.

<!-- CHEMISTRY_RECONSTRUCTION_CHECKPOINT_START -->
## Reconstruction checkpoint — Third Secondary Chemistry

- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Sources processed: **1/58**
- Educational sources processed: **1/26**
- Verified Books / Units / Lessons / Lesson pages: **1 / 9 / 57 / 149**
- Exam source groups processed: **0/32**
- Individual Exam Models / Exam pages / Answer Keys: **0 / 0 of 2,286 / 0**
- Source images technically verified: **178/5,273**
- Chemistry source verification: 178 exists, 178 readable, 178 byte-size matches, 178 SHA-256 matches, 178 MIME matches; page range **11..188** contiguous; duplicate SHA groups within this source: **0**.
- WebP derivatives generated / accepted / rejected: **0 / 0 / 0**. The verified Chemistry RAW source is already WebP; derivative optimization has not been executed yet.
- Legacy questions baseline: **25,755**.
- Structurally lesson-linked: **2,225** (page-local mapping only; semantic correctness `NOT VERIFIED`).
- Review-required from Chemistry unit covers/reviews: **351**.
- Exam-linked to an Individual Exam Model: **0**.
- Remaining unclassified: **23,179**.
- Duplicate fingerprint groups classified: **0/99**.
- RAW mutations / unrelated mutations / new imports / new publications: **0 / 0 / 0 / 0**.
- Last completed source: `f0c5228c-7d5b-4ec2-85ed-ce59139ce0a4` — `الكيمياء الكتاب المدرسي`.
- Next source: `e101d097-7a14-44e5-b242-cdeb9a312b77` — `الكيمياء نماذج وزاريه 1445`.
<!-- CHEMISTRY_RECONSTRUCTION_CHECKPOINT_END -->

<!-- CHEMISTRY_EXAM_1445_CHECKPOINT_START -->
## Reconstruction checkpoint — Chemistry Ministry Exams 1445

- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Sources processed: **2/58**
- Educational sources processed: **1/26**
- Verified Books / Units / Lessons / Lesson pages: **1 / 9 / 57 / 149**
- Exam Source Groups processed: **1/32**
- Individual Exam Models: **20**
- Exam pages processed: **60/2,286**
- Verified Answer Keys: **0**
- Correction/electronic-answer sheet candidates: **20**; official Answer Key status remains `NOT VERIFIED`.
- Source images technically verified: **238/5,273** (178 Chemistry textbook + 60 Chemistry exams 1445).
- Chemistry 1445 source technical result: **60/60** exist, readable, byte-size match, SHA-256 match, MIME match; page sequence 1..60 contiguous; within-source duplicate SHA groups **0**.
- WebP derivatives generated / accepted / rejected: **0 / 0 / 0**.
- Legacy questions baseline: **25,755**.
- Structurally lesson-linked: **2,225**; review-required: **351**; exam-linked to Individual Exam Models: **0**; remaining unclassified: **23,179**.
- Duplicate fingerprint groups classified: **0/99**.
- RAW mutations / unrelated mutations / new imports / new publications: **0 / 0 / 0 / 0**.
- Last completed source: `e101d097-7a14-44e5-b242-cdeb9a312b77` — `الكيمياء نماذج وزاريه 1445`.
- Next source: `c09ce569-ea42-4f0b-997f-95b029a7e6ea` — `الكيمياء نماذج وزاريه 1446`.
<!-- CHEMISTRY_EXAM_1445_CHECKPOINT_END -->

<!-- CHEMISTRY_EXAM_1446_CHECKPOINT_START -->
## Reconstruction checkpoint — Chemistry Ministry Exams 1446

- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Sources processed: **3/58**; Educational: **1/26**; Exam Source Groups: **2/32**.
- Books / Units / Lessons / Lesson pages: **1 / 9 / 57 / 149**.
- Verified Individual Exam Models: **34** total; finalized Exam Pages: **120/2,286**; Verified Answer Keys: **0**.
- 1446: **15** four-page source occurrences = 3 question pages + 1 candidate-specific electronic correction report; **14 unique models**.
- Visible unique model codes: `P.87, P.45, P.52, P.9, P.3, P.27, P.5, P.41, P.72, P.107, P.25, P.40, P.34, P.89`.
- Pages **29..31 == 41..43** by exact SHA and both are `P.41`; correction pages **32** and **44** are distinct candidate records. Classification: `legitimate_repeated_exam_model_occurrence`; all pages preserved.
- Correction-report candidates total: **35** (20 + 15); standalone official Answer Key status remains `NOT VERIFIED`.
- Source images technically verified: **298/5,273**; WebP generated/accepted/rejected: **0/0/0**.
- Legacy Questions: **25,755**; Lesson-linked **2,225**; Exam-linked **0**; Review-required **351**; Unclassified **23,179**.
- Global duplicate fingerprint groups classified: **0/99**; local 1446 pairs are not counted globally without proven mapping.
- RAW / unrelated / import / publication mutations: **0 / 0 / 0 / 0**.
- Last completed: `c09ce569-ea42-4f0b-997f-95b029a7e6ea`; Next: `e7c8291c-e904-4e8c-9cd8-2753818cedf3` — Chemistry 1447.
<!-- CHEMISTRY_EXAM_1446_CHECKPOINT_END -->

<!-- CHEMISTRY_EXAM_1447_CHECKPOINT_START -->
## Reconstruction checkpoint — Chemistry Ministry Exams 1447

- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Sources processed: **4/58**; Educational: **1/26**; Exam Source Groups: **3/32**.
- Books / Units / Lessons / Lesson pages: **1 / 9 / 57 / 149**.
- Verified Individual Exam Models: **62**; finalized Exam Pages: **236/2,286**; Verified Answer Keys: **0**.
- Chemistry 1447: **124/124** technical checks green; all **124** pages visually reviewed; **31** four-page source blocks; **29** verified model-matched occurrences; **28** unique models; **116** finalized model pages; **8** pages isolated as `review_required`.
- Mismatch blocks: pages **37..40** (`P.61` questions / `P.31` correction) and **45..48** (`P.28` questions / `P.88` correction). No missing question pages were fabricated.
- `P.8` at **49..52** and **57..60** is a legitimate repeated model occurrence; exact duplicate question pages are preserved with distinct candidate correction reports.
- Correction/electronic-answer sheet candidates total: **66**; official standalone Answer Keys remain `NOT VERIFIED`.
- Source images technically verified: **422/5,273**; WebP generated/accepted/rejected: **0/0/0**.
- Legacy Questions: **25,755**; Lesson-linked **2225**; Exam-linked **226**; Review-required **351**; Unclassified **22953**.
- 1447 question mapping: **226** structurally exam-linked + **0** review-required = **226/226** accounted for; semantic correctness `NOT VERIFIED`.
- Global duplicate fingerprint groups classified: **0/99**; local 1447 exact-SHA groups are recorded separately and do not alter the global fingerprint baseline without proven mapping.
- RAW / unrelated / import / publication mutations: **0 / 0 / 0 / 0**.
- Last completed: `e7c8291c-e904-4e8c-9cd8-2753818cedf3` — `الكيمياء نماذج وزاريه 1447`.
- Next source: `ef408805-c337-44dd-b903-7838030e6de0` — `العلوم نماذج وزارية 1445`.
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
## Reconstruction checkpoint — Grade 9 Science Part 1

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
<!-- SCIENCE_BOOK_PART1_CHECKPOINT_END -->

<!-- SCIENCE_BOOK_PART2_CHECKPOINT_START -->
## Reconstruction checkpoint — Grade 9 Science Part 2

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
<!-- SCIENCE_BOOK_PART2_CHECKPOINT_END -->
