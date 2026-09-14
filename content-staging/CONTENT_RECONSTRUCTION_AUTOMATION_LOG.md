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

- state: `READY_FOR_NEXT_SOURCE`
- branch: `content/corpus-inventory-20260914`
- latest verified work HEAD before this handoff commit: `f404c5749fc3f96c27ed163ebdec095723df6711`
- last completed source: `f25891fe-ea52-481b-baf2-ff4764c79bde — الاسلاميه ثانوي نماذج وزاريه 1447`
- current source: `cae82d8f-64f9-4d2a-984f-6e6fd19fac5c — الحديث والتهذيب الكتاب `
- current source baseline from live manifest: `62 pages/images, 1483 legacy questions, 0 download failures; manifest anomalies: duplicate_page_numbers=0, missing_images=0, multiple_images=0, malformed_ai_questions=0. Technical verification / source identity / reconstruction remain NOT VERIFIED unless live evidence says otherwise.`
- current operation: `Re-fetch live HEAD and baton; confirm no active/running workflow for this source; technically verify immutable media first; establish educational identity/structure only from source-specific evidence; structurally map its 1,483 legacy questions only where page membership proves placement; quarantine uncertainty as review_required/NOT VERIFIED; reassert the 25,755 invariant.`
- next source: `Resolve from live manifest only after the current source is safely finalized.`
- blockers: `none at handoff; do not inherit Islamic-exam three-page boundaries into the educational source.`
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

## RUN 2026-09-14T11:39:30+03:00 — Worker A

- state: COMPLETE
- start HEAD: `e7d9de180e32cd0315b97831b2376d169a2fe2b4`
- end HEAD before handoff-log commit: `52e2ac53841e5a53ecb4deac85e6e2bdb777fc8a`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `062f0aa0-ae21-454e-ad9a-c390df6e4a08 — الانجليزي نماذج وزارية 1446`
- completed in this run:
  - verified Worker B's English 1445 finalization against live branch state and shared handoff;
  - completed 39/39 non-destructive technical verification for English 1446: existence/readability/byte-size/SHA-256/MIME all match and page sequence 1..39 is contiguous;
  - generated and visually inspected complete contact sheets covering all 39 source pages;
  - independently resolved thirteen source-local three-page exam occurrences, each with two question-paper pages followed by its matching correction/result page;
  - preserved visible correction-form codes as source evidence without promoting them to official model codes;
  - finalized 13 unique Individual Exam Models / 39 finalized Exam Pages / 13 correction-result candidates / 0 verified standalone Answer Keys;
  - preserved the source's 0 legacy questions without fabrication or synthetic mapping;
  - updated MASTER_CONTENT_MANIFEST and canonical reconstruction/status/handoff/inventory/validation/import/continuation reports through exact-head GitHub Actions finalization.
- evidence produced/verified:
  - discovery workflow run `34823356315`: success; artifact `10338234805`, digest `sha256:98637b8b6283b83b0513eeef86f05d46ce132e326f4596ceda3d19a0abf2d49f`;
  - complete visual sheets reviewed: `001-012`, `013-024`, `025-036`, `037-039`;
  - technical report: `content-staging/reconstruction/technical/062f0aa0-ae21-454e-ad9a-c390df6e4a08.json`;
  - discovery report: `content-staging/reconstruction/exams/source-groups/062f0aa0-ae21-454e-ad9a-c390df6e4a08-discovery.json`;
  - final reconstruction: `content-staging/reconstruction/exams/source-groups/062f0aa0-ae21-454e-ad9a-c390df6e4a08.json`;
  - finalization workflow run `34823771285`: success with `ENGLISH_1446_FINALIZATION_VERIFY_PASS`;
  - final artifact `10339383045`, digest `sha256:d42e8508475e4a6a848a634abad3047eab8dfd569b0dd022831f72361712b850`;
  - finalized reconstruction bot commit: `52e2ac53841e5a53ecb4deac85e6e2bdb777fc8a`;
  - within-source duplicate SHA groups: 0.
- ambiguity/review_required:
  - model boundaries: none after full source-local metadata + visual review;
  - standalone official Answer Keys: `NOT VERIFIED`; thirteen correction/result pages remain candidates only;
  - official model codes/titles/term beyond explicit evidence: `NOT VERIFIED`;
  - source legacy questions: 0, so no semantic question mapping was fabricated.
