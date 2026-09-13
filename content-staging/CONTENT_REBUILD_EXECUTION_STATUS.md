# Alwaslh Content Rebuild — Shared Execution Status

> اقرأ هذه النسخة + live heads قبل أي عمل. Code/DB/runtime evidence outrank stale prose.

Last synchronized: **2026-09-13 — full Grade 9 English bulk import verified**.

## Fixed execution contract

`Legacy Supabase -> Immutable RAW -> Reviewed/Recovered Structure -> Dry Run -> Controlled Transaction -> Modern PostgreSQL -> Verification -> Publication`

- لا تستخدم heuristic القديم `69 -> 62` كحقيقة منهجية.
- RAW immutable.
- لا auto-publish لأي AI/legacy content غير مراجع.
- لا حذف anomalies أو تعديل بيانات غير مرتبطة لتجميل الأرقام.
- أي apply يفشل مغلقًا عند identity/count/provenance/publication drift.
- WebP لا يُقبل إلا بعد إثبات فائدة الحجم والوضوح.

## Current live checkpoint

Working repository/branch:

- `7eaur/alwaslh-go@content/legacy-staging-rebuild`
- bulk source commit: `9e58ab3e882b883bddd016099949881801eedc28`
- bulk close-report commit: `fe9ad7cb6f32af22e9a56c84c1839e1e6b0f5f1b`

Railway content service was returned to idle after the run; documentation commits must not replay the apply pipeline.

## FULL-GRADE9-ENGLISH-BULK-IMPORT — DONE / FULL_ASSET_COVERAGE_VERIFIED / UNPUBLISHED

The user explicitly resumed Content Rebuild and authorized the fastest safe complete import of Grade 9 English pages/images/lessons into modern PostgreSQL.

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

- `master` contains the separate Third Secondary/Pupil's Book 6 corpus; it was not used as Grade 9 evidence.
- Grade 9 source evidence comes from `content/legacy-supabase-reconstruction`, immutable RAW, and `content-staging/curated/grade-9/english/pupil-book-3/reconstruction-candidates.json`.

### Runtime execution

Railway deployment:

`de7f9883-b2f0-483d-a7c1-ffbfb15ac30c` — `SUCCESS`

Verified runtime sequence:

- `BULK_G9_EN_INSPECT_PASS`
- `BULK_G9_EN_TRANSACTION_GATE_PASS`
- `BULK_G9_EN_APPLY_PASS`
- `BULK_G9_EN_VERIFY_PASS`
- `BULK_G9_EN_RUNNER_PASS`

Rollback gate before commit proved:

- manifest pages `69`
- source/media/lesson assets `69/69/69`
- involved Lessons `59`
- Sections resolved `8`
- create Sections `6`
- assign Lessons `54`
- reuse Lessons `5`
- question revisions preserved `104`
- publication/media/RAW/question/unrelated mutations `0`
- rollback verified `true`
- committed business writes during gate `0`

Committed apply then verified:

- pages verified `69/69`
- RAW images verified by SHA-256 `69/69`
- ready Media Assets `69/69`
- Lesson Assets `69/69`
- Sections `8/8`
- involved Lesson identities `59`
- new Sections created `6`
- existing Sections reused `2`
- Lessons newly assigned to recovered Section `54`
- existing correct Lesson assignments reused `5`
- Question Revisions preserved `104/104`
- page 70 preserved evidence-only `1`

Publication/isolation state:

- published Lessons `0`
- published Lesson Assets `0`
- published Questions `0`
- RAW mutations `0`
- media-binary mutations `0`
- question mutations `0`
- unrelated mutations `0`

### Lesson-count interpretation

`59` is **not** derived from `69 -> 62` or another arithmetic heuristic. It is the live set of Lesson identities owning the 69 verified Lesson Assets after earlier reviewed curation/reassignment. Every RAW-backed page/image identity is represented exactly once.

The legacy extraction itself stores source rows as `content_type = lesson` page records. Modern curation may group multiple source pages into one Lesson (for example the already-reviewed Unit 2 slice) without losing page/image provenance.

Therefore:

- full book data import = **complete**;
- full page/image coverage = **complete**;
- unit assignment = **complete**;
- provenance/checksum verification = **complete**;
- publication = **closed intentionally**;
- further pedagogical Lesson merge/rename refinement = optional follow-up, not missing-content import work.

Detailed evidence: `content-staging/BULK_GRADE9_ENGLISH_IMPORT_REPORT.md`.

## Prior closed checkpoints retained

- `BATCH-001` — DONE / COMMITTED_STATE_VERIFIED
- `STRUCTURE-001` — DONE / SECTION_BOUNDARY_VERIFIED
- `STRUCTURE-002` — DONE / SECTION_BOUNDARY_VERIFIED
- `CURATION-001` — DONE / LESSON_BOUNDARY_VERIFIED
- `CURATION-002` — DONE / LESSON_BOUNDARY_VERIFIED
- `CONTENT-GAPS-001` — DONE / GAP_INVENTORY_VERIFIED
- `MEDIA-001` — DONE / MEDIA_PROFILE_VERIFIED_PARTIAL_ACCEPTANCE
- `IMPORT-001` — DONE / COMMITTED_STATE_VERIFIED
- `VERIFY-001` — DONE / DELIVERY_ISOLATION_AND_PROVENANCE_VERIFIED
- `ROADMAP-RETURN` — DONE / STUDENT-016I_HANDOFF_VERIFIED

Do not repeat them unless fresh evidence invalidates their results.

## Exact next action

Do **not** rerun bulk import. Grade 9 English technical import is complete and verified.

Next Content action, only if explicitly requested, is one of:

- pedagogical curation refinement of Lesson grouping/naming on the already-imported 69 pages; or
- explicit publication review/gate.

Neither action may delete provenance, fabricate page 70, mutate RAW, reintroduce the `69 -> 62` heuristic, or auto-publish legacy/AI content.
