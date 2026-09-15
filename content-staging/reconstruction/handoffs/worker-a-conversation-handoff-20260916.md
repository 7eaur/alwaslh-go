# Worker A — Conversation Handoff — 2026-09-16

## Repository / branch

- Repository: `7eaur/alwaslh-go`
- Branch: `content/corpus-inventory-20260914`
- Live HEAD verified immediately before this handoff write: `f4e253b9ddff299f95b9301f30de308c7b85e990`
- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Source-of-truth order remains: immutable RAW/provenance -> reconstruction/technical evidence -> visual evidence -> exact proven master references -> later schema/runtime import readiness.

## What was done in this conversation

1. Re-read the live branch and reconstruction evidence instead of relying on chat memory.
2. Confirmed the canonical checkpoint before Arabic Part 2 remained:
   - Sources processed: `37/58`
   - Educational: `17/26`
   - Books / Units / Lessons / Lesson Pages: `15 / 69 / 388 / 1,641`
   - Exam Source Groups: `20/32`
   - Individual Exam Models: `370`
   - Exam Pages: `1,274/2,286`
   - Source images technical: `3,190/5,273`
   - Legacy Questions: `25,755`
   - Lesson-linked: `13,135`
   - Exam-linked: `1,920`
   - Review-required: `1,229`
   - Unclassified: `9,471`
   - Verified standalone Answer Keys: `0`
   - RAW / unrelated / imports / publications mutations: `0 / 0 / 0 / 0`
3. Reviewed Arabic Book Part 2 (`7ddec20e-617e-4e55-bba8-2d371aaf16b6`) evidence:
   - 178/178 RAW images technically verified.
   - stored page sequence = `0` plus contiguous `1..177`; page 0 must remain page 0 for provenance.
   - 12 visually verified units: 13..24.
   - 60 visually verified semantic instructional lessons.
   - exact visual unit assessment starts established.
   - all 178 physical records can be accounted for exactly once.
4. Verified the 11 legacy questions all came from one immutable legacy record:
   - legacy page id: `d79b9858-a33a-413b-9740-06a40f2e1eba`
   - stored page number: `177`
   - legacy title: `تقويم الوحدة الرابعة والعشرين`
   - question count: `11`
5. Detected and then resolved the page-177 provenance conflict:
   - `pages.json` points the record to source image suffix `.../d79b9858-a33a-413b-9740-06a40f2e1eba/page_0178.jpg`.
   - immutable RAW chain is internally consistent; the preserved image is SHA-256 `6cc906d0d1983799ecb15152bb497d4e71f6497b74f6ec919d85fa190643d4b2`, 76,759 bytes, JPEG, Git blob `1179fe5892d5d9955b3a4bf0372babf4bfb8e8b2`.
   - visual evidence proves stored 173 begins Unit 24 assessment, 174 continues assessment, 175 is end-of-part, 176 publisher/contact, 177 back cover.
   - therefore there is no proven image swap; the stale/misattached element is the legacy title/question payload on the back-cover record.
   - the 11 questions were NOT reassigned to pages 173/174 because that would be a guess.
   - disposition: `review_required = 11`, `lesson_linked = 0`, `assessment_linked = 0`, semantic correctness remains `NOT VERIFIED`.
6. Arabic Part 2 structural reconstruction is now present at:
   - `content-staging/reconstruction/educational/7ddec20e-617e-4e55-bba8-2d371aaf16b6.json`
   - state: `EVIDENCE_RECONSTRUCTED_PENDING_MASTER_CHECKPOINT`
   - counts: 1 book, 12 units, 60 semantic lessons, 99 unique lesson physical pages, 48 unit cover/intro pages, 20 assessment pages, 8 front matter, 3 tail.
   - physical invariant: `8 + 48 + 99 + 20 + 3 = 178`.
   - shared lesson pages are preserved as semantic multi-membership without double-counting physical pages.
7. The conflict-resolution evidence is at:
   - `content-staging/reconstruction/educational/7ddec20e-617e-4e55-bba8-2d371aaf16b6-page177-conflict-resolution.json`
8. The source is reconstructed but the canonical MASTER/status checkpoint has not yet been proven updated from the live aggregate at the moment of this handoff.

## Expected canonical counters after Arabic Part 2 checkpoint (do not claim until live MASTER/status is verified and written)

