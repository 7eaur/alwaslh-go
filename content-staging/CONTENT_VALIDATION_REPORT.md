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

<!-- BIOLOGY_BOOK_CHECKPOINT_START -->
## Biology textbook reconstruction validation

- Technical verification: **214/214** files exist, readable, and match manifest size/SHA/MIME.
- Exact reference identity: **214/214** RAW images equal the single canonical master directory by SHA-256.
- Structure: **8 Units / 47 Lessons / 193 Lesson pages / 8 covers / 13 reviews**; all 214 retained pages classified exactly once.
- Questions: **3003** structurally linked; **301** `review_required`; semantic correctness `NOT VERIFIED`.
- RAW mutations: **0**.
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

<!-- ARABIC_PART1_CHECKPOINT_START -->
## Reconstruction checkpoint — Arabic book part 1

- Sources processed: **37/58**; Educational: **17/26**; Exam groups: **20/32**.
- Books / Units / Lessons / unique physical Lesson pages: **15 / 69 / 388 / 1641**.
- Arabic Part 1: **169/169** technical; **12 Units / 60 semantic Lessons / 114 unique physical lesson pages / 35 intro-cover / 18 assessment / 2 tail**.
- Shared physical lesson pages are preserved semantically without double-counting: **11**.
- Questions unchanged: **13135 + 1920 + 1229 + 9471 = 25,755**.
- Technical images: **3190/5273**. RAW/unrelated/import/publication mutations **0/0/0/0**.
- Last completed: `ab701a9e-3efb-409a-8ed1-9752d41c4771 — كتاب العربي - الجزء الأول`. Next: `7ddec20e-617e-4e55-bba8-2d371aaf16b6 — كتاب العربي - الجزء الثاني`.
<!-- ARABIC_PART1_CHECKPOINT_END -->

<!-- ARABIC_PART2_CHECKPOINT_START -->
## Reconstruction checkpoint — Arabic book part 2

- Sources processed: **38/58**; Educational: **18/26**; Exam groups: **20/32**.
- Books / Units / Lessons / unique physical Lesson pages: **16 / 81 / 448 / 1740**.
- Arabic Part 2: **178/178** technical; page **0** preserved plus contiguous **1..177**; **12 Units (13..24) / 60 semantic Lessons / 111 membership edges / 99 unique physical lesson pages / 48 intro-cover / 20 assessment / 8 front matter / 3 tail**.
- Physical invariant: **8 + 48 + 99 + 20 + 3 = 178**.
- Page 177 conflict: immutable image association is verified as the back cover; its **11** stale/misattached legacy questions remain **review_required**, with **0 lesson-linked** and **0 assessment-linked**; semantic correctness is **NOT VERIFIED**.
- Questions: **13135 + 1920 + 1240 + 9460 = 25,755**.
- Technical images: **3368/5273**. RAW/unrelated/import/publication mutations **0/0/0/0**.
- Production PostgreSQL cleanup/import: **NOT EXECUTED**; reconstruction remains not import-ready corpus-wide.
- Last completed: `7ddec20e-617e-4e55-bba8-2d371aaf16b6 — كتاب العربي - الجزء الثاني`. Next: `6fa466f9-b930-437e-b091-947ee56407c4 — التفاضل والتكامل نماذج وزاريه 1445`.
<!-- ARABIC_PART2_CHECKPOINT_END -->

<!-- CALCULUS_EXAM_1445_CHECKPOINT_START -->
## Reconstruction checkpoint — Calculus Ministry Exams 1445

