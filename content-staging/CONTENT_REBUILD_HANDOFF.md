# الوسيلة الذكية — Content Rebuild Handoff

## 2026-09-14 — Corpus-wide metadata inventory checkpoint

Current owner instruction supersedes the earlier Grade 9-only continuation: inventory and reconstruct all available sources and independent exam models; no new publication.

Working branch: `content/corpus-inventory-20260914`, based on `041cb0738f3a76600eebde29dfb0181ef7e76255`.
Read `CONTENT_INVENTORY.md`, `CONTENT_VALIDATION_REPORT.md`, `CONTENT_IMPORT_REPORT.md` and `manifests/MASTER_CONTENT_MANIFEST.json`.
58 legacy manifests read; 5273 image references matched Git paths and sizes; 25755 questions recorded. 32 candidate exam collections cover 2286 pages and 2715 legacy questions. Collection count is NOT individual Exam Model count. 99 recorded checksum duplicate groups retained.
New imports/publications: 0. Current PostgreSQL state and binary SHA-256 recalculation: NOT VERIFIED. No import-ready batch exists yet.
Next: verify source bytes, inspect actual exam boundaries and answer-key evidence, reconcile master against RAW, inspect modern schema/runtime, then run guarded import gates. Direct GitHub access from the execution environment timed out; connector text reads succeeded.
Preserve previously authorized Grade 9 publication; do not rerun prior import or publisher.


> نقطة الاستئناف الرسمية لمسار المحتوى. اقرأ live heads ثم `CONTENT_REBUILD_EXECUTION_STATUS.md` أولًا.

Last synchronized: **2026-09-14 — full Grade 9 English technical import complete; only reviewed Unit 2 pages 5..10 published**.

## العقود الثابتة

- Working repository: `7eaur/alwaslh-go`
- Working branch: `content/legacy-staging-rebuild`
- RAW immutable؛ لا overwrite/recompress in-place.
- provenance وSHA-256 محفوظان.
- `media ready != published`.
- لا auto-publish لأي AI/legacy output غير مراجع.
- لا تستخدم `69 -> 62` كحقيقة منهجية.
- لا تحذف anomalies أو بيانات غير مرتبطة لتجميل الأرقام.
- أي DB apply يفشل مغلقًا عند identity/count/provenance/publication drift.

## Current Grade 9 English truth

`FULL-GRADE9-ENGLISH-BULK-IMPORT = DONE / FULL_ASSET_COVERAGE_VERIFIED`

Full imported scope:

- 69 RAW-backed pages
- 69 RAW images
- 104 Question Revisions
- 8 recovered Units/Sections
- page 70 remains manifest-only/evidence-only because no RAW identity exists

Units:

1. `Unit 1 - Revision`
2. `Unit 2 - Describing: Making plans`
3. `Unit 3 - Other countries`
4. `Unit 4 - Visiting Japan`
5. `Unit 5 - Safety`
6. `Unit 6 - Helping others`
7. `Unit 7 - Communications`
8. `Unit 8 - Winning medals`

Source authority:

- legacy subject: `1794eea5-4772-4c94-bd2b-b08e5815e733`
- immutable reconstruction manifest: `content-staging/curated/grade-9/english/pupil-book-3/reconstruction-candidates.json`
- source extraction: `content/legacy-supabase-reconstruction`
- exact original Grade 9 reference on `master`: `تاسع انجليزي/الانجليزي_تاسع`
- `master` contains other corpora too; never use an adjacent corpus as Grade 9 evidence.

Bulk import runtime evidence remains:

- source commit `9e58ab3e882b883bddd016099949881801eedc28`
- Railway deployment `de7f9883-b2f0-483d-a7c1-ffbfb15ac30c`
- `BULK_G9_EN_INSPECT_PASS`
- `BULK_G9_EN_TRANSACTION_GATE_PASS`
- `BULK_G9_EN_APPLY_PASS`
- `BULK_G9_EN_VERIFY_PASS`
- `BULK_G9_EN_RUNNER_PASS`

Do not rerun that import.

## Reviewed and now published slice

User explicitly authorized publishing the Lessons/questions that had completed review.

### CURATION-001

Pages `5..8`:

- Lesson: `curated-english9-pb3-u2-describing-people-and-animals`
- title: `Describing people and animals`
- 4 published Lesson Assets
- 12 published reviewed Question Revisions

### CURATION-002

Pages `9..10`:

- Lesson: `curated-english9-pb3-u2-time-and-meeting`
- title: `Telling time and arranging a meeting`
- 2 published Lesson Assets
- 7 published reviewed Question Revisions

Question review total: `19`.

- `18` approved unchanged
- `1` corrected before publication

Corrected page-10 item:

