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
- WebP لا يُقبل لمجرد كونه WebP؛ يجب إثبات فائدة الحجم والوضوح لكل candidate.

## Corpus truth retained

Legacy snapshot SHA-256:
`2dfde94f6b70c037bb15d2782d11f036441c4abe130295be772c59b5e0131d0c`

Full RAW extraction:
- Subjects: 58
- Pages/images: 5,273 / 5,273
- Questions: 25,755
- Download failures: 0
- Empty subjects preserved: 2
- Corpus-wide duplicate page-position anomalies preserved: 6

Grade 9 English:
- RAW pages/images: 69 / 69
- questions: 104
- sections recovered: 8
- manifest-only page 70 remains evidence-only
- old 62 Draft lessons are reconciliation state, not curriculum truth

## Completed checkpoints

### BATCH-001 — DONE / COMMITTED_STATE_VERIFIED

`BATCH-001-G9-EN-PB3-U1` retained state:
- Unit 1 Section exactly 1
- reused Lessons 4
- draft Lesson Assets 4
- ready canonical Media Assets 4
- reviewed Question Revisions 13 = 7 corrected + 6 unchanged
- provenance 13/13
- duplicate target lessons 0
- published lessons/assets/questions 0/0/0
- final verifier deployment `c3e609b3-f632-46e9-9fde-680330512eee`
- marker `BATCH001_POST_APPLY_VERIFY_PASS`

Do not redo BATCH-001 unless fresh drift invalidates evidence.

### STRUCTURE-001 — DONE / SECTION_BOUNDARY_VERIFIED

- Unit 2 `Describing: Making plans`
- book pages `5..15`; source pages `9..19`
- 11 source identities; 30 legacy question attachments preserved
- evidence commit `4ff71ca280c432392c8d91737374c77232b3fe69`

### STRUCTURE-002 — DONE / SECTION_BOUNDARY_VERIFIED

- Unit 3 `Other countries`
- book pages `16..25`; source pages `20..29`
- 10 source identities; 3 legacy questions preserved
- evidence commit `9e92a4b4d7658f6ea43f1f0727ffb19e922c66cb`

### CURATION-001 — DONE / LESSON_BOUNDARY_VERIFIED

- Lesson `Describing people and animals`
- book pages `5..8`; source pages `9..12`
- 4 ordered page activities; 12 attached legacy questions preserved
- evidence commit `67f630f42913528405246fad7c541b091a47959e`

### CURATION-002 — DONE / LESSON_BOUNDARY_VERIFIED

- Lesson `Telling time and arranging a meeting`
- book pages `9..10`; source pages `13..14`
- 2 ordered page activities; 7 attached legacy questions preserved
- page 11/source 15 starts the next unresolved boundary
- evidence commit `d14774adc68470e9eea48a1c388a14a66111bf57`

### CONTENT-GAPS-001 — DONE / GAP_INVENTORY_VERIFIED

- 69 RAW page candidates/images
- 104 questions
- 8 recovered sections
- reviewed Lesson-boundary coverage: 10 pages
- unresolved boundary candidates: 59 pages
- immediate Unit 2 remainder pages `11..15` = 5 pages / 11 questions
- page 70 remains manifest-only evidence without RAW identity
- Grade 9 English duplicate page-number anomalies: 0
- corpus-wide duplicate-position anomalies remain preserved: 6
- verified modern mappings in this track: 4; other 65 are `unverified`, not asserted missing
- inventory commit `dd86641decbcb3e3345d1aacfea7e2363fc60474`

No PostgreSQL/RAW/Media/publication mutation occurred in the structural/curation/gap tasks.

## MEDIA-001 — DONE / MEDIA_PROFILE_VERIFIED_PARTIAL_ACCEPTANCE

Scope: smallest reviewed batch only — CURATION-001 pages `5..8`.

