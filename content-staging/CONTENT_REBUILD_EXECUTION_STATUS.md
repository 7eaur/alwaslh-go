# Alwaslh Content Rebuild — Shared Execution Status

> الملف المشترك لجميع جولات التنفيذ. اقرأ هذه النسخة + live heads قبل أي عمل، ثم أكمل أول مهمة غير مكتملة فقط. لا تعتمد على ذاكرة المحادثة.

## Current direction — 2026-09-13

- المسار: `Legacy Supabase -> Immutable RAW -> Reviewed CURATED -> Media Decision -> Dry Run -> Controlled Transaction -> Modern PostgreSQL -> Verification -> Publication`.
- لا تستخدم heuristic القديم `69 -> 62` كحقيقة منهجية.
- RAW immutable.
- لا auto-publish لأي AI/legacy content غير مراجع.
- لا حذف anomalies أو تعديل بيانات غير مرتبطة لتجميل الأرقام.
- أي apply يفشل مغلقًا عند identity/count/provenance drift.

## Live repository heads observed at start of this run

- `7eaur/alwaslh main`: `343ff1fd7b3d64d7e990b72606695365f520fa58`
- `7eaur/alwaslh-go master`: `f81ebb6ef6198818fa091f7a8c1c81b4de7dbd23`
- `7eaur/alwaslh-go content/legacy-staging-rebuild`: `f8e8b09e6d758343abb684101f17edb3aa2b3c69`

Working-branch commits added in this run:

- runtime gate root-cause fix: `3cd817414275aa31bcd67e7015ce48740409a43c`
- controlled SQL parity fix: `c8c15e1d04b7bb353f6ee0755beec7b33c66a7c2`

Previous validated checkpoints retained:

- controlled SQL first implementation: `fa661bd9dfa2551a19d1163752dcaa605af74ee7`
- rollback-gate runtime first implementation: `c782755e5fc213b0018d7aeaa569d5e521b5d5e5`
- modern target dry-run: `557527bf59c71fdeb05c095bda1b4dedc94f8ea2`
- duplicate-safe batch contract: `e008731860612a58d7e3b4a29ec97222ceb62305`
- semantic review: `eae7b9d8b3b61b20f4ca74cb75f222aa5b6f9e60`
- DB/media validation: `e90891c6395813609d0f0cefe726c1cc3d4ac893`
- legacy snapshot SHA-256: `2dfde94f6b70c037bb15d2782d11f036441c4abe130295be772c59b5e0131d0c`

## BATCH-001 — ACTIVE

Batch: `BATCH-001-G9-EN-PB3-U1`

Target: Grade 9 / English / Pupil Book 3 / `Unit 1 - Revision`.

Reviewed boundaries for this batch only:

1. `Presents from London` — page 1 — 4 questions
2. `What's my job?` — page 2 — 4 questions
3. `The holidays` — page 3 — 3 questions
4. `A postcard from London` — page 4 — 2 questions

This does not establish a global one-page-equals-one-lesson rule.

### Validated production pre-state

- active `grade-9` + active `english` + active offering
- target curriculum section count: `0`
- exact existing target lessons: `4`, active and unpublished
- lesson assets: `4`, all `draft`
- ready media/source chains: `4`
- reviewed Question Bank draft revisions: `13`, unpublished
- question source links: `13/13`
- active student entitlements observed: `2`; publication gates remain closed

### Media decision

- RAW JPEG total: `440,502` bytes
- current display WebP total: `549,794` bytes
- delta: `+24.81%`

Current display WebP is not accepted as an optimization success. No media mutation belongs in BATCH-001 apply. RAW stays immutable.

### Semantic question gate — COMPLETE

- reviewed: `13`
- approved unchanged: `6`
- corrected from source evidence: `7`
- rejected: `0`
- auto-published: `0`

Authoritative review artifact:
`content-staging/curated/grade-9/english/pupil-book-3/batches/batch-001-question-review.json`.

### Modern target dry-run — COMPLETE

Duplicate-safe target:

- insert curriculum section: `1`
- insert lessons: `0`; reuse/update exact existing lessons: `4`
- insert lesson assets/media/source rows: `0`
- insert Question Bank identities/revisions/links: `0`
- update reviewed draft revisions: `7`
- question no-ops: `6`
- direct business-row mutations: `12 = 1 + 4 + 7`
- publication mutations: `0`
- unrelated mutations: `0`

No archive/deactivate/delete is used to erase the legacy `62` state.

## Controlled transaction / rollback gate — COMPLETE

### Failure discovered in this run

Latest pre-fix Railway deployment `b140e5c9-d5cd-495a-af55-7386b9515d8d` failed closed before mutation with:

`GATE_FAIL: source تاسع انجليزي/الانجليزي_تاسع/الصور/p001 - Presents from London.jpg resolved 0 modern lessons; expected exactly 1`