- reviewed prompt: `When is Fuad helping Dad on Saturday?`
- answer: `at six o'clock`
- reviewed explanation: `Fuad says he is helping Dad at six o'clock.`

## Publication runtime evidence

Publisher commit:

`ea5a19b7086eb8779701be2b1f47fc073b38aa12`

Reviewed correction/final execution head:

`7d17e19bef37835d500de492053e728f0cdb9f1b`

Railway deployment:

`5024b218-32e0-49fe-b9f8-20ee82c5bcd0` — `SUCCESS`

Verified final markers:

- `G9_U2_PUBLISH_APPLY_PASS`
- `G9_U2_PUBLISH_FULL_PASS`
- `COMMITTED_STATE_VERIFIED_AND_PUBLISHED`

Post-verify result:

- published Grade 9 English Lessons: `2`
- published Grade 9 English Lesson Assets: `6`
- published Grade 9 English Question Revisions: `19`
- Reader-eligible target assets: `6`
- Quiz-Builder-eligible reviewed questions: `19`
- question links: `12 + 7` to the two modern Lessons

Because the total Grade 9 English published counts after the gate are exactly `2 / 6 / 19`, all other imported Grade 9 English content remains Draft/unpublished.

Student delivery note:

- the two Lessons are now student Reader eligible under normal entitlement/auth rules;
- the 19 Question Revisions are published to Question Bank and available for Quiz Builder;
- no standalone Quiz/version is claimed to have been built or published by this gate.

Detailed report:

`content-staging/GRADE9_UNIT2_REVIEWED_PUBLICATION_REPORT.md`

## Isolation retained

- RAW mutations: `0`
- media-binary mutations: `0`
- unrelated publication: `0`
- page 70 fabrication: `0`
- prohibited `69 -> 62` heuristic: not used
- source/provenance identities retained

The Railway content service was returned to an idle start command after publication verification; documentation commits must not replay the publisher.

## Previous checkpoints retained

- `BATCH-001 = DONE / COMMITTED_STATE_VERIFIED`
- `STRUCTURE-001 = DONE / SECTION_BOUNDARY_VERIFIED`
- `STRUCTURE-002 = DONE / SECTION_BOUNDARY_VERIFIED`
- `CURATION-001 = DONE / COMMITTED_STATE_VERIFIED / PUBLISHED`
- `CURATION-002 = DONE / COMMITTED_STATE_VERIFIED / PUBLISHED`
- `CONTENT-GAPS-001 = DONE / GAP_INVENTORY_VERIFIED`
- `MEDIA-001 = DONE / MEDIA_PROFILE_VERIFIED_PARTIAL_ACCEPTANCE`
- `IMPORT-001 = DONE / COMMITTED_STATE_VERIFIED`
- `VERIFY-001 = DONE / DELIVERY_ISOLATION_AND_PROVENANCE_VERIFIED`
- `ROADMAP-RETURN = DONE / STUDENT-016I_HANDOFF_VERIFIED`
- `FULL-GRADE9-ENGLISH-BULK-IMPORT = DONE / FULL_ASSET_COVERAGE_VERIFIED`
- `REVIEWED-UNIT2-PUBLICATION = DONE / COMMITTED_STATE_VERIFIED_AND_PUBLISHED`

## Exact resume rule

Do not rerun the bulk import, CURATION-001/002 structural apply, or the reviewed Unit 2 publication gate unless fresh runtime evidence shows drift.

Continue only from the first unresolved pedagogical boundary in the still-unpublished Grade 9 English corpus. Future Lessons/questions must complete review before any explicit publication gate.

Never delete provenance, fabricate page 70, mutate RAW, hide anomalies, or auto-publish unreviewed AI/legacy content.

<!-- CHEMISTRY_RECONSTRUCTION_CHECKPOINT_START -->
## Active reconstruction handoff — Chemistry complete

- Repository: `7eaur/alwaslh-go`
- Branch: `content/corpus-inventory-20260914`
- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Last completed source: `f0c5228c-7d5b-4ec2-85ed-ce59139ce0a4` — Third Secondary Chemistry textbook.
- Completed source result: **178 technically verified pages; 1 Book; 9 Units; 57 Lessons; 149 Lesson pages; 14 review pages; 5 glossary pages**.
- Evidence: exact RAW/master SHA identity for pages 11..188 plus trusted TOC and selective visual boundary inspection.
- Questions: 2,225 structurally lesson-linked; 351 `review_required`; semantic correctness `NOT VERIFIED`.
- Exam Source Groups completed: **0/32**.
- Current/next source: `e101d097-7a14-44e5-b242-cdeb9a312b77` — `الكيمياء نماذج وزاريه 1445`.
- Exact next operation: technical scan the 60-page exam source group, detect Individual Exam Model boundaries, selectively inspect starts/ends/answer-key candidates, then map pages/questions without treating the 60-page group as one exam.
- Unresolved corpus-wide: remaining 25 educational candidates; all 32 Exam Source Groups; Individual Exam Models; Answer Keys; remaining technical image scan; WebP derivative decisions; 99 duplicate fingerprint groups; remaining question classifications.
- RAW mutations / unrelated mutations / imports / publications remain **0 / 0 / 0 / 0**.
<!-- CHEMISTRY_RECONSTRUCTION_CHECKPOINT_END -->

