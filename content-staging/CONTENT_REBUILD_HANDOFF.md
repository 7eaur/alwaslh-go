# الوسيلة الذكية — Content Rebuild Handoff

> هذا الملف هو نقطة الاستئناف الرسمية لمسار إعادة بناء المحتوى القديم. لا تعتمد على ذاكرة المحادثات بدلًا منه؛ تحقّق دائمًا من الفرع والكود والتقارير الفعلية.

## 1) النطاق والهدف

المستودع: `7eaur/alwaslh-go`

فرع العمل: `content/legacy-staging-rebuild`

الهدف هو تحويل محتوى Supabase القديم إلى مصدر محتوى قابل للمراجعة قبل إدخاله إلى PostgreSQL الحديث عبر خط واضح:

`Legacy Supabase -> Immutable RAW -> Reviewed CURATED -> Media Optimization -> Dry Run -> Modern PostgreSQL -> Verification -> Publication`

المبادئ غير القابلة للكسر:

- RAW نسخة إثباتية immutable ولا يتم تعديل ملفاتها أو إعادة ضغطها in-place.
- لا يُعتبر عنوان صفحة قديمة Lesson نهائيًا تلقائيًا.
- لا يتم اختراع Unit/Section/Lesson boundaries دون دليل من الكتاب/manifest/مصدر موثوق.
- كل Transform يحتفظ بالـprovenance والـSHA-256.
- Media ready لا يعني Published.
- لا يُنشر AI output تلقائيًا.
- لا يُستورد CURATED إلى Production قبل اجتياز review/import gates.
- لا نكمل استيراد بقية Legacy subjects إلى Production باستخدام heuristic القديم.

## 2) لماذا بدأ هذا المسار

تم تدقيق أول دفعة Legacy للصف التاسع/الإنجليزي في قاعدة الوسيلة الحديثة، واتضح أن importer القديم/الجديد كان يبني البنية التعليمية بشكل غير مناسب:

- 69 صفحة مصدر تحولت إلى 62 Lesson باستخدام `normalized title + contiguous pages`.
- كل الـ62 Lesson كانت `section_id = NULL`.
- الـStudent catalog يدعم `sections` و`unsectionedLessons`؛ نشر هذه الدفعة كان سيعرض عشرات العناصر بشكل مسطح ومربك.
- manifest الموثوق لنفس الكتاب يميّز بوضوح بين `Unit/Section` وبين عنوان الصفحة/النشاط.

الاستنتاج المعتمد:

`Class -> Subject -> Offering -> Source Document -> Curriculum Unit/Section -> Lesson/Activity -> Ordered Pages/Assets -> Questions`

وليس:

`Page title -> Production Lesson`.

## 3) دفعة Production السابقة — مرجع فقط

أول import للصف التاسع/الإنجليزي سبق أن نُفذ في PostgreSQL الحديث، لكنه بقي Draft وغير مرئي للطالب.

حقائق مثبتة من verifier/replay:

- Import run ID: `89e213e3-2235-457c-9fe6-76e2b54ef10d`
- Source manifest SHA: `3f92d04fe746328df426a9a911446ababd4077caa09f79459ef382332c140f23`
- Lessons: 62
- Source assets/pages: 69
- Lesson assets: 69
- Unique media assets: 69
- Questions: 104
- Published lessons: 0
- Published question revisions: 0
- Lesson assets published: 0
- Storage variants verified: 276
- Replay reused all 69 media assets and created 0 new duplicates.

لا تُصلح هذه الـ62 يدويًا. بعد اعتماد الـCURATED الصحيح يتم التعامل مع هذه الدفعة بشكل controlled reset/re-import.

## 4) Full RAW Extraction — COMPLETED & VERIFIED

Legacy Supabase project ref:

`zhbgbmqhonqmzpqfiehs`

GitHub Actions secret المستخدم للقراءة فقط:

`LEGACY_SUPABASE_PUBLISHABLE_KEY`

لا تكتب قيمة المفتاح في Git أو في هذا الملف.

تم تنفيذ full raw extraction على GitHub Runner بمادة واحدة/Checkpoint commit، مع حفظ ملفات الصور نفسها وليس الروابط فقط.

التقرير الرسمي:

`content-staging/raw/legacy-supabase/FULL_EXTRACTION_REPORT.json`

Snapshot SHA-256 المعتمد:

`2dfde94f6b70c037bb15d2782d11f036441c4abe130295be772c59b5e0131d0c`

الأرقام النهائية:

- Subjects: **58**
- Pages: **5,273**
- Image references: **5,273**
- Images downloaded: **5,273**
- Questions: **25,755**
- Image download failures: **0**
- Empty subjects preserved: **2**
- Duplicate page positions tracked as anomalies: **6**

