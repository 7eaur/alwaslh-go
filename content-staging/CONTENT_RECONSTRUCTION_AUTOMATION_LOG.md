# Alwaslh Content Reconstruction — Sequential Automation Plan & Shared Handoff

> هذا الملف هو نقطة التنسيق التشغيلية المشتركة بين مهمتي التنفيذ المتعاقبتين. يجب على كل مهمة قراءته من النسخة الحية قبل أي تعديل، ثم تحديثه في نهاية تشغيلها. لا تعتمد أي مهمة على ذاكرة محادثة سابقة بدل المستودع والأدلة.

## 1. الهدف

إكمال مرحلة `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY` لكل مصادر المحتوى بشكل متسلسل، قابل للتدقيق، ومن دون تعارض بين المنفذين، مع الحفاظ الكامل على RAW/provenance وعدم القفز إلى Import/Publication قبل اكتمال بوابات المرحلة الحالية.

نمط التشغيل:

- Worker A يعمل في دورة دورية مستقلة.
- Worker B يعمل في دورة دورية مستقلة بعد A بنصف ساعة.
- كل Worker يبدأ دائمًا من live branch + آخر سجل في هذا الملف.
- كل Worker ينفذ أكبر وحدة عمل آمنة ومتماسكة يمكن إنهاؤها والتحقق منها في تشغيل واحد.
- كل Worker يوثق ما فعل، يثبت HEAD النهائي، ويحدد `Exact next operation` قبل التسليم.

## 2. Source of Truth

الترتيب الإلزامي للحقيقة:

1. immutable RAW files.
2. checksums / byte sizes / IDs / provenance.
3. reconstruction + technical manifests generated from evidence.
4. visual evidence when boundaries/content identity require it.
5. exact proven `master` references only when source identity is established.
6. later: PostgreSQL schema/migrations for Import Readiness only.
7. runtime verification where applicable.
8. documentation.

إذا لم يُثبت شيء بالأدلة: اكتب `NOT VERIFIED`. لا تخمّن.

## 3. Repository / Branch / Phase

- Repository: `7eaur/alwaslh-go`
- Branch: `content/corpus-inventory-20260914`
- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Baseline HEAD before this automation plan: `df62ba1f424b23346af5c49eaee1063022298ca0`
- RAW immutable roots include:
  - `content/legacy-supabase-reconstruction`
  - `content-staging/raw/legacy-supabase/...`

Forbidden during this phase:

- RAW overwrite/delete/recompression/reformat.
- provenance loss.
- silent correction of source evidence.
- inventing Books/Units/Lessons/Exam Models/Answer Keys.
- treating Exam Source Group count as Individual Exam Model count.
- carrying source-local page/model patterns into another source without new evidence.
- new production import.
- new publication.
- rerunning closed Grade 9 English work without fresh drift evidence.

## 4. Verified checkpoint before sequential automation

- Sources processed: **4/58**
- Educational sources processed: **1/26**
- Books / Units / Lessons / Lesson Pages: **1 / 9 / 57 / 149**
- Exam Source Groups processed: **3/32**
- Individual Exam Models: **62**
- Finalized Exam Pages: **236/2,286**
- Verified Answer Keys: **0**
- Correction/report candidates: **66**
- Source images technically verified: **422/5,273**
- WebP generated / accepted / rejected: **0 / 0 / 0**
- Legacy Questions: **25,755**
- Lesson-linked: **2,225**
- Exam-linked: **226**
- Review-required questions: **351**
- Unclassified questions: **22,953**
- Global duplicate fingerprint groups classified: **0/99**
- RAW mutations: **0**
- Unrelated mutations: **0**
- New imports: **0**
- New publications: **0**

Last completed source:

- `e7c8291c-e904-4e8c-9cd8-2753818cedf3` — `الكيمياء نماذج وزاريه 1447`
- Result: 124/124 technically verified and visually reviewed; 29 verified occurrences; 28 unique models; 116 finalized model pages; 8 review-required pages; 226/226 source questions structurally accounted for; 0 verified standalone Answer Keys.

Current source at automation-plan creation:

- Source ID: `ef408805-c337-44dd-b903-7838030e6de0`
- Name: `العلوم نماذج وزارية 1445`
- Class/subject: `تاسع العلوم`
- Manifest evidence: 30 pages/images; 215 legacy questions; no listed manifest anomalies for duplicate page numbers/missing/malformed entries.

## 5. Sequential Worker Protocol

### Startup — mandatory on every run