- invariant result: PASS (`2,236 + 733 + 351 + 22,435 = 25,755`)
- Sources processed: 11/58
- Educational: 3/26
- Books / Units / Lessons / Lesson Pages: 3 / 25 / 110 / 413
- Exam Source Groups: 8/32
- Individual Exam Models: 122
- Exam Pages: 416/2,286
- Verified Answer Keys: 0
- Source images technical: 908/5,273
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
- last completed source: `062f0aa0-ae21-454e-ad9a-c390df6e4a08 — الانجليزي نماذج وزارية 1446`
- current source: `da6fc228-1ada-4627-8306-80d9d3401490 — الانجليزي نماذج وزارية 1447`
- exact next operation: `Fetch English 1447 live manifest/pages and preserve duplicate page-number identities at 18, 27 and 29; technically verify all 42 image records; inspect sequence/SHA/title/storage evidence and render complete contact sheets; resolve model/correction boundaries only from English 1447 evidence; map all 234 legacy questions only where structurally evidenced; quarantine unresolved records as review_required; assert global invariant; checkpoint.`
- next source: `NOT YET RESOLVED — derive after English 1447 from live MASTER_CONTENT_MANIFEST`
- blockers: `none`
- handoff note: `Worker B should re-fetch live HEAD and this baton, confirm English 1446 finalization is complete, then treat English 1447's duplicate page-number records as provenance to investigate rather than normalize. Do not inherit the 13x3 English 1446 pattern without new evidence.`

## RUN 2026-09-14T12:14:00+03:00 — Worker B

- state: COMPLETE
- start HEAD: `d9564231905245126316125e55ae46b5604549a1`
- end HEAD before handoff-log commit: `d28c2943c8ff20ec42f3091e3c693eba373da35d`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `da6fc228-1ada-4627-8306-80d9d3401490 — الانجليزي نماذج وزارية 1447`
- completed in this run:
  - verified Worker A's English 1446 handoff against live HEAD and canonical reconstruction evidence;
  - technically verified all 42 English 1447 source images with existence/readability/byte-size/SHA-256/MIME = 42/42 and no within-source SHA duplicates;
  - preserved source numbering anomalies exactly: missing numeric labels 12, 26, 37 and duplicate numeric labels 18, 27, 29;
  - generated and visually reviewed complete contact sheets for all 42 source records;
  - resolved 13 complete Individual Exam Models / 39 finalized pages from source-record identity + visual evidence, without inheriting 1446 boundaries;
  - isolated 3 page records as review_required rather than fabricating model 13 or silently repairing metadata;
  - structurally mapped all 234/234 legacy questions to finalized models; semantic correctness remains NOT VERIFIED;
  - finalized reconstruction and canonical manifests/status documents;
  - reconciled the global correction-candidate aggregate from the nine processed exam source records only: 140 total; no source evidence changed.
- evidence produced/verified:
  - technical report: `content-staging/reconstruction/technical/da6fc228-1ada-4627-8306-80d9d3401490.json`;
  - discovery report: `content-staging/reconstruction/exams/source-groups/da6fc228-1ada-4627-8306-80d9d3401490-discovery.json`;
  - final reconstruction: `content-staging/reconstruction/exams/source-groups/da6fc228-1ada-4627-8306-80d9d3401490.json`;
  - discovery run `34826039800`: success after validation-only schema correction from initial run `34825927300`;
  - source-order evidence run `34826307823`: success; artifact `10340652157`; SHA-256 `358985b359cc04f8ae14693ddbd0a880b33d132c13a8a26f0eb249139fbe72cd`;
  - finalization run `34826701560`: success with `ENGLISH_1447_FINALIZATION_VERIFY_PASS`;
  - final artifact `10340672655`; SHA-256 `e709c14fb086289ece84a44f0e4cab495b18b08f9d0d413f6838c26631321a95`.
- ambiguity/review_required:
  - source record 29 (stored page 29): distinct unmatched paper-2 record; `review_required`;
  - source records 38..39: model-13 paper 2 + correction, but paper 1 is `NOT VERIFIED`; both `review_required`; numeric page 37 was not fabricated;
  - source record 27 metadata says model-13 paper 1 but visual evidence is a correction/result sheet in completed model 9; RAW metadata remains unchanged;
  - standalone official Answer Keys: 0 / NOT VERIFIED.
