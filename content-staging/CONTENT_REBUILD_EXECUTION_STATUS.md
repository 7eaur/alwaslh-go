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
## Reconstruction checkpoint — Grade 9 History source-local semester 1

- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`.
- Sources processed: **13/58**; Educational: **4/26**; Exam Source Groups: **9/32**.
- Books / explicit Units / Lessons / Lesson pages: **4 / 25 / 119 / 460**.
- History source: **61/61** technically verified images, stored pages **8..68**, complete source-local visual review.
- Master equivalence: **NOT VERIFIED**; current master History references were explicitly rejected as semantic authority for this RAW.
- Source-local structure: page **8** explicit TOC; page **9** `الفصل الدراسي الأول` cover; **9 lessons**, **47 lesson-content pages**, **12 lesson-review pages**; all **61 pages classified exactly once**.
- Questions: **138/138** structurally lesson-linked by verified source page membership; semantic correctness remains `NOT VERIFIED`; source review-required questions **0**.
- Global questions: Lesson-linked **2,374**; Exam-linked **967**; Review-required **351**; Unclassified **22,063** = **25,755**.
- Individual Exam Models **135**; Exam Pages **455/2,286**; Verified Answer Keys **0**.
- Source images technical **1,011/5,273**; WebP **0/0/0**; Duplicate groups **0/99**.
- RAW / unrelated / imports / publications: **0/0/0/0**.
- Last completed: `0a76f44b-0a4f-4e36-9ea9-badecf78bf23 — التاريخ الكتاب المدرسي`.
- Next: `7f02b242-5164-46d1-a82d-7f1023cfa8c9 — التربية الوطنية`.
<!-- HISTORY_SOURCE_LOCAL_CHECKPOINT_END -->

<!-- CIVICS_BOOK_CHECKPOINT_START -->
## Reconstruction checkpoint — Grade 9 Civics

- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Sources processed: **14/58**; Educational: **5/26**; Exam Source Groups: **9/32**.
- Books / Units / Lessons / Lesson pages: **5 / 29 / 133 / 508**.
- Civics: **59/59** technically verified images and **59/59** unique exact RAW/master SHA identities.
- Exact retained mapping: stored pages **6..64** -> master source pages **7..65**.
- Reconstructed source: **1 Book, 4 Units, 14 Lessons, 48 Lesson pages, 4 Unit-cover pages, 7 Unit-review pages, 0 non-lesson pages**.
- Questions: source contains **0** legacy questions; no question records fabricated.
- Global questions unchanged: Lesson-linked **2,374**; Exam-linked **967**; Review-required **351**; Unclassified **22,063** = **25,755**.
- Individual Exam Models **135**; Exam Pages **455/2,286**; Verified Answer Keys **0**.
- Source images technical **1,070/5,273**; WebP **0/0/0**; Duplicate groups **0/99**.
- RAW / unrelated / imports / publications: **0/0/0/0**.
- Last completed: `7f02b242-5164-46d1-a82d-7f1023cfa8c9 — التربية الوطنية`.
- Next: `a7f1e94f-82d1-4146-af5b-4e9b51363f0b — كتاب الجغرافيا`.
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

<!-- FAITH_BOOK_CHECKPOINT_START -->
## Reconstruction checkpoint — Faith Book

- Sources processed: **16/58**; Educational: **7/26**; Exam Source Groups: **9/32**.
- Books / Units / Lessons / Lesson pages: **7 / 33 / 161 / 667**.
- Faith source: **65/65** technically verified + exact SHA-identical to `master/التربية الاسلاميه ثالث ثانوي/كتاب الإيمان/الصور`.
- Exact filename evidence establishes **10 lessons** and assigns **65/65 retained pages** to one lesson; no unit layer was asserted (`NOT VERIFIED`).
- Questions: **976/976 structurally lesson-linked** by exact page membership; semantic correctness remains `NOT VERIFIED`.
- Global question invariant: **3,350 + 967 + 351 + 21,087 = 25,755**.
- Source images technical **1,239/5,273**. RAW/unrelated/import/publication mutations **0/0/0/0**.
- Next: `f25891fe-ea52-481b-baf2-ff4764c79bde — الاسلاميه ثانوي نماذج وزاريه 1447`.
<!-- FAITH_BOOK_CHECKPOINT_END -->

<!-- ISLAMIC_EXAM_1447_CHECKPOINT_START -->
## Reconstruction checkpoint — Islamic Ministry Exams 1447

- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Source `f25891fe-ea52-481b-baf2-ff4764c79bde` — `الاسلاميه ثانوي نماذج وزاريه 1447` completed from source-local evidence.
- Technical verification: **93/93** images exist, readable, byte-size/SHA-256/MIME match; sequence **1..93** contiguous.
- Exact-SHA duplicate groups: **6**, preserved as provenance/evidence and not silently merged.
- Complete visual review resolves **31** verified source occurrences / Individual Exam Models; every occurrence is two question pages followed by one correction/result page.
- Finalized Exam Pages: **93**; review-required pages: **0**; correction-sheet candidates: **31**; verified standalone Answer Keys: **0 / NOT VERIFIED**; official model-code transcription remains **NOT VERIFIED**.
- Source legacy questions: **0**; no questions were fabricated or mapped.
- Progress: Sources **17/58**; Educational **7/26**; Exam Groups **10/32**; Individual Exam Models **166**; Exam Pages **548/2,286**; source images technical **1332/5,273**.
- Global questions: Lesson-linked **3350**; Exam-linked **967**; Review-required **351**; Unclassified **21087**; invariant **PASS = 25,755**.
- RAW/unrelated/import/publication mutations: **0/0/0/0**.
- Next source: `cae82d8f-64f9-4d2a-984f-6e6fd19fac5c` — `الحديث والتهذيب الكتاب `.
<!-- ISLAMIC_EXAM_1447_CHECKPOINT_END -->

<!-- HADITH_BOOK_CHECKPOINT_START -->
## Reconstruction checkpoint — Hadith and Refinement Book

- Sources processed: **18/58**; Educational: **8/26**; Exam Source Groups: **10/32**.
- Books / Units / Lessons / Lesson pages: **8 / 33 / 171 / 729**.
- Hadith source: **62/62** technically verified + exact SHA-identical to `master/التربية الاسلاميه ثالث ثانوي/كتاب الحديث والتهذيب/الصور`.
- Exact filename evidence establishes **10 lessons** and assigns **62/62 retained pages** to one lesson; no unit layer was asserted (`NOT VERIFIED`).
- Questions: **1,483/1,483 structurally lesson-linked** by exact page membership; semantic correctness remains `NOT VERIFIED`.
- Global question invariant: **4,833 + 967 + 351 + 19,604 = 25,755**.
- Source images technical **1,394/5,273**. RAW/unrelated/import/publication mutations **0/0/0/0**.
- Next: `a89c6c5d-d3d2-4aed-b98c-2ef5224cdae8 — السيرة النبوية الكتاب `.
<!-- HADITH_BOOK_CHECKPOINT_END -->

<!-- SEERAH_BOOK_CHECKPOINT_START -->
## Reconstruction checkpoint — Seerah Book

- Sources processed: **19/58**; Educational: **9/26**; Exam Source Groups: **10/32**.
- Books / Units / Lessons / Lesson pages: **9 / 33 / 183 / 810**.
- Seerah source: **81/81** technically verified + exact SHA-identical to `master/التربية الاسلاميه ثالث ثانوي/كتاب السيرة النبوية/الصور`.
- Exact filename evidence establishes **12 lessons** and assigns **81/81 retained pages** to one lesson; no unit layer was asserted (`NOT VERIFIED`).
- Page 88 filename explicitly contains `التقويم والخاتمة`; other page subtype boundaries remain `NOT VERIFIED`.
- Questions: **1,152/1,152 structurally lesson-linked** by exact page membership; semantic correctness remains `NOT VERIFIED`.
- Global question invariant: **5,985 + 967 + 351 + 18,452 = 25,755**.
- Source images technical **1,475/5,273**. RAW/unrelated/import/publication mutations **0/0/0/0**.
- Next: `6a8ea7f2-1e77-4654-a28c-0ea1b82b4830 — الفقه الكتاب المدرسي`.
<!-- SEERAH_BOOK_CHECKPOINT_END -->

<!-- FIQH_BOOK_CHECKPOINT_START -->
## Reconstruction checkpoint — Fiqh Book

- Sources processed: **20/58**; Educational: **10/26**; Exam Source Groups: **10/32**.
- Books / Units / Lessons / Lesson pages: **10 / 33 / 196 / 877**.
- Fiqh source: **67/67** technically verified + exact SHA-identical to `master/التربية الاسلاميه ثالث ثانوي/كتاب الفقه/الصور`.
- Exact filename evidence establishes **13 lessons** and assigns **67/67 retained pages** to one lesson; no unit layer was asserted (`NOT VERIFIED`).
- Independent page subtype/review boundaries remain `NOT VERIFIED`; no unsupported review page was invented.
- Questions: **906/906 structurally lesson-linked** by exact page membership; semantic correctness remains `NOT VERIFIED`.
- Global question invariant: **6,891 + 967 + 351 + 17,546 = 25,755**.
- Source images technical **1,542/5,273**. RAW/unrelated/import/publication mutations **0/0/0/0**.
- Next: `0d4fa9fd-a93c-4d18-9dea-6dd22eb2e199 — الرياضيات نماذج وزارية 1445`.
<!-- FIQH_BOOK_CHECKPOINT_END -->

<!-- MATH_EXAM_1445_CHECKPOINT_START -->
## Reconstruction checkpoint — Mathematics Ministry Exams 1445

- Source `0d4fa9fd-a93c-4d18-9dea-6dd22eb2e199` — `الرياضيات نماذج وزارية 1445` safely processed.
- Technical verification: **42/42** images; contiguous pages 1..42; duplicate SHA groups **0**.
- Verified models: **13** (pages 1..39); finalized exam pages: **39**; correction candidates: **13**; verified standalone Answer Keys: **0 / NOT VERIFIED**.
- Pages **40..42**: `review_required`; metadata repeats model 12 but binaries differ, and semantic identity versus pages 34..36 remains `NOT VERIFIED`; no merge/renumber performed.
- Questions: **28/28** structurally linked to verified model 1 from source page membership; semantic correctness `NOT VERIFIED`.
- Progress: Sources **21/58**; Educational **10/26**; Exam Groups **11/32**; Individual Exam Models **179**; Exam Pages **587/2,286**; source images technical **1584/5,273**.
- Global questions: Lesson-linked **6891**; Exam-linked **995**; Review-required **351**; Unclassified **17518**; invariant **PASS = 25,755**.
- RAW/unrelated/import/publication mutations: **0/0/0/0**.
- Next source: `85c13f3f-fe85-47c3-affb-fb437d10d908` — `الرياضيات نماذج وزارية 1446`.
<!-- MATH_EXAM_1445_CHECKPOINT_END -->

<!-- MATH_EXAM_1446_CHECKPOINT_START -->
## Reconstruction checkpoint — Mathematics Ministry Exams 1446

- Source `85c13f3f-fe85-47c3-affb-fb437d10d908` — `الرياضيات نماذج وزارية 1446` safely processed.
- Technical verification: **39/39** immutable images; duplicate SHA groups **0**.
- Source numbering anomalies preserved exactly: duplicate page numbers **16** and **29**; no normalization, renumbering, merge, or RAW mutation.
- Verified models: **13**; finalized exam pages: **39**; correction/result candidates: **13**; verified standalone Answer Keys: **0 / NOT VERIFIED**.
- Questions: **25/25** structurally linked to verified model 1 by unique legacy-page membership; semantic correctness `NOT VERIFIED`.
- Progress: Sources **22/58**; Educational **10/26**; Exam Groups **12/32**; Individual Exam Models **192**; Exam Pages **626/2,286**; source images technical **1623/5,273**.
- Global questions: Lesson-linked **6891**; Exam-linked **1020**; Review-required **351**; Unclassified **17493**; invariant **PASS = 25,755**.
- RAW/unrelated/import/publication mutations: **0/0/0/0**.
- Next source: `fef5e58f-21df-42e3-81ae-6966cd7bad10` — `الرياضيات نماذج وزارية 1447`.
<!-- MATH_EXAM_1446_CHECKPOINT_END -->

<!-- MATH_EXAM_1447_CHECKPOINT_START -->
## Reconstruction checkpoint — Mathematics Ministry Exams 1447

- Source `fef5e58f-21df-42e3-81ae-6966cd7bad10` — `الرياضيات نماذج وزارية 1447` safely processed.
- Technical verification: **42/42** immutable images; duplicate SHA groups **0**; page sequence **1..42** complete.
- Boundary evidence: explicit unique source-local titles prove **14** three-page model sequences (question sheet 1, question sheet 2, correction-sheet candidate).
- Visual contact sheets were generated in GitHub Actions run `34859563356`; semantic visual inspection remains **NOT VERIFIED** and was not claimed.
- Finalized exam pages: **42**; correction candidates: **14**; verified standalone Answer Keys: **0 / NOT VERIFIED**.
- Questions: **112/112** structurally linked by legacy-page membership; semantic correctness **NOT VERIFIED**.
- Progress: Sources **23/58**; Educational **10/26**; Exam Groups **13/32**; Individual Exam Models **206**; Exam Pages **668/2,286**; source images technical **1665/5,273**.
- Global questions: Lesson-linked **6891**; Exam-linked **1132**; Review-required **351**; Unclassified **17381**; invariant **PASS = 25,755**.
- RAW/unrelated/import/publication mutations: **0/0/0/0**.
- Next source: `1933807f-4cb0-40c9-9b29-3ef3d32c98dc` — `كتاب الرياضيات - الجزء الأول`.
<!-- MATH_EXAM_1447_CHECKPOINT_END -->

## Partial source-identity checkpoint — 2026-09-14T18:43:53+03:00

- Source: `1933807f-4cb0-40c9-9b29-3ef3d32c98dc — كتاب الرياضيات - الجزء الأول`
- 186/186 RAW images technically verified.
- Apparent Third Secondary master reference rejected: 0/186 exact SHA matches and expected page position unique-best in only 1/186 all-vs-all visual comparisons.
- 717 legacy question references are candidate evidence only: 60 pages covered, 126 uncovered, 3 pages with title conflicts, 45 distinct candidate titles.
- Source/book/unit/lesson/review identity and boundaries remain `NOT VERIFIED`; canonical reconstruction counters and the 25,755 classification invariant are unchanged.
- No RAW/unrelated/import/publication mutations.
- Next: independently identify/visually inspect this exact RAW edition before any structural promotion.

<!-- MATH_BOOK_PART1_CHECKPOINT_START -->
## Reconstruction checkpoint — Math Book Part 1

- Sources processed: **24/58**; Educational: **11/26**; Exam Source Groups: **13/32**.
- Books / Units / Lessons / Lesson pages: **11 / 37 / 217 / 1,039**.
- Math Part 1: **186/186** RAW images technically verified; complete direct RAW visual review establishes **4 units / 21 lessons / 162 lesson pages / 24 non-lesson pages**.
- The apparent master reference `الرياضيات ثالث ثانوي/02_الرياضيات_ثالث_ثانوي` remains explicitly rejected (0/186 SHA identity; no structure transferred).
- Non-lesson pages: **2 review + 18 general exercise + 4 unit-test pages**.
- Questions: **620 lesson-linked + 97 review_required = 717**, semantic correctness `NOT VERIFIED`.
- Global invariant: **7,511 + 1,132 + 448 + 16,664 = 25,755**.
- Source images technical **1,851/5,273**. RAW/unrelated/import/publication mutations **0/0/0/0**.
- Next: `b80cbba1-410a-4346-9446-c3f01c4f9e56 — كتاب الرياضيات - الجزء الثاني`.
<!-- MATH_BOOK_PART1_CHECKPOINT_END -->

<!-- MATH_BOOK_PART2_CHECKPOINT_START -->
## Reconstruction checkpoint — Math Book Part 2

- Sources processed: **25/58**; Educational: **12/26**; Exam Source Groups: **13/32**.
- Books / Units / Lessons / Lesson pages: **12 / 40 / 236 / 1,161**.
- Math Part 2: **135/135** RAW images technically verified; complete visual review establishes **3 units / 19 lessons / 122 lesson pages / 13 non-lesson pages**.
- Verified unit banners: **الوحدة الخامسة — الهندسة**; **الوحدة السادسة — الهندسة الإحداثية والتحويلات**; **الوحدة السابعة — الإحصاء**.
- Non-lesson pages: **7 general-exercise + 6 unit-test pages**.
- Questions: this source contains **0 legacy questions**; no question mappings invented.
- Global invariant: **7,511 + 1,132 + 448 + 16,664 = 25,755**.
- Source images technical **1,986/5,273**. RAW/unrelated/import/publication mutations **0/0/0/0**.
- Next: `b6ce737e-26d4-4219-a607-27bfb7d2f518 — كتاب الإسلامية - الجزء الأول`.
<!-- MATH_BOOK_PART2_CHECKPOINT_END -->

<!-- WORKER_B_EMPTY_ISLAMIC_PART1_BLOCKER_START -->
## Worker B — Islamic Part 1 empty-source fail-closed checkpoint

- source: `b6ce737e-26d4-4219-a607-27bfb7d2f518 — كتاب الإسلامية - الجزء الأول`
- evidence HEAD: `8e2d8e3cc922e2455b85559c60578cc40c048301`
- retained manifest: `status=empty`; pages/images/questions/download failures = `0/0/0/0`; all anomaly arrays empty.
- `pages.json`: verified exact empty array.
- `subject.json`: source/class identity matches the manifest.
- technical image verification: `NOT APPLICABLE` because there are zero image references.
- Book / Units / Lessons / page boundaries: `NOT VERIFIED`; the legacy label alone is not semantic reconstruction evidence.
- MASTER schema review: no established canonical verified-empty disposition exists in `review_status`, `classification`, `technical_verification.status`, `reconstruction.status`, or `exam_reconstruction.status`.
- decision: `FAIL_CLOSED_KEEP_ACTIVE`; MASTER canonical classification/counters intentionally unchanged.
- evidence: `content-staging/reconstruction/educational/b6ce737e-26d4-4219-a607-27bfb7d2f518-empty-source-analysis.json`.
- canonical progress remains: Sources `25/58`; Educational `12/26`; Books/Units/Lessons/Lesson Pages `12/40/236/1,161`; Exam Groups `13/32`; Models `206`; Exam Pages `668/2,286`; Source images technical `1,986/5,273`.
- questions invariant remains: `7,511 + 1,132 + 448 + 16,664 = 25,755`.
- RAW/unrelated/import/publication mutations: `0/0/0/0`.
- exact next operation: define or discover a repository-approved empty-source disposition contract; only then apply it to this source and decide whether it counts as explicitly unresolved/processed. Do not advance to a following source before that disposition is recorded.
<!-- WORKER_B_EMPTY_ISLAMIC_PART1_BLOCKER_END -->

## Verified-empty retained-source disposition — 2026-09-14 Worker A

- Canonical policy: `content-staging/reconstruction/VERIFIED_EMPTY_SOURCE_DISPOSITION_POLICY.json`.
- Finalized as processed source occurrences without inventing semantic educational structure:
  - `b6ce737e-26d4-4219-a607-27bfb7d2f518 — كتاب الإسلامية - الجزء الأول`
  - `e36ec148-0913-4bcc-a35c-268d464fecab — كتاب الإسلامية - الجزء الثاني`
- Both have manifest `status=empty`, `pages.json=[]`, 0 pages/images/questions/failures, empty anomaly arrays, and matching subject identity.
- Counter rule: each increments Sources processed + Educational processed only; Books/Units/Lessons/Lesson Pages/images/questions remain unchanged.
- Book/Unit/Lesson/page semantics remain `NOT VERIFIED`; technical image verification is `NOT APPLICABLE`.
- No RAW/import/publication mutation.
- Next source from live MASTER order: `67d4ffae-68e1-42e8-9c3b-72329973c93d — الأحياء الكتاب المدرسي`.

<!-- BIOLOGY_BOOK_CHECKPOINT_START -->
## Reconstruction checkpoint — Biology textbook

- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Sources processed: **28/58**; Educational: **15/26**; Exam Source Groups: **13/32**.
- Books / Units / Lessons / Lesson pages: **13 / 48 / 283 / 1354**.
- Biology: **214/214** technically verified and **214/214** exact RAW/master SHA identities in `الأحياء ثالث ثانوي/الاحياء الكتاب المدرسي/الصور`; retained pages **8..221**.
- Reconstructed source: **1 Book, 8 Units, 47 Lessons, 193 Lesson pages, 8 Unit-cover pages, 13 Unit-review pages**.
- Questions: **3003** structurally lesson-linked; **301** `review_required` on non-lesson unit cover/review pages; semantic correctness `NOT VERIFIED`.
- Global questions: Lesson-linked **10514**; Exam-linked **1132**; Review-required **749**; Unclassified **13360** = **25,755**.
- Individual Exam Models **206**; Exam Pages **668/2286**; Verified Answer Keys **0**.
- Source images technical **2200/5273**; Duplicate groups **0/99**.
- RAW / unrelated / imports / publications: **0/0/0/0**.
- Last completed: `67d4ffae-68e1-42e8-9c3b-72329973c93d — الأحياء الكتاب المدرسي`.
- Next candidate: `3d91d812-ab78-476a-b2fc-dc2c31152e1a — UNKNOWN`; must be re-read from live manifest/baton before work.
<!-- BIOLOGY_BOOK_CHECKPOINT_END -->

<!-- BIOLOGY_EXAM_1445_CHECKPOINT_START -->
## Reconstruction checkpoint — Biology Ministry Exams 1445

- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Source `3d91d812-ab78-476a-b2fc-dc2c31152e1a` — `الاحياء نماذج وزارية 1445` completed from source-local evidence.
- Technical verification: **60/60** images exist, readable, byte-size/SHA-256/MIME match; sequence **1..60** contiguous; duplicate SHA groups **0**.
- Reference identity: **60/60** RAW binaries match the page-aligned repository reference directory for Biology 1445.
- Full visual review resolves **20** verified Individual Exam Model occurrences; each is two question pages + one correction/result sheet candidate.
- Finalized Exam Pages: **60**; review-required pages: **0**; correction-sheet candidates: **20**; verified standalone Answer Keys: **0 / NOT VERIFIED**.
- Source legacy questions: **0**; no question mapping was invented.
- Progress: Sources **29/58**; Educational **15/26**; Exam Groups **14/32**; Individual Exam Models **226**; Exam Pages **728/2,286**; source images technical **2260/5,273**.
- Global questions: Lesson-linked **10514**; Exam-linked **1132**; Review-required **749**; Unclassified **13360**; invariant **PASS = 25,755**.
- RAW/unrelated/import/publication mutations: **0/0/0/0**.
- Next source: `62d827b3-8ab6-4c2b-8ff2-de6156947276` — `الاحياء نماذج وزارية 1446`.
<!-- BIOLOGY_EXAM_1445_CHECKPOINT_END -->

<!-- BIOLOGY_EXAM_1446_CHECKPOINT_START -->
## Reconstruction checkpoint — Biology Ministry Exams 1446

- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Source `62d827b3-8ab6-4c2b-8ff2-de6156947276` — `الاحياء نماذج وزارية 1446` completed from source-local evidence.
- Technical verification: **100/100** images exist, readable, byte-size/SHA-256/MIME match; sequence **1..100** contiguous.
- Duplicate evidence: **6** SHA-256 duplicate groups (each two source occurrences) preserved exactly; no merge, renumber, deletion, or RAW mutation.
- Full visual review resolves **25** verified Individual Exam Model occurrences; each is three question pages + one correction/result sheet candidate.
- Finalized Exam Pages: **100**; review-required pages: **0**; correction-sheet candidates: **25**; verified standalone Answer Keys: **0 / NOT VERIFIED**.
- Source legacy questions: **200/200** structurally linked by verified page membership; semantic correctness remains **NOT VERIFIED**.
- Progress: Sources **30/58**; Educational **15/26**; Exam Groups **15/32**; Individual Exam Models **251**; Exam Pages **828/2,286**; source images technical **2360/5,273**.
- Global questions: Lesson-linked **10514**; Exam-linked **1332**; Review-required **749**; Unclassified **13160**; invariant **PASS = 25,755**.
- RAW/unrelated/import/publication mutations: **0/0/0/0**.
- Next source: `3df6f57e-26cb-414e-97c5-ef6bd2ff4487` — `الاحياء نماذج وزارية 1447`.
<!-- BIOLOGY_EXAM_1446_CHECKPOINT_END -->

<!-- BIOLOGY_EXAM_1447_CHECKPOINT_START -->
## Reconstruction checkpoint — Biology Ministry Exams 1447

- Source `3df6f57e-26cb-414e-97c5-ef6bd2ff4487` completed from source-local evidence.
- Technical verification: **124/124**; contiguous pages **1..124**; **9** within-source SHA duplicate groups preserved.
- Visual review: **31** four-page blocks reviewed; **29** verified occurrences; **2** mismatched question/correction blocks isolated as `review_required`; **28** unique Individual Exam Models.
- Finalized Exam Pages: **116**; review-required pages: **8**; correction candidates: **29**; verified standalone Answer Keys: **0 / NOT VERIFIED**.
- Legacy questions: **50** exam-linked structurally; **0** review-required; semantic correctness `NOT VERIFIED`.
- Global progress: Sources **31/58**; Exam Groups **16/32**; Individual Models **279**; Exam Pages **944/2,286**; source images **2484/5,273**.
- Question invariant: PASS = 25,755. RAW/unrelated/import/publication mutations: **0/0/0/0**.
- Next source: `4863bbf6-6cf3-4238-9407-75825724292a` — `الفيزياء الكتاب المدرسي`.
<!-- BIOLOGY_EXAM_1447_CHECKPOINT_END -->

<!-- PHYSICS_BOOK_CHECKPOINT_START -->
## Reconstruction checkpoint — Physics textbook

- Sources processed: **32/58**; Educational: **16/26**; Exam groups: **16/32**.
- Books / Units / Lessons / Lesson pages: **14 / 57 / 328 / 1527**.
- Physics: **207/207** technical + exact SHA identity; pages **9..215**; **9 Units / 45 Lessons / 173 Lesson pages / 9 covers / 25 reviews**.
- Questions: **2621 lesson-linked; 480 review_required; semantic correctness NOT VERIFIED**.
- Global questions: **13135 + 1382 + 1229 + 10009 = 25,755**.
- Technical images: **2691/5273**. RAW/unrelated/import/publication mutations **0/0/0/0**.
- Last completed: `4863bbf6-6cf3-4238-9407-75825724292a — الفيزياء الكتاب المدرسي`. Next: `41e5a81c-3b93-479c-9b76-33815cae9430 — الفيزياء نماذج وزاريه 1445`.
<!-- PHYSICS_BOOK_CHECKPOINT_END -->

<!-- PHYSICS_EXAM_1445_CHECKPOINT_START -->
## Reconstruction checkpoint — Physics Ministry Exams 1445

- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Source `41e5a81c-3b93-479c-9b76-33815cae9430` — `الفيزياء نماذج وزاريه 1445` completed from source-local evidence.
- Technical verification: **60/60** images exist/readable and byte-size/SHA-256/MIME match the immutable manifest; sequence **1..60** contiguous; duplicate SHA groups **0**.
- Full visual review resolves **20** verified source occurrences; each has two question pages followed by one correction/result-sheet candidate; all **60** source pages are finalized exactly once.
- Correction/result candidates: **20**; verified standalone official Answer Keys: **0 / NOT VERIFIED**.
- Source questions: **83/83 structurally exam-linked** by verified page membership; semantic question/answer correctness remains `NOT VERIFIED`.
- Progress: Sources **33/58**; Educational **16/26**; Exam Groups **17/32**; Individual Exam Models **299**; Exam Pages **1004/2,286**; source images technical **2751/5,273**.
- Global questions: Lesson-linked **13135**; Exam-linked **1465**; Review-required **1229**; Unclassified **9926**; invariant **PASS = 25,755**.
- RAW/unrelated/import/publication mutations: **0/0/0/0**.
- Next source: `0b28dc73-7e43-45f1-99c8-14825dcf3ded` — `الفيزياء نماذج وزاريه 1446`.
<!-- PHYSICS_EXAM_1445_CHECKPOINT_END -->

<!-- PHYSICS_EXAM_1446_CHECKPOINT_START -->
## Reconstruction checkpoint — Physics Ministry Exams 1446

- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Source `0b28dc73-7e43-45f1-99c8-14825dcf3ded` — `الفيزياء نماذج وزاريه 1446` completed from source-local evidence.
- Technical verification: **104/104** images verified; sequence **1..104** contiguous; duplicate SHA groups **6**, preserved without merge or RAW mutation.
- Full visual review resolves **26** verified source occurrences; each has three question pages followed by one correction/result-sheet candidate; all **104** source pages finalized exactly once.
- Partial-page SHA duplication does not collapse occurrences because paired fourth-page correction/result sheets differ; official model codes remain `NOT VERIFIED`.
- Correction/result candidates: **26**; verified standalone official Answer Keys: **0 / NOT VERIFIED**.
- Source questions: **200/200 structurally exam-linked** by verified page membership; semantic correctness remains `NOT VERIFIED`.
- Progress: Sources **34/58**; Educational **16/26**; Exam Groups **18/32**; Individual Exam Models **325**; Exam Pages **1108/2,286**; source images technical **2855/5,273**.
- Global questions: Lesson-linked **13135**; Exam-linked **1665**; Review-required **1229**; Unclassified **9726**; invariant **PASS = 25,755**.
- RAW/unrelated/import/publication mutations: **0/0/0/0**.
- Next source: `bbc5c2e7-9b96-4502-a8b0-6a14d2f8782a` — `الفيزياء نماذج وزاريه 1447`.
<!-- PHYSICS_EXAM_1446_CHECKPOINT_END -->

<!-- PHYSICS_EXAM_1447_CHECKPOINT_START -->
## Reconstruction checkpoint — Physics Ministry Exams 1447

- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Source `bbc5c2e7-9b96-4502-a8b0-6a14d2f8782a` — `الفيزياء نماذج وزاريه 1447` completed from source-local evidence.
- Technical verification: **124/124** images verified; sequence **1..124** contiguous; duplicate SHA groups **9**, preserved without merge or RAW mutation.
- Full visual review resolves **31** verified source occurrences; each has three question pages followed by one correction/result-sheet candidate; all **124** source pages finalized exactly once.
- The 9 duplicate SHA groups form three repeated question-sheet triplets. Their source occurrences are retained separately; partial-page duplication alone is not evidence for collapsing a complete occurrence.
- Correction/result candidates: **31**; verified standalone official Answer Keys: **0 / NOT VERIFIED**.
- Source questions: **255/255 structurally exam-linked** by verified page membership; semantic correctness remains `NOT VERIFIED`.
- Progress: Sources **35/58**; Educational **16/26**; Exam Groups **19/32**; Individual Exam Models **356**; Exam Pages **1232/2,286**; source images technical **2979/5,273**.
- Global questions: Lesson-linked **13135**; Exam-linked **1920**; Review-required **1229**; Unclassified **9471**; invariant **PASS = 25,755**.
- RAW/unrelated/import/publication mutations: **0/0/0/0**.
- Next source: `d1a6b8f8-d81b-4824-86e1-d370ec28bdf1` — `العربي نماذج وزارية 1447`.
<!-- PHYSICS_EXAM_1447_CHECKPOINT_END -->


## RUN 2026-09-15T00:06:20+00:00 — Worker A

- state: `COMPLETE_METADATA_BOUNDARY_VERIFIED_VISUAL_SEMANTICS_NOT_VERIFIED`
- start HEAD: `6e9d8e191a432d50f3fedd5cdd6eca57fd5e25d6`
- end HEAD (canonical evidence): `912cf61044d5295954dd702cefc760a7d487467a`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source: `d1a6b8f8-d81b-4824-86e1-d370ec28bdf1 — العربي نماذج وزارية 1447`
- completed: verified **42/42** immutable RAW images (byte-size/SHA-256/MIME), sequence **1..42**, **0** RAW mutations; proved **14** source-local model boundaries from complete exact 42-page titles; finalized **14 models / 42 exam pages / 14 correction candidates**; standalone official Answer Keys and visual semantic page review remain `NOT VERIFIED`; source has **0 legacy questions**, so no mappings were invented.
- artifacts/evidence: `content-staging/reconstruction/technical/d1a6b8f8-d81b-4824-86e1-d370ec28bdf1.json`; `content-staging/reconstruction/exams/source-groups/d1a6b8f8-d81b-4824-86e1-d370ec28bdf1.json`; canonical evidence commit `912cf61044d5295954dd702cefc760a7d487467a`.
- invariant: PASS (`13,135 + 1,920 + 1,229 + 9,471 = 25,755`).
- progress: Sources `36/58`; Educational `16/26`; Books/Units/Lessons/Lesson Pages `14/57/328/1,527`; Exam Groups `20/32`; Models `370`; Exam Pages `1,274/2,286`; Answer Keys `0`; technical images `3,021/5,273`; Legacy Questions `25,755`; Lesson-linked `13,135`; Exam-linked `1,920`; Review-required `1,229`; Unclassified `9,471`.
- invariants/mutations: RAW `0`; unrelated `0`; new imports `0`; new publications `0`.
- last completed source: `d1a6b8f8-d81b-4824-86e1-d370ec28bdf1 — العربي نماذج وزارية 1447`
- current source: `ab701a9e-3efb-409a-8ed1-9752d41c4771 — كتاب العربي - الجزء الأول`
- current source baseline: `169 pages; 169 images; 0 legacy questions; 0 download failures`
- exact next operation: `Re-fetch live HEAD/baton; verify no active workflow for the current source; reconstruct only from that source's own RAW/manifest/page evidence; preserve uncertainty as NOT VERIFIED/review_required; assert invariant; checkpoint.`
- blockers: `none for structural boundary finalization; visual semantic inspection of Arabic 1447 remains explicitly NOT VERIFIED and was not used to justify Answer Keys.`
- handoff for Worker B: `Start only from ab701a9e-3efb-409a-8ed1-9752d41c4771 — كتاب العربي - الجزء الأول; do not rerun/finalize Arabic 1447 absent fresh drift evidence.`


