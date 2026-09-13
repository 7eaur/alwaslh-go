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

## 7) ما لم يتم بعد — IMPORTANT

### STRUCTURE-001 — P1 — IN PROGRESS

بناء inventory لتغطية الـstructural manifests على كل الـ58 subject/document.

لا تعمم Grade 9 English على بقية المواد. لكل مستند صنفه إلى:

- `VERIFIED_MANIFEST_AVAILABLE`
- `STRUCTURE_EVIDENCE_AVAILABLE_BUT_NOT_VERIFIED`
- `NEEDS_STRUCTURE_EXTRACTION`
- `EMPTY_SOURCE`
- `ANOMALOUS_SOURCE`

هذه المهمة كانت النقطة التالية المباشرة عند إنشاء هذا handoff.

### STRUCTURE-002 — P1 — TODO

تحديد canonical Document boundaries لكل subject، خصوصًا المواد التي تجمع:

- كتاب مدرسي
- أجزاء متعددة
- نماذج وزارية حسب السنوات
- activity/workbook إن وجد

لا تفترض أن legacy subject = one final curriculum document إذا أثبت المصدر غير ذلك.

### CURATION-001 — P1 — TODO

مراجعة Lesson/Activity boundaries داخل Grade 9 English.

الـ69 عنصر الحالية Page Candidates فقط؛ لم يتم اعتماد 69 Lesson ولا 62 Lesson.

يجب استخدام Unit structure + عناوين الصفحات + الكتاب الفعلي لتحديد ما إذا كانت الصفحات المتجاورة تمثل Lesson واحدًا أو أنشطة مستقلة.

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

### IMPORT-001 — P1 — BLOCKED BY CURATION

لا تستورد curated legacy content إلى PostgreSQL الحديث بعد.

قبل الاستيراد:

- full structural verification
- dry-run counts
- provenance verification
- media transformation verification
- question validity/report
- controlled cleanup/reset للدفعة التجريبية legacy القديمة إن لزم
- replay/idempotency verification

## 8) Modern Alwaslh DB facts التي يجب الحفاظ عليها

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

Student Reader/Student Catalog لا يعرضان المحتوى لمجرد وجوده. يلزم على الأقل التحقق من العقود الفعلية التالية قبل أي demo/production publication:

- active class
- active subject
- active offering
- lesson active + published_at
- section active إذا كان lesson داخل section
- student entitlement يسمح بالوصول
- lesson asset publication status = published
- media asset ready
- media bytes/variants valid

## 9) Published Student Demo Data — TASK REQUESTED / NOT YET VERIFIED HERE

طلب المستخدم إضافة بيانات تجريبية منشورة صحيحة End-to-End حتى يرى الشكل الحقيقي عند الطالب:

- Section
- Lesson
- صور/Pages
- Questions مرتبطة بشكل صحيح
- Training/Quiz حسب ما يدعمه runtime الفعلي
- Published correctly
- Student-visible with proper entitlement

قواعد التنفيذ:

- لا تستخدم Legacy RAW كبيانات Demo منشورة مباشرة.
- افحص schema + services + student UI + quiz/training runtime قبل الإنشاء.
- استخدم scope واضح مثل `DEMO-PUBLISHED-CONTENT` وقابل للإزالة.
- لا تضف migration دائمة تحقن demo data في كل بيئة إلا إذا أثبتت بنية المشروع أن هذا هو الأسلوب المعتمد.
- فضّل seed/admin/runtime operation قابلة للتراجع.
- استخدم canonical media pipeline/storage، لا external image URLs.
- وثّق IDs غير الحساسة، verification، وطريقة cleanup.
- حدّث `PROJECT_ENGINEERING_LOG.md` و`PROJECT_STATUS.md` في `7eaur/alwaslh` عند تنفيذ التغيير.

حالة هذه المهمة عند كتابة هذا الملف: **NOT YET VERIFIED / التنفيذ جارٍ في المحادثة التي أنشأت الـhandoff**.

## 10) UX/Product roadmap isolation

الـcontent rebuild ليس تصريحًا لتغيير الـUX roadmap أو دمج تغييرات واجهة غير مرتبطة.

في `7eaur/alwaslh` كان Stage 17/UX refoundation جارٍ في مسار منفصل. لا تخلط changeset المحتوى/seed التجريبي مع refactor الواجهة إلا عند الحاجة للتحقق المرئي فقط.

بعد اكتمال مسار UX الحالي، نقطة استئناف roadmap الطبيعية المحفوظة سابقًا هي `STUDENT-016I` وفق skill/project docs، لكن تحقّق من `PROJECT_STATUS.md` الحي قبل أي قرار.

## 11) Verification gates الحالية

قبل أي خطوة جديدة:

1. اقرأ `.agents/skills/alwaslh-product-engineering/SKILL.md` من `7eaur/alwaslh`.
2. اقرأ `PROJECT_STATUS.md` و`PROJECT_ENGINEERING_LOG.md`.
3. تحقق من live branch SHA في `alwaslh-go/content/legacy-staging-rebuild`.
4. تحقق من `FULL_EXTRACTION_REPORT.json` وأن snapshot SHA يساوي القيمة المعتمدة أعلاه.
5. تحقق أن Grade 9 English reconstruction ما زال schema v3 / not_importable / 69 candidates / 8 sections / 104 questions / 1 manifest-only page.
6. لا تعتمد على أرقام المحادثة إذا اختلفت عن live repo/report.

## 12) Definition of Done لمسار إعادة بناء المحتوى

لا يعتبر المسار منتهيًا إلا عند:

- 100% Raw source preserved and verified — **DONE**.
- Document/section structure verified for all importable sources.
- Lesson/activity boundaries reviewed.
- Questions mapped and invalid/unknown answers isolated.
- Missing content explicitly classified and reviewed.
- Optimized media derived with checksum/readability validation.
- Curated repository passes machine validation.
- Production dry-run passes.
- Controlled import passes.
- Replay/idempotency passes.
- Student/Admin read paths verified.
- No unintended publication.
- Engineering/status docs updated.

## 13) Immediate next execution order

1. Finish live Published Student Demo Data task in `7eaur/alwaslh` and document it.
2. Finish structural-manifest coverage inventory for all RAW subjects/documents.
3. Review Grade 9 English lesson/activity boundaries.
4. Build reusable curated document contract from verified evidence.
5. Expand reconstruction incrementally across documents.
6. Only after content structure is stable: derive WebP/optimized media.
7. Run full curated validation/report.
8. Design controlled Production import/reset plan.
9. Import only after explicit gates pass.

---

**Source of Truth order:** live repository/code + PostgreSQL migrations + executable tests/CI + verified runtime + generated verification reports, then documentation.