1. Fetch live branch HEAD.
2. Fetch this file from live branch, never from a remembered copy.
3. Read the latest `RUN` block and `ACTIVE CHECKPOINT` below.
4. Read `content-staging/CONTENT_REBUILD_EXECUTION_STATUS.md` and `content-staging/CONTENT_REBUILD_HANDOFF.md` only as supporting documentation; live code/manifests/evidence outrank stale prose.
5. Confirm no conflicting active mutation is visible. Because workers are staggered, a changed HEAD from the previous worker is expected: re-read it and continue from it.
6. Never reuse a stale blob SHA for a shared-file update. Fetch the latest file/blob immediately before writing.
7. If another change makes the intended update non-fast-forward or semantically conflicting, do not overwrite. Re-read, reconcile, then write only if safe. Otherwise record a blocker.

### Work unit — mandatory order per source

For an Exam Source Group:

`manifest/read -> technical verification -> duplicate scan -> boundary discovery -> visual inspection -> model occurrence resolution -> unique model resolution -> correction/answer-key evidence -> question mapping -> invariant checks -> reconstruction/manifests -> checkpoint -> next source`

For an Educational source:

`manifest/read -> technical verification -> exact source identity -> structure evidence -> Book/Unit/Lesson/page boundaries -> non-lesson/review/glossary isolation -> question mapping -> invariant checks -> reconstruction/manifests -> checkpoint -> next source`

Rules:

- Finish an evidence-backed source when possible before switching.
- If a source has isolated ambiguity, quarantine only the ambiguous pages/items as `review_required` and continue when the remainder is safe.
- Do not turn a local duplicate group into a global 99-group classification unless the baseline global fingerprint group mapping is actually proven.
- Official Answer Key must be explicit evidence. Candidate correction/electronic report != verified standalone official Answer Key.
- Do not silently merge duplicate source occurrences. Preserve provenance and classify relation.

### Heavy/visual work

Use existing generic/source-specific tooling and GitHub Actions where appropriate. Generated artifacts may be used for visual boundary evidence. Never claim a workflow result before its run is successful and its emitted evidence is inspected.

### Commit discipline

- Keep commits source-local and meaningful.
- A discovery commit/workflow may be separate from finalization when visual evidence is required.
- After automation/bot commits, re-fetch live branch HEAD before continuing.
- Do not assume a commit SHA until GitHub confirms it exists on the branch.
- No production DB mutation/publication in this phase.

## 6. Cross-worker conflict prevention

The shared handoff is logical locking, not permission to overwrite:

- Only one worker writes this file at the end of its run.
- The next worker must consume the latest committed version.
- Start HEAD and end HEAD must be recorded.
- If previous worker left `state: IN_PROGRESS`, inspect GitHub/workflow state first. Continue only when the work is safely resumable and no live conflicting run is still mutating the same source.
- If the same source has a running workflow, prefer inspecting/completing that workflow rather than creating a duplicate.
- Never create two source-finalization paths for the same source concurrently.
- If a workflow is still running and its completion is required for truth, record `WAITING_ON_WORKFLOW` and do another non-conflicting evidence/read-only unit if available; otherwise hand off without guessing.

## 7. Mandatory invariants after every finalized source

Verify and document:

- `lesson_linked + exam_linked + review_required + unclassified == 25,755`
- technical source page/image counts reconcile to source manifest.
- cumulative source images verified never exceed 5,273.
- finalized Exam Pages are evidence-backed pages only.
- Exam Source Group count remains distinct from Individual Exam Model count.
- no unsupported Answer Keys.
- RAW mutations = 0.
- unrelated mutations = 0.
- new imports = 0.
- new publications = 0.

If any invariant fails: fail closed, mark blocker, do not normalize numbers to make them fit.

## 8. Phase-completion gate

Continue source-by-source automatically through all 58 sources.

When reconstruction is complete:

1. Reconcile all source manifests, question classification, duplicates, models, Answer Keys, review-required items.
2. Complete global duplicate fingerprint classification with evidence.
3. Complete WebP derivative decision/gating separately from RAW.
4. Produce a full reconstruction validation checkpoint.
5. Move only to **Import Readiness / Dry Run planning**.

Do **not** perform production Apply or new Publication merely because reconstruction completed. Production DB apply/publication remains a separate guarded decision/gate unless explicitly authorized by the owner.

## 9. Mandatory run report format

Append a new section at the bottom on every run using exactly this shape:

