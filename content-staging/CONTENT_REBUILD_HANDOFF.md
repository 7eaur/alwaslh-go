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

Do not repeat completed tasks unless fresh drift invalidates their evidence.

## IMPORT-001 close evidence

Scope: CURATION-001 `Describing people and animals`, book pages `5..8` / source pages `9..12`.

Pre-apply:
- identity inspector `4cf8665b-4dd1-4e90-9ec8-92d897c34f59` — `IMPORT001_INSPECT_PASS`.
- rollback gate commit `177b91572ac6fe3b37acd9bcc094876a1cbb3beb`.
- rollback deployment `8e4cdcbb-2783-4dca-b025-e1191fa9e330` — `IMPORT001_TRANSACTION_GATE_PASS`.
- allowed boundary: create 1 Section + 1 Lesson, reassign 4 existing Lesson Assets; zero Media/Question/publication/unrelated mutations.

Concurrent advancement was handled fail-closed:
- apply script commit `2af3b935512c853eb4c2b1f3767766f8513a1c0a`.
- deployment `026bfc1b-8ba0-4ae8-a74b-7170086f45e1` still used the old rollback command, so it did not apply.
- later apply deployment `efb92e21-e8df-4674-92d9-041321da9f92` aborted before mutation because the target Section already existed.
- do not claim that this run's apply executor created the rows; PostgreSQL advanced concurrently and the duplicate apply was refused.

Independent verification then established the committed target state:
- initial verifier commit `3727dde8f6f037d34691a75feae3d46d164f1041`, deployment `4144bf3c-1eeb-4c9f-8a77-65e60b1ed1c8`, PASS.
- exact-identity verifier commit `2f3d0fa9923f9dceb692477c2fd1a0fd89d2b0c8`, deployment `3e1ce24a-39ca-498c-b219-8ceb895eda84`, marker `IMPORT001_POST_APPLY_VERIFY_PASS`.

Verified exact state:
- Section ID `434f9978-efae-471e-b37d-6b151edecc5b`, one exact target Section.
- Lesson ID `1a6e3a6e-06e8-496e-8d18-c8d4545d1da9`, one exact target Lesson under that Section.
- 4 exact reviewed Lesson Assets ordered 0..3.
- 4 exact ready Media Assets and exact source paths/checksums.
- Lesson unpublished; all 4 assets draft/unpublished.
- 0 unauthorized target Question links.
- 4 legacy source Lessons preserved active/unpublished/sectionless with 0 reviewed page assets remaining on them.
- exactly 12 legacy Question Revisions preserved and unpublished on the legacy Lessons.
- no RAW/media-binary/question/publication/unrelated repair was made by the close step.

Railway inspector start command was returned to idle after verification.

## Exact resume action

Start `VERIFY-001` only:
1. read live heads for `7eaur/alwaslh` and `7eaur/alwaslh-go`;
2. read execution status + this handoff + project status/log as needed;
3. verify the smallest independent end-to-end slice for the just-imported Unit 2 lesson against modern PostgreSQL contracts and provenance/publication invariants;
4. do not publish automatically;
5. update status after the batch and project docs only if product/runtime truth changes;
6. only after `VERIFY-001` reaches its documented gate, proceed to `ROADMAP-RETURN -> STUDENT-016I`.

## Ordered queue

- `BATCH-001` — DONE
- `STRUCTURE-001` — DONE
- `STRUCTURE-002` — DONE
- `CURATION-001` — DONE
- `CURATION-002` — DONE
- `CONTENT-GAPS-001` — DONE
- `MEDIA-001` — DONE
- `IMPORT-001` — DONE / COMMITTED_STATE_VERIFIED
- `VERIFY-001` — TODO
- `ROADMAP-RETURN -> STUDENT-016I` — TODO
