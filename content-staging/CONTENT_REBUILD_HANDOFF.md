# الوسيلة الذكية — Content Rebuild Handoff

> نقطة الاستئناف الرسمية لمسار إعادة بناء المحتوى. اقرأ live heads ثم `CONTENT_REBUILD_EXECUTION_STATUS.md` أولًا؛ هو المرجع التنفيذي الأدق إذا اختلفا.

## 1. العقود الثابتة

المستودع: `7eaur/alwaslh-go`

فرع العمل: `content/legacy-staging-rebuild`

المسار:

`Legacy Supabase -> Immutable RAW -> Reviewed CURATED -> Media Decision -> Dry Run -> Controlled Transaction -> Modern PostgreSQL -> Verification -> Publication`

قواعد لا تكسر:

- RAW immutable؛ لا overwrite/recompress in-place.
- لا page-title -> Lesson تلقائيًا؛ الحدود تأتي من evidence + review.
- provenance وSHA-256 محفوظان.
- Media ready لا يعني Published.
- لا auto-publish لأي AI/legacy output.
- لا تستخدم `69 -> 62` كحقيقة منهجية.
- لا تحذف anomalies أو بيانات غير مرتبطة لتجميل الأرقام.
- أي DB apply يفشل مغلقًا عند identity/count/provenance drift.

## 2. Corpus truth

Legacy snapshot SHA-256:

`2dfde94f6b70c037bb15d2782d11f036441c4abe130295be772c59b5e0131d0c`

Full RAW extraction:

- Subjects: 58
- Pages: 5,273
- Images: 5,273 / 5,273
- Questions: 25,755
- Download failures: 0
- Empty subjects preserved: 2
- Duplicate page-position anomalies preserved: 6

Grade 9 English legacy subject UUID:

`1794eea5-4772-4c94-bd2b-b08e5815e733`

Corpus facts:

- RAW pages/images: 69 / 69
- questions: 104
- sections recovered: 8
- manifest-only page 70: `Back Matter / Blank Final Page` evidence only
- old importer produced 62 Draft/unpublished lessons by heuristic; those 62 are reconciliation state only, not curriculum truth.

## 3. BATCH-001 — ACTIVE

Batch: `BATCH-001-G9-EN-PB3-U1`

Reviewed structure for this batch only:

- Section: `Unit 1 - Revision`
- page 1 — `Presents from London` — 4 questions
- page 2 — `What's my job?` — 4 questions
- page 3 — `The holidays` — 3 questions
- page 4 — `A postcard from London` — 2 questions

Do not generalize one-page=one-lesson.

Authoritative artifacts:

- `content-staging/curated/grade-9/english/pupil-book-3/batches/batch-001-unit-1-revision.json`
- `content-staging/curated/grade-9/english/pupil-book-3/batches/batch-001-question-review.json`
- `content-staging/curated/grade-9/english/pupil-book-3/batches/BATCH-001_DB_MEDIA_VALIDATION.md`
- `content-staging/curated/grade-9/english/pupil-book-3/batches/BATCH-001_MODERN_TARGET_DRY_RUN.md`
- `content-staging/tools/batch-001-controlled-apply.sql`
- `content-staging/runtime/batch-001-transaction-gate.mjs`

## 4. Completed gates

### DB / media / provenance — DONE

- active grade-9/english offering
- target section count: 0
- 4 exact existing lessons, active/unpublished
- 4 lesson assets, draft
- 4 ready media/source chains
- 13 linked Question Bank draft revisions, unpublished
- 13/13 source links
- 2 active student entitlements observed; publication remains closed

Media:

- RAW JPEG total: 440,502 bytes
- current display WebP total: 549,794 bytes
- WebP delta: +24.81%

Therefore no media mutation in BATCH-001. RAW remains immutable.

### Semantic questions — DONE

- reviewed: 13
- unchanged: 6
- corrected: 7
- rejected: 0
- published: 0

### Modern target dry-run — DONE

Exact duplicate-safe target:

- section insert: 1
- lesson inserts: 0
- reuse/update lessons: 4
- lesson asset/media/source inserts: 0
- Question Bank identity/revision/link inserts: 0
- corrected revision updates: 7
- question no-ops: 6
- total direct business-row mutations: 12
- publication changes: 0
- unrelated changes: 0

## 5. Controlled rollback transaction — DONE

### Important root-cause correction

A pre-fix deployment failed closed because the transaction gate used the local RAW extraction path as `content_source_assets.source_path`.

That was incorrect for the modern PostgreSQL import. The canonical DB source identities are:

- `public.lessons/2d98475c-91bf-4000-bfbc-79f7a6a854f9/image/0`
- `public.lessons/5e207993-508f-426b-ae71-f00aa4f782df/image/0`
- `public.lessons/dc1d6249-c0cb-4982-9711-092b1dcffee3/image/0`
- `public.lessons/f2947d7f-5697-4bdc-b561-ad880a1afdf1/image/0`

The local paths under `تاسع انجليزي/.../الصور/...` remain immutable RAW evidence only.

Fixes:

- runtime gate commit: `3cd817414275aa31bcd67e7015ce48740409a43c`
- SQL parity commit: `c8c15e1d04b7bb353f6ee0755beec7b33c66a7c2`

The fixed gate requires:

- canonical source path + immutable SHA-256;
- expected legacy lesson slug before mutation;
- exact lesson -> draft lesson_asset -> ready media -> content_source_asset chain;
- question source page + checksum + same `content_source_asset_id`;
- 13 exact draft revisions;
- no target section before apply;
- no target slug collision;
- no publish/status promotion.

### Live proof

Existing Railway utility service reused: `alwaslh-content-inspector`.

Successful rollback-only deployment:

`a79244c2-731a-4573-b86b-089d31254933`

Commit:

`3cd817414275aa31bcd67e7015ce48740409a43c`

Observed markers:

`BATCH001_GATE_MUTATION_PHASE_PASS`

- section inserts: 1
- lesson updates: 4
- question updates: 7
- question no-ops: 6
- corrected post-checks: 7
- publication changes: 0
- unrelated rows: 0
- audit rows required by schema: 0

`BATCH001_GATE_PASS_ROLLBACK_VERIFIED`

- post-rollback section count: 0
- post-rollback lessons verified: 4
- post-rollback corrected questions verified: 7

Resolved lesson IDs:

- `767ec1b0-1447-4cb6-824f-4a544d709837`
- `2959accf-c984-44f1-9959-c3d1507c8ce7`
- `bb066699-f2ba-4b7e-bcdb-d6b313cdbc84`
- `df8d57bd-ff0c-4303-abe1-83874838bc88`

Committed DB writes from this gate: 0.
Publication changes: 0.
RAW/media changes: 0.

## 6. Current checkpoint

`BATCH-001 = CONTROLLED_TRANSACTION_VERIFIED / APPLY_PENDING`

Do not redo semantic review, media validation, or target dry-run.

`PROJECT_STATUS.md` and `PROJECT_ENGINEERING_LOG.md` were intentionally not changed at this checkpoint because no product/runtime business data was committed and publication truth did not change.

## 7. Exact resume action

1. Read live heads for `7eaur/alwaslh`, `7eaur/alwaslh-go`, and the working branch.
2. Read `CONTENT_REBUILD_EXECUTION_STATUS.md` + this handoff.
3. Reconfirm immediate pre-apply drift guards only: target section still 0; four canonical source identities uniquely resolve; 13 revisions remain draft; publication is still closed.
4. Execute the existing controlled PostgreSQL apply for exactly `1 section + 4 lesson updates + 7 corrected revisions`; no expansion.
5. Immediately VERIFY committed counts, publication invariants, replay/idempotency, RAW/media immutability, and unrelated-row invariance.
6. Update execution status, handoff, and product/project logs only where committed truth changes.
7. Only after BATCH-001 closes, move to `STRUCTURE-001`.

## 8. Ordered queue

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

لا تنتقل للمهمة التالية قبل إغلاق الحالية بأدلتها.
