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
- latest verified work HEAD before this handoff commit: `1030dcbcbe56d39da24fd6277186f966b4e2fd33`
- last completed source: `004c02be-3f55-49e1-bbdc-b0824491bd68 — العلوم نماذج وزارية 1446`
- current source: `14ef15e0-5524-473a-bbdb-996df35ba535 — العلوم نماذج وزارية 1447`
- current operation: `read manifest/pages -> technical verification from 1447 source evidence -> source-local duplicate/boundary discovery -> full visual evidence -> resolve only evidence-supported models/correction relations -> map source questions -> invariant/checkpoint`
- next source: `NOT YET RESOLVED — determine from live MASTER_CONTENT_MANIFEST only after Science 1447 is processed`
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
