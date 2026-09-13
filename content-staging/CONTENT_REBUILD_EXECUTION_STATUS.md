# Alwaslh Content Rebuild — Shared Execution Status

> اقرأ هذه النسخة + live heads قبل أي عمل، ثم أكمل أول مهمة غير مكتملة فقط. لا تعتمد على ذاكرة المحادثة.

## Fixed execution contract

`Legacy Supabase -> Immutable RAW -> Reviewed CURATED -> Media Decision -> Dry Run -> Controlled Transaction -> Modern PostgreSQL -> Verification -> Publication`

- لا تستخدم heuristic القديم `69 -> 62` كحقيقة منهجية.
- RAW immutable.
- لا auto-publish لأي AI/legacy content غير مراجع.
- لا حذف anomalies أو تعديل بيانات غير مرتبطة لتجميل الأرقام.
- أي apply يفشل مغلقًا عند identity/count/provenance/publication drift.
- WebP لا يُقبل إلا بعد إثبات فائدة الحجم والوضوح.

## Live heads observed in the closing IMPORT-001 run — 2026-09-13

- `7eaur/alwaslh main`: `0c7c9f9c5e4ec6ae020484a9a4892eaf3b8b5194`
- `7eaur/alwaslh-go content/legacy-staging-rebuild`: initial `4e55a6993c2139fe303ceab463ee07d179020c15`; re-read before close at `2f3d0fa9923f9dceb692477c2fd1a0fd89d2b0c8`.

## Completed checkpoints

- `BATCH-001` — DONE / COMMITTED_STATE_VERIFIED
- `STRUCTURE-001` — DONE / SECTION_BOUNDARY_VERIFIED
- `STRUCTURE-002` — DONE / SECTION_BOUNDARY_VERIFIED
- `CURATION-001` — DONE / LESSON_BOUNDARY_VERIFIED
- `CURATION-002` — DONE / LESSON_BOUNDARY_VERIFIED
- `CONTENT-GAPS-001` — DONE / GAP_INVENTORY_VERIFIED
- `MEDIA-001` — DONE / MEDIA_PROFILE_VERIFIED_PARTIAL_ACCEPTANCE

Do not repeat them unless fresh evidence-invalidating drift is demonstrated.

## IMPORT-001 — DONE / COMMITTED_STATE_VERIFIED

Scope closed only for CURATION-001:
- target Section `Unit 2 - Describing: Making plans`
- target Lesson `Describing people and animals`
- book pages `5..8` / source pages `9..12`
- 4 existing reviewed Lesson Assets / 4 existing ready Media Assets
- 12 legacy Question Revisions preserved on their legacy Lessons
- publication remains closed.

Pre-apply evidence retained:
- identity inspector deployment `4cf8665b-4dd1-4e90-9ec8-92d897c34f59`; marker `IMPORT001_INSPECT_PASS`.
- rollback gate commit `177b91572ac6fe3b37acd9bcc094876a1cbb3beb`.
- rollback deployment `8e4cdcbb-2783-4dca-b025-e1191fa9e330`; marker `IMPORT001_TRANSACTION_GATE_PASS`.
- intended mutation boundary was exactly `1 Section + 1 Lesson + 4 Lesson Asset reassignments`; Media/Question/publication/unrelated mutation counts = `0`.

Current-run apply handling:
- fail-closed apply script commit `2af3b935512c853eb4c2b1f3767766f8513a1c0a`.
- deployment `026bfc1b-8ba0-4ae8-a74b-7170086f45e1` built with the prior rollback command and therefore did not perform the controlled apply.
- later apply deployment `efb92e21-e8df-4674-92d9-041321da9f92` failed closed before mutation with `IMPORT001_APPLY_FAIL: target section already exists count=1`.
- therefore this run does **not** claim that its apply executor committed the target rows. The database had advanced concurrently to the target shape; duplicate write was intentionally not attempted.

Independent committed-state verification:
- verifier file `content-staging/runtime/import-001-post-apply-verify.mjs`.
- initial verifier commit `3727dde8f6f037d34691a75feae3d46d164f1041`; deployment `4144bf3c-1eeb-4c9f-8a77-65e60b1ed1c8`; marker `IMPORT001_POST_APPLY_VERIFY_PASS`.
- tightened exact-identity verifier commit `2f3d0fa9923f9dceb692477c2fd1a0fd89d2b0c8`; deployment `3e1ce24a-39ca-498c-b219-8ceb895eda84`; marker `IMPORT001_POST_APPLY_VERIFY_PASS`.

Verified committed state from tightened verifier:
- target Section count: `1`; ID `434f9978-efae-471e-b37d-6b151edecc5b`.
- target Lesson count: `1`; ID `1a6e3a6e-06e8-496e-8d18-c8d4545d1da9`.
- target Lesson Assets: `4`, exact previously reviewed asset IDs, ordered `0..3`.
- ready Media Assets: `4`, exact previously reviewed media IDs.
- source paths + source/media checksums + presence: exact match for all 4 pages.
- target Lesson published: `false`.
- target Lesson Assets draft/unpublished: `4/4`.
- unauthorized Question links to target Lesson: `0`.
- preserved legacy Lessons: `4`, still active/unpublished/sectionless and now holding `0` reviewed page assets.
- preserved legacy Question Revisions: exactly `12`, still unpublished and still linked to the legacy Lessons.
- RAW mutation by this close step: `0`.
- Media binary mutation by this close step: `0`.
- Question mutation by this close step: `0`.
- publication mutation by this close step: `0`.
- no unrelated repair/delete was performed.

Railway inspector was returned to an idle start command after verification so documentation commits do not replay the verifier or apply gate.

## Exact next action

`VERIFY-001` only. Start by reading both live heads again, then define the smallest independent verification batch for the just-imported Unit 2 lesson. Do not reopen IMPORT-001 unless new drift invalidates the exact committed-state evidence above. Do not publish content automatically.

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
