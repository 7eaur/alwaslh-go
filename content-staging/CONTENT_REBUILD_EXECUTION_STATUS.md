# Alwaslh Content Rebuild — Shared Execution Status

> اقرأ هذه النسخة + live heads قبل أي عمل، ثم أكمل أول مهمة غير مكتملة فقط. لا تعتمد على ذاكرة المحادثة.

## Current direction — 2026-09-13

`Legacy Supabase -> Immutable RAW -> Reviewed CURATED -> Media Decision -> Dry Run -> Controlled Transaction -> Modern PostgreSQL -> Verification -> Publication`

Fixed rules:
- لا تستخدم heuristic القديم `69 -> 62` كحقيقة منهجية.
- RAW immutable.
- لا auto-publish لأي AI/legacy content غير مراجع.
- لا حذف anomalies أو تعديل بيانات غير مرتبطة لتجميل الأرقام.
- أي apply يفشل مغلقًا عند identity/count/provenance drift.
- WebP لا يُقبل لمجرد الامتداد؛ يجب إثبات فائدة الحجم والوضوح.

## Live heads observed at start of current IMPORT-001 continuation

- `7eaur/alwaslh main`: `0c7c9f9c5e4ec6ae020484a9a4892eaf3b8b5194`
- `7eaur/alwaslh-go content/legacy-staging-rebuild`: `b51cc0df7a127f8d2f458850eed395732ddc8075`

No evidence-invalidating drift was found before continuing IMPORT-001.

## BATCH-001 — DONE / COMMITTED_STATE_VERIFIED

`BATCH-001-G9-EN-PB3-U1`

Verified retained state:
- target Section: exactly `1`
- reused Lessons: `4`
- Lesson Assets: `4`, all `draft`
- Media Assets: `4`, all `ready`
- Question Revisions: `13` = `7 corrected + 6 unchanged`
- question provenance links: `13/13`
- target-slug duplicates: `0`
- publication: lessons `0`, lesson assets `0`, questions `0`
- RAW/media mutation: `0`
- final verifier deployment: `c3e609b3-f632-46e9-9fde-680330512eee`
- marker: `BATCH001_POST_APPLY_VERIFY_PASS`

Prior media decision retained:
- RAW JPEG total: `440,502` bytes
- existing display WebP total: `549,794` bytes
- delta: `+24.81%`
- current BATCH-001 WebP profile is not an optimization success

Do not perform more BATCH-001 mutation unless fresh drift invalidates this evidence.

## STRUCTURE-001 — DONE / SECTION_BOUNDARY_VERIFIED

Grade 9 / English / Pupil Book 3 / `Unit 2 - Describing: Making plans`.

Evidence:
- commit `4ff71ca280c432392c8d91737374c77232b3fe69`
- `content-staging/curated/grade-9/english/pupil-book-3/structure-001-unit-2.json`
- book pages `5..15`
- source pages `9..19`
- page count `11`
- preserved legacy questions `30`
- book page `16` explicitly transitions to `Unit 3 - Other countries`

No RAW/DB/publication mutation occurred.

## STRUCTURE-002 — DONE / SECTION_BOUNDARY_VERIFIED

Grade 9 / English / Pupil Book 3 / `Unit 3 - Other countries`.

Evidence:
- commit `9e92a4b4d7658f6ea43f1f0727ffb19e922c66cb`
- `content-staging/curated/grade-9/english/pupil-book-3/structure-002-unit-3.json`
- book pages `16..25`
- source pages `20..29`
- page count `10`
- preserved legacy questions `3`
- page `26` / source `30` explicitly starts `Unit 4 - Visiting Japan`

No question rewrite, RAW/DB/publication mutation, anomaly deletion or unrelated-record mutation occurred.

## CURATION-001 — DONE / LESSON_BOUNDARY_VERIFIED

Evidence:
- commit `67f630f42913528405246fad7c541b091a47959e`
- `content-staging/curated/grade-9/english/pupil-book-3/curation-001-unit-2-describing.json`

Reviewed Lesson:
- title `Describing people and animals`
- book pages `5..8`
- source pages `9..12`
- ordered activity/page assets `4`
- legacy questions preserved `12`

Page 9/source 13 changes to time expressions and starts the next boundary. No question semantics were approved/re-written; no RAW/DB/publication mutation occurred.

## CURATION-002 — DONE / LESSON_BOUNDARY_VERIFIED