```md
## RUN YYYY-MM-DDTHH:MM:SS+03:00 — Worker A|B

- state: COMPLETE | PARTIAL_SAFE_HANDOFF | WAITING_ON_WORKFLOW | BLOCKED
- start HEAD: `<sha>`
- end HEAD: `<sha>`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `<id> — <name>`
- completed in this run:
  - ...
- evidence produced/verified:
  - ...
- ambiguity/review_required:
  - ...
- invariant result: PASS | FAIL
- Sources processed: X/58
- Educational: X/26
- Books / Units / Lessons / Lesson Pages: X / X / X / X
- Exam Source Groups: X/32
- Individual Exam Models: X
- Exam Pages: X/2,286
- Verified Answer Keys: X
- Source images technical: X/5,273
- WebP generated / accepted / rejected: X / X / X
- Legacy Questions: 25,755
- Lesson-linked: X
- Exam-linked: X
- Review-required: X
- Unclassified: X
- Duplicate groups classified: X/99
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `<id — name>`
- current source: `<id — name>`
- exact next operation: `...`
- next source: `<id — name or NOT YET RESOLVED>`
- blockers: `none | ...`
- handoff note: `...`
```

Do not rewrite or delete older RUN sections. Append-only history makes handoff auditable.

## 10. ACTIVE CHECKPOINT

- state: `READY`
- branch: `content/corpus-inventory-20260914`
- latest verified work HEAD before this handoff commit: `cbb294ada860c16bbf647499983361a5bae0def0`
- last completed source: `8489a487-91d9-47fb-80b8-35d0e7a074a4 — الانجليزي نماذج وزارية 1445`
- current source: `062f0aa0-ae21-454e-ad9a-c390df6e4a08 — الانجليزي نماذج وزارية 1446`
- current source baseline from live manifest: `39 images/pages; 0 legacy questions; manifest anomaly arrays empty`
- current operation: `read live manifest/pages -> technically verify all 39 images -> scan source-local duplicate SHA/sequence -> generate complete visual evidence -> resolve Individual Exam Model and correction/answer-key boundaries only from English 1446 evidence -> preserve NOT VERIFIED where evidence is insufficient -> map 0 legacy questions without fabrication -> assert global invariant -> checkpoint`
- next source: `NOT YET RESOLVED — derive only after English 1446 from live MASTER_CONTENT_MANIFEST`
- blockers: `none`
- owner decision required now: `no`

---

### Shared handoff rule

Worker A and Worker B must treat this file as the operational baton. Read latest -> verify live state -> execute one safe coherent unit -> append RUN -> update ACTIVE CHECKPOINT to the newest truth -> hand off. Never skip evidence, never overwrite the other worker's unreviewed work, and never trade correctness for apparent progress.

## RUN 2026-09-14T08:39:00+03:00 — Worker A

- state: COMPLETE
- start HEAD: `659ba2323cc0c79c737d4bd657913e7ba9889a33`
- end HEAD before handoff-log commit: `7fa9297a44cefb80de470c873c9b646c3910bc5d`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `ef408805-c337-44dd-b903-7838030e6de0 — العلوم نماذج وزارية 1445`
- completed in this run:
  - added the source-local Science 1445 discovery workflow using only generic verification/discovery tools and source-local evidence;
  - completed 30/30 technical verification;
  - generated and inspected complete contact sheets covering pages 1..30;
  - verified ten source-local three-page model occurrences, each with two question pages followed by an explicitly titled correction-model page;
  - created `reconstruct_science_exam_1445.py` and evidence-backed final reconstruction JSON;
  - structurally mapped all 215 legacy questions to the ten verified models;
  - created/ran the checkpoint recorder and updated MASTER_CONTENT_MANIFEST plus status/handoff/inventory/validation/import/continuation docs;
  - exact-head GitHub Actions finalization job completed successfully and committed the derived checkpoint.
- evidence produced/verified:
  - technical report: `content-staging/reconstruction/technical/ef408805-c337-44dd-b903-7838030e6de0.json`;
  - discovery report: `content-staging/reconstruction/exams/source-groups/ef408805-c337-44dd-b903-7838030e6de0-discovery.json`;
  - final reconstruction: `content-staging/reconstruction/exams/source-groups/ef408805-c337-44dd-b903-7838030e6de0.json`;
  - GitHub Actions run `34810342183`: all finalization steps success;
  - visual evidence: complete contact sheets 001-012, 013-024, 025-030;
  - within-source duplicate SHA groups: 0.
- ambiguity/review_required:
  - source model boundaries: none; explicit metadata titles and full visual review agree;
  - standalone official Answer Keys: `NOT VERIFIED`; correction-model pages are retained as correction-sheet candidates only;
  - semantic correctness of legacy AI questions: `NOT VERIFIED`.