<!-- CHEMISTRY_EXAM_1445_CHECKPOINT_START -->
## Active reconstruction handoff — Chemistry Exams 1445 complete

- Repository: `7eaur/alwaslh-go`
- Branch: `content/corpus-inventory-20260914`
- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Last completed source: `e101d097-7a14-44e5-b242-cdeb9a312b77` — Chemistry Ministry Exams 1445.
- Result: **60 technically verified pages; 20 Individual Exam Models; 3 pages/model; 20 correction-sheet candidates; 0 verified Answer Keys**.
- Full source-group visual review completed; model boundaries are verified. Official model codes/titles/term and official Answer Key status remain `NOT VERIFIED` where evidence is insufficient.
- Completed corpus so far: **2/58 sources**, including **1/26 educational sources** and **1/32 Exam Source Groups**.
- Current/next source: `c09ce569-ea42-4f0b-997f-95b029a7e6ea` — `الكيمياء نماذج وزاريه 1446`.
- Exact next operation: technical scan all 60 pages, detect storage/metadata candidates, export full visual contact sheets, resolve Individual Exam Model boundaries and correction/answer-key relations, then checkpoint and continue.
- RAW mutations / unrelated mutations / imports / publications: **0 / 0 / 0 / 0**.
<!-- CHEMISTRY_EXAM_1445_CHECKPOINT_END -->

<!-- CHEMISTRY_EXAM_1446_CHECKPOINT_START -->
## Active reconstruction handoff — Chemistry Exams 1446 complete

- Repository/branch: `7eaur/alwaslh-go@content/corpus-inventory-20260914`.
- Last completed: `c09ce569-ea42-4f0b-997f-95b029a7e6ea` — Chemistry Ministry Exams 1446.
- Result: **60 technically verified/classified pages; 15 source occurrences; 14 unique Individual Exam Models; 15 correction-report candidates; 0 verified standalone Answer Keys**.
- `P.41` repeats at 29..32 and 41..44; question pages are exact SHA duplicates, correction reports are distinct candidate records. Classification `legitimate_repeated_exam_model_occurrence`; all pages preserved.
- Progress: Sources **3/58**; Educational **1/26**; Exam Groups **2/32**; Individual Exam Models **34**; Exam Pages **120/2,286**; images verified **298/5,273**.
- Next: `e7c8291c-e904-4e8c-9cd8-2753818cedf3` — Chemistry 1447. Verify locally from its own evidence; do not assume prior-year page patterns.
- RAW/unrelated/import/publication mutations: **0/0/0/0**.
<!-- CHEMISTRY_EXAM_1446_CHECKPOINT_END -->

<!-- CHEMISTRY_EXAM_1447_CHECKPOINT_START -->
## Active reconstruction handoff — Chemistry Exams 1447 complete

- Repository/branch: `7eaur/alwaslh-go@content/corpus-inventory-20260914`.
- Last completed: `e7c8291c-e904-4e8c-9cd8-2753818cedf3` — Chemistry Ministry Exams 1447.
- Result: **124/124** technically verified and visually reviewed pages; **29** verified occurrences; **28** unique models; **116** finalized model pages; **8** pages isolated as review-required; **31** correction-report candidates; **0** verified standalone Answer Keys.
- Review-required blocks: `37..40` (`P.61` questions / `P.31` correction) and `45..48` (`P.28` questions / `P.88` correction). Keep all provenance; do not fabricate or silently repair.
- Questions: **226** exam-linked + **0** review-required = **226/226** source questions accounted for.
- Progress: Sources **4/58**; Educational **1/26**; Exam Groups **3/32**; Individual Exam Models **62**; Exam Pages **236/2,286**; images verified **422/5,273**.
- Next: `ef408805-c337-44dd-b903-7838030e6de0` — `العلوم نماذج وزارية 1445`. Start from its own technical/visual evidence; do not reuse chemistry-year boundary assumptions.
- RAW/unrelated/import/publication mutations: **0/0/0/0**.
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
## Active reconstruction handoff — Science Part 1 complete