If the live MASTER/status still reflects 37/58 and no concurrent source changed these counters, Arabic Part 2 should move the aggregate to:

- Sources processed: `38/58`
- Educational: `18/26`
- Books: `16`
- Units: `81`
- Lessons: `448`
- Lesson Pages: `1,740`
- Exam Source Groups: `20/32`
- Individual Exam Models: `370`
- Exam Pages: `1,274/2,286`
- Source images technical: `3,368/5,273`
- Legacy Questions: `25,755`
- Lesson-linked: `13,135`
- Exam-linked: `1,920`
- Review-required: `1,240`
- Unclassified: `9,460`
- question invariant: `13,135 + 1,920 + 1,240 + 9,460 = 25,755`
- RAW / unrelated / imports / publications mutations remain `0 / 0 / 0 / 0`.

## Exact next reconstruction operation

1. Fetch live HEAD first.
2. Read the live operational baton and live `manifests/MASTER_CONTENT_MANIFEST.json` plus status/handoff files.
3. Check whether another worker has already applied the Arabic Part 2 checkpoint.
4. If not, validate the Arabic Part 2 reconstruction against the live aggregate and checkpoint it with the counts above only if all invariants still pass.
5. Resolve the next source from the live MASTER; do not guess it from memory.
6. Continue source-by-source automatically under the same RAW/provenance/fail-closed rules.

## Database/import request from owner — IMPORTANT

The owner separately authorized a later operation against the NEW Alwaslh PostgreSQL database for the published project:

- remove OLD CONTENT data only;
- do not delete users/accounts/auth/system settings;
- import only the newly reconstructed/verified ready content;
- target is the new PostgreSQL database used by the current Alwaslh project on Railway, NOT the old Supabase database.

Conversation-level investigation established that the modern project has curriculum/question-bank/quiz-oriented tables and that an older importer path exists, but a fully verified reconstruction-to-modern-schema import batch was NOT completed in this conversation.

**No production database delete or new reconstruction import was executed in this conversation.**

Before any database mutation in the next conversation:

1. Re-verify the exact Railway project/environment/PostgreSQL service and current schema from live tools/repository.
2. Inventory content tables and FK dependencies; distinguish content from users/auth/system data.
3. Build/verify a dry-run importer from CLOSED reconstruction sources only.
4. Explicitly exclude `review_required`, unresolved, and unclassified questions from the clean import unless the import design intentionally stores them as non-published review records.
5. Perform counts/provenance/idempotency/rollback checks.
6. Only then execute content-only cleanup + transactional import + post-import verification.

## Import cleanliness boundary currently known

Prior to Arabic Part 2 canonical checkpoint, the clean structural question relations were:

- lesson-linked: `13,135`
- exam-linked: `1,920`

Arabic Part 2 adds NO clean lesson/exam-linked questions; its 11 questions move from unclassified to `review_required` after checkpoint. Therefore the clean structurally linked question total remains `15,055` after this source.

Do not import the 11 Arabic Part 2 page-177 questions as lesson/assessment questions until separately resolved.

## Safety / unresolved notes

- Verified standalone Answer Keys remain 0 unless newer live evidence proves otherwise.
- Exam-linked means structurally linked by source page/model evidence; it does not universally mean every question text was freshly OCR/extracted and visually compared character-for-character to the exam image.
- Do not invent model codes, lesson membership, answer keys, or reassignment of stale legacy questions.
- RAW is immutable.
- No production import/publication should be inferred from reconstruction completion.

## Side effect created accidentally during documentation

An unintended branch `tmp-do-not-create` was created at `f4e253b9ddff299f95b9301f30de308c7b85e990` while attempting to refresh branch state. No files/commits were added to that branch. If a branch-delete capability is available, delete it; do not use it for work.

## Handoff summary

Start from live repository truth, not this document alone. The most important current fact is: Arabic Part 2 page-177 conflict is resolved by proving the image is the back cover and quarantining the 11 stale/misattached legacy questions as `review_required`; structural reconstruction is complete and the immediate task is live MASTER/status checkpointing, then resolve the next source and continue reconstruction. Database cleanup/import remains authorized by the owner but has NOT been executed and must use a separately verified guarded import path against the modern PostgreSQL database.