- invariant result: PASS
- Sources processed: 5/58
- Educational: 1/26
- Books / Units / Lessons / Lesson Pages: 1 / 9 / 57 / 149
- Exam Source Groups: 4/32
- Individual Exam Models: 72
- Exam Pages: 266/2,286
- Verified Answer Keys: 0
- Source images technical: 452/5,273
- WebP generated / accepted / rejected: 0 / 0 / 0
- Legacy Questions: 25,755
- Lesson-linked: 2,225
- Exam-linked: 441
- Review-required: 351
- Unclassified: 22,738
- Duplicate groups classified: 0/99
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `ef408805-c337-44dd-b903-7838030e6de0 — العلوم نماذج وزارية 1445`
- current source: `004c02be-3f55-49e1-bbdc-b0824491bd68 — العلوم نماذج وزارية 1446`
- exact next operation: `Read the 1446 Science manifest and pages metadata; technically verify all 39 source images; scan local duplicates/sequence; generate full contact sheets; resolve model/correction boundaries only from 1446 evidence; map all 30 source questions; assert global invariant; checkpoint and continue.`
- next source: `14ef15e0-5524-473a-bbdb-996df35ba535 — العلوم نماذج وزارية 1447`
- blockers: `none`
- handoff note: `Worker B should re-fetch live HEAD and this file, confirm no workflow remains active for Science 1445, then start Science 1446 from its own evidence. Do not inherit the 3-page model pattern merely because 1445 used it.`

## RUN 2026-09-14T09:05:39+03:00 — Worker B

- state: COMPLETE
- start HEAD: `cfd49a55b8787a156a8b2fe3c9a23a396a0f92ae`
- end HEAD before handoff-log commit: `1030dcbcbe56d39da24fd6277186f966b4e2fd33`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `004c02be-3f55-49e1-bbdc-b0824491bd68 — العلوم نماذج وزارية 1446`
- completed in this run:
  - verified Worker A's Science 1445 finalization against live HEAD and successful Actions evidence before continuing;
  - completed 39/39 non-destructive technical verification for Science 1446;
  - corrected only a validation-schema defect exposed by the first discovery run; no RAW/source evidence was altered;
  - generated and reviewed complete visual contact sheets covering pages 1..39;
  - independently verified thirteen source-local three-page occurrences, each with two question pages followed by a matching electronic correction/result page;
  - created `reconstruct_science_exam_1446.py` and `record_science_exam_1446_checkpoint.py`;
  - structurally mapped all 30 legacy questions to the thirteen verified Individual Exam Models;
  - completed exact-head finalization and updated MASTER_CONTENT_MANIFEST plus canonical status/handoff/inventory/validation/import/continuation documents.
- evidence produced/verified:
  - technical report: `content-staging/reconstruction/technical/004c02be-3f55-49e1-bbdc-b0824491bd68.json`;
  - discovery report: `content-staging/reconstruction/exams/source-groups/004c02be-3f55-49e1-bbdc-b0824491bd68-discovery.json`;
  - final reconstruction: `content-staging/reconstruction/exams/source-groups/004c02be-3f55-49e1-bbdc-b0824491bd68.json`;
  - discovery workflow run `34811638024`: success after correcting the validation-only schema assertion;
  - finalization workflow run `34811873986`: success with `SCIENCE_1446_FINALIZATION_VERIFY_PASS`;
  - final artifact `10335330050`, SHA-256 `e1455d59dc6d12b66259fd2c9d412b5134ba719048358645179423826eca7e81`;
  - visual evidence: contact sheets 001-012, 013-024, 025-036, 037-039;
  - within-source duplicate SHA groups: 0.
- ambiguity/review_required:
  - model boundaries: none; explicit metadata and complete visual evidence agree for all thirteen blocks;
  - standalone official Answer Keys: `NOT VERIFIED`; thirteen correction/result pages remain correction-sheet candidates only;
  - semantic correctness of legacy AI questions: `NOT VERIFIED`.
