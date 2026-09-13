# الوسيلة الذكية — Content Rebuild Handoff

> نقطة الاستئناف الرسمية لمسار إعادة بناء المحتوى. الحقيقة التنفيذية الأدق توجد أيضًا في `CONTENT_REBUILD_EXECUTION_STATUS.md`. ابدأ دائمًا من live heads ولا تعتمد على ذاكرة المحادثات.

## 1. الهدف والعقود الثابتة

المستودع: `7eaur/alwaslh-go`

فرع العمل: `content/legacy-staging-rebuild`

المسار المعتمد:

`Legacy Supabase -> Immutable RAW -> Reviewed CURATED -> Media Decision -> Dry Run -> Controlled Transaction -> Modern PostgreSQL -> Verification -> Publication`

قواعد غير قابلة للكسر:

- RAW immutable؛ لا overwrite ولا recompress in-place.
- لا page-title -> Lesson تلقائيًا؛ الحدود تأتي من manifest/source evidence/review.
- provenance وSHA-256 محفوظان عبر كل transform.
- Media ready لا يعني Published.
- لا auto-publish لأي AI/legacy output.
- لا heuristic `69 -> 62` لبناء المنهج النهائي.
- لا حذف anomalies أو بيانات غير مرتبطة لتجميل الأرقام.
- أي DB apply يفشل مغلقًا عند identity/count/provenance drift.

## 2. Corpus / RAW truth

Legacy Supabase snapshot المعتمد:

`2dfde94f6b70c037bb15d2782d11f036441c4abe130295be772c59b5e0131d0c`

Full RAW extraction الموثق:

- Subjects: 58
- Pages: 5,273
- Image references/downloads: 5,273 / 5,273
- Questions: 25,755
- Download failures: 0
- Empty subjects preserved: 2
- Duplicate page-position anomalies preserved: 6

الـRAW يحتفظ بالمشاكل كما هي بدل إخفائها.

## 3. Grade 9 English reconstruction truth

Legacy subject UUID:

`1794eea5-4772-4c94-bd2b-b08e5815e733`

Structural manifest:

`تاسع انجليزي/الانجليزي_تاسع/manifest.json`

Curated candidates:

`content-staging/curated/grade-9/english/pupil-book-3/reconstruction-candidates.json`

Corpus facts:

- RAW pages/images: 69 / 69
- questions: 104
- sections recovered: 8
- manifest-only page 70: `Back Matter / Blank Final Page` evidence only
- full candidate set remains review-required / not globally importable

المستورد القديم أنشأ 62 Lesson من 69 صفحة باستخدام grouping heuristic. هذه الـ62 بقيت Draft/unpublished وهي evidence/state للمصالحة، وليست curriculum truth نهائية.

## 4. BATCH-001 — ACTIVE

Batch:

`BATCH-001-G9-EN-PB3-U1`

الحدود المراجعة للدفعة فقط:

- Section: `Unit 1 - Revision`
- page 1 — `Presents from London` — 4 questions
- page 2 — `What's my job?` — 4 questions
- page 3 — `The holidays` — 3 questions
- page 4 — `A postcard from London` — 2 questions

لا تعمم one-page=one-lesson على بقية الكتاب.

ملفات الدفعة:

- `content-staging/curated/grade-9/english/pupil-book-3/batches/batch-001-unit-1-revision.json`
- `content-staging/curated/grade-9/english/pupil-book-3/batches/batch-001-question-review.json`
- `content-staging/curated/grade-9/english/pupil-book-3/batches/BATCH-001_DB_MEDIA_VALIDATION.md`
- `content-staging/curated/grade-9/english/pupil-book-3/batches/BATCH-001_MODERN_TARGET_DRY_RUN.md`

### DB / media / provenance gate — DONE

Production read-only validation أثبت:

- active grade-9 + english offering
- target section existing before apply: 0
- exact matching lessons: 4, active/unpublished
- lesson assets: 4, draft
- ready media/source provenance chains: 4
- linked Question Bank revisions: 13, draft/unpublished
- source links: 13/13

Media decision:

- RAW JPEG: 440,502 bytes
- current display WebP: 549,794 bytes
- WebP delta: +24.81%

لذلك current WebP profile ليس optimization ناجحًا. لا media mutation في BATCH-001.

### Semantic question gate — DONE

- reviewed: 13
- approved unchanged: 6
- corrected source-grounded: 7
- rejected: 0
- auto-published: 0

التصحيحات عالجت buyer attribution في page 1، doctor/dentist/Taha attribution في page 2، وcross-page London/Amna leakage في page 3. RAW questions لم تُعدّل؛ curated review هو المدخل الوحيد للدفعة.

### Modern target dry-run — DONE

Duplicate-safe target النهائي لهذه الدفعة:

- create curriculum section: 1
- create lessons: 0; reuse/update existing exact lessons: 4
- create lesson assets/media/source rows: 0
- create Question Bank items/revisions/links: 0
- update existing reviewed draft revisions: 7
- no-op reviewed revisions: 6
- expected direct business-row mutations: 12 = 1 + 4 + 7
- publication changes: 0
- unrelated mutations: 0

Rollback يعيد قيم الـ4 lessons والـ7 corrected draft revisions؛ لا يحذف identities القديمة. القسم الجديد فقط يمكن حذفه بعد فك مراجع lessons عند rollback خارجي مخطط.

## 5. Controlled transaction gate — CURRENT CHECKPOINT

تمت قراءة عقود schema الحالية من `7eaur/alwaslh main` ثم تنفيذ gate حقيقية بدل الاعتماد على تقرير نظري.

### Implemented artifacts

Commit `fa661bd9dfa2551a19d1163752dcaa605af74ee7`:

`content-staging/tools/batch-001-controlled-apply.sql`

خصائصه:

- default = rollback-only؛ COMMIT يحتاج `-v apply=true` صريح.
- re-resolve active grade-9/english offering before write.
- lock exact scope + 4 lessons + 13 draft revisions.
- verify target section absent under validated pre-state.
- verify exact lesson -> draft lesson_asset -> ready media -> exact content_source_asset path/checksum chains.
- resolve all reviewed questions by exact lesson + current prompt + page/checksum provenance.
- abort on zero/multiple identity match, count drift, slug collision, provenance drift, or publication drift.
- exercise exactly 1 section insert + 4 lesson structural updates + 7 question corrections.
- no lesson/question/media identity creation on mismatch.
- no publish/status promotion.
- audit accounting explicit: schema requires 0 event rows for this migration gate; no actor is fabricated for `question_bank_events`.

Commit `c782755e5fc213b0018d7aeaa569d5e521b5d5e5`:

`content-staging/runtime/batch-001-transaction-gate.mjs`

هذه نسخة live rollback-only لخدمة Railway inspector: تنفذ نفس mutation set داخل transaction، تعمل post-validation، ثم ترمي sentinel متعمدًا ليقوم postgres.js بالـROLLBACK، وبعده تتحقق خارج transaction أن target section count عاد إلى 0.

### Live verification state

Existing Railway utility service: `alwaslh-content-inspector` — reused؛ لم يتم إنشاء خدمة جديدة.

تم ضبط start command للـgate إلى:

`node batch-001-transaction-gate.mjs`

Deployment الجاري لهذا checkpoint:

`21020740-d3ff-4848-bf87-6cb2a4299021`

عند آخر تحقق كان `BUILDING` ولم يصدر runtime log بعد. محاولتا Railway Agent one-off انتهتا بtimeout ولم تُحتسبا نجاحًا.

لا تعتبر transaction gate ناجحة حتى يظهر كلا السطرين:

- `BATCH001_GATE_MUTATION_PHASE_PASS` مع `1 / 4 / 7`, question no-ops 6, publication 0, unrelated 0.
- `BATCH001_GATE_PASS_ROLLBACK_VERIFIED` مع `postRollbackSectionCount=0`.

حتى الآن لا يوجد DB apply مصرح أو publication change في هذا checkpoint.

## 6. Exact resume action

1. اقرأ live heads للمستودعين والـworking branch.
2. اقرأ `CONTENT_REBUILD_EXECUTION_STATUS.md` أولًا؛ هو أحدث من هذا handoff إذا اختلفا.
3. افحص deployment `21020740-d3ff-4848-bf87-6cb2a4299021`.
4. إذا اكتمل build لكنه لم يشغّل start command الجديد، redeploy **نفس** inspector service فقط؛ لا تنشئ service جديدًا.
5. اقرأ logs واطلب PASS markers الاثنين أعلاه.
6. إذا ظهر drift حقيقي، أصلح root cause في executor ثم أعد rollback-only gate.
7. إذا PASS فقط: حدّث status/handoff وأغلق خطوة transaction gate. لا تعد تنفيذ semantic review أو dry-run.
8. الخطوة التالية بعد إغلاق gate هي controlled PostgreSQL apply لنفس set فقط، ثم VERIFY؛ لا توسع الدفعة.

## 7. Remaining ordered queue

- `BATCH-001` — `CONTROLLED_TRANSACTION_IMPLEMENTED / LIVE_ROLLBACK_PENDING`
- `STRUCTURE-001`
- `STRUCTURE-002`
- `CURATION-001`
- `CURATION-002`
- `CONTENT-GAPS-001`
- `MEDIA-001`
- `IMPORT-001`
- `VERIFY-001`
- `ROADMAP-RETURN -> STUDENT-016I`

لا تنتقل إلى المهمة التالية قبل إغلاق المهمة الحالية بأدلتها.
