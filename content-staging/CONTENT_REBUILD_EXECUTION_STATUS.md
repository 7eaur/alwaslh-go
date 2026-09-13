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

## Live heads observed at start of current run — 2026-09-13

- `7eaur/alwaslh main`: `0c7c9f9c5e4ec6ae020484a9a4892eaf3b8b5194`
- `7eaur/alwaslh-go content/legacy-staging-rebuild`: `4e55a6993c2139fe303ceab463ee07d179020c15`

No evidence-invalidating drift was present before continuing `IMPORT-001`.

## Completed checkpoints

- `BATCH-001` — DONE / COMMITTED_STATE_VERIFIED
  - 1 Unit 1 Section, 4 reused Lessons, 4 draft Lesson Assets, 4 ready Media Assets.
  - Question Revisions 13 = 7 corrected + 6 unchanged; provenance 13/13; publication 0.
  - final verifier deployment `c3e609b3-f632-46e9-9fde-680330512eee`; marker `BATCH001_POST_APPLY_VERIFY_PASS`.
- `STRUCTURE-001` — DONE / SECTION_BOUNDARY_VERIFIED
  - Unit 2 book pages 5..15 / source 9..19; 11 pages; 30 questions.
  - evidence commit `4ff71ca280c432392c8d91737374c77232b3fe69`.
- `STRUCTURE-002` — DONE / SECTION_BOUNDARY_VERIFIED
  - Unit 3 book pages 16..25 / source 20..29; 10 pages; 3 questions.
  - evidence commit `9e92a4b4d7658f6ea43f1f0727ffb19e922c66cb`.
- `CURATION-001` — DONE / LESSON_BOUNDARY_VERIFIED
  - `Describing people and animals`; book 5..8 / source 9..12; 4 ordered activities; 12 legacy questions preserved.
  - evidence commit `67f630f42913528405246fad7c541b091a47959e`.
- `CURATION-002` — DONE / LESSON_BOUNDARY_VERIFIED
  - `Telling time and arranging a meeting`; book 9..10 / source 13..14; 2 activities; 7 questions preserved.
  - evidence commit `d14774adc68470e9eea48a1c388a14a66111bf57`.
- `CONTENT-GAPS-001` — DONE / GAP_INVENTORY_VERIFIED
  - 69 RAW pages/images, 104 questions, 8 sections; reviewed boundary coverage 10 pages; unresolved 59.
  - page 70 remains manifest-only evidence; corpus duplicate-position anomalies 6 preserved.
  - inventory commit `dd86641decbcb3e3345d1aacfea7e2363fc60474`.
- `MEDIA-001` — DONE / MEDIA_PROFILE_VERIFIED_PARTIAL_ACCEPTANCE
  - run `34761171601` SUCCESS; page 5 q76 WebP accepted only as reproducible derived candidate: 20.66% smaller, PSNR 39.52 dB, same dimensions.
  - pages 6..8 rejected; RAW unchanged; no production media mutation.
  - decision commit `bb3dbbeff5d866930c1921124a8868b79af5703e`.

## IMPORT-001 — IN PROGRESS / CONTROLLED_APPLY_BUILDING

Scope remains only CURATION-001:
- target Lesson `Describing people and animals`
- book pages 5..8 / source pages 9..12
- no unresolved page, question rewrite, publication, RAW or media-binary mutation authorized.

Already verified before this run:
- live identity inspector deployment `4cf8665b-4dd1-4e90-9ec8-92d897c34f59`, marker `IMPORT001_INSPECT_PASS`.
- rollback-only gate commit `177b91572ac6fe3b37acd9bcc094876a1cbb3beb`.
- rollback deployment `8e4cdcbb-2783-4dca-b025-e1191fa9e330`, marker `IMPORT001_TRANSACTION_GATE_PASS`.
- intended mutation exactly: create `1 Section + 1 Lesson`, reassign `4 Lesson Assets`; all Media/Question/publication/unrelated mutation counts = 0.
- 12 legacy Question Revisions remain preserved.

Current run progress:
- created fail-closed controlled apply script `content-staging/runtime/import-001-apply.mjs`.
- apply script commit: `2af3b935512c853eb4c2b1f3767766f8513a1c0a`.
- guards retained: exact grade-9/english scope; target Section/Lesson absence; exact 4 source paths/checksums/presence; ready Media; draft/unpublished Lesson Assets; active/unpublished/sectionless legacy Lessons; unique source/media/asset/lesson identities; exact 12 preserved legacy Question Revisions; zero publication change.
- Railway service start command changed to `node import-001-apply.mjs`.
- auto deployment: `026bfc1b-8ba0-4ae8-a74b-7170086f45e1`.
- latest observed deployment state: `BUILDING`.
- no `IMPORT001_APPLY_PASS` marker has been observed yet.
- committed PostgreSQL business writes attributable to this run at this checkpoint: not claimed / unverified until deployment exits and logs are checked.

Transient blocker:
- Railway builder is still scheduling/building deployment `026bfc1b-8ba0-4ae8-a74b-7170086f45e1`; deploy logs are not available yet. Do not trigger another apply deployment while this one is active.

Exact next action:
1. read both live heads again;
2. inspect deployment `026bfc1b-8ba0-4ae8-a74b-7170086f45e1` until it reaches a terminal state;
3. if SUCCESS, require marker `IMPORT001_APPLY_PASS` and exact mutation counts `1/1/4` with all forbidden mutation counts zero;
4. if FAILED/CRASHED, inspect root cause and do not bypass guards;
5. after a confirmed apply, create/run an independent read-only post-apply verifier before closing `IMPORT-001`;
6. update this file with exact deployment/commit IDs and committed counts;
7. update handoff plus `PROJECT_STATUS.md` and `PROJECT_ENGINEERING_LOG.md` only if PostgreSQL product truth actually changes;
8. do not start `VERIFY-001` before `IMPORT-001` committed state is independently verified.

## Ordered queue

- `BATCH-001` — DONE
- `STRUCTURE-001` — DONE
- `STRUCTURE-002` — DONE
- `CURATION-001` — DONE
- `CURATION-002` — DONE
- `CONTENT-GAPS-001` — DONE
- `MEDIA-001` — DONE
- `IMPORT-001` — IN PROGRESS / CONTROLLED_APPLY_BUILDING
- `VERIFY-001` — TODO
- `ROADMAP-RETURN -> STUDENT-016I` — TODO