## RECONCILIATION 2026-09-15T00:08:05+00:00 — Worker A

- reason: canonical source reconstruction for `d1a6b8f8-d81b-4824-86e1-d370ec28bdf1` was committed correctly, but `MASTER_CONTENT_MANIFEST.json.reconstruction_progress` still held pre-source aggregate counters.
- action: reconciled aggregate counters to the evidence-backed source state; no RAW/provenance/import/publication mutations.
- canonical progress: Sources `36/58`; Educational `16/26`; Books/Units/Lessons/Lesson Pages `14/57/328/1,527`; Exam Groups `20/32`; Models `370`; Exam Pages `1,274/2,286`; correction candidates `376`; Answer Keys `0`; technical images `3,021/5,273`; Legacy Questions `25,755`; Lesson-linked `13,135`; Exam-linked `1,920`; Review-required `1,229`; Unclassified `9,471`.
- invariant: PASS (`13,135 + 1,920 + 1,229 + 9,471 = 25,755`).
- mutations: RAW `0`; unrelated `0`; new imports `0`; new publications `0`.

## ACTIVE CHECKPOINT

- last completed source: `d1a6b8f8-d81b-4824-86e1-d370ec28bdf1 — العربي نماذج وزارية 1447`
- current source: `ab701a9e-3efb-409a-8ed1-9752d41c4771 — كتاب العربي - الجزء الأول`
- baseline: `169 pages; 169 images; 0 legacy questions; 0 download failures`
- exact next operation: `Re-fetch live HEAD/baton; verify no active workflow for ab701a9e-3efb-409a-8ed1-9752d41c4771; technically verify all 169 immutable RAW images; reconstruct book/unit/lesson/review boundaries only from source-local evidence; do not infer missing questions; preserve insufficient evidence as NOT VERIFIED/review_required; assert invariant; checkpoint.`
- handoff for Worker B: `Start only from ab701a9e-3efb-409a-8ed1-9752d41c4771; Arabic exam 1447 is structurally finalized from complete metadata-title evidence, while visual semantic inspection and standalone official Answer Keys remain NOT VERIFIED.`
