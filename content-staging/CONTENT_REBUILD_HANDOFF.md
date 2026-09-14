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