Execution evidence:
- probe script commit `2f1849536738e3f877018539a80b73e83a969c3f`
- workflow commit `10ce6c2b250de28b5de9389cbcaf9b2e7cddad09`
- workflow run `34761171601` — SUCCESS
- artifact `media-001-evidence`, ID `10318976732`
- artifact digest `sha256:9702cbac1ed18e1be1809eaf844685b78c24c150958da1781ce0b7f1ad75e91a`
- decision contract `content-staging/curated/grade-9/english/pupil-book-3/media-001-unit2-describing.json`
- decision commit `bb3dbbeff5d866930c1921124a8868b79af5703e`

Acceptance gate:
- same dimensions as RAW
- PSNR >= 32 dB
- at least 20% byte reduction
- manual side-by-side legibility review required for accepted candidates

Measured result:
- four RAW JPEGs total `457,747` bytes
- q82/method6 total `464,290` bytes = `+1.43%`; reject as a batch profile
- q76/method6 total `387,774` bytes = `15.29%` reduction overall; page-level gate still applies
- book page 5: RAW `93,793` -> q76 `74,416`, reduction `20.66%`, PSNR `39.52 dB`, unchanged `962x1360`; manual contact-sheet review passed for headings/body/labels/numbers -> accepted as a reproducible derived candidate
- page 6 q76 `15.83%` reduction -> reject
- page 7 q76 `9.61%` reduction -> reject
- page 8 q76 `17.42%` reduction -> reject
- all q82 candidates rejected for insufficient savings; pages 6 and 7 q82 are larger than RAW

Important:
- q76 is not a global profile.
- only page 5 passed every gate.
- pages 6..8 keep RAW/preferred existing media until another candidate is separately verified.
- exact accepted page-5 derived SHA-256: `4fdeb9e17a0a269481ee046bcbf67053f834c8e75fdb4d5bda445977b742a5e2`.
- no binary media was committed/uploaded to production in MEDIA-001.
- RAW/DB/publication/unrelated mutation: 0.

## Current checkpoint

- `BATCH-001 = DONE / COMMITTED_STATE_VERIFIED`
- `STRUCTURE-001 = DONE / SECTION_BOUNDARY_VERIFIED`
- `STRUCTURE-002 = DONE / SECTION_BOUNDARY_VERIFIED`
- `CURATION-001 = DONE / LESSON_BOUNDARY_VERIFIED`
- `CURATION-002 = DONE / LESSON_BOUNDARY_VERIFIED`
- `CONTENT-GAPS-001 = DONE / GAP_INVENTORY_VERIFIED`
- `MEDIA-001 = DONE / MEDIA_PROFILE_VERIFIED_PARTIAL_ACCEPTANCE`
- `IMPORT-001 = NEXT`

## Exact resume action

On the next run:
1. read live heads for both repositories + execution status + this handoff;
2. if no evidence-invalidating drift exists, execute `IMPORT-001` only;
3. choose the smallest controlled import from content whose Lesson/Activity boundaries are already reviewed;
4. resolve live modern identities/provenance and fail closed on ambiguity or count drift;
5. dry-run before any controlled apply;
6. page 5 may use the tested q76/method6 derivative only if deterministic regeneration yields SHA-256 `4fdeb9e17a0a269481ee046bcbf67053f834c8e75fdb4d5bda445977b742a5e2`; otherwise fail closed;
7. pages 6..8 do not inherit q76 automatically; retain RAW/preferred media unless another candidate passes a separate media gate;
8. do not import unresolved pages, auto-publish, mutate RAW, use `69 -> 62`, delete anomalies, or touch unrelated records;
9. document exact create/reuse/update counts, rollback evidence, verification evidence, failures and next action.

## Ordered queue

- `BATCH-001` — DONE
- `STRUCTURE-001` — DONE
- `STRUCTURE-002` — DONE
- `CURATION-001` — DONE
- `CURATION-002` — DONE
- `CONTENT-GAPS-001` — DONE
- `MEDIA-001` — DONE
- `IMPORT-001` — NEXT
- `VERIFY-001` — TODO
- `ROADMAP-RETURN -> STUDENT-016I` — TODO

لا تنتقل للمهمة التالية قبل إغلاق الحالية بأدلتها.
