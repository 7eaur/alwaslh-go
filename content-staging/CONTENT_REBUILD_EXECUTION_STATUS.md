# Alwaslh Content Rebuild — Shared Execution Status

> الملف المشترك لجميع جولات التنفيذ. اقرأ هذه النسخة + live heads قبل أي عمل، ثم أكمل أول مهمة غير مكتملة فقط. لا تعتمد على ذاكرة المحادثة.

## Current direction — 2026-09-13

- المطلوب تجهيز دفعات محتوى حقيقية ومراجعة من `7eaur/alwaslh-go` ثم إدخالها إلى PostgreSQL الحديثة فقط بعد validation + dry-run + controlled transaction gate.
- لا يتم إدخال RAW كما هو، ولا يتم استخدام heuristic القديم `69 -> 62`.
- RAW immutable.
- لا auto-publish لأي محتوى AI/legacy غير مراجع.
- لا حذف anomalies أو بيانات غير مرتبطة لإخفاء المشاكل.

## Repository checkpoints

Live heads observed at start of this run:

- `7eaur/alwaslh main`: `691263d816185447a173ec80ccc82e58cec2325f`
- `7eaur/alwaslh-go master`: `eec62d26193164c6be91c0ade36805abfd3687d0`
- `7eaur/alwaslh-go content/legacy-staging-rebuild`: `219b5347d4a6be7c6bf5113247a6e046152d3835`

This run advanced the working branch with:

- controlled SQL executor: `fa661bd9dfa2551a19d1163752dcaa605af74ee7`
  - `content-staging/tools/batch-001-controlled-apply.sql`
- live rollback-gate runtime: `c782755e5fc213b0018d7aeaa569d5e521b5d5e5`
  - `content-staging/runtime/batch-001-transaction-gate.mjs`

Previous validated checkpoints:

- modern target dry-run report: `557527bf59c71fdeb05c095bda1b4dedc94f8ea2`
- duplicate-safe batch contract: `e008731860612a58d7e3b4a29ec97222ceb62305`
- semantic review artifact: `eae7b9d8b3b61b20f4ca74cb75f222aa5b6f9e60`
- DB/media validation report: `e90891c6395813609d0f0cefe726c1cc3d4ac893`
- legacy snapshot SHA-256: `2dfde94f6b70c037bb15d2782d11f036441c4abe130295be772c59b5e0131d0c`

## BATCH-001 — ACTIVE

Batch: `BATCH-001-G9-EN-PB3-U1`

Target: Grade 9 / English / Pupil Book 3 / `Unit 1 - Revision`.

Bounded reviewed structure:

1. `Presents from London` — page 1 — 4 questions
2. `What's my job?` — page 2 — 4 questions
3. `The holidays` — page 3 — 3 questions
4. `A postcard from London` — page 4 — 2 questions

This is batch-specific and is not a global one-page-equals-one-lesson rule.

### Production pre-state already validated

- active `grade-9` class + active `english` subject + active offering
- matching curriculum section: `0`
- exact existing target lessons: `4`, all unpublished
- lesson assets: `4`, all `draft`
- ready media/source provenance chains: `4`
- reviewed Question Bank draft revisions: `13`, all unpublished
- question source links: present for all `13`
- active student entitlements observed: `2`; publication gates remain closed

### Media decision

- RAW JPEG total: `440,502` bytes
- current display WebP total: `549,794` bytes
- current WebP delta: `+24.81%`

Therefore current WebP profile is not accepted as an optimization success. RAW remains immutable and no media transformation belongs in BATCH-001 apply.

### Semantic question gate — COMPLETE

- reviewed: `13`
- approved unchanged: `6`
- corrected from source evidence: `7`
- rejected: `0`
- auto-published: `0`

Authoritative input: `content-staging/curated/grade-9/english/pupil-book-3/batches/batch-001-question-review.json`.

### Modern target dry-run — COMPLETE

Duplicate-safe target:

- insert section: `1`
- insert lessons: `0`; reuse/update exact existing lessons: `4`
- insert lesson assets/media/source rows: `0`
- insert Question Bank items/revisions/links: `0`
- update reviewed draft revisions: `7`
- question no-ops: `6`
- expected direct business-row mutations: `12` = `1 + 4 + 7`
- unrelated mutations: `0`
- publication mutations: `0`

No archive/deactivate/delete is used to erase the legacy `62` count.

## Controlled apply / rollback gate — IMPLEMENTED, LIVE VERIFICATION PENDING

Schema contracts were re-read from current `7eaur/alwaslh main` migrations before implementation:

- `database/migrations/0001_core.sql`
- `0008_content_source_import.sql`
- `0009_media_pipeline.sql`
- `0016_curriculum_structure.sql`
- `0017_content_ingestion_publication.sql`
- `0019_question_bank.sql`
- `0026_legacy_supabase_import_support.sql`

### Executor guarantees

`content-staging/tools/batch-001-controlled-apply.sql` now:

