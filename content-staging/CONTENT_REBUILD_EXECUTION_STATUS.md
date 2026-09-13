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

## Live repository heads observed at start of CONTENT-GAPS-001

- `7eaur/alwaslh main`: `c5ccbc9b0d0e88ef8798bbae6a3cc0bf933b5a7e`
- `7eaur/alwaslh-go work branch`: `content/legacy-staging-rebuild` = `1132773d2fb5b93b6a58a27201d4275b8462c233`
- CONTENT-GAPS-001 inventory commit: `dd86641decbcb3e3345d1aacfea7e2363fc60474`

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

Grade 9 / English / Pupil Book 3 / `Unit 2 - Describing: Making plans`.

Evidence:
- commit `4ff71ca280c432392c8d91737374c77232b3fe69`
- `content-staging/curated/grade-9/english/pupil-book-3/structure-001-unit-2.json`
- book pages `5..15`
- source pages `9..19`
- page count `11`
- preserved legacy questions `30`
- book page `16` explicitly transitions to `Unit 3 - Other countries`

Lesson boundaries were intentionally unresolved at this stage; no RAW/DB/publication mutation occurred.

## STRUCTURE-002 — DONE / SECTION BOUNDARY VERIFIED

Grade 9 / English / Pupil Book 3 / `Unit 3 - Other countries`.

Evidence:
- commit `9e92a4b4d7658f6ea43f1f0727ffb19e922c66cb`
- `content-staging/curated/grade-9/english/pupil-book-3/structure-002-unit-3.json`
- book pages `16..25`
- source pages `20..29`
- page count `10`
- preserved legacy questions `3`
- next book page `26` / source page `30` explicitly belongs to `Unit 4 - Visiting Japan`

All source identities/checksums remain preserved; no question rewrite, RAW/DB/publication mutation, anomaly deletion or unrelated-record mutation occurred.

## CURATION-001 — DONE / LESSON BOUNDARY VERIFIED

Evidence:
- commit `67f630f42913528405246fad7c541b091a47959e`
- `content-staging/curated/grade-9/english/pupil-book-3/curation-001-unit-2-describing.json`

Reviewed Lesson:
- title `Describing people and animals`
- book pages `5..8`
- source pages `9..12`
- ordered source/activity pages `4`
- legacy questions preserved `12`

Page 9/source 13 changes to time expressions and starts the next boundary. No question semantics were approved/re-written; no RAW/DB/publication mutation occurred.

## CURATION-002 — DONE / LESSON BOUNDARY VERIFIED

Evidence:
- commit `d14774adc68470e9eea48a1c388a14a66111bf57`
- `content-staging/curated/grade-9/english/pupil-book-3/curation-002-unit-2-time-and-meeting.json`

Reviewed Lesson:
- title `Telling time and arranging a meeting`
- book pages `9..10`
- source pages `13..14`
- ordered source/activity pages `2`
- legacy questions preserved `7`

Page 11/source 15 changes focus to obligations/tasks (`Things to do`) and remains outside this Lesson. No question semantics were approved/re-written; no RAW/Media/DB/publication mutation occurred.

## CONTENT-GAPS-001 — DONE / GAP INVENTORY VERIFIED

Evidence:
- inventory commit `dd86641decbcb3e3345d1aacfea7e2363fc60474`
- `content-staging/curated/grade-9/english/pupil-book-3/content-gaps-001.json`
- reconstruction blob `2d054712b6013675f7ad24d573c3a06745972067`
- Grade 9 English RAW manifest blob `70a6c37000eb0dc8249a64fa5cade5d5de61686e`

Exact Grade 9 English inventory:
- RAW page candidates: `69`
- RAW images: `69`
- legacy questions: `104`
- recovered sections: `8`
- reviewed boundary coverage: `10` pages = Unit 1 pages `1..4` + Unit 2 pages `5..10`
- unresolved boundary candidates: `59` pages
- Unit 2 immediate unresolved remainder: book pages `11..15` / source pages `15..19` = `5` pages / `11` questions
- source-manifest-only evidence: `1` page = book page `70`, source page `74`, `Blank Final Page`, Back Matter
- Grade 9 English RAW duplicate page-number anomalies: `0`
- corpus-wide duplicate-position anomalies remain preserved: `6`; they are not Grade 9 English anomalies
- verified modern page mappings in this rebuild track: `4` (BATCH-001)
- remaining modern page mappings not yet verified by this rebuild track: `65`; this means `unverified`, not `missing`

Important scope correction:
- the legacy Grade 9 English RAW manifest itself reports no duplicate page numbers, missing images, multiple images, malformed AI questions, malformed image URLs or invalid page numbers, and `0` image download failures;
- the corpus-wide `6` duplicate-position anomalies must stay preserved in corpus evidence and must not be projected onto Grade 9 English or deleted;
- historical `62 Draft lessons` remains reconciliation evidence only and is not used to derive `69 -> 62`, deletion, curriculum membership or mapping truth.