Root cause was not missing content. The gate incorrectly used the local immutable RAW extraction path as `content_source_assets.source_path`.

The previously validated live DB evidence shows the canonical imported source identities are:

- `public.lessons/2d98475c-91bf-4000-bfbc-79f7a6a854f9/image/0`
- `public.lessons/5e207993-508f-426b-ae71-f00aa4f782df/image/0`
- `public.lessons/dc1d6249-c0cb-4982-9711-092b1dcffee3/image/0`
- `public.lessons/f2947d7f-5697-4bdc-b561-ad880a1afdf1/image/0`

with the same immutable SHA-256 values already validated for pages 1–4.

### Root-cause fix

Commit `3cd817414275aa31bcd67e7015ce48740409a43c` changed the live rollback gate to:

- use canonical PostgreSQL source path + SHA-256 for identity;
- keep local RAW path documentary/immutable only;
- also require the expected legacy lesson slug before mutation;
- require each Question Bank source to match the same `content_source_asset_id` in addition to page + checksum;
- post-rollback verify the section, all 4 lesson identities, and all 7 corrected question prompts returned to pre-state.

Commit `c8c15e1d04b7bb353f6ee0755beec7b33c66a7c2` made `batch-001-controlled-apply.sql` use the same canonical provenance rules. It still defaults to rollback and requires explicit `-v apply=true` for COMMIT.

### Live rollback verification — PASS

Railway service: `alwaslh-content-inspector` (existing service reused; no new service created).

Verified deployment:

- deployment: `a79244c2-731a-4573-b86b-089d31254933`
- commit: `3cd817414275aa31bcd67e7015ce48740409a43c`
- result: `SUCCESS`

Required marker 1 observed:

`BATCH001_GATE_MUTATION_PHASE_PASS`

Counts:

- `sectionInserts=1`
- `lessonUpdates=4`
- `questionUpdates=7`
- `questionNoops=6`
- `correctedPostCount=7`
- `auditRowsRequiredBySchema=0`
- `publicationChanges=0`
- `unrelatedRows=0`
- `expectedRollback=true`

Required marker 2 observed:

`BATCH001_GATE_PASS_ROLLBACK_VERIFIED`

Rollback post-state:

- `postRollbackSectionCount=0`
- `postRollbackLessonCount=4`
- `postRollbackQuestionCount=7`

Resolved modern lesson IDs remained exactly:

- `767ec1b0-1447-4cb6-824f-4a544d709837`
- `2959accf-c984-44f1-9959-c3d1507c8ce7`
- `bb066699-f2ba-4b7e-bcdb-d6b313cdbc84`
- `df8d57bd-ff0c-4303-abe1-83874838bc88`

Committed PostgreSQL business writes in this run: **0**.
Publication changes in this run: **0**.
RAW/media changes in this run: **0**.

The later auto-deployment for SQL-only commit `c8c15e1d04b7bb353f6ee0755beec7b33c66a7c2` was still building when this checkpoint was written; it does not invalidate the successful rollback proof above because the runtime gate file is unchanged from the verified `3cd8174...` version.

## Gate checklist

1. `[DONE]` Bound Unit 1 into 4 reviewed Lesson/Activity boundaries.
2. `[DONE]` Verify DB/media/provenance read-only.
3. `[DONE]` Reject oversized current WebP profile as optimization success.
4. `[DONE]` Keep publication closed.
5. `[DONE]` Review all 13 questions: 6 unchanged / 7 corrected / 0 rejected.
6. `[DONE]` Produce duplicate-safe modern target dry-run.
7. `[DONE]` Fix expected direct effect at exactly 12 business rows.
8. `[DONE]` Controlled apply/rollback executor implemented, root-cause corrected, and live rollback verified.
9. `[PENDING]` Perform controlled PostgreSQL apply of the exact same bounded set only.
10. `[PENDING]` Verify committed rows, publication invariants, replay/idempotency, and unrelated-row invariance.

Current batch status: `CONTROLLED_TRANSACTION_VERIFIED / APPLY_PENDING`.

## Exact next action

On the next run:

1. Re-read live heads and this status/handoff.
2. Confirm no drift since the successful rollback gate: target section still absent, four canonical provenance chains resolve uniquely, 13 reviewed revisions remain draft, and no target publication occurred.
3. Execute the existing controlled apply with explicit commit authorization for **only** `1 section + 4 lesson updates + 7 reviewed question corrections`.
4. Immediately verify committed counts, publication remains closed, RAW/media remain unchanged, and unrelated rows remain invariant.
5. Do not start `STRUCTURE-001` until BATCH-001 committed apply + verification is documented.

## Remaining ordered queue

- `BATCH-001` — `CONTROLLED_TRANSACTION_VERIFIED / APPLY_PENDING`
- `STRUCTURE-001` — TODO
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
