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

- `7eaur/alwaslh main`: `343ff1fd7b3d64d7e990b72606695365f520fa58`
- `7eaur/alwaslh-go master`: `f81ebb6ef6198818fa091f7a8c1c81b4de7dbd23`
- work branch at start: `content/legacy-staging-rebuild` = `0f6b7036ae025071bce7d25f535868a1369f7b15`

## BATCH-001 — CLOSED / COMMITTED STATE VERIFIED

Batch: `BATCH-001-G9-EN-PB3-U1`

Target: Grade 9 / English / Pupil Book 3 / `Unit 1 - Revision`.

Reviewed boundaries:
1. `Presents from London` — page 1 — 4 questions
2. `What's my job?` — page 2 — 4 questions
3. `The holidays` — page 3 — 3 questions
4. `A postcard from London` — page 4 — 2 questions

This does not establish a global one-page-equals-one-lesson rule.

### Prior completed gates retained

- semantic review: `13` reviewed = `6` unchanged + `7` corrected + `0` rejected
- duplicate-safe dry-run: exact intended business effect `12 = 1 section + 4 lesson updates + 7 question corrections`
- publication mutations expected: `0`
- unrelated mutations expected: `0`
- rollback transaction gate previously verified live
- runtime gate root-cause fix: `3cd817414275aa31bcd67e7015ce48740409a43c`
- controlled SQL parity: `c8c15e1d04b7bb353f6ee0755beec7b33c66a7c2`
- modern target dry-run: `557527bf59c71fdeb05c095bda1b4dedc94f8ea2`
- duplicate-safe contract: `e008731860612a58d7e3b4a29ec97222ceb62305`
- semantic review: `eae7b9d8b3b61b20f4ca74cb75f222aa5b6f9e60`
- DB/media validation: `e90891c6395813609d0f0cefe726c1cc3d4ac893`
- immutable legacy snapshot SHA-256: `2dfde94f6b70c037bb15d2782d11f036441c4abe130295be772c59b5e0131d0c`

### Media decision remains unchanged

- RAW JPEG total: `440,502` bytes
- existing display WebP total: `549,794` bytes
- delta: `+24.81%`
- current WebP profile is not an optimization success
- BATCH-001 performed no RAW/media mutation

## This run — concurrent advancement detected and handled safely

A bounded commit executor was added in commit:
- `cebde403957b5932d4dd123784a6684e1be77bd3`

Its explicit Railway apply deployment:
- `90867b02-30af-4886-9dbf-b26f0c1d8281`

failed closed before mutation because the first lesson no longer had its expected legacy slug. No writes from that executor were committed.

The failure was treated as live-state drift, not bypassed.

A read-only state inspector was added in:
- `d0a7efff94683d5647c81b0589c6b2bfab822fa6`

Railway deployment:
- `bb20e38e-4167-4706-9e0d-b3e514206704`
- result: `SUCCESS`

It proved that the exact intended BATCH-001 target state had already advanced in PostgreSQL through another concurrent path before this run's apply could execute. We did not overwrite or re-apply it.

Observed committed state:
- target Section: exactly `1`
- Section ID: `1b4a98df-014d-4815-b496-46891df3f3f7`
- exact reused Lessons: `4`
- exact Lesson Assets: `4`, all still `draft`
- exact Media Assets: `4`, all `ready`
- Question Revisions: `13`
- corrected questions present: `7`
- unchanged questions present: `6`
- publication: lessons `0`, lesson assets `0`, questions `0`

Exact lesson IDs remained:
- `767ec1b0-1447-4cb6-824f-4a544d709837`
- `2959accf-c984-44f1-9959-c3d1507c8ce7`
- `bb066699-f2ba-4b7e-bcdb-d6b313cdbc84`
- `df8d57bd-ff0c-4303-abe1-83874838bc88`

## Post-apply committed-state verification — PASS

Read-only verifier added in:
- `1fdbb809da5030ce32a283c3765f90847d76ba0b`

Verified Railway deployment:
- `c3e609b3-f632-46e9-9fde-680330512eee`
- result: `SUCCESS`
- required marker: `BATCH001_POST_APPLY_VERIFY_PASS`

Verified counts/invariants:
- curriculum sections: target exactly `1`
- lessons: `4`
- lesson assets: `4`
- media assets: `4`
- question revisions: `13`
- question source/provenance links: `13/13`
- corrected: `7`
- unchanged: `6`
- target-slug duplicates: `0`
- display variants: `4`
- display WebP bytes: `549,794` unchanged
- all media variant rows for the 4 media assets: `16`
- published lessons: `0`
- published lesson assets: `0`
- published questions: `0`

Canonical source path + immutable SHA-256 chains still resolve uniquely for all four lessons. Question provenance remains bound to the matching canonical source asset/checksum.

### Mutation attribution for this run

- writes committed by this run's explicit apply executor: `0`
- reason: fail-closed drift guard triggered before mutation
- target state found already committed by concurrent advancement: exact intended BATCH-001 state
- no duplicate apply attempted after detection
- publication changes by this run: `0`
- RAW/media changes by this run: `0`

## Gate checklist

1. `[DONE]` Bound Unit 1 into 4 reviewed Lesson/Activity boundaries.
2. `[DONE]` Verify DB/media/provenance read-only.
3. `[DONE]` Reject oversized current WebP profile as optimization success.
4. `[DONE]` Keep publication closed.
5. `[DONE]` Review all 13 questions: 6 unchanged / 7 corrected / 0 rejected.
6. `[DONE]` Produce duplicate-safe modern target dry-run.
7. `[DONE]` Fix expected direct effect at exactly 12 business rows.
8. `[DONE]` Controlled rollback executor verified live.
9. `[DONE]` Detect committed target state without re-applying concurrent work.
10. `[DONE]` Verify committed rows, provenance, duplicates, publication and media invariants.

Current batch status: `BATCH-001 = CLOSED / COMMITTED_STATE_VERIFIED`.

## Exact next action

Do not perform more BATCH-001 mutation. On the next run:
1. read live heads + status + handoff;
2. confirm BATCH-001 remains stable if any new drift is visible;
3. start `STRUCTURE-001` only, using the smallest reviewable structural batch;
4. keep BATCH-001 content unpublished until its later explicit publication gate.

## Remaining ordered queue

- `BATCH-001` — DONE: `CLOSED / COMMITTED_STATE_VERIFIED`
- `STRUCTURE-001` — NEXT
- `STRUCTURE-002` — TODO
- `CURATION-001` — TODO
- `CURATION-002` — TODO
- `CONTENT-GAPS-001` — TODO
- `MEDIA-001` — TODO
- `IMPORT-001` — TODO
- `VERIFY-001` — TODO
- `ROADMAP-RETURN -> STUDENT-016I` — TODO

## Run rules

At every run: read live heads + this file + handoff; continue the first incomplete task only; use the smallest reviewable batch; verify before declaring pass; update this file with exact SHAs, deployment IDs, counts, failures, and next action.

Never mutate RAW in place, auto-publish legacy/AI content, use `69 -> 62` as curriculum truth, delete anomalies for cosmetic counts, import unreviewed candidates, or mutate unrelated records.
