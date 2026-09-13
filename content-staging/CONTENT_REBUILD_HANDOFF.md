# الوسيلة الذكية — Content Rebuild Handoff

> نقطة الاستئناف الرسمية لمسار المحتوى. اقرأ live heads ثم `CONTENT_REBUILD_EXECUTION_STATUS.md` أولًا.

Last synchronized: **2026-09-13 — Grade 9 English full technical import complete and verified**.

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
- `master` contains a different Third Secondary/Pupil's Book 6 corpus and must not be treated as Grade 9 evidence

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

Verified committed state:

- 69/69 pages verified
- 69/69 RAW image SHA-256 checks verified
- 69/69 source identities
- 69/69 ready Media Assets
- 69/69 Lesson Assets
- 8/8 Sections
- 59 live Lesson identities own those 69 Lesson Assets
- 6 missing Sections created and 2 existing Sections reused
- 54 Lessons assigned to recovered Sections and 5 existing assignments reused
- 104/104 Question Revisions preserved
- manifest-only page 70 remains evidence-only
- published Lessons = 0
- published Lesson Assets = 0
- published Questions = 0
- RAW/media/question/unrelated mutation counts = 0

`59` is the observed live Lesson identity count after earlier curation/reassignment; it is not a derived `69 -> 62` heuristic. All 69 pages/images remain represented exactly once.

Detailed report:

`content-staging/BULK_GRADE9_ENGLISH_IMPORT_REPORT.md`

## Previous checkpoints retained

- `BATCH-001 = DONE / COMMITTED_STATE_VERIFIED`
- `STRUCTURE-001 = DONE / SECTION_BOUNDARY_VERIFIED`
- `STRUCTURE-002 = DONE / SECTION_BOUNDARY_VERIFIED`
- `CURATION-001 = DONE / LESSON_BOUNDARY_VERIFIED`
- `CURATION-002 = DONE / LESSON_BOUNDARY_VERIFIED`
- `CONTENT-GAPS-001 = DONE / GAP_INVENTORY_VERIFIED`
- `MEDIA-001 = DONE / MEDIA_PROFILE_VERIFIED_PARTIAL_ACCEPTANCE`
- `IMPORT-001 = DONE / COMMITTED_STATE_VERIFIED`
- `VERIFY-001 = DONE / DELIVERY_ISOLATION_AND_PROVENANCE_VERIFIED`
- `ROADMAP-RETURN = DONE / STUDENT-016I_HANDOFF_VERIFIED`

## Exact resume rule

Do not rerun the Grade 9 English bulk import unless fresh drift invalidates the verifier evidence.

The full source corpus is already in modern PostgreSQL and structurally verified. Further work is a separate semantic/product decision:

- optional pedagogical cleanup of Lesson grouping/naming on already-imported pages; and/or
- explicit publication review/gate.

Neither is permission to delete provenance, fabricate page 70, mutate RAW, hide anomalies, or auto-publish AI/legacy content.