Evidence:
- commit `d14774adc68470e9eea48a1c388a14a66111bf57`
- `content-staging/curated/grade-9/english/pupil-book-3/curation-002-unit-2-time-and-meeting.json`

Reviewed Lesson:
- title `Telling time and arranging a meeting`
- book pages `9..10`
- source pages `13..14`
- ordered activity/page assets `2`
- legacy questions preserved `7`

Page 11/source 15 changes focus to obligations/tasks and remains outside this Lesson. No question semantics were approved/re-written; no RAW/Media/DB/publication mutation occurred.

## CONTENT-GAPS-001 — DONE / GAP_INVENTORY_VERIFIED

Evidence:
- inventory commit `dd86641decbcb3e3345d1aacfea7e2363fc60474`
- `content-staging/curated/grade-9/english/pupil-book-3/content-gaps-001.json`
- reconstruction blob `2d054712b6013675f7ad24d573c3a06745972067`

Exact Grade 9 English inventory:
- RAW page candidates/images: `69 / 69`
- legacy questions: `104`
- recovered sections: `8`
- reviewed boundary coverage: `10` pages
- unresolved boundary candidates: `59` pages
- Unit 2 immediate unresolved remainder: pages `11..15` / source `15..19` = `5` pages / `11` questions
- source-manifest-only evidence: book page `70`, source page `74`, `Blank Final Page`; evidence-only, no RAW identity
- Grade 9 English RAW duplicate page-number anomalies: `0`
- corpus-wide duplicate-position anomalies remain preserved: `6`
- verified modern page mappings in this rebuild track: `4`
- other `65` mappings remain `unverified`, not asserted missing

No PostgreSQL/RAW/Media/publication mutation occurred.

## MEDIA-001 — DONE / MEDIA_PROFILE_VERIFIED_PARTIAL_ACCEPTANCE

Scope: smallest reviewed media batch only — CURATION-001, book pages `5..8` / source pages `9..12`.

Evidence:
- deterministic probe script commit: `2f1849536738e3f877018539a80b73e83a969c3f`
- workflow commit: `10ce6c2b250de28b5de9389cbcaf9b2e7cddad09`
- GitHub Actions run: `34761171601` — SUCCESS
- artifact: `media-001-evidence`, ID `10318976732`
- artifact digest: `sha256:9702cbac1ed18e1be1809eaf844685b78c24c150958da1781ce0b7f1ad75e91a`
- decision contract commit: `bb3dbbeff5d866930c1921124a8868b79af5703e`
- `content-staging/curated/grade-9/english/pupil-book-3/media-001-unit2-describing.json`

Probe rules:
- dimensions must match RAW
- PSNR >= `32 dB`
- byte reduction >= `20%`
- accepted candidate requires manual contact-sheet legibility review

Measured aggregate:
- RAW JPEG total: `457,747` bytes
- WebP q82/method6 total: `464,290` bytes = `+1.43%` larger than RAW -> profile not accepted
- WebP q76/method6 total: `387,774` bytes = `15.29%` smaller overall, but page-level acceptance remains mandatory

Page-level decisions:
- page 5 RAW `93,793` -> q76 WebP `74,416` bytes, reduction `20.66%`, PSNR `39.52 dB`, dimensions `962x1360` unchanged; manual side-by-side review retained readable headings/body/labels/numbers and no material readability regression -> `ACCEPTED_AS_REPRODUCIBLE_DERIVED_CANDIDATE`
- page 6 q76 reduction `15.83%` -> rejected; q82 is larger than RAW
- page 7 q76 reduction `9.61%` -> rejected; q82 is larger than RAW
- page 8 q76 reduction `17.42%` -> rejected; q82 reduction only `0.24%`

Candidate count:
- accepted: `1`
- rejected: `7`

Important interpretation:
- q76 is **not** a global profile; only page 5 passed all gates.
- pages 6..8 retain RAW as the preferred media until a better candidate is verified.
- accepted page 5 derivative is reproducible from immutable RAW using the exact tested profile/checksum; no binary was pushed to production by MEDIA-001.
- RAW mutation: `0`
- PostgreSQL mutation: `0`
- publication change: `0`
- unrelated-record mutation: `0`

## IMPORT-001 — IN PROGRESS / ROLLBACK_GATE_VERIFIED

Smallest import scope remains CURATION-001 only:
- one reviewed Lesson: `Describing people and animals`
- book pages `5..8` / source pages `9..12`
- four ordered page/activity identities
- unresolved pages excluded
- no question import/rewrite authorized