- invariant result: PASS (`2,225 + 471 + 351 + 22,708 = 25,755`)
- Sources processed: 6/58
- Educational: 1/26
- Books / Units / Lessons / Lesson Pages: 1 / 9 / 57 / 149
- Exam Source Groups: 5/32
- Individual Exam Models: 85
- Exam Pages: 305/2,286
- Verified Answer Keys: 0
- Correction/report candidates: 89
- Source images technical: 491/5,273
- WebP generated / accepted / rejected: 0 / 0 / 0
- Legacy Questions: 25,755
- Lesson-linked: 2,225
- Exam-linked: 471
- Review-required: 351
- Unclassified: 22,708
- Duplicate groups classified: 0/99
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `004c02be-3f55-49e1-bbdc-b0824491bd68 — العلوم نماذج وزارية 1446`
- current source: `14ef15e0-5524-473a-bbdb-996df35ba535 — العلوم نماذج وزارية 1447`
- exact next operation: `Fetch Science 1447 live manifest/pages; technically verify every source image; scan source-local duplicates/sequence; generate full visual evidence; resolve model/correction boundaries only from 1447 evidence; map its legacy questions; assert the 25,755 invariant; checkpoint; then resolve the following source from live MASTER_CONTENT_MANIFEST.`
- next source: `NOT YET RESOLVED — derive after Science 1447 from live MASTER_CONTENT_MANIFEST`
- blockers: `none`
- handoff note: `Worker A must re-fetch live HEAD and this baton, verify no Science 1446 workflow remains active, then start Science 1447 from its own evidence. Do not inherit the 13x3 page pattern from 1446.`

## RUN 2026-09-14T09:46:00+03:00 — Worker A

- state: COMPLETE
- start HEAD: `d5b3ceac50e73d42c13dea2531af5d3a876780c4`
- end HEAD before handoff-log commit: `fc5718a9c678386b2b5c6e6ad16838c972c2f89f`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `14ef15e0-5524-473a-bbdb-996df35ba535 — العلوم نماذج وزارية 1447`
- completed in this run:
  - verified Worker B's Science 1446 finalization against the live reconstruction and branch state;
  - completed 42/42 non-destructive technical verification for Science 1447: file existence, readability, byte size, SHA-256 and MIME all match;
  - generated and reviewed complete visual evidence for all 42 source image records;
  - detected and preserved the source metadata numbering anomaly: stored page 35 is absent and page number 36 occurs twice;
  - proved the two stored page-36 image records are distinct identities and distinct SHA-256 binaries, not duplicate files;
  - reconciled model 12 from source-record order + legacy IDs + visual evidence: record d37e... is paper 1; e5be... is visually paper 2 despite its corrupted correction title/page number; 4e7b... is the correction/result record;
  - did not fabricate page 35 and did not rewrite RAW or legacy metadata;
  - independently resolved fourteen source-local Individual Exam Models and fourteen correction/result candidates;
  - structurally mapped all 262 legacy questions to the fourteen verified models;
  - finalized the source and updated MASTER_CONTENT_MANIFEST plus canonical status/handoff/inventory/validation/import/continuation documents.
- evidence produced/verified:
  - technical report: `content-staging/reconstruction/technical/14ef15e0-5524-473a-bbdb-996df35ba535.json`;
  - discovery report: `content-staging/reconstruction/exams/source-groups/14ef15e0-5524-473a-bbdb-996df35ba535-discovery.json`;
  - anomaly evidence: `content-staging/reconstruction/exams/source-groups/14ef15e0-5524-473a-bbdb-996df35ba535-anomaly-evidence.json`;
  - final reconstruction: `content-staging/reconstruction/exams/source-groups/14ef15e0-5524-473a-bbdb-996df35ba535.json`;
  - discovery workflow run `34814241092`: success;
  - anomaly-evidence workflow run `34814423651`: success;
  - finalization workflow run `34814757302`: success with `SCIENCE_1447_FINALIZATION_VERIFY_PASS`;
  - final artifact `10336311813`, SHA-256 `f5cd59cb5851a84d3c3dad5555ae8976da61abb9033e051af39b23a4a1f4f4a6`;
  - within-source duplicate SHA groups: 0.
- ambiguity/review_required:
  - source numbering/title anomaly for model 12 is preserved as provenance and logically resolved without changing RAW; no model/page block remains review_required;
  - standalone official Answer Keys: `NOT VERIFIED`; fourteen correction/result records remain candidates only;
  - semantic correctness of legacy AI questions: `NOT VERIFIED`.
