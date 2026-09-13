# الوسيلة الذكية — Content Rebuild Handoff

> نقطة الاستئناف الرسمية. اقرأ live heads ثم `CONTENT_REBUILD_EXECUTION_STATUS.md` أولًا؛ هو المرجع التنفيذي الأدق إذا اختلفا.

## العقود الثابتة

- Working repository: `7eaur/alwaslh-go`
- Working branch: `content/legacy-staging-rebuild`
- Flow: `Legacy Supabase -> Immutable RAW -> Reviewed CURATED -> Media Decision -> Dry Run -> Controlled Transaction -> Modern PostgreSQL -> Verification -> Publication`
- RAW immutable؛ لا overwrite/recompress in-place.
- لا page-title -> Lesson تلقائيًا.
- provenance وSHA-256 محفوظان.
- Media ready لا يعني Published.
- لا auto-publish لأي AI/legacy output.
- لا تستخدم `69 -> 62` كحقيقة منهجية.
- لا تحذف anomalies أو بيانات غير مرتبطة لتجميل الأرقام.
- أي DB apply يفشل مغلقًا عند identity/count/provenance/publication drift.

## Corpus truth retained

- Legacy snapshot SHA-256: `2dfde94f6b70c037bb15d2782d11f036441c4abe130295be772c59b5e0131d0c`
- Full RAW extraction: 58 subjects; 5,273 pages/images; 25,755 questions; 0 download failures; 2 empty subjects preserved; 6 corpus-wide duplicate-position anomalies preserved.
- Grade 9 English: 69 RAW pages/images; 104 questions; 8 recovered sections; manifest-only page 70 remains evidence-only; old 62 Draft lessons are reconciliation state, not curriculum truth.

## Completed checkpoints

- `BATCH-001 = DONE / COMMITTED_STATE_VERIFIED`
- `STRUCTURE-001 = DONE / SECTION_BOUNDARY_VERIFIED`
- `STRUCTURE-002 = DONE / SECTION_BOUNDARY_VERIFIED`
- `CURATION-001 = DONE / LESSON_BOUNDARY_VERIFIED`
- `CURATION-002 = DONE / LESSON_BOUNDARY_VERIFIED`
- `CONTENT-GAPS-001 = DONE / GAP_INVENTORY_VERIFIED`
- `MEDIA-001 = DONE / MEDIA_PROFILE_VERIFIED_PARTIAL_ACCEPTANCE`
- `IMPORT-001 = DONE / COMMITTED_STATE_VERIFIED`
- `VERIFY-001 = DONE / DELIVERY_ISOLATION_AND_PROVENANCE_VERIFIED`
- `ROADMAP-RETURN = DONE / STUDENT-016I_HANDOFF_VERIFIED`

Do not repeat completed tasks unless fresh drift invalidates their evidence.

## IMPORT-001 retained close evidence

Scope: CURATION-001 `Describing people and animals`, book pages `5..8` / source pages `9..12`.

- exact Section ID `434f9978-efae-471e-b37d-6b151edecc5b`;
- exact Lesson ID `1a6e3a6e-06e8-496e-8d18-c8d4545d1da9`;
- 4 exact reviewed Lesson Assets ordered 0..3;
- 4 exact ready Media Assets and exact source paths/checksums;
- Lesson unpublished; all 4 assets draft/unpublished;
- 0 unauthorized target Question links;
- exactly 12 legacy Question Revisions preserved unpublished on legacy Lessons.

Concurrent advancement had been handled fail-closed and no duplicate apply was attempted. The exact-state close marker was `IMPORT001_POST_APPLY_VERIFY_PASS` in deployment `3e1ce24a-39ca-498c-b219-8ceb895eda84`.

## VERIFY-001 close evidence

The verification batch remained limited to the same imported CURATION-001 slice and did not mutate business data.

Verifier:
- `content-staging/runtime/verify-001-unit2-describing.mjs`
- source commit `12fb1a5268e97f0a0d70eee4d33322c139e3deb5`
- Railway deployment `e5e8fef8-f8e7-467e-b3d8-60529c1a652a` — SUCCESS
- marker `VERIFY001_PASS`

Verified:
- exact Section identity count `1` and exact Lesson identity count `1`;
- Lesson content revision `1`;
- 4/4 exact Lesson Assets;
- 4/4 ready Media Assets;
- 4/4 exact source path + source/media checksum provenance;
- 4/4 assets remain draft/unpublished;
- Student Reader base-contract eligible lesson rows `0`;
- Student Reader publication-guard eligible asset rows `0`;
- unauthorized Question links to curated Lesson `0`;
- 12 preserved legacy Question Revisions remain unpublished;
- publication/RAW/media-binary/question mutation counts `0`;
- failures `0`.

This independently proves the imported slice is structurally/provenance-consistent while still isolated from Student delivery. It does not authorize publication.

The Railway content inspector was returned to idle after the verification run so later documentation commits do not replay the verifier.

## ROADMAP-RETURN close evidence

Live state observed on 2026-09-13:

- `7eaur/alwaslh main` began at `8d11cddb2cde510f233926d394434a384d480745`;
- `7eaur/alwaslh-go content/legacy-staging-rebuild` began at `61bb699b1dbb421f3ca031b8f8d3f53c48235678`;
- PR #55 is already merged: accepted head `8ceb4d5a5f70f7896f6cb358e05605479942d442`, merge commit `343ff1fd7b3d64d7e990b72606695365f520fa58`;
- current Student architecture still identifies `STUDENT-016I` as the first unfinished Stage16 item;
- concurrent Student execution already opened PR #57 on `stage16/student-016i`, exact head `4624dcc824555c1d29e9d697a7474bf76223468b`;
- PR #57 owns true cold-start offline Reader closure and must be continued from its live evidence rather than duplicated here;
- exact-head PR #57 CI is not fully green at this checkpoint: `Stage 8 · Student activation browser E2E` is failing;
- no Content Rebuild data, media binary, RAW, question, or publication mutation occurred during roadmap return.

## Exact resume action

The ordered Content Rebuild sequence requested for this workstream is complete through `ROADMAP-RETURN`.

Continue **Student workstream PR #57 / `STUDENT-016I`** from its current exact head and CI evidence. Do not start a second 016I implementation from the Content Rebuild branch.

Content publication remains closed. If Content Rebuild is explicitly resumed later, re-read both live heads plus this handoff/status before editing and preserve all completed checkpoints.

## Ordered queue

- `BATCH-001` — DONE
- `STRUCTURE-001` — DONE
- `STRUCTURE-002` — DONE
- `CURATION-001` — DONE
- `CURATION-002` — DONE
- `CONTENT-GAPS-001` — DONE
- `MEDIA-001` — DONE / MEDIA_PROFILE_VERIFIED_PARTIAL_ACCEPTANCE
- `IMPORT-001` — DONE / COMMITTED_STATE_VERIFIED
- `VERIFY-001` — DONE / DELIVERY_ISOLATION_AND_PROVENANCE_VERIFIED
- `ROADMAP-RETURN -> STUDENT-016I` — DONE / STUDENT-016I_HANDOFF_VERIFIED