ملاحظة مهمة: تدقيق أقدم كان يسجل 25,715 سؤالًا. المصدر الحي عند الـsnapshot النهائي أصبح 25,755، ولذلك المرجع الصحيح لهذا المسار هو الـsnapshot أعلاه وليس الرقم القديم.

لكل subject توجد بياناته الخام + الصور + manifest/provenance/checksums. الـRAW يحفظ anomalies بدل حذفها.

## 5) أدوات/Workflows التي أضيفت

داخل `content-staging/tools/` توجد أدوات من بينها:

- Raw Supabase extractor — read-only، يحفظ البيانات كما هي ويحسب SHA-256.
- Image optimization/WebP tooling — موجود لكنه **لم يُستخدم على الـRAW بعد**.
- Curated reconstruction candidate builder.

داخل `.github/workflows/` توجد workflows خاصة بـ:

- Content Staging CI.
- Full legacy raw extraction.
- Subject extraction/checkpoints.
- Grade 9 English curation.

تم تعديل extractor ليقبل modern Supabase publishable keys من نوع `sb_publishable_...` بالطريقة الصحيحة بدل معاملتها كـJWT bearer token.

## 6) Grade 9 English — أول Reconstruction مرجعي

Legacy class: `تاسع انجليزي`

Legacy subject UUID:

`1794eea5-4772-4c94-bd2b-b08e5815e733`

Legacy subject name: `انجليزي الكتاب `

Raw facts:

- 69 pages
- 69 raw images
- 104 questions
- 0 duplicate page positions
- 0 title mismatches مقابل manifest الموثوق

Source structure manifest:

`تاسع انجليزي/الانجليزي_تاسع/manifest.json`

Curated reconstruction output:

`content-staging/curated/grade-9/english/pupil-book-3/reconstruction-candidates.json`

آخر نتيجة مثبتة:

- Schema version: 3
- Raw pages: 69
- Raw images: 69
- Sections recovered: 8
- Page candidates: 69
- Questions: 104
- Title mismatches: 0
- Source-manifest-only pages: 1
- Publication status: `not_importable`
- كل candidate: `review_required`

كل page candidate يحتفظ بـ:

- `legacy_page_id`
- `book_page`
- `source_page`
- `section`
- legacy title
- manifest title
- question count
- raw image path
- raw image SHA-256
- byte size
- storage bucket/object path
- review status/reason

### Manifest-only page 70

أول curation run توقف عمدًا لأن manifest يحتوي `book_page=70` بينما RAW يحتوي 69 صفحة فقط.

التحقق أثبت أن الصفحة الإضافية هي:

- Section: `Back Matter`
- Title: `Blank Final Page`

السياسة الصحيحة التي تم تنفيذها:

- أي Raw page يجب أن تجد reviewed structural evidence.
- أي صفحة موجودة فقط في manifest تُحفظ تحت `unresolved.source_manifest_only_pages`.
- manifest-only pages لا تتحول إلى Lesson/Page candidate ولا يتم اختراع Raw لها.

Curation v2 وContent Staging CI نجحا بالكامل.

آخر checkpoint output commit الموثق:

`a724586f2646a061881dfabf02a3f5cbb9d075a9`

Message:

`data(curated): reconstruct grade 9 English source hierarchy [skip ci]`

Commits مهمة قبل ذلك:

- `70e434f728446f088bbf31685639af70120e597d` — preserve manifest-only structural pages.
- `c252eec3363c5e88869883f4c15d0ceacf81ead2` — tests for manifest-only evidence.
- `91d3576bba57958dcdabd25d94db309a2f0ce4b4` — workflow validation.
- `e6913278c44f74ed246ff39a36c037e99d5393d6` — curation v2 trigger.

## 7) BATCH-001 — First real Grade 9 English batch — ACTIVE

الدفعة الحالية:

`BATCH-001-G9-EN-PB3-U1`

النطاق المعتمد فقط لهذه الدفعة:

- Section: `Unit 1 - Revision`
- `Presents from London` — page 1
- `What's my job?` — page 2
- `The holidays` — page 3
- `A postcard from London` — page 4
- total questions: 13

هذه الحدود مثبتة لهذه الدفعة فقط، ولا تعني اعتماد `one page = one lesson` لبقية الكتاب.

ملفات التنفيذ:

- Contract: `content-staging/curated/grade-9/english/pupil-book-3/batches/batch-001-unit-1-revision.json`
- Semantic question review: `content-staging/curated/grade-9/english/pupil-book-3/batches/batch-001-question-review.json`
- DB/media validation: `content-staging/curated/grade-9/english/pupil-book-3/batches/BATCH-001_DB_MEDIA_VALIDATION.md`
- Shared live status: `content-staging/CONTENT_REBUILD_EXECUTION_STATUS.md`

