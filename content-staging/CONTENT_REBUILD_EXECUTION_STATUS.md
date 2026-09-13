# Alwaslh Content Rebuild — Shared Execution Status

> اقرأ هذه النسخة + live heads قبل أي عمل. Code/DB/runtime evidence outrank stale prose.

Last synchronized: **2026-09-14 — Grade 9 English full import verified; CURATION-002 committed state verified**.

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
- full-bulk source commit: `9e58ab3e882b883bddd016099949881801eedc28`
- CURATION-002 implementation commit: `8e7b6c242a810aeb9d56e50277bc4d55aa66a3c6`
- CURATION-002 reconciliation verifier commit: `2575d399db03be62911a927d5ce15bb8614fa9e8`

Railway content service is configured to return to idle after this checkpoint; documentation commits must not replay import/apply logic.

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

- `master` contains the original Grade 9 English reference under `تاسع انجليزي/الانجليزي_تاسع` (`manifest.json`, page-by-page guide and source images). It is valid structural/reference evidence and was used to cross-check page/unit/title layout.
- `master` also contains other corpora (including Third Secondary/Pupil's Book 6); those must not be confused with Grade 9.
- Immutable RAW + reconstruction manifest + modern PostgreSQL remain the write/import authority; the original `master` corpus is reference evidence, not permission to overwrite modern state blindly.

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
- involved Lesson identities at bulk checkpoint `59`
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

`59` was the observed asset-owning Lesson identity count at the full bulk-import checkpoint. It was **not** derived from `69 -> 62` or another arithmetic heuristic. Every RAW-backed page/image identity was represented exactly once.

Modern curation may reduce the number of asset-owning Lessons by grouping multiple source pages into one reviewed Lesson while preserving the original page/image provenance and legacy question records.

Detailed bulk evidence: `content-staging/BULK_GRADE9_ENGLISH_IMPORT_REPORT.md`.

## CURATION-001 structural state — DONE / COMMITTED_STATE_VERIFIED

Previously reviewed Unit 2 pages `5..8` are one modern Lesson:

- slug: `curated-english9-pb3-u2-describing-people-and-animals`
- title: `Describing people and animals`
- Lesson Assets: `4` ordered pages `5,6,7,8`
- source legacy question revisions preserved: `12`
- target question links intentionally remain `0` pending explicit semantic question curation
- publication changes: `0`

This grouping is backed by the reviewed `curation-001-unit-2-describing.json` contract and verified import/runtime evidence.

## CURATION-002 structural state — DONE / COMMITTED_STATE_VERIFIED

Reviewed Unit 2 pages `9..10` are now verified as one modern Lesson:

- slug: `curated-english9-pb3-u2-time-and-meeting`
- title: `Telling time and arranging a meeting`
- target Lesson ID: `4e106cb7-bc27-4e0d-bd51-d401bc7e980e`
- Lesson Assets: `2`, positions `0..1`, exact pages `9,10`
- provenance/SHA verified: `2/2`
- source legacy Lesson rows preserved: `2`, active/unpublished, sectionless and no longer owning those assets
- source question revisions preserved unchanged/unpublished: `7/7`
- target question links: `0` (semantic question migration remains intentionally separate)
- publication changes: `0`
- RAW mutations: `0`
- media mutations: `0`

Concurrency handling:

- first controlled apply attempt failed closed because the target Lesson already existed (`target lesson already exists count=1`); no write was made by that attempt.
- read-only reconciliation then verified the committed state instead of overwriting it.

Railway verification deployment:

`484f49af-01b4-4755-b8e3-d107641605b5` — `SUCCESS`

Markers:

- `CURATION002_RECONCILE_PASS`
- `CURATION002_FULL_PASS`
- status: `COMMITTED_STATE_VERIFIED`

## Prior closed checkpoints retained

- `BATCH-001` — DONE / COMMITTED_STATE_VERIFIED
- `STRUCTURE-001` — DONE / SECTION_BOUNDARY_VERIFIED
- `STRUCTURE-002` — DONE / SECTION_BOUNDARY_VERIFIED
- `CURATION-001` — DONE / LESSON_BOUNDARY_VERIFIED + COMMITTED_STATE_VERIFIED
- `CURATION-002` — DONE / LESSON_BOUNDARY_VERIFIED + COMMITTED_STATE_VERIFIED
- `CONTENT-GAPS-001` — DONE / GAP_INVENTORY_VERIFIED
- `MEDIA-001` — DONE / MEDIA_PROFILE_VERIFIED_PARTIAL_ACCEPTANCE
- `IMPORT-001` — DONE / COMMITTED_STATE_VERIFIED
- `VERIFY-001` — DONE / DELIVERY_ISOLATION_AND_PROVENANCE_VERIFIED
- `ROADMAP-RETURN` — DONE / STUDENT-016I_HANDOFF_VERIFIED

Do not repeat them unless fresh evidence invalidates their results.

## Exact next Content action

Do **not** rerun the full Grade 9 English bulk import.

Continue pedagogical refinement only from evidence-backed boundaries. The original `master` Grade 9 reference may be used to accelerate unit/page/title cross-checking, but differing adjacent page titles must not be merged solely by guesswork.

Highest-value remaining Content work:

1. inventory the remaining Unit 2+ lesson boundaries against the original Grade 9 source and existing multi-page legacy groupings;
2. apply only reviewed/evidence-backed grouping/renaming through rollback gate + controlled apply + post-verify;
3. separately curate/migrate question semantics where required; do not infer question ownership from page grouping alone;
4. keep publication locked until an explicit publication gate is approved.

Never delete provenance, fabricate page 70, mutate RAW, reintroduce the `69 -> 62` heuristic, or auto-publish legacy/AI content.