- defaults to `apply=false` and ends in `ROLLBACK`;
- requires explicit `-v apply=true` before a COMMIT is possible;
- resolves the active `grade-9 / english` offering immediately before mutation;
- locks scope, 4 exact lesson identities, and 13 exact draft revisions;
- fails closed if the target section already exists, if an identity resolves zero/multiple rows, or if counts drift;
- validates exact lesson -> lesson_asset -> ready media -> content_source_asset provenance path/checksum for all 4 pages;
- validates all 13 question locators by exact lesson linkage + current prompt + page/checksum provenance;
- creates no replacement lesson/question/media identity on drift;
- exercises only the planned `1 section + 4 lesson + 7 question` changes;
- post-validates publication remains closed;
- accounts for audit rows explicitly: `0` required by schema for this migration gate. `question_bank_events` requires a real actor and none is fabricated because lifecycle state is not changed; review/publish events remain application-owned.

`content-staging/runtime/batch-001-transaction-gate.mjs` mirrors the same bounded transaction for a live Railway rollback test and deliberately throws a sentinel after post-validation so postgres.js rolls the transaction back. It then performs an out-of-transaction post-check requiring the target section count to return to `0`.

### Live verification state in this run

Railway project: `charming-peace`

Existing utility service reused: `alwaslh-content-inspector`.

- No new Railway service/resource was created.
- Service source already points to `7eaur/alwaslh-go`, branch `content/legacy-staging-rebuild`, root `content-staging/runtime`.
- Start command was staged/changed to `node batch-001-transaction-gate.mjs` for the rollback-only gate.
- Deployment `21020740-d3ff-4848-bf87-6cb2a4299021` was still `BUILDING` at the end of this checkpoint and had not produced execution logs yet.
- Two Railway Agent one-off execution attempts timed out and were not counted as verification success.
- PostgreSQL committed writes from this run: **0 known/authorized**.
- Publication changes from this run: **0**.

Do **not** mark transaction gate PASS until Railway logs contain both:

1. `BATCH001_GATE_MUTATION_PHASE_PASS` with counts `sectionInserts=1`, `lessonUpdates=4`, `questionUpdates=7`, `questionNoops=6`, `publicationChanges=0`, `unrelatedRows=0`.
2. `BATCH001_GATE_PASS_ROLLBACK_VERIFIED` with `postRollbackSectionCount=0`.

The Railway build wait is treated as a transient execution blocker, not authorization to skip verification or apply the batch.

## Gate checklist

1. `[DONE]` Bound Unit 1 into 4 reviewed Lesson/Activity boundaries.
2. `[DONE]` Verify DB/media/provenance read-only.
3. `[DONE]` Reject current oversized WebP profile as optimization success.
4. `[DONE]` Keep publication closed.
5. `[DONE]` Review all 13 questions: 6 unchanged / 7 corrected / 0 rejected.
6. `[DONE]` Produce duplicate-safe modern target dry-run.
7. `[DONE]` Fix expected effect at exactly 12 direct business-row mutations.
8. `[PARTIAL]` Controlled apply/rollback executor implemented and schema-audited; live rollback execution is waiting on Railway deployment completion.
9. `[PENDING]` Only after step 8 passes, perform controlled PostgreSQL apply of the same bounded set.
10. `[PENDING]` Verify resulting rows, publication rules, replay/idempotency, and unrelated-row invariance.

Current batch status: `controlled_transaction_implemented_live_rollback_pending`.

## Exact next action

On the next run, first re-read live heads. Then inspect Railway deployment `21020740-d3ff-4848-bf87-6cb2a4299021` for completion/logs. If it did not execute the gate because the start-command change landed after that build, trigger a redeploy of the existing inspector service only; do not create a service. Require the two PASS log markers above. If the live rollback gate reveals a real schema/data drift, fix that root cause in the executor and repeat rollback-only verification. Do **not** apply/commit BATCH-001 in the same step unless the transaction gate is first proven clean and the next-task boundary is reached.

## Remaining work queue

- `BATCH-001` — `CONTROLLED_TRANSACTION_IMPLEMENTED / LIVE_ROLLBACK_PENDING`
- `STRUCTURE-001` — TODO
- `STRUCTURE-002` — TODO
- `CURATION-001` — TODO
- `CURATION-002` — TODO
- `CONTENT-GAPS-001` — TODO
- `MEDIA-001` — TODO
- `IMPORT-001` — TODO
- `VERIFY-001` — TODO
- `ROADMAP-RETURN` to `STUDENT-016I` — TODO

## Run rules

At every run: read live heads + this file + handoff; continue first incomplete task only; use smallest reviewable batch; verify before declaring pass; update this file with commit/deployment/count/failure/next action.

Never mutate RAW in place, auto-publish legacy/AI content, use `69 -> 62`, delete anomalies for cosmetic counts, import unreviewed candidates, or mutate unrelated records.