- invariant result: PASS (`2,236 + 967 + 351 + 22,201 = 25,755`)
- Sources processed: 12/58
- Educational: 3/26
- Books / Units / Lessons / Lesson Pages: 3 / 25 / 110 / 413
- Exam Source Groups: 9/32
- Individual Exam Models: 135
- Exam Pages: 455/2,286
- Verified Answer Keys: 0
- Correction/report candidates: 140
- Source images technical: 950/5,273
- WebP generated / accepted / rejected: 0 / 0 / 0
- Legacy Questions: 25,755
- Lesson-linked: 2,236
- Exam-linked: 967
- Review-required: 351
- Unclassified: 22,201
- Duplicate groups classified: 0/99
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `da6fc228-1ada-4627-8306-80d9d3401490 — الانجليزي نماذج وزارية 1447`
- current source: `0a76f44b-0a4f-4e36-9ea9-badecf78bf23 — التاريخ الكتاب المدرسي`
- exact next operation: `Do not rerun closed Grade 9 English source 1794eea5-4772-4c94-bd2b-b08e5815e733 absent fresh drift evidence. Start History from its own 61-image/138-question manifest: technical verification -> exact identity -> visual/structural reconstruction -> question mapping -> invariant -> checkpoint.`
- next source: `7f02b242-5164-46d1-a82d-7f1023cfa8c9 — التربية الوطنية`
- blockers: `none for History; Grade 9 English corpus-master review_needed state is a deferred non-rerun reconciliation item, not permission to rerun its closed work.`
- handoff note: `Worker A must re-fetch live HEAD and this baton. English 1447 is closed. Proceed with History while preserving the no-rerun rule for Grade 9 English.`

## RUN 2026-09-14T12:50:00+03:00 — Worker A

- state: PARTIAL_SAFE_HANDOFF
- start HEAD: `a4f6a268e8a62d526d3187ec0f476fbedfc0cccb`
- end HEAD before handoff-log commit: `2b9460f218a7b3d1a410abda089040b0f510f92c`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `0a76f44b-0a4f-4e36-9ea9-badecf78bf23 — التاريخ الكتاب المدرسي`
- completed in this run:
  - verified Worker B's English 1447 closure and consumed the live baton;
  - read the History 61-page/138-question immutable source manifest;
  - completed non-destructive technical verification for all 61 History images: existence/readability/byte-size/SHA-256/MIME = 61/61, no missing/duplicate stored page numbers, no within-source SHA duplicate groups;
  - identified both available trusted master History references under `تاسع إجتماعيات` and tested them rather than assuming either part matched;
  - rejected exact-SHA identity safely: 0/61 RAW images are byte-identical to the 211 master History reference images;
  - rejected a page-number/filename-offset mapping after source-local evidence showed no strong perceptual matches;
  - ran global pHash+dHash+wHash ranking for every RAW page against all 211 pages across both master History parts;
  - global matching also failed closed: 0 strong page matches, best candidates do not come from one master part and do not form a consecutive sequence; therefore no master-derived unit/lesson/title mapping was accepted;
  - committed technical and diagnostic discovery evidence without mutating RAW, questions, imports or publications.
- evidence produced/verified:
  - technical report: `content-staging/reconstruction/technical/0a76f44b-0a4f-4e36-9ea9-badecf78bf23.json`;
  - diagnostic discovery: `content-staging/reconstruction/educational/0a76f44b-0a4f-4e36-9ea9-badecf78bf23-discovery.json`;
  - discovery workflow run `34828958697`: technical gate passed, exact-master identity intentionally failed closed;
  - perceptual diagnostic run `34829150813`: technical gate passed, fixed-page mapping rejected and evidence committed;
  - global visual matching run `34829503083`: technical gate passed, global comparison completed and evidence committed at `2b9460f218a7b3d1a410abda089040b0f510f92c`; identity assertion failed because evidence remained NOT VERIFIED;
  - global report: `master_reference_images_indexed=211`, `exact_master_sha_count=0`, `content_equivalence_verified_count=0`, `strong_page_count=0`, `sequence_verified=false`.
- ambiguity/review_required:
  - source identity against current master History references: `NOT VERIFIED`;
  - Book/Unit/Lesson/review boundaries: `NOT VERIFIED`;
  - 138 legacy questions remain structurally unclassified in the global baseline; semantic correctness: `NOT VERIFIED`;
  - no question was force-linked and no master title/section was copied onto this RAW.
- invariant result: PASS (`2,236 + 967 + 351 + 22,201 = 25,755`)
- Sources processed: 12/58
- Educational: 3/26
- Books / Units / Lessons / Lesson Pages: 3 / 25 / 110 / 413
- Exam Source Groups: 9/32
- Individual Exam Models: 135
- Exam Pages: 455/2,286
- Verified Answer Keys: 0
- Source images technical: 1,011/5,273
- WebP generated / accepted / rejected: 0 / 0 / 0
- Legacy Questions: 25,755
- Lesson-linked: 2,236
- Exam-linked: 967
- Review-required: 351
- Unclassified: 22,201
- Duplicate groups classified: 0/99
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `da6fc228-1ada-4627-8306-80d9d3401490 — الانجليزي نماذج وزارية 1447`
- current source: `0a76f44b-0a4f-4e36-9ea9-badecf78bf23 — التاريخ الكتاب المدرسي`
- exact next operation: `Use the verified 61 RAW pages themselves as authority: generate complete ordered contact sheets/visual evidence for stored pages 8..68; inspect cover/TOC/unit/lesson/review boundaries and source edition markers; derive a source-local reconstruction without importing master titles unless an individual page equivalence is later proven; map the 138 questions only after page-to-lesson boundaries are evidenced; quarantine ambiguous pages/items as review_required; reassert global invariant; finalize History only then.`
- next source: `7f02b242-5164-46d1-a82d-7f1023cfa8c9 — التربية الوطنية`
- blockers: `Current master History parts are not proven equivalent to the immutable RAW; source-local visual reconstruction is required before structural/question finalization.`
- handoff note: `Worker B should not retry the rejected exact-SHA or fixed-offset assumptions. Re-fetch live HEAD and this baton, confirm the three diagnostic runs/evidence, then continue History from complete RAW visual evidence. Keep History active; do not advance to التربية الوطنية until History is either evidence-finalized or only irreducible ambiguities are quarantined.`

