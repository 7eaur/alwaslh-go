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
- `7eaur/alwaslh-go default master`: `f81ebb6ef6198818fa091f7a8c1c81b4de7dbd23`
- `7eaur/alwaslh-go work branch at start`: `content/legacy-staging-rebuild` = `b4f304b59bfaf82ed75012e8426da07e57f8f4e3`

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

## CURATION-001 — DONE / LESSON BOUNDARY VERIFIED

Smallest curation batch: first coherent Lesson inside Unit 2 only.

Evidence file:
- creation commit: `67f630f42913528405246fad7c541b091a47959e`
- `content-staging/curated/grade-9/english/pupil-book-3/curation-001-unit-2-describing.json`

Reviewed Lesson boundary:
- reviewed title: `Describing people and animals`
- book pages: `5..8`
- source pages: `9..12`
- ordered page/activity count: `4`
- attached legacy questions preserved: `12`

Boundary evidence:
- page 5 introduces physical description (`What do they look like?`) with evidence around height/build/weight/eye colour;
- page 6 develops descriptive vocabulary through `Opposites`;
- page 7 applies description language to people;
- page 8 applies the same describing skill to animals;
- book page 9/source page 13 changes topic to `What's the time?`, with question evidence about hour/minute/quarter-past expressions, and is therefore the next Lesson boundary rather than part of the describing Lesson.

Curation safety assertions:
- the four legacy page identities remain separate ordered page assets/activities; they were not promoted to four Lessons merely because they have four titles;
- all four RAW SHA-256 values remain preserved;
- all 12 attached questions remain on their exact source pages;
- question semantics were not approved, corrected, rejected or rewritten in this task;
- no RAW mutation;
- no PostgreSQL mutation;
- no publication state change;
- no anomaly deletion or unrelated-record mutation.

## CURATION-002 — DONE / LESSON BOUNDARY VERIFIED

Smallest next coherent Lesson inside Unit 2 only.

Evidence file:
- creation commit: `d14774adc68470e9eea48a1c388a14a66111bf57`
- `content-staging/curated/grade-9/english/pupil-book-3/curation-002-unit-2-time-and-meeting.json`

Reviewed Lesson boundary:
- reviewed title: `Telling time and arranging a meeting`
- book pages: `9..10`
- source pages: `13..14`
- ordered page/activity count: `2`
- attached legacy questions preserved: `7`

Boundary evidence:
- page 9 introduces and practises clock/time expressions, including quarter-past, minutes per hour and half-hour evidence;
- page 10 applies clock language to schedules and arranging a meeting;
- page 11/source page 15 changes instructional focus to `Things to do`, with obligation/task evidence (`has to do` before football), so it is excluded from this Lesson and remains the next unresolved boundary.

Curation safety assertions:
- both source identities remain separate ordered activity/page assets;
- both RAW SHA-256 values are preserved exactly;
- all 7 attached legacy AI questions remain on their exact source pages;
- the questions were not semantically approved, corrected, rejected or rewritten;
- no RAW or Media mutation;
- no PostgreSQL mutation;
- no publication state change;
- no anomaly deletion or unrelated-record mutation.

This closes CURATION-002 only. Unit 2 book pages `11..15` remain explicitly unresolved and preserved for later review; they are not silently converted into Lessons.

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

### CURATION-001
1. `[DONE]` Select the smallest coherent curation cluster inside Unit 2.
2. `[DONE]` Verify pages 5..8 form one describing-skill sequence from content/question evidence.
3. `[DONE]` Verify page 9 starts a different time/making-plans sequence.
4. `[DONE]` Preserve four source identities, ordering and RAW SHA-256 provenance.
5. `[DONE]` Preserve 12 question attachments without semantic approval/rewrite.
6. `[DONE]` Keep PostgreSQL/RAW/publication untouched.

### CURATION-002
1. `[DONE]` Start from book page 9/source page 13 as required.
2. `[DONE]` Verify pages 9..10 form the smallest coherent time-to-meeting Lesson sequence.
3. `[DONE]` Verify book page 11/source page 15 changes instructional focus to obligations/tasks and remains outside this Lesson.
4. `[DONE]` Preserve both source identities, order and RAW SHA-256 provenance.
5. `[DONE]` Preserve 7 question attachments without semantic approval/rewrite.
6. `[DONE]` Keep PostgreSQL/RAW/Media/publication untouched.

Current task status: `CURATION-002 = DONE / LESSON_BOUNDARY_VERIFIED`.

## Exact next action

On the next run:
1. read live heads + this status + handoff;
2. do not reopen completed tasks unless live drift invalidates evidence;
3. execute `CONTENT-GAPS-001` only;
4. begin by inventorying explicit content gaps/unresolved evidence from the reviewed Grade 9 English corpus, including Unit 2 pages `11..15`, manifest-only page 70, duplicate-position anomalies and any missing modern mappings;
5. do not infer deletion or curriculum membership from the old `69 -> 62` heuristic;
6. preserve anomalies and provenance rather than hiding them;
7. do not mutate PostgreSQL, RAW or publication state merely to close the gap inventory;
8. document the exact gap counts and evidence before moving to `MEDIA-001`.

## Remaining ordered queue

- `BATCH-001` — DONE: `CLOSED / COMMITTED_STATE_VERIFIED`
- `STRUCTURE-001` — DONE: `SECTION_BOUNDARY_VERIFIED`
- `STRUCTURE-002` — DONE: `SECTION_BOUNDARY_VERIFIED`
- `CURATION-001` — DONE: `LESSON_BOUNDARY_VERIFIED`
- `CURATION-002` — DONE: `LESSON_BOUNDARY_VERIFIED`
- `CONTENT-GAPS-001` — NEXT
- `MEDIA-001` — TODO
- `IMPORT-001` — TODO
- `VERIFY-001` — TODO
- `ROADMAP-RETURN -> STUDENT-016I` — TODO

## Run rules

At every run: read live heads + this file + handoff; continue the first incomplete task only; use the smallest reviewable batch; verify before declaring pass; update this file with exact SHAs, deployment IDs/counts/failures when relevant, and next action.

Never mutate RAW in place, auto-publish legacy/AI content, use `69 -> 62` as curriculum truth, delete anomalies for cosmetic counts, import unreviewed candidates, or mutate unrelated records.
