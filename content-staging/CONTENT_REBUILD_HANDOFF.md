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

Do not repeat those tasks unless fresh drift invalidates their evidence.

## IMPORT-001 — IN PROGRESS / CONTROLLED_APPLY_BUILDING

Scope remains only CURATION-001 `Describing people and animals`, book pages `5..8` / source pages `9..12`.

Verified evidence retained:
- identity inspector deployment `4cf8665b-4dd1-4e90-9ec8-92d897c34f59` — marker `IMPORT001_INSPECT_PASS`.
- rollback gate script commit `177b91572ac6fe3b37acd9bcc094876a1cbb3beb`.
- rollback deployment `8e4cdcbb-2783-4dca-b025-e1191fa9e330` — marker `IMPORT001_TRANSACTION_GATE_PASS`.
- validated mutation boundary: create exactly 1 Section + 1 Lesson; reassign exactly 4 existing Lesson Assets in reviewed order 0..3.
- create/mutate Media Assets: 0/0.
- mutate legacy Lessons: 0.
- mutate Questions: 0.
- publication changes: 0.
- unrelated rows: 0.
- preserved legacy Question Revisions: 12.

Current run added the controlled apply gate:
- file `content-staging/runtime/import-001-apply.mjs`
- commit `2af3b935512c853eb4c2b1f3767766f8513a1c0a`
- fail-closed guards mirror the verified rollback gate and re-check identities/checksums/publication immediately inside the transaction.
- Railway service `alwaslh-content-inspector` start command is now `node import-001-apply.mjs`.
- deployment `026bfc1b-8ba0-4ae8-a74b-7170086f45e1` is the only apply deployment for this checkpoint.
- latest observed state: `BUILDING`.
- no `IMPORT001_APPLY_PASS` marker observed yet; therefore no committed PostgreSQL mutation is claimed yet.

Important: do not trigger another apply while deployment `026bfc1b-8ba0-4ae8-a74b-7170086f45e1` remains non-terminal.

## Exact resume action

1. Read both live heads + execution status + this handoff.
2. Inspect Railway deployment `026bfc1b-8ba0-4ae8-a74b-7170086f45e1`.
3. On SUCCESS, inspect deploy logs and require `IMPORT001_APPLY_PASS` with exact counts: createSections=1, createLessons=1, reassignLessonAssets=4, forbidden mutation counters all zero, preservedQuestionRevisions=12.
4. On FAILED/CRASHED, inspect root cause; do not weaken identity/checksum/publication guards and do not issue a second write blindly.
5. After confirmed apply, create/run an independent read-only post-apply verifier against the committed state.
6. Only after verifier PASS, close `IMPORT-001`, update execution status/handoff, and update `PROJECT_STATUS.md` + `PROJECT_ENGINEERING_LOG.md` because PostgreSQL product truth will then have changed.
7. Do not start `VERIFY-001` before `IMPORT-001` committed state is independently verified.

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