## RUN 2026-09-14T13:15:00+03:00 — Worker B

- state: COMPLETE
- start HEAD: `aa707183aa03e0d47de68b717d6d097d7149c976`
- end HEAD before handoff-log commit: `fcbf85fde72e7b9d3a11d111f3ab01d00aeeee78`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `0a76f44b-0a4f-4e36-9ea9-badecf78bf23 — التاريخ الكتاب المدرسي`
- completed in this run:
  - verified Worker A's partial History handoff against live technical/discovery evidence and preserved the rejection of non-equivalent master History references;
  - generated complete ordered source-local visual evidence directly from all 61 immutable RAW pages and visually reviewed stored pages 8..68;
  - verified page 8 as an explicit TOC and page 9 as the `الفصل الدراسي الأول` cover;
  - resolved nine source-local lesson boundaries and twelve lesson-review pages without inventing an explicit Unit layer;
  - classified all 61 retained pages exactly once: 1 TOC + 1 semester cover + 47 lesson-content pages + 12 lesson-review pages;
  - structurally mapped all 138/138 legacy questions by verified page membership; semantic correctness remains NOT VERIFIED;
  - finalized the History reconstruction and updated MASTER_CONTENT_MANIFEST plus canonical status/inventory/validation/import/continuation files;
  - corrected one validation-only baseline assertion after discovering MASTER_CONTENT_MANIFEST still held the pre-History technical-image counter 950; no RAW/semantic state was mutated by the failed run.
- evidence produced/verified:
  - technical report: `content-staging/reconstruction/technical/0a76f44b-0a4f-4e36-9ea9-badecf78bf23.json`;
  - diagnostic master-equivalence report: `content-staging/reconstruction/educational/0a76f44b-0a4f-4e36-9ea9-badecf78bf23-discovery.json`;
  - visual index: `content-staging/reconstruction/educational/0a76f44b-0a4f-4e36-9ea9-badecf78bf23-visual-index.json`;
  - final reconstruction: `content-staging/reconstruction/educational/0a76f44b-0a4f-4e36-9ea9-badecf78bf23.json`;
  - source-local visual run `34831599212`; artifact `10342118472`; digest `sha256:dbb6cc5f980b293920f378ef24587ab9d9df65787e250fa955d33fbb3323a169`;
  - initial finalization run `34832016086` failed closed only on stale aggregate counter expectation (expected 1011, live manifest 950);
  - corrected finalization run `34832127755` passed `HISTORY_SOURCE_LOCAL_FINALIZATION_VERIFY_PASS`;
  - final artifact `10342790603`; digest `sha256:9c3cde6996f3cbb29741ffa1e22c989671ed1f241dfc0e7e8bf44666c88df1ca`;
  - final checkpoint commit: `fcbf85fde72e7b9d3a11d111f3ab01d00aeeee78`.
- ambiguity/review_required:
  - current master History parts remain `NOT VERIFIED` as equivalent to this RAW and were not used for semantic mapping;
  - formal book title beyond the legacy source label remains `NOT VERIFIED`;
  - no explicit Unit construct was proven in the retained slice, so no units were invented;
  - question semantic correctness remains `NOT VERIFIED`; structural membership is verified;
  - source review-required questions: 0.
