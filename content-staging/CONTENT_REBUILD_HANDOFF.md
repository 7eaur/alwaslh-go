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
- book pages `5..15`; source pages `9..19`
- 11 source identities; 30 legacy question attachments preserved
- page 16 starts Unit 3

## STRUCTURE-002 — DONE

`Unit 3 - Other countries`:
- evidence: `content-staging/curated/grade-9/english/pupil-book-3/structure-002-unit-3.json`
- creation commit: `9e92a4b4d7658f6ea43f1f0727ffb19e922c66cb`
- book pages `16..25`; source pages `20..29`
- 10 source identities; 3 legacy questions preserved
- page 26/source 30 starts Unit 4

## CURATION-001 — DONE

- evidence: `content-staging/curated/grade-9/english/pupil-book-3/curation-001-unit-2-describing.json`
- creation commit: `67f630f42913528405246fad7c541b091a47959e`
- Lesson: `Describing people and animals`
- book pages `5..8`; source pages `9..12`
- 4 ordered activities/page assets; 12 attached legacy questions preserved

## CURATION-002 — DONE

- evidence: `content-staging/curated/grade-9/english/pupil-book-3/curation-002-unit-2-time-and-meeting.json`
- creation commit: `d14774adc68470e9eea48a1c388a14a66111bf57`
- Lesson: `Telling time and arranging a meeting`
- book pages `9..10`; source pages `13..14`
- 2 ordered activities/page assets; 7 attached legacy questions preserved
- page 11/source 15 begins the next unresolved boundary

## CONTENT-GAPS-001 — DONE

Status: `GAP_INVENTORY_VERIFIED`.

Evidence:
- `content-staging/curated/grade-9/english/pupil-book-3/content-gaps-001.json`
- inventory commit `dd86641decbcb3e3345d1aacfea7e2363fc60474`
- status close commit `34d194f48a9c4da87352ed3be58d6f06f8b14e40`

Exact inventory:
- 69 RAW page candidates / 69 RAW images / 104 legacy questions / 8 recovered sections
- reviewed Lesson-boundary page coverage: 10 pages
- unresolved boundary candidates: 59 pages
- immediate Unit 2 unresolved remainder: book pages `11..15` / source pages `15..19` = 5 pages / 11 questions
- source-manifest-only evidence: one entry, book page `70` / source page `74`, `Blank Final Page`, Back Matter; it has no corresponding immutable RAW identity and is not importable as curriculum content without new evidence
- Grade 9 English RAW subject anomaly truth: duplicate page numbers 0; missing images 0; multiple images 0; malformed AI questions 0; malformed image URLs 0; invalid/null page numbers 0; download failures 0
- corpus-wide duplicate-position anomalies remain preserved at 6; they are not Grade 9 English anomalies
- verified modern page mappings in this rebuild track: 4 (BATCH-001)
- other 65 RAW candidates: modern mapping `unverified`, not asserted missing

Important interpretation:
- do not derive a desired count from historical `62 Draft lessons`;
- do not infer `69 -> 62` deletion, curriculum membership or missing mappings;
- anomalies remain visible and preserved rather than being removed to normalize counts.

No PostgreSQL, RAW, Media or publication mutation occurred in CONTENT-GAPS-001.

## Current checkpoint

- `BATCH-001 = DONE / COMMITTED_STATE_VERIFIED`
- `STRUCTURE-001 = DONE / SECTION_BOUNDARY_VERIFIED`
- `STRUCTURE-002 = DONE / SECTION_BOUNDARY_VERIFIED`
- `CURATION-001 = DONE / LESSON_BOUNDARY_VERIFIED`
- `CURATION-002 = DONE / LESSON_BOUNDARY_VERIFIED`
- `CONTENT-GAPS-001 = DONE / GAP_INVENTORY_VERIFIED`
- `MEDIA-001 = NEXT`

## Exact resume action

On the next run:
1. read live heads for `7eaur/alwaslh` and `7eaur/alwaslh-go` plus status/handoff;
2. if no evidence-invalidating drift exists, execute `MEDIA-001` only;
3. choose the smallest reviewable media batch from preserved RAW identities;
4. measure RAW vs derived candidate byte counts and verify visual legibility before accepting a derivative;
5. do not accept WebP merely because it is WebP; BATCH-001 existing WebP was `+24.81%` larger than RAW;
6. never overwrite RAW in place;
7. do not use media processing to resolve curriculum membership or Lesson boundaries;
8. do not publish or mutate unrelated PostgreSQL content to close MEDIA-001;
9. document input/output checksums, byte counts, acceptance/rejection reason and exact next action.

## Ordered queue

- `BATCH-001` — DONE
- `STRUCTURE-001` — DONE
- `STRUCTURE-002` — DONE
- `CURATION-001` — DONE
- `CURATION-002` — DONE
- `CONTENT-GAPS-001` — DONE
- `MEDIA-001` — NEXT
- `IMPORT-001` — TODO
- `VERIFY-001` — TODO
- `ROADMAP-RETURN -> STUDENT-016I` — TODO

لا تنتقل للمهمة التالية قبل إغلاق الحالية بأدلتها.
