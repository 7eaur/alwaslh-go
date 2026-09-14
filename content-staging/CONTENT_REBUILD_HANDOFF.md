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