- invariant result: PASS (`2,374 + 967 + 351 + 22,063 = 25,755`)
- Sources processed: 13/58
- Educational: 4/26
- Books / Units / Lessons / Lesson Pages: 4 / 25 / 119 / 460
- Exam Source Groups: 9/32
- Individual Exam Models: 135
- Exam Pages: 455/2,286
- Verified Answer Keys: 0
- Correction/report candidates: 140
- Source images technical: 1,011/5,273
- WebP generated / accepted / rejected: 0 / 0 / 0
- Legacy Questions: 25,755
- Lesson-linked: 2,374
- Exam-linked: 967
- Review-required: 351
- Unclassified: 22,063
- Duplicate groups classified: 0/99
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `0a76f44b-0a4f-4e36-9ea9-badecf78bf23 — التاريخ الكتاب المدرسي`
- current source: `7f02b242-5164-46d1-a82d-7f1023cfa8c9 — التربية الوطنية`
- exact next operation: `Fetch التربية الوطنية live manifest/pages; technically verify every source image and source-local sequence/SHA/MIME; establish identity and book/section/unit/lesson/review boundaries only from its own evidence; map its legacy questions only where structurally proven; quarantine ambiguity as review_required; assert 25,755 invariant; checkpoint.`
- next source: `NOT YET RESOLVED — derive after التربية الوطنية from live MASTER_CONTENT_MANIFEST`
- blockers: `none`
- handoff note: `Worker A should re-fetch live HEAD and this baton, verify History final reconstruction at fcbf85f..., then begin التربية الوطنية from its own evidence. Do not reopen History absent new drift evidence and do not inherit its semester/lesson pattern.`

## RUN 2026-09-14T13:40:00+03:00 — Worker A

- state: COMPLETE
- start HEAD: `1d11d21d75bd73b641b1f97c677b38f4a5f26583`
- end verified work HEAD before handoff tooling/log commit: `c6497f06a2810915d39e58b249e8060932ec3932`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `7f02b242-5164-46d1-a82d-7f1023cfa8c9 — التربية الوطنية`
- completed in this run:
  - verified Worker B's History completion against the live baton, manifest and evidence, then continued exactly from التربية الوطنية;
  - confirmed Civics baseline: 59 pages/images, 0 legacy questions, no manifest anomalies;
  - required unique exact SHA identity before using the explicit master Civics reference;
  - technically verified all 59 immutable RAW images: existence/readability/size/SHA-256/MIME 59/59, contiguous stored sequence 6..64, duplicate SHA groups 0;
  - established 59/59 unique byte-identical master matches, mapping stored 6..64 exactly to source pages 7..65;
  - reconstructed 4 units / 14 lessons / 48 lesson pages / 4 unit covers / 7 unit-review pages, with every retained page classified exactly once;
  - kept master-only source pages 1..6 and 66 reference-only rather than fabricating them;
  - confirmed 0 legacy questions; no question was fabricated or linked; semantic question review `NOT APPLICABLE`;
  - updated MASTER_CONTENT_MANIFEST and canonical status/inventory/validation/import/continuation evidence; no production import/publication;
  - fail-closed probe run `34833981327` stopped before any derived commit because a status guard did not recognize baseline `review_needed`; evidence stages had passed and no semantic state was written;
  - after verifying no prior technical/reconstruction finalization existed, successful run `34834237115` passed source reconstruction, both live-HEAD conflict gates and `CIVICS_FINALIZATION_VERIFY_PASS`, producing `c6497f06a2810915d39e58b249e8060932ec3932`.
- evidence produced/verified:
  - `content-staging/reconstruction/technical/7f02b242-5164-46d1-a82d-7f1023cfa8c9.json`;
  - `content-staging/reconstruction/educational/7f02b242-5164-46d1-a82d-7f1023cfa8c9-discovery.json`;
  - `content-staging/reconstruction/educational/7f02b242-5164-46d1-a82d-7f1023cfa8c9.json`;
  - exact reference: `master/تاسع إجتماعيات/التربية_الوطنية_تاسع`;
  - successful workflow run: `34834237115`;
  - final checkpoint commit: `c6497f06a2810915d39e58b249e8060932ec3932`.
- ambiguity/review_required:
  - Civics source ambiguity requiring quarantine: 0;
  - source questions: 0; no semantic claims invented;
  - Geography identity/lesson boundaries remain `NOT VERIFIED` until its own gates pass.
