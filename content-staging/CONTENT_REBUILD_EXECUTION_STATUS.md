# Alwaslh Content Rebuild — Shared Execution Status

> اقرأ هذه النسخة + live heads قبل أي عمل، ثم أكمل أول مهمة غير مكتملة فقط. لا تعتمد على ذاكرة المحادثة.

## Current direction — 2026-09-13

`Legacy Supabase -> Immutable RAW -> Reviewed CURATED -> Media Decision -> Dry Run -> Controlled Transaction -> Modern PostgreSQL -> Verification -> Publication`

Rules remain fixed:
- لا تستخدم heuristic القديم `69 -> 62` كحقيقة منهجية.
- RAW immutable.
- لا auto-publish لأي AI/legacy content غير مراجع.
- لا حذف anomalies أو تعديل بيانات غير مرتبطة لتجميل الأرقام.
- أي apply يفشل مغلقًا عند identity/count/provenance drift.

## Live repository heads observed at start of this run

- `7eaur/alwaslh main`: `c5ccbc9b0d0e88ef8798bbae6a3cc0bf933b5a7e`
- `7eaur/alwaslh-go work branch at start`: `content/legacy-staging-rebuild` = `0c4a307a1db1ab02370d0be0741e2481087a0fa1`

## BATCH-001 — CLOSED / COMMITTED STATE VERIFIED

Batch: `BATCH-001-G9-EN-PB3-U1`

Target: Grade 9 / English / Pupil Book 3 / `Unit 1 - Revision`.

Verified committed state retained:
- target Section: exactly `1`
- exact reused Lessons: `4`
- exact Lesson Assets: `4`, all `draft`
- exact Media Assets: `4`, all `ready`
- Question Revisions: `13` = `7 corrected + 6 unchanged`
- question provenance links: `13/13`
- target-slug duplicates: `0`
- publication: lessons `0`, lesson assets `0`, questions `0`
- RAW/media mutation: `0`
- final verifier deployment: `c3e609b3-f632-46e9-9fde-680330512eee`
- marker: `BATCH001_POST_APPLY_VERIFY_PASS`

Media decision remains unchanged:
- RAW JPEG total: `440,502` bytes
- existing display WebP total: `549,794` bytes
- delta: `+24.81%`
- current WebP profile is not an optimization success

Do not perform more BATCH-001 mutation.

## STRUCTURE-001 — DONE / SECTION BOUNDARY VERIFIED

Smallest reviewable structural batch: Grade 9 / English / Pupil Book 3 / `Unit 2 - Describing: Making plans`.

Evidence file:
- creation commit: `4ff71ca280c432392c8d91737374c77232b3fe69`
- `content-staging/curated/grade-9/english/pupil-book-3/structure-001-unit-2.json`

Verified section boundary:
- book pages `5..15`
- source pages `9..19`
- page count `11`
- preserved legacy questions `30`
- book page `16` explicitly transitions to `Unit 3 - Other countries`

Lesson boundaries remain unresolved; no RAW/DB/publication mutation occurred.

## STRUCTURE-002 — DONE / SECTION BOUNDARY VERIFIED

Smallest next structural batch: Grade 9 / English / Pupil Book 3 / `Unit 3 - Other countries`.

Evidence file created in commit:
- `9e92a4b4d7658f6ea43f1f0727ffb19e922c66cb`
- `content-staging/curated/grade-9/english/pupil-book-3/structure-002-unit-3.json`

Verified section boundary:
- first book page: `16`
- last book page: `25`
- first source page: `20`
- last source page: `29`
- page count: `10`
- preserved legacy questions: `3`
- next book page `26` / source page `30` explicitly belongs to `Unit 4 - Visiting Japan` (`A Japanese pen-friend`)

Structural safety assertions:
- all 10 candidate/source identities are preserved with RAW SHA-256 references;
- repeated title `Four countries` remains two distinct source identities and is not merged;
- page titles remain Lesson/Activity candidates only;
- `lesson_boundaries_approved = false`;
- the 3 questions remain attached to book page `22` / source page `26` and are not approved or rewritten;
- no RAW mutation;
- no PostgreSQL mutation;
- no publication state change;
- no anomaly deletion or unrelated-record mutation.

This closes only the Unit 3 Section boundary task. It does not curate Lesson boundaries or approve questions.

## Gate checklist

### BATCH-001
1. `[DONE]` Reviewed Unit 1 boundaries and 13 questions.
2. `[DONE]` Duplicate-safe dry-run + controlled transaction verification.
3. `[DONE]` Committed target state verification with publication closed.

### STRUCTURE-001
1. `[DONE]` Select smallest structural batch: Unit 2 only.
2. `[DONE]` Verify book/source page start and end.
3. `[DONE]` Verify explicit transition to next section.
4. `[DONE]` Preserve source identities/question attachments.
5. `[DONE]` Keep Lesson boundaries unresolved.
6. `[DONE]` Keep DB/RAW/publication untouched.

### STRUCTURE-002
1. `[DONE]` Select smallest next structural batch: Unit 3 only.
2. `[DONE]` Verify book/source page start and end.
3. `[DONE]` Verify explicit transition to Unit 4.
4. `[DONE]` Preserve all 10 source identities and RAW SHA-256 references.
5. `[DONE]` Preserve all 3 question attachments without review/rewrite.
6. `[DONE]` Keep Lesson boundaries unresolved and DB/RAW/publication untouched.

Current task status: `STRUCTURE-002 = DONE / SECTION_BOUNDARY_VERIFIED`.

## Exact next action

On the next run:
1. read live heads + this status + handoff;
2. do not reopen BATCH-001, STRUCTURE-001 or STRUCTURE-002 unless live drift invalidates evidence;
3. execute `CURATION-001` only, using the smallest reviewable curation batch;
4. determine Lesson/Activity boundaries from actual content evidence rather than page-title heuristics;
5. preserve source identities, RAW and question provenance;
6. do not publish unreviewed content;
7. document results before moving to CURATION-002.

## Remaining ordered queue

- `BATCH-001` — DONE: `CLOSED / COMMITTED_STATE_VERIFIED`
- `STRUCTURE-001` — DONE: `SECTION_BOUNDARY_VERIFIED`
- `STRUCTURE-002` — DONE: `SECTION_BOUNDARY_VERIFIED`
- `CURATION-001` — NEXT
- `CURATION-002` — TODO
- `CONTENT-GAPS-001` — TODO
- `MEDIA-001` — TODO
- `IMPORT-001` — TODO
- `VERIFY-001` — TODO
- `ROADMAP-RETURN -> STUDENT-016I` — TODO

## Run rules

At every run: read live heads + this file + handoff; continue the first incomplete task only; use the smallest reviewable batch; verify before declaring pass; update this file with exact SHAs, deployment IDs/counts/failures when relevant, and next action.

Never mutate RAW in place, auto-publish legacy/AI content, use `69 -> 62` as curriculum truth, delete anomalies for cosmetic counts, import unreviewed candidates, or mutate unrelated records.