### BATCH-001 DB/media gate — DONE

Production read-only validation أثبت:

- 4 matching prior legacy-import lessons, all unpublished.
- 4 lesson assets, all draft.
- 4 ready media assets with source provenance.
- 13 linked question revisions, all draft/unpublished.
- 0 PostgreSQL writes during validation.

Current display WebP profile is not a size optimization:

- RAW JPEG total: `440,502` bytes
- existing display WebP total: `549,794` bytes
- delta: `+24.81%`

لذلك RAW يبقى immutable ولا تُقبل صيغة WebP لمجرد الامتداد؛ أي derived profile لاحق يجب أن يكون أصغر فعلًا مع الحفاظ على وضوح المحتوى التعليمي.

### BATCH-001 semantic question gate — DONE

تمت مراجعة الأسئلة الـ13 سؤالًا بسؤال مقابل محتوى الصفحات الأربع المتطابقة مع manifest والنسخة المصدرية للكتاب:

- reviewed: **13**
- approved unchanged: **6**
- corrected source-grounded: **7**
- rejected: **0**
- published automatically: **0**

أهم الأخطاء المكتشفة:

- سؤال في page 1 غيّر المشتري وجعل الإجابة عامة بدل الاقتراح الفعلي.
- page 2 احتوت attribution غير صحيح إلى Taha وخلطًا بين doctor/dentist؛ صُححت 3 أسئلة إلى أوصاف الوظائف الموجودة فعلًا.
- page 3 احتوت cross-page leakage من قصة London ونسبت نشاطًا إلى Amna دون دليل؛ صُححت الأسئلة الثلاثة إلى حقائق موجودة فعلًا في صفحة `The holidays`.
- page 4: السؤالان صحيحان وبقيا دون تغيير.

Commits:

- reviewed question set: `eae7b9d8b3b61b20f4ca74cb75f222aa5b6f9e60`
- batch contract after semantic gate: `4f2fb8d0a559add5b6c2e75c92bf075fabae32f5`

الـRAW questions لم تُعدل؛ ملف review هو الطبقة curated التي يجب أن يستخدمها الـdry-run والاستيراد.

### BATCH-001 immediate next action

`[NEXT]` Modern target dry-run فقط، بدون mutation:

- one curriculum section
- four curated lesson slugs
- four lesson assets reusing exact existing media/source provenance
- reviewed 13-question set فقط
- duplicate-safe handling of the existing unpublished 62-lesson legacy import
- exact create/reuse/update/deactivate counts
- exact rollback scope/counts
- prove unrelated rows remain untouched

لا توجد صلاحية لعمل PostgreSQL mutation قبل نجاح هذه البوابة وتوثيق أعدادها.

## 8) Remaining content work after BATCH-001

### STRUCTURE-001 — P1 — TODO AFTER BATCH-001

بناء inventory لتغطية الـstructural manifests على كل الـ58 subject/document.

لا تعمم Grade 9 English على بقية المواد. لكل مستند صنفه إلى:

- `VERIFIED_MANIFEST_AVAILABLE`
- `STRUCTURE_EVIDENCE_AVAILABLE_BUT_NOT_VERIFIED`
- `NEEDS_STRUCTURE_EXTRACTION`
- `EMPTY_SOURCE`
- `ANOMALOUS_SOURCE`

### STRUCTURE-002 — P1 — TODO

تحديد canonical Document boundaries لكل subject، خصوصًا المواد التي تجمع:

- كتاب مدرسي
- أجزاء متعددة
- نماذج وزارية حسب السنوات
- activity/workbook إن وجد

لا تفترض أن legacy subject = one final curriculum document إذا أثبت المصدر غير ذلك.

### CURATION-001 — P1 — TODO

مراجعة بقية Lesson/Activity boundaries داخل Grade 9 English.

الـ69 عنصر الكاملة Page Candidates فقط؛ BATCH-001 اعتمد أول 4 فقط كحدود موثقة.

### CURATION-002 — P1 — TODO

بناء نفس reconstruction contract للوثائق الأخرى فقط بعد وجود structure evidence موثوق.

### CONTENT-GAPS-001 — P2 — TODO

بعد تثبيت البنية، تحديد النواقص الحقيقية مثل:

- summaries
- extracted text/OCR
- explanations
- question answer gaps
- metadata

Generated content يبقى `review_required` ولا يصبح Truth أو Published تلقائيًا.

### MEDIA-001 — P1/P2 — TODO AFTER CURATION GATE

تحسين الصور إلى WebP بعد اكتمال تنظيم المحتوى، وليس الآن على RAW.

القواعد:

- RAW original لا يُمس.
- Preserve readability over maximum compression.
- No unnecessary upscale.
- حفظ raw SHA + optimized SHA + dimensions + byte sizes.
- verify decodability/readability.
- derive output; never overwrite evidence.