- invariant result: PASS (`2,374 + 967 + 351 + 22,063 = 25,755`)
- Sources processed: 14/58
- Educational: 5/26
- Books / Units / Lessons / Lesson Pages: 5 / 29 / 133 / 508
- Exam Source Groups: 9/32
- Individual Exam Models: 135
- Exam Pages: 455/2,286
- Verified Answer Keys: 0
- Correction/report candidates: 140
- Source images technical: 1,070/5,273
- WebP generated / accepted / rejected: 0 / 0 / 0
- Legacy Questions: 25,755
- Lesson-linked: 2,374
- Exam-linked: 967
- Review-required: 351
- Unclassified: 22,063
- Duplicate groups classified: 0/99
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `7f02b242-5164-46d1-a82d-7f1023cfa8c9 — التربية الوطنية`
- current source: `a7f1e94f-82d1-4146-af5b-4e9b51363f0b — كتاب الجغرافيا`
- current source baseline: `104 pages/images; 0 legacy questions; no manifest anomalies; technical verification NOT YET RUN.`
- exact next operation: `Re-fetch live HEAD/log; technically verify all 104 Geography RAW images and sequence/SHA/MIME; test identity against the explicit Geography reference only by exact/source evidence; reconstruct unit/lesson/review boundaries only after identity is proven; preserve any missing slice as reference-only; assert 25,755 invariant; checkpoint.`
- next source: `NOT YET RESOLVED — derive after Geography from live MASTER_CONTENT_MANIFEST`
- blockers: `none`
- handoff note: `Worker B should start with Geography from its own live evidence. Do not reopen Civics absent drift evidence and do not assume the Civics unit/title-run pattern applies to Geography.`

## RUN 2026-09-14T14:02:00+03:00 — Worker B

- state: COMPLETE
- start HEAD: `16064f06bf374f9b0875e6690a12775757fd45a8`
- end HEAD before handoff-log commit: `8c93e3846375ec0188c938dcc3fd8e1f25c83e6e`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `a7f1e94f-82d1-4146-af5b-4e9b51363f0b — كتاب الجغرافيا`
- completed in this run:
  - verified Worker A's Civics completion against the live branch, baton and canonical status evidence;
  - confirmed Geography baseline at 104 pages/images, 0 legacy questions and no manifest anomalies;
  - added a source-local fail-closed Geography reconstruction tool and exact-head finalization workflow;
  - technically verified 104/104 immutable RAW images without mutation;
  - established 104/104 unique exact SHA-256 identities against `master/تاسع إجتماعيات/جغرافيا_تاسع`;
  - proved the retained contiguous slice is stored/source pages 8..111; master-only pages 1..7 and 112..114 remain reference-only;
  - reconstructed 4 Units / 18 Lessons / 94 Lesson pages / 4 Unit covers / 6 Unit reviews / 0 non-lesson pages from exact section/title runs;
  - classified every retained page exactly once and preserved the zero-question source without fabrication;
  - updated MASTER_CONTENT_MANIFEST and canonical status/inventory/validation/import/continuation evidence;
  - GitHub Actions run `34835911183` completed successfully and pushed the verified checkpoint commit.
- evidence produced/verified:
  - `content-staging/reconstruction/technical/a7f1e94f-82d1-4146-af5b-4e9b51363f0b.json`;
  - `content-staging/reconstruction/educational/a7f1e94f-82d1-4146-af5b-4e9b51363f0b-discovery.json`;
  - `content-staging/reconstruction/educational/a7f1e94f-82d1-4146-af5b-4e9b51363f0b.json`;
  - exact reference: `master/تاسع إجتماعيات/جغرافيا_تاسع`;
  - workflow run `34835911183`: success; final checkpoint commit `8c93e3846375ec0188c938dcc3fd8e1f25c83e6e`;
  - next source manifest: 65 pages/images, 976 questions, 0 download failures, empty anomaly arrays.
- ambiguity/review_required:
  - Geography structural ambiguity requiring quarantine: 0;
  - Geography source questions: 0; semantic review `NOT APPLICABLE`;
  - الإيمان identity, structure, question semantics and page-to-lesson mapping remain `NOT VERIFIED` until its own evidence gates pass.
- invariant result: PASS (`2,374 + 967 + 351 + 22,063 = 25,755`)
- Sources processed: 15/58
- Educational: 6/26
- Books / Units / Lessons / Lesson Pages: 6 / 33 / 151 / 602
- Exam Source Groups: 9/32
- Individual Exam Models: 135
- Exam Pages: 455/2,286
- Verified Answer Keys: 0
- Source images technical: 1,174/5,273
- WebP generated / accepted / rejected: 0 / 0 / 0
- Legacy Questions: 25,755
- Lesson-linked: 2,374
- Exam-linked: 967
- Review-required: 351
- Unclassified: 22,063
- Duplicate groups classified: 0/99
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `a7f1e94f-82d1-4146-af5b-4e9b51363f0b — كتاب الجغرافيا`
- current source: `516f1c1d-acc0-4b1c-8e50-8f92a7c737e0 — الإيمان الكتاب المدرسي`
- exact next operation: `Fetch the live الإيمان manifest/pages and any explicit master candidate; technically verify all 65 images and source-local sequence/SHA/MIME; require exact/source evidence before accepting master equivalence; reconstruct book/unit/lesson/review boundaries only from proven evidence; structurally map all 976 questions only where their source-page membership proves a lesson or review location; use review_required/NOT VERIFIED for unresolved evidence; assert the 25,755 invariant; checkpoint.`
- next source: `NOT YET RESOLVED — derive only after الإيمان الكتاب المدرسي from live MASTER_CONTENT_MANIFEST`
- blockers: `none`
- handoff note: `Worker A must re-fetch live HEAD and baton, verify Geography checkpoint 8c93e384..., then start الإيمان from its own evidence. Do not inherit Geography/Civics title-run assumptions unless the Faith source proves the same structure.`

