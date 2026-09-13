# الوسيلة الذكية — Content Rebuild Handoff

> نقطة الاستئناف الرسمية لمسار المحتوى. اقرأ live heads ثم `CONTENT_REBUILD_EXECUTION_STATUS.md` أولًا.

Last synchronized: **2026-09-14 — Grade 9 English full technical import complete; reviewed Unit 2 CURATION-001/002 structurally verified**.

## العقود الثابتة

- Working repository: `7eaur/alwaslh-go`
- Working branch: `content/legacy-staging-rebuild`
- RAW immutable؛ لا overwrite/recompress in-place.
- provenance وSHA-256 محفوظان.
- `media ready != published`.
- لا auto-publish لأي AI/legacy output.
- لا تستخدم `69 -> 62` كحقيقة منهجية.
- لا تحذف anomalies أو بيانات غير مرتبطة لتجميل الأرقام.
- أي DB apply يفشل مغلقًا عند identity/count/provenance/publication drift.

## Current Grade 9 English truth

`FULL-GRADE9-ENGLISH-BULK-IMPORT = DONE / FULL_ASSET_COVERAGE_VERIFIED / UNPUBLISHED`

Scope:

- 69 RAW-backed pages
- 69 RAW images
- 104 Question Revisions
- 8 recovered Units/Sections
- 1 manifest-only final page (page 70) preserved as evidence-only because no RAW identity exists

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

- Legacy subject: `1794eea5-4772-4c94-bd2b-b08e5815e733`
- immutable reconstruction manifest: `content-staging/curated/grade-9/english/pupil-book-3/reconstruction-candidates.json`
- source extraction: branch `content/legacy-supabase-reconstruction`
- original Grade 9 reference on `master`: `تاسع انجليزي/الانجليزي_تاسع` (`manifest.json`, page-by-page guide and source images)
- `master` also contains unrelated corpora; always resolve the exact Grade 9 path before using it as reference evidence.

## Full import runtime evidence

Source commit:

`9e58ab3e882b883bddd016099949881801eedc28`

Railway deployment:

`de7f9883-b2f0-483d-a7c1-ffbfb15ac30c` — `SUCCESS`

Markers:

- `BULK_G9_EN_INSPECT_PASS`
- `BULK_G9_EN_TRANSACTION_GATE_PASS`
- `BULK_G9_EN_APPLY_PASS`
- `BULK_G9_EN_VERIFY_PASS`
- `BULK_G9_EN_RUNNER_PASS`

Verified bulk state:

- 69/69 pages verified
- 69/69 RAW image SHA-256 checks verified
- 69/69 source identities
- 69/69 ready Media Assets
- 69/69 Lesson Assets
- 8/8 Sections
- 59 asset-owning Lesson identities at the bulk checkpoint
- 104/104 Question Revisions preserved
- manifest-only page 70 remains evidence-only
- published Lessons = 0
- published Lesson Assets = 0
- published Questions = 0
- RAW/media/question/unrelated mutation counts = 0

`59` was an observed checkpoint count, not a `69 -> 62` heuristic. Later reviewed curation may consolidate source pages into fewer asset-owning modern Lessons without losing provenance.

Detailed report:

`content-staging/BULK_GRADE9_ENGLISH_IMPORT_REPORT.md`

## Reviewed Unit 2 structural curation

### CURATION-001 — committed and verified

Pages `5..8` are one reviewed Lesson:

- `curated-english9-pb3-u2-describing-people-and-animals`
- `Describing people and animals`
- 4 ordered Lesson Assets
- 12 source legacy Question Revisions preserved/unpublished
- target question links intentionally remain 0 pending semantic question curation
- no publication/RAW/media mutation

### CURATION-002 — committed and verified

Pages `9..10` are one reviewed Lesson:

- `curated-english9-pb3-u2-time-and-meeting`
- `Telling time and arranging a meeting`
- target Lesson ID `4e106cb7-bc27-4e0d-bd51-d401bc7e980e`
- 2 ordered Lesson Assets with exact source paths/SHA-256 verified
- 2 source legacy Lessons preserved active/unpublished, sectionless and asset-free
- 7 source legacy Question Revisions preserved unchanged/unpublished
- target question links = 0
- publication changes = 0
- RAW/media mutations = 0

Concurrency note:

- a write attempt detected the target Lesson already existed and failed closed before mutation;
- read-only reconciliation verified the live state rather than overwriting it.

Verifier commit:

`2575d399db03be62911a927d5ce15bb8614fa9e8`

Railway verification deployment:

`484f49af-01b4-4755-b8e3-d107641605b5` — `SUCCESS`

Markers:

- `CURATION002_RECONCILE_PASS`
- `CURATION002_FULL_PASS`
- `COMMITTED_STATE_VERIFIED`

## Previous checkpoints retained

- `BATCH-001 = DONE / COMMITTED_STATE_VERIFIED`
- `STRUCTURE-001 = DONE / SECTION_BOUNDARY_VERIFIED`
- `STRUCTURE-002 = DONE / SECTION_BOUNDARY_VERIFIED`
- `CURATION-001 = DONE / LESSON_BOUNDARY_VERIFIED + COMMITTED_STATE_VERIFIED`
- `CURATION-002 = DONE / LESSON_BOUNDARY_VERIFIED + COMMITTED_STATE_VERIFIED`
- `CONTENT-GAPS-001 = DONE / GAP_INVENTORY_VERIFIED`
- `MEDIA-001 = DONE / MEDIA_PROFILE_VERIFIED_PARTIAL_ACCEPTANCE`
- `IMPORT-001 = DONE / COMMITTED_STATE_VERIFIED`
- `VERIFY-001 = DONE / DELIVERY_ISOLATION_AND_PROVENANCE_VERIFIED`
- `ROADMAP-RETURN = DONE / STUDENT-016I_HANDOFF_VERIFIED`

## Exact resume rule

Do not rerun Grade 9 English bulk import or CURATION-001/002 unless fresh drift invalidates verifier evidence.

Continue only with the first remaining evidence-backed pedagogical boundary. Use the exact Grade 9 source on `master` to accelerate page/unit/title comparison, then require a rollback gate before any structural write.

Question migration remains a separate semantic step: preserving source questions does not automatically authorize relinking them to a curated Lesson.

Publication remains locked until an explicit publication review/gate is approved.

Never delete provenance, fabricate page 70, mutate RAW, hide anomalies, or auto-publish legacy/AI content.