Manifest-only page 70 handling:
- source manifest contains `Blank Final Page` at book page `70` / source page `74`;
- immutable legacy RAW subject has only `69` page/image identities and no RAW identity for that entry;
- therefore it remains evidence-only and must not be synthesized/imported as curriculum content without new source evidence.

Modern mapping handling:
- only the four Unit 1 page identities have verified committed modern mappings in this rebuild track;
- the other `65` candidates require identity-by-identity mapping verification before import;
- no claim is made that 65 rows are absent from PostgreSQL.

CONTENT-GAPS-001 safety result:
- heuristic `69 -> 62`: not used
- RAW mutation: `0`
- Media mutation: `0`
- PostgreSQL mutation: `0`
- publication change: `0`
- anomaly deletion: `0`
- unrelated-record mutation: `0`

## Gate checklist

### BATCH-001
1. `[DONE]` Reviewed Unit 1 boundaries and 13 questions.
2. `[DONE]` Duplicate-safe dry-run + controlled transaction verification.
3. `[DONE]` Committed target state verification with publication closed.

### STRUCTURE-001
1. `[DONE]` Verify Unit 2 structural boundary and preserve source/question identities.
2. `[DONE]` Keep Lesson boundaries unresolved and DB/RAW/publication untouched.

### STRUCTURE-002
1. `[DONE]` Verify Unit 3 structural boundary and transition to Unit 4.
2. `[DONE]` Preserve source/question identities and keep DB/RAW/publication untouched.

### CURATION-001
1. `[DONE]` Review smallest coherent describing cluster pages 5..8.
2. `[DONE]` Preserve activity/page identities and question provenance without semantic rewrite.

### CURATION-002
1. `[DONE]` Review time/meeting cluster pages 9..10.
2. `[DONE]` Preserve page identities and keep page 11 as next unresolved boundary.

### CONTENT-GAPS-001
1. `[DONE]` Inventory Unit 2 unresolved pages 11..15 with exact identities/checksums/questions.
2. `[DONE]` Quantify total reviewed vs unresolved boundary coverage without inferring desired lesson count.
3. `[DONE]` Preserve manifest-only page 70 as evidence-only.
4. `[DONE]` Separate Grade 9 English anomaly truth (`0` duplicate page numbers) from corpus-wide preserved anomalies (`6`).
5. `[DONE]` Classify non-BATCH-001 modern mappings as unverified, not missing, and avoid `69 -> 62` inference.
6. `[DONE]` Keep PostgreSQL/RAW/Media/publication untouched.

Current task status: `CONTENT-GAPS-001 = DONE / GAP_INVENTORY_VERIFIED`.

## Exact next action

On the next run:
1. read both live repository heads + this status + handoff;
2. do not reopen completed tasks unless live drift invalidates their evidence;
3. execute `MEDIA-001` only, using the smallest reviewable media batch;
4. start from preserved RAW identities and evaluate derived media candidates with measured byte-size and visual-legibility evidence;
5. do not accept WebP merely because of format; BATCH-001 already proved the current profile can be larger than RAW (`+24.81%`);
6. never overwrite/recompress RAW in place;
7. do not use media work to decide curriculum membership or unresolved Lesson boundaries;
8. do not publish or mutate unrelated PostgreSQL content merely to close MEDIA-001;
9. document exact input/output byte counts, checksums, acceptance/rejection reasons and next action.

## Remaining ordered queue

- `BATCH-001` — DONE: `CLOSED / COMMITTED_STATE_VERIFIED`
- `STRUCTURE-001` — DONE: `SECTION_BOUNDARY_VERIFIED`
- `STRUCTURE-002` — DONE: `SECTION_BOUNDARY_VERIFIED`
- `CURATION-001` — DONE: `LESSON_BOUNDARY_VERIFIED`
- `CURATION-002` — DONE: `LESSON_BOUNDARY_VERIFIED`
- `CONTENT-GAPS-001` — DONE: `GAP_INVENTORY_VERIFIED`
- `MEDIA-001` — NEXT
- `IMPORT-001` — TODO
- `VERIFY-001` — TODO
- `ROADMAP-RETURN -> STUDENT-016I` — TODO

## Run rules

At every run: read live heads + this file + handoff; continue the first incomplete task only; use the smallest reviewable batch; verify before declaring pass; update this file with exact SHAs, deployment IDs/counts/failures when relevant, and next action.

Never mutate RAW in place, auto-publish legacy/AI content, use `69 -> 62` as curriculum truth, delete anomalies for cosmetic counts, import unreviewed candidates, or mutate unrelated records.