- Source `6fa466f9-b930-437e-b091-947ee56407c4` — `التفاضل والتكامل نماذج وزاريه 1445` completed from source-local technical and visual evidence.
- Technical verification: **80/80** images exist, readable, byte-size/SHA-256/MIME match; sequence **1..80** contiguous; duplicate SHA groups **0**.
- Complete visual review resolves **20** Individual Exam Model occurrences, each with three question pages plus one paired correction/result sheet candidate.
- Finalized Exam Pages: **80**; review-required pages: **0**; correction-sheet candidates: **20**; verified standalone Answer Keys: **0 / NOT VERIFIED**.
- Source legacy questions: **0**; no question mapping was invented.
- Progress: Sources **39/58**; Educational **18/26**; Exam Groups **21/32**; Individual Exam Models **390**; Exam Pages **1354/2,286**; source images technical **3448/5,273**.
- Global questions: Lesson-linked **13135**; Exam-linked **1920**; Review-required **1240**; Unclassified **9460**; invariant **PASS = 25,755**.
- RAW/unrelated/import/publication mutations: **0/0/0/0**. Production PostgreSQL cleanup/import: **NOT EXECUTED**; corpus remains reconstruction-in-progress.
- Next source: `012196f1-a633-41cd-927b-d0b1b8845781` — `التفاضل والتكامل نماذج وزاريه 1446`.
<!-- CALCULUS_EXAM_1445_CHECKPOINT_END -->

<!-- CALCULUS_EXAM_1446_CHECKPOINT_START -->
## Reconstruction checkpoint — Calculus Ministry Exams 1446

- Source `012196f1-a633-41cd-927b-d0b1b8845781` — `التفاضل والتكامل نماذج وزاريه 1446` completed from source-local technical and visual evidence.
- Technical verification: **100/100** images match byte-size/SHA-256/MIME; sequence **1..100** contiguous.
- Duplicate evidence: **6** SHA-256 groups, each containing two source occurrences, preserved without merge, deletion, renumbering, or RAW mutation.
- Complete visual review resolves **25** Individual Exam Model occurrences, each with three question pages plus one correction/result-sheet candidate.
- Finalized Exam Pages: **100**; review-required pages: **0**; correction candidates: **25**; verified standalone Answer Keys: **0 / NOT VERIFIED**.
- Source legacy questions: **40/40** structurally linked to the first model by their preserved page membership on pages **1..3**; semantic correctness remains **NOT VERIFIED**.
- Progress: Sources **40/58**; Educational **18/26**; Exam Groups **22/32**; Individual Models **415**; Exam Pages **1454/2,286**; technical images **3548/5,273**.
- Global questions: **13135 + 1960 + 1240 + 9420 = 25,755**.
- RAW/unrelated/import/publication mutations: **0/0/0/0**. Production PostgreSQL cleanup/import: **NOT EXECUTED**; corpus remains reconstruction-in-progress.
- Next source: `dcc316bc-b7b8-4a9f-9022-ecc1e7762a9e` — `التفاضل والتكامل نماذج وزاريه 1447`.
<!-- CALCULUS_EXAM_1446_CHECKPOINT_END -->

<!-- CALCULUS_EXAM_1447_CHECKPOINT_START -->
## Reconstruction checkpoint — Calculus Ministry Exams 1447

- Source `dcc316bc-b7b8-4a9f-9022-ecc1e7762a9e` — `التفاضل والتكامل نماذج وزاريه 1447` completed from source-local evidence: **124/124** technical images, contiguous **1..124**, and complete visual review.
- Resolved **31** Individual Exam Models / **124** Exam Pages; each occurrence has three question pages plus one correction/result candidate.
- Duplicate SHA groups: **9**, preserved as distinct source occurrences without merge or RAW mutation.
- Legacy questions: **454/454** structurally linked by preserved page membership to the first ten models; semantic correctness **NOT VERIFIED**.
- Correction candidates **31**; verified standalone Answer Keys **0 / NOT VERIFIED**.
- Progress: Sources **41/58**; Educational **18/26**; Exam Groups **23/32**; Models **446**; Exam Pages **1578/2,286**; technical images **3672/5,273**.
- Questions: **13135 + 2414 + 1240 + 8966 = 25,755**. RAW/unrelated/import/publication mutations **0/0/0/0**.
- Production PostgreSQL cleanup/import: **NOT EXECUTED**; reconstruction remains corpus-wide in progress.
- Next source: `78292a85-06b3-4ec3-879e-8810ed0595d1` — `الجبر والهندسة نماذج وزارية 1446`.
<!-- CALCULUS_EXAM_1447_CHECKPOINT_END -->