- invariant result: PASS (`2,225 + 733 + 351 + 22,446 = 25,755`)
- Sources processed: 7/58
- Educational: 1/26
- Books / Units / Lessons / Lesson Pages: 1 / 9 / 57 / 149
- Exam Source Groups: 6/32
- Individual Exam Models: 99
- Exam Pages: 347/2,286
- Verified Answer Keys: 0
- Correction/report candidates: 103
- Source images technical: 533/5,273
- WebP generated / accepted / rejected: 0 / 0 / 0
- Legacy Questions: 25,755
- Lesson-linked: 2,225
- Exam-linked: 733
- Review-required: 351
- Unclassified: 22,446
- Duplicate groups classified: 0/99
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `14ef15e0-5524-473a-bbdb-996df35ba535 — العلوم نماذج وزارية 1447`
- current source: `f4b6708c-027f-4883-9e85-e6e7acb52ecc — كتاب العلوم - الجزء الأول`
- current source baseline from live manifest: `161 images/pages; 11 legacy questions; manifest anomaly arrays currently empty`
- exact next operation: `Fetch the current educational source live manifest/pages and any source-specific reference evidence; technically verify all 161 image records; determine the actual book page range and structure from its own metadata/visual evidence; reconstruct units/lessons/reviews/appendices without inheriting Chemistry structure; structurally map the 11 questions only where evidence supports it; mark unresolved items review_required; assert the 25,755 question invariant; checkpoint; then resolve the following source from live MASTER_CONTENT_MANIFEST.`
- next source: `NOT YET RESOLVED — derive only after the current source from live MASTER_CONTENT_MANIFEST`
- blockers: `none`
- handoff note: `Worker B must re-fetch live HEAD and this baton, verify no Science 1447 finalization workflow remains active, then treat f4b6708c... as an educational book source. Do not apply exam-model logic or inherit Chemistry book boundaries; reconstruct from this Science book's own evidence.`

## RUN 2026-09-14T10:11:00+03:00 — Worker B

- state: COMPLETE
- start HEAD: `82f36c98862709c396fa0cc98002bd2bbaa2815e`
- end verified content HEAD: `45f5065a5027ac9cf9c2876e7d4051d8387b3481`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `f4b6708c-027f-4883-9e85-e6e7acb52ecc — كتاب العلوم - الجزء الأول`
- completed in this run:
  - verified Worker A's Science 1447 handoff against live reconstruction evidence and branch state;
  - completed 161/161 non-destructive technical verification for Science Part 1;
  - established exact source identity against `master/تاسع علوم/علوم_تاسع_الجزء_الأول`: 161/161 retained RAW images are exact SHA-256 matches;
  - proved the retained stored range 7..167 corresponds to master source pages 8..168, while master-only pages outside that slice remain reference-only;
  - reconstructed 8 Units, 22 Lessons, 138 Lesson pages, 8 Unit-cover pages and 15 Unit-review pages from exact master section/title runs;
  - classified every retained page exactly once and created the finalized educational reconstruction;
  - structurally linked all 11 source questions to the verified `المحلول ومكوناته` lesson; semantic correctness remains NOT VERIFIED;
  - updated MASTER_CONTENT_MANIFEST and canonical execution/handoff/inventory/validation/import/continuation reports;
  - exact-head finalization workflow completed successfully with final invariant verification.
- evidence produced/verified:
  - technical report: `content-staging/reconstruction/technical/f4b6708c-027f-4883-9e85-e6e7acb52ecc.json`;
  - identity/structure discovery: `content-staging/reconstruction/educational/f4b6708c-027f-4883-9e85-e6e7acb52ecc-discovery.json`;
  - final reconstruction: `content-staging/reconstruction/educational/f4b6708c-027f-4883-9e85-e6e7acb52ecc.json`;
  - discovery workflow run `34816305370`: success with 161/161 exact identity;
  - finalization workflow run `34816564726`: success with `SCIENCE_BOOK_PART1_FINALIZATION_VERIFY_PASS`;
  - master reference: `تاسع علوم/علوم_تاسع_الجزء_الأول`;
  - within-source duplicate SHA groups: 0.
- ambiguity/review_required:
  - no retained structural page remains ambiguous after exact identity/title-run reconstruction;
  - source question review-required count: 0;
  - semantic correctness of the 11 legacy AI questions: `NOT VERIFIED`;
  - master-only pages 1..7 and 169..170 are not fabricated into the retained source.
