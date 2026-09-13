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
- Live `main` observed at start of latest run: `54491c1b619322709fc5273eebadecf9f27fe4fb`
- Content repo: `7eaur/alwaslh-go`
- Live `master` observed at start of latest run: `f81ec3935bb363401950978014244720deb56cdc`
- Working branch: `content/legacy-staging-rebuild`
- Latest completed BATCH-001 work commit: `df3d7a795954143442b41697cb1fbb2f88f1e66b`
- Validation report commit: `e90891c6395813609d0f0cefe726c1cc3d4ac893`
- Legacy snapshot SHA-256: `2dfde94f6b70c037bb15d2782d11f036441c4abe130295be772c59b5e0131d0c`

## First real batch — ACTIVE

Target source:

- Batch: `BATCH-001-G9-EN-PB3-U1`
- Grade 9 English
- Legacy subject UUID: `1794eea5-4772-4c94-bd2b-b08e5815e733`
- Structural manifest: `تاسع انجليزي/الانجليزي_تاسع/manifest.json`
- Curated evidence: `content-staging/curated/grade-9/english/pupil-book-3/reconstruction-candidates.json`
- Bounded batch contract: `content-staging/curated/grade-9/english/pupil-book-3/batches/batch-001-unit-1-revision.json`
- DB/media validation report: `content-staging/curated/grade-9/english/pupil-book-3/batches/BATCH-001_DB_MEDIA_VALIDATION.md`

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

Per page the display WebP is larger by approximately +24.01%, +26.38%, +18.39%, and +30.57%.

Decision:

- RAW remains immutable.
- Do not claim current WebP profile as optimization success.
- Do not regenerate/overwrite RAW.
- A later derived profile may be accepted only if it is measurably smaller while preserving educational readability; otherwise retain the smaller readable source/delivery choice allowed by the application media contract.

### Gate for first batch

Completed for bounded BATCH-001:

1. `[DONE]` Identify smallest coherent structural slice: Unit 1 / four distinct boundaries.
2. `[DONE]` Verify DB linkage, RAW/source checksums, media provenance and question-source linkage read-only.
3. `[DONE]` Record exact current media sizes and reject the existing WebP profile as a size-reduction claim.
4. `[DONE]` Keep publication state closed: lessons unpublished, assets/questions draft.

Still required before direct DB mutation:

5. `[NEXT]` Semantically review the 13 prompts/options/answers against the four source pages; record approved/corrected/rejected decisions.
6. `[PENDING]` Produce modern target dry-run for one section + four curated lesson slugs, including handling of the existing unpublished legacy import so no duplicate semantic content is created.
7. `[PENDING]` Produce exact mutation/rollback counts from that dry-run.
8. `[PENDING]` Apply controlled PostgreSQL mutation only after all BATCH-001 gates pass.
9. `[PENDING]` Verify resulting records, publication visibility rules, idempotency/replay, and unrelated-row invariance.

Current batch contract status: `validation_in_progress`.

## Remaining work queue

- `BATCH-001` — First real Grade 9 English content batch: VALIDATION_IN_PROGRESS
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

Both scheduled workers MUST use this same file.

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

2026-09-13 — BATCH-001 advanced from a misleading `prepared_for_db_import` state back to the correct `validation_in_progress` gate after a successful production read-only inventory. The four-page Unit 1 slice has valid provenance/media/question linkage, but its 13 questions still require semantic source-page review and the existing display WebP profile is 24.81% larger than RAW in aggregate. No DB mutation or publication occurred. Next action is question-by-question semantic review, then modern target dry-run with duplicate-safe handling of the prior unpublished legacy import.
