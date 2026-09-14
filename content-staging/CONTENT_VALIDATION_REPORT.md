# CONTENT VALIDATION REPORT

Checkpoint: metadata inventory only; NOT DONE.

- Manifests read: 58/58.
- Image path/size matches: 5273/5273.
- Missing referenced paths: 0.
- Byte-size mismatches: 0.
- Invalid SHA-256 strings: 0.
- Duplicate recorded-checksum groups: 99; no automatic merge.
- Binary SHA-256 recalculation: NOT VERIFIED.
- Image readability/WebP quality: NOT VERIFIED.
- Individual exam boundaries/order/answer keys: NOT VERIFIED.
- Global source completeness across all branches: NOT VERIFIED.
- Current PostgreSQL contents/schema match: NOT VERIFIED.
- Dry Run: NOT RUN (no import-ready batch).
- Transaction Gate: NOT RUN.
- Apply: NOT RUN.
- Final Runtime Verification: NOT RUN.
- DB writes / new publication in this checkpoint: 0 / 0.

No import is permitted from this candidate catalog. Legacy page numbering anomalies are retained in MASTER_CONTENT_MANIFEST.json. Page number is not a unique identity; preserve legacy page UUID and source image index.

<!-- CHEMISTRY_RECONSTRUCTION_CHECKPOINT_START -->
## Chemistry reconstruction validation

`f0c5228c-7d5b-4ec2-85ed-ce59139ce0a4` passed the first complete source reconstruction gate:

- Technical image scan: **178/178** exist, readable, byte-size matched, SHA-256 matched, MIME matched; **0 errors**; **0 within-source duplicate SHA groups**.
- Sequence: exact contiguous numbered range **11..188**; no missing or duplicate page numbers.
- Trusted-master cross-check: all **178/178** retained RAW pages are byte-identical by SHA-256 to `master@f81ebb6ef6198818fa091f7a8c1c81b4de7dbd23` for the same numbered pages.
- Boundary evidence: trusted table of contents pages 7..10, exact page-title runs, and selective visual review of unit starts, unit reviews, glossary start/end, and master-only front/back pages.
- Verified structure: **9 Units, 57 Lessons, 149 Lesson pages, 10 Unit-cover pages, 14 Unit-review pages, 5 Glossary pages**.
- No page was equated to a Lesson merely because it existed; multi-page title runs were grouped and Unit/Review/Glossary pages were modeled separately.
- RAW mutations: **0**.

Still `NOT VERIFIED`: semantic correctness of the legacy questions, cross-lesson meaning for unit-review questions, WebP derivative optimization, and all unprocessed sources/exam-model boundaries.
<!-- CHEMISTRY_RECONSTRUCTION_CHECKPOINT_END -->

<!-- CHEMISTRY_EXAM_1445_CHECKPOINT_START -->
## Chemistry 1445 exam boundary validation

`e101d097-7a14-44e5-b242-cdeb9a312b77` passed technical and boundary-discovery gates:

- **60/60** images technically verified (exist/readable/size/SHA/MIME), **0 errors**, **0 within-source duplicate SHA groups**.
- Exact contiguous page sequence **1..60**.
- Every page was visually inspected through five complete contact sheets: 001–012, 013–024, 025–036, 037–048, 049–060.
- A consistent repeated structure was verified across the entire source: two exam-question pages followed by a correction/electronic-answer sheet, yielding **20 non-overlapping three-page Individual Exam Models**.
- The single storage `/lesson/` identity is explicitly not used as the model boundary.
- The third page of each model is not promoted to official `Answer Key`; all **20** remain correction-sheet candidates and Answer Key status is `NOT VERIFIED`.
- RAW mutations: **0**.
<!-- CHEMISTRY_EXAM_1445_CHECKPOINT_END -->

<!-- CHEMISTRY_EXAM_1446_CHECKPOINT_START -->
## Chemistry 1446 exam boundary validation

- **60/60** images passed existence/readability/size/SHA/MIME checks; sequence **1..60** contiguous; failures **0**.
- All 60 pages were visually reviewed via contact sheets 001–012, 013–024, 025–036, 037–048, 049–060.
- 1446 evidence independently establishes **15 × 4-page occurrences** (3 question pages + correction report), not the 1445 three-page pattern.
- Visible model codes resolve to **14 unique models** because `P.41` repeats.
- Explicit duplicate resolution: 29==41, 30==42, 31==43 by SHA; both blocks show `P.41`; correction reports 32/44 differ by candidate record. Classification `legitimate_repeated_exam_model_occurrence`.
- Correction relation is visually verified; standalone official Answer Key status remains `NOT VERIFIED`; verified Answer Keys **0**.
- RAW mutations: **0**.
<!-- CHEMISTRY_EXAM_1446_CHECKPOINT_END -->

