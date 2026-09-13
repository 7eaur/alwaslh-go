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

`BATCH-001-G9-EN-PB3-U1 = CLOSED / COMMITTED_STATE_VERIFIED`.

Retained verified state:
- Unit 1 Section exactly 1
- 4 reused Lessons
- 4 draft Lesson Assets
- 4 ready canonical Media Assets
- 13 reviewed Question Revisions = 7 corrected + 6 unchanged
- provenance links 13/13
- duplicate target lessons 0
- published lessons/assets/questions all 0
- RAW/media mutation 0
- final verifier deployment `c3e609b3-f632-46e9-9fde-680330512eee`
- marker `BATCH001_POST_APPLY_VERIFY_PASS`

Do not redo BATCH-001 review, dry-run, transaction gate, import, or verification unless fresh drift invalidates evidence.

## STRUCTURE-001 — DONE

Smallest structural batch completed:
`Unit 2 - Describing: Making plans`.

Evidence contract:
`content-staging/curated/grade-9/english/pupil-book-3/structure-001-unit-2.json`

Creation commit:
`4ff71ca280c432392c8d91737374c77232b3fe69`

Verified structural boundary:
- book pages `5..15`
- source pages `9..19`
- `11` page/source identities preserved
- `30` legacy questions remain attached to their exact pages
- book page `16` begins `Unit 3 - Other countries`, providing the explicit next-section boundary

Important interpretation:
- this approves Unit/Section membership only;
- page titles remain Lesson/Activity candidates;
- final Lesson boundaries are NOT approved;
- no one-page-equals-one-lesson inference is permitted;
- no question rewrite occurred;
- no RAW, PostgreSQL, publication, or unrelated-record mutation occurred.

Execution status update commit:
`bb833a9f1cb3ce084feb3526d4ab4bfa4b6c4431`

## Current checkpoint

- `BATCH-001 = DONE / COMMITTED_STATE_VERIFIED`
- `STRUCTURE-001 = DONE / SECTION_BOUNDARY_VERIFIED`
- `STRUCTURE-002 = NEXT`

## Exact resume action

On the next run:
1. read live heads for `7eaur/alwaslh` and `7eaur/alwaslh-go` plus status/handoff;
2. if no evidence-invalidating drift exists, execute `STRUCTURE-002` only;
3. choose the smallest next reviewable structural batch;
4. recover/verify only Unit/Section membership and exact page/source boundaries;
5. preserve every source identity, anomaly, checksum and question-to-page provenance;
6. do not promote page candidates to final Lessons during STRUCTURE work;
7. do not mutate PostgreSQL or publish content as part of structural reconstruction;
8. document the exact result before moving to CURATION-001.

## Ordered queue

- `BATCH-001` — DONE
- `STRUCTURE-001` — DONE
- `STRUCTURE-002` — NEXT
- `CURATION-001` — TODO
- `CURATION-002` — TODO
- `CONTENT-GAPS-001` — TODO
- `MEDIA-001` — TODO
- `IMPORT-001` — TODO
- `VERIFY-001` — TODO
- `ROADMAP-RETURN -> STUDENT-016I` — TODO

لا تنتقل للمهمة التالية قبل إغلاق الحالية بأدلتها.
