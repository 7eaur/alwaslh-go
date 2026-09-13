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

### MEDIA-001 — DONE / MEDIA_PROFILE_VERIFIED_PARTIAL_ACCEPTANCE

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
- book page 5: RAW `93,793` -> q76 `74,416`, reduction `20.66%`, PSNR `39.52 dB`, unchanged `962x1360`; manual contact-sheet review passed -> accepted as a reproducible derived candidate
- page 6 q76 `15.83%` reduction -> reject
- page 7 q76 `9.61%` reduction -> reject
- page 8 q76 `17.42%` reduction -> reject
- exact accepted page-5 derived SHA-256: `4fdeb9e17a0a269481ee046bcbf67053f834c8e75fdb4d5bda445977b742a5e2`
- no binary media was committed/uploaded to production in MEDIA-001
- RAW/DB/publication/unrelated mutation: 0

## IMPORT-001 — IN PROGRESS / ROLLBACK_GATE_VERIFIED

IMPORT-001 continues only on CURATION-001 `Describing people and animals`, book pages `5..8` / source pages `9..12`.

Live identity inspection passed:
- deployment `4cf8665b-4dd1-4e90-9ec8-92d897c34f59` — SUCCESS
- marker `IMPORT001_INSPECT_PASS`
- exact active Grade 9/English offering: 1
- exact source identities/checksums: 4/4
- Media Assets: 4, all ready
- Lesson Assets: 4, all draft/unpublished
- legacy Lessons: 4, active/unpublished/sectionless
- target Unit 2 Section absent
- target curated Lesson slug absent
- publication count lessons/assets: 0/0

Rollback-only transaction gate passed:
- script `content-staging/runtime/import-001-transaction-gate.mjs`
- script commit `177b91572ac6fe3b37acd9bcc094876a1cbb3beb`
- deployment `8e4cdcbb-2783-4dca-b025-e1191fa9e330` — SUCCESS
- marker `IMPORT001_TRANSACTION_GATE_PASS`
- rollback verified: true
- committed business writes: 0

Validated eventual mutation boundary:
- create 1 Section: `curated-english9-pb3-unit-2-describing-making-plans`
- create 1 Lesson: `curated-english9-pb3-u2-describing-people-and-animals`
- reassign exactly 4 existing Lesson Assets into reviewed order 0..3
- create/mutate Media Assets: 0/0
- mutate legacy Lessons: 0
- mutate Questions: 0
- publication changes: 0
- unrelated rows: 0
- preserved legacy Question Revisions: 12

Reused Media IDs:
- `3d53954b-95ef-4833-ae06-407f2325e28e`
- `9d4f61a2-8c00-44cf-9baa-7e48740e0ef6`
- `3aadf23a-432d-4391-bd2f-467eaefe486b`
- `b0b1d37e-1b9f-43a3-9987-4973423d822c`

Reused Lesson Asset IDs:
- `d8dfb014-23bb-4db0-b6c2-3aa8e98862eb`
- `b474bec6-8828-45e9-8b28-40ff0b52a9c2`
- `cec764c8-dce3-4917-8dea-66a36165ec89`
- `bdaca047-29a2-4730-81d5-2abd173a93ce`

Media policy retained:
- structural import reuses existing Media chains; it does not silently replace media binaries.
- accepted page-5 q76 derivative remains a reproducible verified candidate, not a production mutation in this gate.
- pages 6..8 remain on current source/preferred media state.

No PostgreSQL committed business write, RAW mutation, media binary mutation, publication mutation, question mutation, anomaly deletion or unrelated mutation occurred in this checkpoint.

## Current checkpoint

- `BATCH-001 = DONE / COMMITTED_STATE_VERIFIED`
- `STRUCTURE-001 = DONE / SECTION_BOUNDARY_VERIFIED`
- `STRUCTURE-002 = DONE / SECTION_BOUNDARY_VERIFIED`
- `CURATION-001 = DONE / LESSON_BOUNDARY_VERIFIED`
- `CURATION-002 = DONE / LESSON_BOUNDARY_VERIFIED`
- `CONTENT-GAPS-001 = DONE / GAP_INVENTORY_VERIFIED`
- `MEDIA-001 = DONE / MEDIA_PROFILE_VERIFIED_PARTIAL_ACCEPTANCE`
- `IMPORT-001 = IN PROGRESS / ROLLBACK_GATE_VERIFIED`

## Exact resume action

On the next run:
1. read both live heads + execution status + this handoff;
2. re-run strict identity/count/checksum/provenance/publication guards immediately before writing;
3. derive a controlled apply from the verified rollback gate with exactly `1 Section + 1 Lesson + 4 Lesson Asset reassignments`;
4. fail closed on any drift;
5. do not mutate legacy Lessons, Questions, Media binaries/assets, RAW, publication, anomalies or unrelated rows;
6. after commit, run an independent post-apply verifier and only then close IMPORT-001;
7. do not start VERIFY-001 until IMPORT-001 committed state is verified.

## Ordered queue

- `BATCH-001` — DONE
- `STRUCTURE-001` — DONE
- `STRUCTURE-002` — DONE
- `CURATION-001` — DONE
- `CURATION-002` — DONE
- `CONTENT-GAPS-001` — DONE
- `MEDIA-001` — DONE
- `IMPORT-001` — IN PROGRESS
- `VERIFY-001` — TODO
- `ROADMAP-RETURN -> STUDENT-016I` — TODO

لا تنتقل للمهمة التالية قبل إغلاق الحالية بأدلتها.