- invariant result: PASS (`2,236 + 733 + 351 + 22,435 = 25,755`)
- Sources processed: 8/58
- Educational: 2/26
- Books / Units / Lessons / Lesson Pages: 2 / 17 / 79 / 287
- Exam Source Groups: 6/32
- Individual Exam Models: 99
- Exam Pages: 347/2,286
- Verified Answer Keys: 0
- Source images technical: 694/5,273
- WebP generated / accepted / rejected: 0 / 0 / 0
- Legacy Questions: 25,755
- Lesson-linked: 2,236
- Exam-linked: 733
- Review-required: 351
- Unclassified: 22,435
- Duplicate groups classified: 0/99
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `f4b6708c-027f-4883-9e85-e6e7acb52ecc — كتاب العلوم - الجزء الأول`
- current source: `81e99fe6-1421-462b-9562-1c0c5053a809 — كتاب العلوم - الجزء الثاني`
- exact next operation: `Fetch Science Part 2 live manifest/pages; technically verify all 145 images; establish exact RAW/master identity against master/تاسع علوم/علوم_تاسع_الجزء_الثاني; reconstruct its own units/lessons/reviews from exact evidence; confirm the manifest's 0-question state; assert the 25,755 global invariant; checkpoint; then continue to English Ministry Exams 1445.`
- next source: `8489a487-91d9-47fb-80b8-35d0e7a074a4 — الانجليزي نماذج وزارية 1445`
- blockers: `none`
- handoff note: `Worker A should re-fetch live HEAD and this baton, confirm Science Part 1 finalization is complete, then start Science Part 2 from its own evidence. Do not assume Part 1 unit/lesson counts or retained ranges.`

## RUN 2026-09-14T10:42:23+03:00 — Worker A

- state: COMPLETE
- start HEAD: `5f6f0450e6c9c19a38579950e0e80cf34e690be2`
- end HEAD before handoff-log commit: `30cca9916e801a1d1e8085b71bf6f3fbb8e9d41c`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `81e99fe6-1421-462b-9562-1c0c5053a809 — كتاب العلوم - الجزء الثاني`
- completed in this run:
  - verified Worker B's Science Part 1 finalization against the live branch and shared handoff;
  - completed 145/145 non-destructive technical verification for Science Part 2;
  - established exact source identity against `master/تاسع علوم/علوم_تاسع_الجزء_الثاني`: 145/145 retained RAW images are exact SHA-256 matches;
  - proved retained stored pages 7..151 correspond to master source pages 8..152; master-only pages 1..7 and 153..154 remain reference-only;
  - reconstructed units 9..16 as 8 Units, 31 Lessons, 126 Lesson pages, 8 Unit-cover pages and 11 Unit-review pages from exact master section/title runs;
  - classified every retained page exactly once and finalized the educational reconstruction;
  - confirmed the source contains 0 legacy questions and fabricated no question links;
  - updated MASTER_CONTENT_MANIFEST and canonical execution/handoff/inventory/validation/import/continuation reports;
  - exact-head finalization workflow completed successfully with all final invariant steps green.
- evidence produced/verified:
  - technical report: `content-staging/reconstruction/technical/81e99fe6-1421-462b-9562-1c0c5053a809.json`;
  - identity/structure discovery: `content-staging/reconstruction/educational/81e99fe6-1421-462b-9562-1c0c5053a809-discovery.json`;
  - final reconstruction: `content-staging/reconstruction/educational/81e99fe6-1421-462b-9562-1c0c5053a809.json`;
  - discovery workflow run `34818641697`: success;
  - finalization workflow run `34818819467`: success including `SCIENCE_BOOK_PART2_FINALIZATION_VERIFY_PASS`;
  - master reference: `تاسع علوم/علوم_تاسع_الجزء_الثاني`;
  - within-source duplicate SHA groups: 0.
- ambiguity/review_required:
  - no retained structural page remains ambiguous after exact identity/title-run reconstruction;
  - source question review-required count: 0 because the source contains 0 questions;
  - master-only pages outside the retained slice were not fabricated.
- invariant result: PASS (`2,236 + 733 + 351 + 22,435 = 25,755`)
- Sources processed: 9/58
- Educational: 3/26
- Books / Units / Lessons / Lesson Pages: 3 / 25 / 110 / 413
- Exam Source Groups: 6/32
- Individual Exam Models: 99
- Exam Pages: 347/2,286
- Verified Answer Keys: 0
- Source images technical: 839/5,273
- WebP generated / accepted / rejected: 0 / 0 / 0
- Legacy Questions: 25,755
- Lesson-linked: 2,236
- Exam-linked: 733
- Review-required: 351
- Unclassified: 22,435
- Duplicate groups classified: 0/99
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `81e99fe6-1421-462b-9562-1c0c5053a809 — كتاب العلوم - الجزء الثاني`
- current source: `8489a487-91d9-47fb-80b8-35d0e7a074a4 — الانجليزي نماذج وزارية 1445`
- exact next operation: `Fetch English 1445 live manifest/pages; technically verify all 30 images; scan source-local duplicate SHA/sequence; generate complete visual evidence; resolve exam-model and correction/answer-key boundaries only from English 1445 evidence; map its 0 current legacy questions without fabrication; assert the 25,755 invariant; checkpoint and continue.`
- next source: `NOT YET RESOLVED — derive after English 1445 from live MASTER_CONTENT_MANIFEST`
- blockers: `none`
- handoff note: `Worker B must re-fetch live HEAD and this baton, confirm Science Part 2 finalization is complete, then start English Ministry Exams 1445 from its own evidence. Do not inherit Science or Chemistry page/model patterns.`

