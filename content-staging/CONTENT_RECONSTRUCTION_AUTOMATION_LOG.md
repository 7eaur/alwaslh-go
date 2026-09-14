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

Current source:

- Source ID: `ef408805-c337-44dd-b903-7838030e6de0`
- Name: `العلوم نماذج وزارية 1445`
- Class/subject: `تاسع العلوم`
- Manifest evidence: 30 pages/images; 215 legacy questions; no listed manifest anomalies for duplicate page numbers/missing/malformed entries.
- Technical verification: `NOT VERIFIED`
- Individual Exam Models: `NOT VERIFIED`
- Answer Keys: `NOT VERIFIED`

Exact next operation:

1. Re-fetch live branch HEAD and this file.
2. Read the source manifest and existing generic verification/discovery tools.
3. Create/use a source-local workflow for Science 1445 based only on this source's evidence.
4. Technically verify all 30 page images: existence, readability, byte size, SHA-256, MIME, sequence, duplicate SHA groups.
5. Generate visual evidence/contact sheets covering all 30 pages.
6. Inspect every page needed to establish model boundaries, repeated occurrences, mismatch blocks, correction/answer-key candidates.
7. Finalize only evidence-supported Individual Exam Models; isolate ambiguity as `review_required` with reasons.
8. Map all 215 source questions structurally to finalized models/review-required/unassigned as evidence allows.
9. Assert the global question invariant before checkpointing.
10. Update reconstruction JSON/manifests/status docs and this shared handoff; then move to the next source automatically.

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
- baseline HEAD before this plan: `df62ba1f424b23346af5c49eaee1063022298ca0`
- last completed source: `e7c8291c-e904-4e8c-9cd8-2753818cedf3 — الكيمياء نماذج وزاريه 1447`
- current source: `ef408805-c337-44dd-b903-7838030e6de0 — العلوم نماذج وزارية 1445`
- current operation: `technical verification + source-local exam boundary discovery`
- next source: `NOT YET RESOLVED from live ordered manifest after Science 1445 finalization`
- blockers: `none known; Science 1445 technical/boundary evidence is NOT VERIFIED yet`
- owner decision required now: `no`

---

### Shared handoff rule

Worker A and Worker B must treat this file as the operational baton. Read latest -> verify live state -> execute one safe coherent unit -> append RUN -> update ACTIVE CHECKPOINT to the newest truth -> hand off. Never skip evidence, never overwrite the other worker's unreviewed work, and never trade correctness for apparent progress.