Live identity inspection:
- successful deployment: `4cf8665b-4dd1-4e90-9ec8-92d897c34f59`
- marker: `IMPORT001_INSPECT_PASS`
- Grade 9/English active offering count: `1`
- Unit 1 existing Section count in scope: `1`
- Unit 2 target Section count: `0`
- target curated Lesson slug count: `0`
- exact source assets: `4`, all present with expected immutable checksums
- Media Assets: `4`, all `ready`
- existing Lesson Assets: `4`, all `draft` and unpublished
- legacy Lessons: `4`, active/unpublished and sectionless
- published lesson/asset count in scope: `0/0`

Rollback-only transaction gate:
- gate script commit: `177b91572ac6fe3b37acd9bcc094876a1cbb3beb`
- script: `content-staging/runtime/import-001-transaction-gate.mjs`
- Railway deployment: `8e4cdcbb-2783-4dca-b025-e1191fa9e330` — SUCCESS
- marker: `IMPORT001_TRANSACTION_GATE_PASS`
- rollback verified: `true`
- committed business writes: `0`

Exact validated intended PostgreSQL mutation for the eventual controlled apply:
- create Sections: `1`
- create Lessons: `1`
- reassign existing Lesson Assets: `4` in reviewed order `0..3`
- create Media Assets: `0`
- mutate Media Assets: `0`
- mutate legacy Lessons: `0`
- mutate Questions: `0`
- publication changes: `0`
- unrelated rows: `0`
- preserved legacy Question Revisions on old lessons: `12`

Reused Media Asset IDs:
- `3d53954b-95ef-4833-ae06-407f2325e28e`
- `9d4f61a2-8c00-44cf-9baa-7e48740e0ef6`
- `3aadf23a-432d-4391-bd2f-467eaefe486b`
- `b0b1d37e-1b9f-43a3-9987-4973423d822c`

Reused Lesson Asset IDs:
- `d8dfb014-23bb-4db0-b6c2-3aa8e98862eb`
- `b474bec6-8828-45e9-8b28-40ff0b52a9c2`
- `cec764c8-dce3-4917-8dea-66a36165ec89`
- `bdaca047-29a2-4730-81d5-2abd173a93ce`

Media interpretation for this import gate:
- existing Media Assets/variants are reused; no binary/media mutation occurs in this structural import transaction.
- page 5 accepted derived WebP remains a verified reproducible candidate, not silently substituted into production storage by IMPORT-001.
- pages 6..8 retain their current source/preferred media state.

No RAW/Media binary/PostgreSQL committed/publication/unrelated mutation occurred in the inspector or rollback gate.

Exact next action:
1. read both live heads again;
2. re-run strict identity/count/provenance drift guards immediately before write;
3. build controlled apply from the verified rollback gate with exactly `1 Section + 1 Lesson + 4 Lesson Asset reassignments`;
4. fail closed on any identity/count/checksum/publication drift;
5. perform no Question/Media/RAW/publication/unrelated mutation;
6. verify committed state independently before closing IMPORT-001;
7. do not start VERIFY-001 until IMPORT-001 committed state is verified.

## Gate checklist

- `BATCH-001` — DONE / COMMITTED_STATE_VERIFIED
- `STRUCTURE-001` — DONE / SECTION_BOUNDARY_VERIFIED
- `STRUCTURE-002` — DONE / SECTION_BOUNDARY_VERIFIED
- `CURATION-001` — DONE / LESSON_BOUNDARY_VERIFIED
- `CURATION-002` — DONE / LESSON_BOUNDARY_VERIFIED
- `CONTENT-GAPS-001` — DONE / GAP_INVENTORY_VERIFIED
- `MEDIA-001` — DONE / MEDIA_PROFILE_VERIFIED_PARTIAL_ACCEPTANCE
- `IMPORT-001` — IN PROGRESS / ROLLBACK_GATE_VERIFIED

## Remaining ordered queue

- `BATCH-001` — DONE
- `STRUCTURE-001` — DONE
- `STRUCTURE-002` — DONE
- `CURATION-001` — DONE
- `CURATION-002` — DONE
- `CONTENT-GAPS-001` — DONE
- `MEDIA-001` — DONE
- `IMPORT-001` — IN PROGRESS
- `VERIFY-001` — TODO
- `ROADMAP-RETURN -> STUDENT-016I` — TODO

At every run: read live heads + this file + handoff; continue the first incomplete task only; use the smallest reviewable batch; verify before declaring pass; update this file with exact SHAs/run IDs/counts/failures and next action.