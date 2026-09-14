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

<!-- SCIENCE_BOOK_PART2_CHECKPOINT_START -->
## Science Part 2 reconstruction checkpoint — no import performed

The reconstruction artifact is verified, but the corpus remains `RECONSTRUCTION_IN_PROGRESS_NOT_IMPORT_READY`.

- New imports: **0**; new publications: **0**; production mutations: **0**; RAW mutations: **0**.
- Import readiness remains deferred until corpus reconstruction/boundary discovery is complete.
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
## History reconstruction checkpoint — no import performed

The History source-local reconstruction is verified, but the corpus remains `RECONSTRUCTION_IN_PROGRESS_NOT_IMPORT_READY`.

- New imports: **0**; new publications: **0**; production mutations: **0**; RAW mutations: **0**.
- Import readiness remains deferred until corpus reconstruction/boundary discovery is complete.
<!-- HISTORY_SOURCE_LOCAL_CHECKPOINT_END -->

<!-- CIVICS_BOOK_CHECKPOINT_START -->
## Civics reconstruction checkpoint — no import performed

The reconstruction artifact is verified, but the corpus remains `RECONSTRUCTION_IN_PROGRESS_NOT_IMPORT_READY`.

- New imports: **0**; new publications: **0**; production mutations: **0**; RAW mutations: **0**.
- Import readiness remains deferred until corpus reconstruction/boundary discovery is complete.
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
