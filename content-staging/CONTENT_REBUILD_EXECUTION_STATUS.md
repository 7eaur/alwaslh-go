# Alwaslh Content Rebuild — Shared Execution Status

> الملف المشترك لجميع جولات التنفيذ المجدولة. يجب قراءة آخر نسخة منه + آخر commits قبل أي عمل، ثم تحديثه في نهاية كل دفعة. لا تعتمد على ذاكرة المحادثة.

## Current direction — 2026-09-13

- Product Owner ألغى فكرة Published Student Demo المعزول.
- PR `7eaur/alwaslh#56` أُغلق بدون merge.
- المطلوب الآن: تجهيز **أول دفعة حقيقية** من المحتوى الموجود في `7eaur/alwaslh-go` ثم إدخالها مباشرة إلى قاعدة Alwaslh الحديثة بعد اجتياز validation الخاصة بهذه الدفعة.
- لا يتم إدخال RAW كما هو، ولا يتم الرجوع إلى heuristic `69 pages -> 62 lessons`.
- RAW يبقى immutable.

## Repository checkpoints

- Application repo: `7eaur/alwaslh`
- Live `main` observed at start of latest run: `343ff1fd7b3d64d7e990b72606695365f520fa58`
- Content repo: `7eaur/alwaslh-go`
- Working branch: `content/legacy-staging-rebuild`
- Live working-branch HEAD observed at start of latest run: `3c6f8f2f5d549a1ee0b6f41f50a9abf1dc9b9c11`
- BATCH-001 dry-run report commit: `557527bf59c71fdeb05c095bda1b4dedc94f8ea2`
- Duplicate-safe batch-contract commit: `e008731860612a58d7e3b4a29ec97222ceb62305`
- Previous semantic-review data commit: `4f2fb8d0a559add5b6c2e75c92bf075fabae32f5`
- Question-review artifact commit: `eae7b9d8b3b61b20f4ca74cb75f222aa5b6f9e60`
- DB/media validation report commit: `e90891c6395813609d0f0cefe726c1cc3d4ac893`
- Legacy snapshot SHA-256: `2dfde94f6b70c037bb15d2782d11f036441c4abe130295be772c59b5e0131d0c`

## First real batch — ACTIVE

Target source:

- Batch: `BATCH-001-G9-EN-PB3-U1`
- Grade 9 English
- Legacy subject UUID: `1794eea5-4772-4c94-bd2b-b08e5815e733`
- Structural manifest: `تاسع انجليزي/الانجليزي_تاسع/manifest.json`
- Curated evidence: `content-staging/curated/grade-9/english/pupil-book-3/reconstruction-candidates.json`
- Bounded batch contract: `content-staging/curated/grade-9/english/pupil-book-3/batches/batch-001-unit-1-revision.json`
- Question semantic review: `content-staging/curated/grade-9/english/pupil-book-3/batches/batch-001-question-review.json`
- DB/media validation report: `content-staging/curated/grade-9/english/pupil-book-3/batches/BATCH-001_DB_MEDIA_VALIDATION.md`
- Modern target dry-run: `content-staging/curated/grade-9/english/pupil-book-3/batches/BATCH-001_MODERN_TARGET_DRY_RUN.md`

Known corpus facts:

- 69 RAW pages / images
- 8 recovered sections
- 104 questions
- page 70 = manifest-only `Back Matter / Blank Final Page` evidence only
- full reconstruction candidates are page candidates, **not final lessons**
- full curated publication status remains `not_importable`

### BATCH-001 bounded decision

For the first bounded slice only, manifest + source evidence supports one section `Unit 1 - Revision` containing four distinct lesson/activity boundaries:

1. `Presents from London` — book page 1 — 4 questions
2. `What's my job?` — book page 2 — 4 questions
3. `The holidays` — book page 3 — 3 questions
4. `A postcard from London` — book page 4 — 2 questions

This is **not** a global one-page-equals-one-lesson rule.

### Latest production read-only validation

Inspector source checkpoint: `a4ec103a0bb36a40f144a65ee6635a70f15f059a`

Railway deployment: `00e69a2d-05f4-4e22-9449-5d82f80c8849`

Result:

- modern `grade-9` class: active
- modern `english` subject: active
- offering: active
- curriculum sections currently present for this scope: 0
- four corresponding legacy-import lessons found: 4, all unpublished
- lesson assets: 4, all draft
- ready media assets with immutable source provenance: 4
- source media variants: 4
- display WebP variants: 4
- thumbnail variants: 4
- AI variants: 4
- question revisions linked to the four pages: 13, all draft/unpublished
- source links for those 13 question revisions: present
- active student entitlements observed: 2; this does not bypass publication gates
- PostgreSQL writes during this validation: **0**

### Media result

Existing display WebP profile is readable/derived but is **not a size optimization** for these four pages:

- RAW JPEG total: `440,502` bytes
- current display WebP total: `549,794` bytes
- delta: `+24.81%`

Decision:

- RAW remains immutable.
- Do not claim current WebP profile as optimization success.
- Do not regenerate/overwrite RAW.
- No media transformation belongs in BATCH-001's controlled apply unless a later profile proves smaller and readable.

### Semantic question review — COMPLETED

All 13 legacy AI questions in the four-page slice were reviewed against the matching Unit 1 source-page content and page structure.

Result:

- reviewed: **13**
- approved unchanged: **6**
- corrected with source-grounded wording/options: **7**
- rejected: **0**
- auto-published: **0**