<!-- CHEMISTRY_EXAM_1447_CHECKPOINT_START -->
## Chemistry 1447 exam boundary validation

- **124/124** images passed existence/readability/byte-size/SHA/MIME verification; sequence **1..124** contiguous; failures **0**.
- Every page was visually inspected through eleven contact sheets, including final sheet 121–124.
- Source-local structure: **31** four-page blocks; **29** model-code-matched occurrences; **28** unique verified Individual Exam Models; **116** finalized pages.
- Two mismatched blocks are deliberately not finalized: `37..40` (`P.61` / `P.31`) and `45..48` (`P.28` / `P.88`). They remain `review_required`; no synthetic pages or inferred model relations were created.
- Nine exact-SHA duplicate page pairs reduce to three repeated three-page question blocks. `P.8` is classified `legitimate_repeated_exam_model_occurrence`; the `P.28` and `P.61` mismatched duplicate blocks remain `review_required` / duplicate-source-import candidates rather than being auto-deleted.
- **226/226** legacy questions are structurally accounted for: **226** exam-linked and **0** review-required. Semantic correctness remains `NOT VERIFIED`.
- Standalone official Answer Keys: **0 / NOT VERIFIED**. RAW mutations: **0**.
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
## Grade 9 Science Part 1 reconstruction validation

- Technical verification: **161/161** files exist, readable, size/SHA/MIME match.
- Exact reference identity: **161/161** RAW images equal the corresponding master images by SHA-256.
- Exact retained reference range: source pages **8..168**; no retained identity failure.
- Structure: **8 Units / 22 Lessons / 138 Lesson pages / 8 covers / 15 reviews**; every one of the 161 retained pages is classified exactly once.
- Questions: **11/11** structurally linked by verified page membership; semantic correctness `NOT VERIFIED`.
- RAW mutations: **0**.
<!-- SCIENCE_BOOK_PART1_CHECKPOINT_END -->

<!-- SCIENCE_BOOK_PART2_CHECKPOINT_START -->
## Grade 9 Science Part 2 reconstruction validation

- Technical verification: **145/145** files exist, readable, size/SHA/MIME match.
- Exact reference identity: **145/145** RAW images equal the corresponding master images by SHA-256.
- Exact retained reference range: source pages **8..152**; no retained identity failure.
- Structure: **8 Units / 31 Lessons / 126 Lesson pages / 8 covers / 11 reviews**; every one of the 145 retained pages is classified exactly once.
- Questions: **0** source questions; no fabricated question links.
- RAW mutations: **0**.
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
## Grade 9 History source-local reconstruction validation

- Technical verification: **61/61** files exist, readable, size/SHA/MIME match; no within-source SHA duplicates.
- Source-local visual evidence: complete stored-page coverage **8..68**; explicit TOC and semester cover visually verified; all nine lesson start pages and twelve lesson-review pages visually checked.
- Structure: **1 semester section / 9 lessons / 47 lesson-content pages / 12 lesson-review pages**; every one of the **61** retained pages is classified exactly once.
- Questions: **138/138** structurally accounted for by verified page membership; semantic correctness `NOT VERIFIED`.
- Master-equivalence status: `NOT VERIFIED`; 0/61 exact SHA and 0 strong global visual matches against the currently indexed 211 master History pages.
- RAW mutations: **0**.
<!-- HISTORY_SOURCE_LOCAL_CHECKPOINT_END -->

<!-- CIVICS_BOOK_CHECKPOINT_START -->
## Grade 9 Civics reconstruction validation

- Technical verification: **59/59** files exist, readable, size/SHA/MIME match.
- Exact reference identity: **59/59** RAW images equal unique images in the exact Civics master reference by SHA-256.
- Structure: **4 Units / 14 Lessons / 48 Lesson pages / 4 covers / 7 reviews / 0 non-lesson pages**; every retained page is classified exactly once.
- Questions: **0** source questions; no fabricated question links.
- RAW mutations: **0**.
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
