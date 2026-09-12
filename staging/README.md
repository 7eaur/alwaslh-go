# Alwaslh Content Staging

هذا المسار هو منطقة تجهيز ومراجعة للمحتوى قبل إدخاله إلى PostgreSQL الخاصة بتطبيق «الوسيلة الذكية».

## القاعدة الأساسية

`raw` يحفظ المصدر كما هو، و`curated` يحفظ المحتوى بعد إعادة بنائه تربويًا. لا يُستورد أي محتوى إلى Production مباشرة من `raw`.

```text
staging/
├── raw/legacy-supabase/        # نسخ مصدرية immutable + صور أصلية + SHA-256
├── curated/                    # Class → Subject → Document → Section → Lesson → Page
├── config/                     # خرائط المصدر إلى النموذج الحديث
├── reports/                    # inventory / validation / image optimization
└── schemas/                    # عقود JSON القابلة للتحقق
```

## Source of truth أثناء إعادة البناء

1. Legacy Supabase record identity/provenance.
2. الصور الأصلية الفعلية وSHA-256 المحسوب من bytes.
3. manifests/دلائل الكتب الموجودة في هذا المستودع عندما تقدم بنية موثوقة مثل Unit/Section وbook_page.
4. مراجعة بشرية لأي حالة لا يمكن إثباتها آليًا.

لا يُستخدم عنوان الصفحة وحده لتعريف Unit. ولا تُخترع إجابات أو عناوين أو علاقات غير موجودة في المصدر.

## Pilot

أول نطاق تنفيذي:

- legacy class: `تاسع انجليزي`
- legacy subject: `انجليزي الكتاب`
- subject id: `1794eea5-4772-4c94-bd2b-b08e5815e733`
- expected source pages: `69`
- expected source questions: `104`
- canonical target: `grade-9 / english / pupil-book`
- structure reference: `تاسع انجليزي/الانجليزي_تاسع/manifest.json`

## الصور

- الأصل لا يُعدّل ولا يُضغط in-place.
- `raw` يحتفظ بالصورة الأصلية و`raw_sha256`.
- `curated` يولد WebP منفصلًا مع نفس الأبعاد الافتراضية.
- التحسين لا يقبل ملفًا تالفًا أو تغيرًا في الأبعاد دون قرار صريح.
- تقرير التحسين يسجل الحجم قبل/بعد وSHA-256 للنسختين.

## أوامر pipeline

```bash
python tools/content_pipeline/extract_legacy_supabase.py --subject-id 1794eea5-4772-4c94-bd2b-b08e5815e733 --download-images
python tools/content_pipeline/reconstruct_content.py --mapping staging/config/legacy-subject-map.json --key grade-9-english-pupil-book
python tools/content_pipeline/optimize_webp.py --root staging/curated/grade-9/english/pupil-book
python tools/content_pipeline/validate_staging.py --mapping staging/config/legacy-subject-map.json --key grade-9-english-pupil-book
```

`LEGACY_SUPABASE_URL` و`LEGACY_SUPABASE_PUBLISHABLE_KEY` يجب تمريرهما كمتغيرات بيئة. المفتاح لا يُحفظ في Git.