The machine-readable reviewed set is the only question input permitted for apply planning. Legacy raw questions remain immutable evidence and are not overwritten.

### Modern target dry-run — COMPLETED

Dry-run result: `MODERN_TARGET_DRY_RUN_PASS / APPLY_NOT_AUTHORIZED_YET`.

The previous contract incorrectly projected creation of 4 new lessons + 13 new Question Bank identities even though the production inventory already contains the matching unpublished semantic rows. That projection is now corrected to duplicate-safe reuse.

Verified target effect under the documented pre-state:

- new curriculum section: **1 max / expected 1**
- new lessons: **0**; reuse/update existing: **4**
- new lesson assets: **0**; reuse existing draft assets: **4**
- new media/source rows: **0**; reuse existing ready media: **4**
- new Question Bank items/revisions: **0**
- existing reviewed question revisions: **13**
  - semantic no-op: **6**
  - source-grounded content updates: **7**
- new revision lesson/source links: **0**
- direct business-row mutations expected: **12** = 1 section insert + 4 lesson structural updates + 7 draft revision content updates
- unrelated rows changed: **0**
- publication changes: **0**

All other legacy-import lesson/question rows remain untouched. No archive/deactivate/delete is used to hide the old `62` count.

Rollback is value-restoring for the four reused lessons and seven corrected draft revisions; it must not delete those pre-existing identities. The newly created section is removable only after restoring lesson section references. Media/source/RAW remain preserved.

### Gate for first batch

Completed for bounded BATCH-001:

1. `[DONE]` Identify smallest coherent structural slice: Unit 1 / four distinct boundaries.
2. `[DONE]` Verify DB linkage, RAW/source checksums, media provenance and question-source linkage read-only.
3. `[DONE]` Record exact current media sizes and reject the existing WebP profile as a size-reduction claim.
4. `[DONE]` Keep publication state closed: lessons unpublished, assets/questions draft.
5. `[DONE]` Semantically review all 13 prompts/options/answers; 6 approved unchanged, 7 corrected, 0 rejected.
6. `[DONE]` Produce duplicate-safe modern target dry-run and correct the batch contract away from duplicate creation.
7. `[DONE]` Produce dry-run mutation/rollback counts: 12 expected direct business-row mutations; 0 unrelated mutations.

Still required before direct DB mutation:

8. `[NEXT]` Build/verify an executable controlled PostgreSQL apply + rollback transaction that re-resolves all live identities immediately before mutation and aborts on drift/ambiguity; enumerate any required append-only curriculum/question audit-event rows explicitly.
9. `[PENDING]` Apply controlled PostgreSQL mutation only after that executable transaction gate passes.
10. `[PENDING]` Verify resulting records, publication visibility rules, idempotency/replay, and unrelated-row invariance.

Current batch contract status: `dry_run_validated`.

## Remaining work queue

- `BATCH-001` — First real Grade 9 English content batch: DRY_RUN_VALIDATED / APPLY_TRANSACTION_NEXT
- `STRUCTURE-001` — Structural Manifest Coverage Inventory for all 58 sources: TODO
- `STRUCTURE-002` — Canonical Document Boundaries: TODO
- `CURATION-001` — Complete Grade 9 English Lesson/Activity boundaries: TODO
- `CURATION-002` — Reusable Curated Contract: TODO
- `CONTENT-GAPS-001` — Missing content classification: TODO
- `MEDIA-001` — Derived image optimization after curation gate: TODO
- `IMPORT-001` — Incremental production import of reviewed batches: TODO
- `VERIFY-001` — Student/Admin/runtime verification after each imported batch: TODO
- `ROADMAP-RETURN` — Return to `STUDENT-016I` only after content work reaches its documented gate: TODO

## Scheduled-run coordination rules

At the start of every run:

1. Read this file, `CONTENT_REBUILD_HANDOFF.md`, live `alwaslh main`, live `alwaslh-go master`, and live `alwaslh-go/content/legacy-staging-rebuild` HEADs.
2. Compare the latest commits with the checkpoint recorded here.
3. Continue the **first incomplete task** only; never redo completed work.
4. If another run already advanced the same task, continue from its newest checkpoint instead of overwriting it.
5. Work in one bounded, reviewable batch.
6. Run relevant verification/tests before declaring a batch complete.
7. Update this file with evidence, commit SHA, counts, failures, and exact next action.
8. Also update `CONTENT_REBUILD_HANDOFF.md` when a product/content truth changes materially.

Never:

- mutate RAW in-place;
- publish AI-generated content automatically;
- delete anomalies to make counts look clean;
- import unreviewed page candidates as lessons;
- assume a legacy Subject equals one final Document;
- continue from memory when repository evidence differs.

## Latest execution note

2026-09-13 — BATCH-001 modern target dry-run completed without PostgreSQL writes. Dry-run report commit `557527bf59c71fdeb05c095bda1b4dedc94f8ea2`; duplicate-safe contract correction commit `e008731860612a58d7e3b4a29ec97222ceb62305`. The plan now reuses the four existing unpublished lessons, four draft lesson assets, four ready media identities and thirteen existing draft Question Bank identities; it creates no duplicate lesson/question/media rows. Expected direct future business-row mutation set is exactly 12 under the verified pre-state: 1 section insert + 4 lesson structural updates + 7 reviewed draft question corrections. PostgreSQL writes in this run: **0**. Next action is executable controlled apply/rollback transaction verification against live identities immediately before mutation.