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