## RUN 2026-09-14T11:04:50+03:00 — Worker B

- state: COMPLETE
- start HEAD: `e54247c7163021845d9ccff9725ae0c95a6179f1`
- end HEAD before handoff-log commit: `cbb294ada860c16bbf647499983361a5bae0def0`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `8489a487-91d9-47fb-80b8-35d0e7a074a4 — الانجليزي نماذج وزارية 1445`
- completed in this run:
  - verified Worker A's Science Part 2 handoff against the live reconstructed source and branch HEAD;
  - read the English 1445 live manifest/pages and preserved its zero-question baseline;
  - added and ran a source-local technical/boundary discovery workflow;
  - corrected one validation-only workflow assertion after confirming the actual technical-report schema; no RAW or derived content was mutated by the failed validation run;
  - completed 30/30 technical verification and generated/inspected complete visual contact sheets covering all source pages;
  - independently verified ten three-page source occurrences, each consisting of two question-paper pages followed by a correction/result page;
  - created the source-specific reconstruction and checkpoint runners;
  - finalized 10 unique Individual Exam Models / 30 finalized Exam Pages / 10 correction-result candidates / 0 verified standalone Answer Keys;
  - preserved the source's 0 legacy questions without fabrication or synthetic mapping;
  - updated MASTER_CONTENT_MANIFEST and canonical reconstruction/status reports through the exact-head finalization workflow.
- evidence produced/verified:
  - discovery workflow successful run: `34820548866`; visual artifact `10337464503`, digest `sha256:01fdf1fe21e5e22b31ea03bc997b7fd235b29df3760eb1a9b13a53fe68379123`;
  - finalization workflow successful run: `34820816202`, exact input HEAD `3b36508c2bd6d088952eae324f696b348790bf29`;
  - final gate marker: `ENGLISH_1445_FINALIZATION_VERIFY_PASS`;
  - final artifact: `10338470690`, digest `sha256:cd738188943122d5ec16b30f99f63a7d4b4fa8a7648bff13449ebed76dce0812`;
  - final reconstruction: `content-staging/reconstruction/exams/source-groups/8489a487-91d9-47fb-80b8-35d0e7a074a4.json`;
  - final checkpoint bot commit: `cbb294ada860c16bbf647499983361a5bae0def0`.
- ambiguity/review_required:
  - model boundaries: none; metadata sequence and complete visual inspection agree on 10 source-local occurrences;
  - standalone official Answer Keys: `NOT VERIFIED`; the third pages remain correction/result candidates only;
  - official model codes/titles/term beyond evidence: `NOT VERIFIED`;
  - source legacy questions: 0, so semantic question review is not applicable to this source.
- invariant result: PASS
- Sources processed: 10/58
- Educational: 3/26
- Books / Units / Lessons / Lesson Pages: 3 / 25 / 110 / 413
- Exam Source Groups: 7/32
- Individual Exam Models: 109
- Exam Pages: 377/2,286
- Verified Answer Keys: 0
- Source images technical: 869/5,273
- WebP generated / accepted / rejected: 0 / 0 / 0
- Legacy Questions: 25,755
- Lesson-linked: 2,236
- Exam-linked: 733
- Review-required: 351
- Unclassified: 22,435
- Duplicate groups classified: 0/99
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `8489a487-91d9-47fb-80b8-35d0e7a074a4 — الانجليزي نماذج وزارية 1445`
- current source: `062f0aa0-ae21-454e-ad9a-c390df6e4a08 — الانجليزي نماذج وزارية 1446`
- exact next operation: `Fetch English 1446 live manifest/pages; technically verify all 39 images; inspect source-local page-number/SHA/title/storage evidence; generate complete visual contact sheets; derive model/correction boundaries only from English 1446 evidence; keep official Answer Keys NOT VERIFIED unless explicit evidence exists; preserve its 0-question baseline; assert the 25,755 invariant; checkpoint.`
- next source: `NOT YET RESOLVED — derive after English 1446 from live MASTER_CONTENT_MANIFEST`
- blockers: `none`
- handoff note: `Worker A must re-fetch live HEAD and this baton, verify the English 1445 finalization checkpoint, then begin English 1446 from its own evidence. Do not inherit the English 1445 three-page pattern without verifying all 39 pages.`

