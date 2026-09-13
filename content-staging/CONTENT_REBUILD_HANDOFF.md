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

Do not redo BATCH-001 unless fresh drift invalidates evidence.

## STRUCTURE-001 — DONE

`Unit 2 - Describing: Making plans`:
- evidence: `content-staging/curated/grade-9/english/pupil-book-3/structure-001-unit-2.json`
- creation commit: `4ff71ca280c432392c8d91737374c77232b3fe69`
- book pages `5..15`
- source pages `9..19`
- 11 source identities
- 30 legacy question attachments preserved
- page 16 starts Unit 3
- Lesson boundaries intentionally unresolved at this stage

## STRUCTURE-002 — DONE

`Unit 3 - Other countries`:
- evidence: `content-staging/curated/grade-9/english/pupil-book-3/structure-002-unit-3.json`
- creation commit: `9e92a4b4d7658f6ea43f1f0727ffb19e922c66cb`
- book pages `16..25`
- source pages `20..29`
- 10 source identities with RAW SHA-256 references preserved
- 3 legacy questions preserved on book page 22/source page 26
- page 26/source page 30 starts `Unit 4 - Visiting Japan` (`A Japanese pen-friend`)
- repeated `Four countries` pages remain distinct source identities
- no question rewrite, RAW mutation, PostgreSQL mutation, publication change, anomaly deletion, or unrelated-record mutation

## CURATION-001 — DONE

First reviewed Lesson boundary inside Unit 2:
- evidence: `content-staging/curated/grade-9/english/pupil-book-3/curation-001-unit-2-describing.json`
- creation commit: `67f630f42913528405246fad7c541b091a47959e`
- reviewed Lesson: `Describing people and animals`
- book pages `5..8`
- source pages `9..12`
- four ordered source pages retained as activities/page assets, not four automatically promoted Lessons
- attached legacy questions preserved: `12`
- all four RAW SHA-256 values preserved

Boundary evidence retained:
- page 5 introduces physical description;
- page 6 develops descriptive vocabulary/opposites;
- page 7 applies description to people;
- page 8 applies description to animals;
- page 9/source page 13 changes topic to `What's the time?`, so it begins the next curation boundary.

Question text was used only as supporting boundary evidence. The 12 legacy AI questions were not semantically approved, corrected, rejected or published in CURATION-001.

No PostgreSQL, RAW, Media or publication mutation occurred.

## CURATION-002 — DONE

Second reviewed Lesson boundary inside Unit 2:
- evidence: `content-staging/curated/grade-9/english/pupil-book-3/curation-002-unit-2-time-and-meeting.json`
- creation commit: `d14774adc68470e9eea48a1c388a14a66111bf57`
- reviewed Lesson: `Telling time and arranging a meeting`
- book pages `9..10`
- source pages `13..14`
- two ordered source pages retained as activities/page assets, not two auto-promoted Lessons
- attached legacy questions preserved: `7`
- RAW SHA-256 values preserved for both pages

Boundary evidence retained:
- page 9 establishes clock/time expressions;
- page 10 applies those expressions to a schedule and arranging a meeting;
- page 11/source page 15 changes instructional focus to `Things to do` and obligation/task language, so it begins the next unresolved boundary.

The 7 legacy AI questions were used only as supporting boundary evidence; none was semantically approved, corrected, rejected or published in CURATION-002.

Unit 2 pages `11..15` remain unresolved and preserved. No PostgreSQL, RAW, Media or publication mutation occurred.

## Current checkpoint

- `BATCH-001 = DONE / COMMITTED_STATE_VERIFIED`
- `STRUCTURE-001 = DONE / SECTION_BOUNDARY_VERIFIED`
- `STRUCTURE-002 = DONE / SECTION_BOUNDARY_VERIFIED`
- `CURATION-001 = DONE / LESSON_BOUNDARY_VERIFIED`
- `CURATION-002 = DONE / LESSON_BOUNDARY_VERIFIED`
- `CONTENT-GAPS-001 = NEXT`

## Exact resume action

On the next run:
1. read live heads for `7eaur/alwaslh` and `7eaur/alwaslh-go` plus status/handoff;
2. if no evidence-invalidating drift exists, execute `CONTENT-GAPS-001` only;
3. inventory explicit unresolved/missing content evidence rather than guessing curriculum membership;
4. include at minimum unresolved Unit 2 book pages `11..15`, manifest-only page 70, preserved duplicate-position anomalies, and missing/ambiguous modern mappings;
5. do not use `69 -> 62` as deletion or curriculum logic;
6. preserve source identities, anomalies, checksums and question provenance;
7. do not publish or mutate PostgreSQL/RAW merely to close the inventory;
8. document exact gap counts before moving to `MEDIA-001`.

## Ordered queue

- `BATCH-001` — DONE
- `STRUCTURE-001` — DONE
- `STRUCTURE-002` — DONE
- `CURATION-001` — DONE
- `CURATION-002` — DONE
- `CONTENT-GAPS-001` — NEXT
- `MEDIA-001` — TODO
- `IMPORT-001` — TODO
- `VERIFY-001` — TODO
- `ROADMAP-RETURN -> STUDENT-016I` — TODO

لا تنتقل للمهمة التالية قبل إغلاق الحالية بأدلتها.
