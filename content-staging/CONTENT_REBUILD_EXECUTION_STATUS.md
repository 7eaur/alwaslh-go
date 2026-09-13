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
- Verified live main baseline before canceled demo work: `c3734366c132ea3919a925bdd0dd37cfd5d82104`
- Content repo: `7eaur/alwaslh-go`
- Working branch: `content/legacy-staging-rebuild`
- Content branch baseline before this status file: `097cadc85382b47d956020dda9c6fe0e990459bb`
- Legacy snapshot SHA-256: `2dfde94f6b70c037bb15d2782d11f036441c4abe130295be772c59b5e0131d0c`

## First real batch — ACTIVE

Target source currently under preparation:

- Grade 9 English
- Legacy subject UUID: `1794eea5-4772-4c94-bd2b-b08e5815e733`
- Structural manifest: `تاسع انجليزي/الانجليزي_تاسع/manifest.json`
- Curated evidence: `content-staging/curated/grade-9/english/pupil-book-3/reconstruction-candidates.json`

Known facts:

- 69 RAW pages / images
- 8 recovered sections
- 104 questions
- page 70 = manifest-only `Back Matter / Blank Final Page` evidence only
- current candidates are page candidates, **not final lessons**
- current curated publication status is `not_importable`

### Gate for first batch

Before direct DB insertion of the first batch:

1. Determine real Lesson/Activity boundaries for the smallest coherent first batch from source evidence.
2. Validate all questions selected for that batch and known answers.
3. Preserve provenance from lesson/pages/questions back to RAW.
4. Map to modern DB contracts: class/subject/offering/section/lesson/media/question bank/quiz where applicable.
5. Produce exact expected row/media/question counts and rollback scope.
6. Insert the validated batch into the modern PostgreSQL database.
7. Verify inserted records, publication visibility rules, and that unrelated rows are unchanged.
8. Record non-sensitive IDs/counts and verification here.

## Remaining work queue

- `BATCH-001` — First real Grade 9 English content batch: PREPARING
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

1. Read this file, `CONTENT_REBUILD_HANDOFF.md`, live `alwaslh main`, and live `alwaslh-go/content/legacy-staging-rebuild` HEADs.
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

2026-09-13: Demo path canceled by Product Owner. PR #56 closed without merge. First real content batch preparation is the active execution target.