- Last completed: `f4b6708c-027f-4883-9e85-e6e7acb52ecc — كتاب العلوم - الجزء الأول`.
- Verified: **161/161** technical + exact master SHA identity; **8 Units / 22 Lessons / 138 Lesson pages / 8 covers / 15 reviews**.
- Questions: **11 lesson-linked; 0 source review-required; semantic correctness NOT VERIFIED**.
- Current/next: `81e99fe6-1421-462b-9562-1c0c5053a809 — كتاب العلوم - الجزء الثاني` (145 images/pages; 0 questions in current manifest).
- Exact next operation: technically verify all 145 images; establish exact identity against `master/تاسع علوم/علوم_تاسع_الجزء_الثاني`; reconstruct its own units/lessons/reviews; assert invariant; checkpoint.
- RAW/unrelated/import/publication mutations remain **0/0/0/0**.
<!-- SCIENCE_BOOK_PART1_CHECKPOINT_END -->

<!-- SCIENCE_BOOK_PART2_CHECKPOINT_START -->
## Active reconstruction handoff — Science Part 2 complete

- Last completed: `81e99fe6-1421-462b-9562-1c0c5053a809 — كتاب العلوم - الجزء الثاني`.
- Verified: **145/145** technical + exact master SHA identity; **8 Units / 31 Lessons / 126 Lesson pages / 8 covers / 11 reviews**.
- Questions: source contains **0 legacy questions**; no fabricated links; semantic question review `NOT APPLICABLE`.
- Current/next: `8489a487-91d9-47fb-80b8-35d0e7a074a4 — الانجليزي نماذج وزارية 1445`.
- Exact next operation: read the English 1445 live manifest/pages; verify all images; scan duplicates/sequence; derive exam model/correction boundaries only from that source's evidence; map questions; assert invariant; checkpoint.
- RAW/unrelated/import/publication mutations remain **0/0/0/0**.
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
## Active reconstruction handoff — History source-local reconstruction complete

- Last completed: `0a76f44b-0a4f-4e36-9ea9-badecf78bf23 — التاريخ الكتاب المدرسي`.
- Verified: **61/61** technical + complete source-local visual review; **1 explicit semester section / 9 lessons / 47 lesson-content pages / 12 lesson-review pages**.
- Master equivalence remains `NOT VERIFIED`; no master title/boundary was copied.
- Questions: **138/138 structurally lesson-linked; semantic correctness NOT VERIFIED; 0 source review-required**.
- Current/next: `7f02b242-5164-46d1-a82d-7f1023cfa8c9 — التربية الوطنية`.
- Exact next operation: fetch the live National Education manifest/pages; technical verification first; establish source identity only from its own evidence; reconstruct explicit book/section/unit/lesson/review boundaries without inheriting History patterns; map questions only where page membership is proven; assert global invariant; checkpoint.
- RAW/unrelated/import/publication mutations remain **0/0/0/0**.
<!-- HISTORY_SOURCE_LOCAL_CHECKPOINT_END -->

<!-- CIVICS_BOOK_CHECKPOINT_START -->
## Active reconstruction handoff — Civics complete

- Last completed: `7f02b242-5164-46d1-a82d-7f1023cfa8c9 — التربية الوطنية`.
- Verified: **59/59** technical + unique exact master SHA identity; **4 Units / 14 Lessons / 48 Lesson pages / 4 covers / 7 reviews / 0 non-lesson pages**.
- Questions: source contains **0 legacy questions**; no fabricated links; semantic question review `NOT APPLICABLE`.
- Current/next: `a7f1e94f-82d1-4146-af5b-4e9b51363f0b — كتاب الجغرافيا`.
- Exact next operation: fetch that source's live manifest/pages, verify immutable media, then reconstruct only evidence-backed boundaries from its own exact source/master evidence.
- RAW/unrelated/import/publication mutations remain **0/0/0/0**.
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

<!-- WORKER_B_EMPTY_ISLAMIC_PART1_HANDOFF_START -->
## Worker B handoff — current source remains ACTIVE

- last completed source: `b80cbba1-410a-4346-9446-c3f01c4f9e56 — كتاب الرياضيات - الجزء الثاني`.
- current source: `b6ce737e-26d4-4219-a607-27bfb7d2f518 — كتاب الإسلامية - الجزء الأول`.
- verified this run: manifest/pages/subject are mutually consistent and prove an empty retained legacy payload; no content structure can be reconstructed from that evidence.
- blocker: the live MASTER/status contract has no canonical verified-empty source disposition.
- handoff to Worker A: do **not** retry RAW/content discovery and do **not** skip this source. First establish an evidence-backed canonical empty-source disposition in the repository contract, then record it with exact-head guards. Until then all canonical counters remain unchanged and the next source remains `NOT YET RESOLVED`.
- evidence: `content-staging/reconstruction/educational/b6ce737e-26d4-4219-a607-27bfb7d2f518-empty-source-analysis.json`.
<!-- WORKER_B_EMPTY_ISLAMIC_PART1_HANDOFF_END -->