## RUN 2026-09-14T14:45:39+03:00 — Worker A

- state: COMPLETE_SOURCE_HANDOFF
- start HEAD: `90e6580845197880eb0c20ee137be3484cb18259`
- end HEAD before handoff-log commit: `556ffc76d0fb3d3fa632cbf0c1f678b986f8d4d7`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `516f1c1d-acc0-4b1c-8e50-8f92a7c737e0 — الإيمان الكتاب المدرسي`
- completed in this run:
  - re-fetched live branch and consumed Worker B's Geography handoff from the shared baton;
  - confirmed no duplicate/active Faith finalization workflow before starting;
  - technically verified all **65/65** immutable Faith RAW images (exist/readable/byte-size/SHA-256/MIME) without RAW mutation;
  - proved **65/65 exact SHA-256 identities** against `master/التربية الاسلاميه ثالث ثانوي/كتاب الإيمان/الصور`, with zero unmatched retained pages;
  - generated complete contact-sheet visual evidence for the retained pages 8..72;
  - used only exact-SHA master filename evidence to establish **10 lesson groups** and assign **65/65 retained pages** exactly once to a lesson; no Unit layer was invented (`NOT VERIFIED`);
  - structurally linked **976/976 legacy questions** to the evidence-backed lesson containing their immutable legacy page; question semantic correctness remains `NOT VERIFIED`;
  - updated the master manifest and evidence-backed status/handoff/validation/import-report documents; no production import/publication was created;
  - passed `FAITH_RECONSTRUCTION_VERIFY_PASS` and `FAITH_FINALIZATION_VERIFY_PASS`; both live-HEAD safety gates passed immediately before finalization/write.
- evidence/artifacts:
  - `content-staging/reconstruction/technical/516f1c1d-acc0-4b1c-8e50-8f92a7c737e0.json`;
  - `content-staging/reconstruction/educational/516f1c1d-acc0-4b1c-8e50-8f92a7c737e0-discovery.json`;
  - `content-staging/reconstruction/educational/516f1c1d-acc0-4b1c-8e50-8f92a7c737e0.json`;
  - discovery workflow run `34839217675` (success; contact-sheet artifact `faith-contact-sheets`);
  - finalization workflow run `34839580526` (success);
  - final evidence/status commit `556ffc76d0fb3d3fa632cbf0c1f678b986f8d4d7`.
- ambiguity/review_required:
  - Faith Unit hierarchy: `NOT VERIFIED`; no unit layer was asserted;
  - lesson membership is verified from exact page identity + explicit reference filename lesson labels;
  - page subtype/review-boundary semantics beyond lesson membership: `NOT VERIFIED`;
  - semantic correctness of all 976 question texts/answers: `NOT VERIFIED`;
  - no forced semantic claims were made.
- invariant result: PASS (`3,350 + 967 + 351 + 21,087 = 25,755`)
- Sources processed: 16/58
- Educational: 7/26
- Books / Units / Lessons / Lesson Pages: 7 / 33 / 161 / 667
- Exam Source Groups: 9/32
- Individual Exam Models: 135
- Exam Pages: 455/2,286
- Source images technical: 1,239/5,273
- Legacy Questions: 25,755
- Lesson-linked: 3,350
- Exam-linked: 967
- Review-required: 351
- Unclassified: 21,087
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `516f1c1d-acc0-4b1c-8e50-8f92a7c737e0 — الإيمان الكتاب المدرسي`
- current/next source: `f25891fe-ea52-481b-baf2-ff4764c79bde — الاسلاميه ثانوي نماذج وزاريه 1447`
- current source live baseline: `93 pages/images, 0 legacy questions, 0 download failures; manifest anomalies: duplicate_page_numbers=0, missing_images=0, multiple_images=0, malformed_ai_questions=0. Technical verification / source identity / reconstruction remain NOT VERIFIED unless live evidence says otherwise.`
- exact next operation: `Re-fetch live HEAD/baton; verify no active workflow for f25891fe-ea52-481b-baf2-ff4764c79bde; read its live manifest/pages; run full technical verification; establish identity/structure from its own source-specific evidence; then link questions only where evidence proves membership and reassert the 25,755 global invariant.`
- blockers: `none at handoff.`
- handoff note: `Worker B should start from f25891fe-ea52-481b-baf2-ff4764c79bde only after re-fetching live HEAD and this baton. Do not rerun/finalize Faith unless new drift evidence appears. Preserve Faith's unit hierarchy and semantic question review as NOT VERIFIED; do not upgrade those claims without new evidence.`