### IMPORT-001 — P1 — BLOCKED BY BATCH/STRUCTURE GATES

لا تستورد أي curated legacy content غير مراجع إلى PostgreSQL الحديث.

قبل كل import:

- structural verification
- dry-run counts
- provenance verification
- media transformation/delivery verification
- question validity/report
- duplicate-safe handling of prior legacy import
- rollback plan
- replay/idempotency verification

## 9) Modern Alwaslh DB facts التي يجب الحفاظ عليها

المستودع الرئيسي للتطبيق:

`7eaur/alwaslh`

Canonical curriculum/content chain:

`Class -> Subject -> subject_class_links -> curriculum_sections -> lessons -> lesson_assets -> media_assets -> media_variants/OCR`

Source provenance chain:

`content_import_runs -> content_source_documents -> content_source_assets -> media_assets -> lesson_assets -> lessons`

Question Bank:

`question_bank_items -> question_bank_revisions`

مع:

- `question_bank_revision_lessons`
- `question_bank_revision_sources`

Quiz Builder يفرض scope integrity على class/subject/lesson/questions، والـpublished structure immutable.

Student Reader/Student Catalog لا يعرضان المحتوى لمجرد وجوده. يلزم على الأقل التحقق من العقود الفعلية التالية قبل أي publication:

- active class
- active subject
- active offering
- lesson active + published_at
- section active إذا كان lesson داخل section
- student entitlement يسمح بالوصول
- lesson asset publication status = published
- media asset ready
- media bytes/variants valid

## 10) UX/Product roadmap isolation

الـcontent rebuild ليس تصريحًا لتغيير الـUX roadmap أو دمج تغييرات واجهة غير مرتبطة.

في `7eaur/alwaslh` كان Stage 17/UX refoundation جارٍ في مسار منفصل. لا تخلط changeset المحتوى مع refactor الواجهة إلا عند الحاجة للتحقق المرئي فقط.

بعد الوصول إلى content gate الموثق، نقطة العودة المطلوبة هي `STUDENT-016I`، لكن يجب التحقق من `PROJECT_STATUS.md` الحي قبل أي قرار.

## 11) Verification gates الحالية

قبل أي خطوة جديدة:

1. اقرأ `.agents/skills/alwaslh-product-engineering/SKILL.md` من `7eaur/alwaslh` عند الحاجة إلى تعديل التطبيق/DB tooling.
2. اقرأ `PROJECT_STATUS.md` و`PROJECT_ENGINEERING_LOG.md` عند أي تغيير في حقيقة التطبيق أو runtime.
3. تحقق من live heads لـ`alwaslh main` و`alwaslh-go master` و`alwaslh-go/content/legacy-staging-rebuild`.
4. اقرأ `CONTENT_REBUILD_EXECUTION_STATUS.md` وابدأ من أول `[NEXT]` فقط.
5. تحقق من `FULL_EXTRACTION_REPORT.json` وأن snapshot SHA يساوي القيمة المعتمدة أعلاه إذا دخلت في corpus-wide work.
6. لا تعتمد على أرقام المحادثة إذا اختلفت عن live repo/report.
7. لا تنشر محتوى غير مراجع تلقائيًا.

## 12) Definition of Done لمسار إعادة بناء المحتوى

لا يعتبر المسار منتهيًا إلا عند:

- 100% Raw source preserved and verified — **DONE**.
- Document/section structure verified for all importable sources.
- Lesson/activity boundaries reviewed.
- Questions mapped and invalid/unknown answers isolated.
- Missing content explicitly classified and reviewed.
- Optimized media derived with checksum/readability validation where it is actually beneficial.
- Curated repository passes machine validation.
- Production dry-run passes.
- Controlled import passes.
- Replay/idempotency passes.
- Student/Admin read paths verified.
- No unintended publication.
- Engineering/status docs updated.

## 13) Immediate next execution order

1. `BATCH-001`: modern target dry-run using the reviewed 13-question set.
2. `BATCH-001`: exact mutation/rollback counts.
3. `BATCH-001`: controlled PostgreSQL mutation only if every gate passes.
4. `BATCH-001`: verify records, visibility rules, idempotency, and unrelated-row invariance.
5. `STRUCTURE-001`.
6. `STRUCTURE-002`.
7. `CURATION-001`.
8. `CURATION-002`.
9. `CONTENT-GAPS-001`.
10. `MEDIA-001`.
11. `IMPORT-001`.
12. `VERIFY-001`.
13. `ROADMAP-RETURN` to `STUDENT-016I` when the content gate is documented as reached.

---

**Source of Truth order:** live repository/code + PostgreSQL migrations + executable tests/CI + verified runtime + generated verification reports, then documentation.
