# الوسيلة الذكية — Content Rebuild Handoff

> نقطة الاستئناف الرسمية. اقرأ live heads ثم `CONTENT_REBUILD_EXECUTION_STATUS.md` أولًا؛ هو المرجع التنفيذي الأدق إذا اختلفا.

## العقود الثابتة

- Working repository: `7eaur/alwaslh-go`
- Working branch: `content/legacy-staging-rebuild`
- Flow: `Legacy Supabase -> Immutable RAW -> Reviewed CURATED -> Media Decision -> Dry Run -> Controlled Transaction -> Modern PostgreSQL -> Verification -> Publication`
- RAW immutable؛ لا overwrite/recompress in-place.
- لا page-title -> Lesson تلقائيًا؛ الحدود تأتي من evidence + review.
- provenance وSHA-256 محفوظان.
- Media ready لا يعني Published.
- لا auto-publish لأي AI/legacy output.
- لا تستخدم `69 -> 62` كحقيقة منهجية.
- لا تحذف anomalies أو بيانات غير مرتبطة لتجميل الأرقام.
- أي DB apply يفشل مغلقًا عند identity/count/provenance drift.

## Corpus truth retained

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

Grade 9 English legacy corpus:
- RAW pages/images: 69 / 69
- questions: 104
- sections recovered: 8
- manifest-only page 70 remains evidence only
- old 62 Draft lessons are reconciliation state, not curriculum truth

## BATCH-001 — DONE

Batch: `BATCH-001-G9-EN-PB3-U1`

Reviewed Unit 1 boundaries:
- page 1 — `Presents from London` — 4 questions
- page 2 — `What's my job?` — 4 questions
- page 3 — `The holidays` — 3 questions
- page 4 — `A postcard from London` — 2 questions

Do not generalize one-page=one-lesson.

Completed evidence before commit:
- 13 semantic questions reviewed = 6 unchanged + 7 corrected + 0 rejected
- duplicate-safe target dry-run = exactly `1 section + 4 lesson updates + 7 question corrections`
- publication mutations = 0
- rollback transaction gate = PASS
- RAW JPEG `440,502` bytes vs existing display WebP `549,794` bytes (`+24.81%`), so no media mutation accepted

## Latest execution truth

A bounded apply executor was added at:
`cebde403957b5932d4dd123784a6684e1be77bd3`

Its deployment `90867b02-30af-4886-9dbf-b26f0c1d8281` failed closed **before mutation** because the first lesson no longer matched its expected legacy slug. Do not retry that pre-state apply blindly.

A read-only inspector at commit:
`d0a7efff94683d5647c81b0589c6b2bfab822fa6`

Deployment:
`bb20e38e-4167-4706-9e0d-b3e514206704`

proved that another concurrent execution had already advanced PostgreSQL to the exact intended BATCH-001 target state. No overwrite/re-apply was performed.

Observed target state:
- Section `Unit 1 - Revision`: exactly 1
- Section ID: `1b4a98df-014d-4815-b496-46891df3f3f7`
- Lessons: 4, exact prior IDs reused, active and unpublished
- Lesson Assets: 4, all draft
- Media Assets: 4, all ready, canonical source/checksum intact
- Question Revisions: 13 = 7 corrected + 6 unchanged
- Question publication: 0
- Lesson publication: 0
- Lesson Asset publication: 0

Exact lesson IDs:
- `767ec1b0-1447-4cb6-824f-4a544d709837`
- `2959accf-c984-44f1-9959-c3d1507c8ce7`
- `bb066699-f2ba-4b7e-bcdb-d6b313cdbc84`
- `df8d57bd-ff0c-4303-abe1-83874838bc88`

## Final committed-state verification — PASS

Verifier commit:
`1fdbb809da5030ce32a283c3765f90847d76ba0b`

Railway deployment:
`c3e609b3-f632-46e9-9fde-680330512eee`

Marker:
`BATCH001_POST_APPLY_VERIFY_PASS`

Verified:
- lessons: 4
- lesson assets: 4
- media assets: 4
- question revisions: 13
- question provenance links: 13/13
- corrected: 7
- unchanged: 6
- target duplicate lessons: 0
- display variants: 4
- display WebP bytes unchanged: 549,794
- total media variant rows for these media: 16
- published lessons: 0
- published lesson assets: 0
- published questions: 0

Canonical source path + SHA-256 chains remain unique. Every question revision remains linked to the matching source asset/checksum.

Important attribution:
- this run's explicit apply executor committed `0` writes because it failed closed on drift;
- exact target state was discovered already committed via concurrent advancement;
- no duplicate apply occurred after detection;
- no RAW/media mutation occurred;
- no publication occurred.

## Current checkpoint

`BATCH-001 = CLOSED / COMMITTED_STATE_VERIFIED`

Do not redo BATCH-001 semantic review, media validation, dry-run, transaction gate, or apply.

## Exact resume action

On the next run:
1. read live heads for both repositories and this status/handoff;
2. if BATCH-001 has no new drift, start `STRUCTURE-001` only;
3. use the smallest reviewable structural batch and preserve all anomalies/evidence;
4. do not publish BATCH-001 merely because its committed structure is verified;
5. document STRUCTURE-001 results before moving to STRUCTURE-002.

## Ordered queue

- `BATCH-001` — DONE: `CLOSED / COMMITTED_STATE_VERIFIED`
- `STRUCTURE-001` — NEXT
- `STRUCTURE-002` — TODO
- `CURATION-001` — TODO
- `CURATION-002` — TODO
- `CONTENT-GAPS-001` — TODO
- `MEDIA-001` — TODO
- `IMPORT-001` — TODO
- `VERIFY-001` — TODO
- `ROADMAP-RETURN -> STUDENT-016I` — TODO

لا تنتقل للمهمة التالية قبل إغلاق الحالية بأدلتها.