## RUN 2026-09-14T15:04:58+03:00 — Worker A

- state: COMPLETE_SOURCE_HANDOFF
- start HEAD: `405c424792ff31dd66311328213dd23d10dc673e`
- end HEAD before handoff-log commit: `f404c5749fc3f96c27ed163ebdec095723df6711`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `f25891fe-ea52-481b-baf2-ff4764c79bde — الاسلاميه ثانوي نماذج وزاريه 1447`
- completed in this run:
  - re-fetched live branch/baton and verified the preceding Geography/Faith state rather than redoing completed work;
  - confirmed no active/queued workflow for this source before starting;
  - technically verified **93/93** immutable RAW images (exist/readable/byte-size/SHA-256/MIME), sequence **1..93** contiguous;
  - generated and visually reviewed complete contact-sheet evidence for all **93** pages;
  - established **31** source-local three-page exam occurrences, each two question pages followed by one correction/result page, covering all 93 pages exactly once;
  - preserved **6 exact-SHA duplicate groups** as provenance occurrences and did not merge or mutate RAW;
  - finalized **31 Individual Exam Models / 93 Exam Pages**, **31 correction/result candidates**, **0 review-required pages**, and **0 verified standalone Answer Keys**; official model-code transcription remains `NOT VERIFIED`;
  - source has **0 legacy questions**, so no question records were fabricated or mapped;
  - updated master manifest plus evidence-backed status/handoff/validation/import-report documents; no production import/publication was created;
  - discovery run `34840720032` and finalization run `34841162130` succeeded; both live-HEAD safety gates and global invariants passed.
- evidence/artifacts:
  - `content-staging/reconstruction/technical/f25891fe-ea52-481b-baf2-ff4764c79bde.json`;
  - `content-staging/reconstruction/exams/source-groups/f25891fe-ea52-481b-baf2-ff4764c79bde-discovery.json`;
  - `content-staging/reconstruction/exams/source-groups/f25891fe-ea52-481b-baf2-ff4764c79bde.json`;
  - discovery workflow run `34840720032` (artifact `islamic-exam-1447-discovery-evidence`);
  - finalization workflow run `34841162130` (success);
  - final evidence/status commit `f404c5749fc3f96c27ed163ebdec095723df6711`.
- ambiguity/review_required:
  - standalone official Answer Keys: `NOT VERIFIED`;
  - official model codes/titles/term transcription: `NOT VERIFIED`;
  - exact-SHA duplicate question pages are preserved as distinct source occurrences inside visually complete exam blocks, not silently deduplicated;
  - source legacy-question semantics: `NOT APPLICABLE — 0 legacy questions`.
- invariant result: PASS (`3,350 + 967 + 351 + 21,087 = 25,755`)
- Sources processed: 17/58
- Educational: 7/26
- Books / Units / Lessons / Lesson Pages: 7 / 33 / 161 / 667
- Exam Source Groups: 10/32
- Individual Exam Models: 166
- Exam Pages: 548/2,286
- Source images technical: 1,332/5,273
- Legacy Questions: 25,755
- Lesson-linked: 3,350
- Exam-linked: 967
- Review-required: 351
- Unclassified: 21,087
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `f25891fe-ea52-481b-baf2-ff4764c79bde — الاسلاميه ثانوي نماذج وزاريه 1447`
- current/next source: `cae82d8f-64f9-4d2a-984f-6e6fd19fac5c — الحديث والتهذيب الكتاب `
- current source live baseline: `62 pages/images, 1483 legacy questions, 0 download failures; manifest anomalies: duplicate_page_numbers=0, missing_images=0, multiple_images=0, malformed_ai_questions=0. Technical verification / source identity / reconstruction remain NOT VERIFIED unless live evidence says otherwise.`
- exact next operation: `Re-fetch live HEAD/baton; verify no active workflow for cae82d8f-64f9-4d2a-984f-6e6fd19fac5c; technically verify all 62 images; prove source identity/lesson or unit boundaries from its own evidence; map 1,483 questions only where page membership is proven; preserve uncertainty as review_required/NOT VERIFIED; assert the global invariant; checkpoint.`
- blockers: `none at handoff.`
- handoff note: `Worker B should start only from cae82d8f-64f9-4d2a-984f-6e6fd19fac5c after re-fetching live HEAD and this baton. Do not rerun Islamic 1447 absent new drift evidence, and do not treat the six duplicate SHA groups as permission to delete or merge provenance.`
