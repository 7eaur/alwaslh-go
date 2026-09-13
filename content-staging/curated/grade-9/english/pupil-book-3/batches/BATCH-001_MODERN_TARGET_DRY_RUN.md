# BATCH-001 — Modern Target Dry Run

Batch: `BATCH-001-G9-EN-PB3-U1`

Mode: **dry-run only / zero PostgreSQL writes**

Application schema checkpoint: `7eaur/alwaslh@343ff1fd7b3d64d7e990b72606695365f520fa58`

Content checkpoint before this dry-run: `7eaur/alwaslh-go@3c6f8f2f5d549a1ee0b6f41f50a9abf1dc9b9c11`

## Inputs

- bounded batch contract: `batch-001-unit-1-revision.json`
- semantic review: `batch-001-question-review.json`
- DB/media inventory: `BATCH-001_DB_MEDIA_VALIDATION.md`
- modern schema authorities:
  - `database/migrations/0016_curriculum_structure.sql`
  - `database/migrations/0017_content_ingestion_publication.sql`
  - `database/migrations/0019_question_bank.sql`
  - `database/migrations/0026_legacy_supabase_import_support.sql`

## Verified pre-state

For active `grade-9 / english` production scope:

- curriculum section matching this curated unit: `0`
- semantic lesson rows already present for pages 1–4: `4`, all unpublished
- lesson assets already present for those lessons: `4`, all draft
- ready media assets already linked to the four source pages: `4`
- reviewed question revisions represented by existing draft rows: `13`
- question source links for the four source pages: present for all `13`
- published lessons/questions/assets in this batch: `0`

The previous 62-row legacy import is evidence/state to reconcile, not a source of final curriculum boundaries. No global `69 -> 62` heuristic is used by this dry-run.

## Duplicate-safe target

Create exactly one curriculum section if the canonical section slug is absent:

- slug: `curated-english9-pb3-unit-1-revision`
- title: `Unit 1 - Revision`
- position: `1`

Reuse the four existing unpublished semantic lesson rows identified through the exact legacy page/source provenance. Do **not** insert four duplicate lessons.

Target lesson identities:

1. book page 1 — `2d98475c-91bf-4000-bfbc-79f7a6a854f9` — `curated-english9-pb3-u1-p001-presents-from-london`
2. book page 2 — `5e207993-508f-426b-ae71-f00aa4f782df` — `curated-english9-pb3-u1-p002-whats-my-job`
3. book page 3 — `dc1d6249-c0cb-4982-9711-092b1dcffee3` — `curated-english9-pb3-u1-p003-the-holidays`
4. book page 4 — `f2947d7f-5697-4bdc-b561-ad880a1afdf1` — `curated-english9-pb3-u1-p004-a-postcard-from-london`

For each reused lesson the controlled apply may update only curated structural fields required by the target contract: `section_id`, curated `slug`, canonical `title` if different, and section-local `position`. Publication remains closed (`published_at = NULL`).

Reuse all four existing `lesson_assets` and all four Ready `media_assets`. The asset rows remain `draft`. No media/source asset is duplicated or replaced, and immutable RAW bytes/checksums remain unchanged.

For Question Bank, reuse the existing 13 draft revisions linked to these four page sources. The semantic review is authoritative for the batch:

- unchanged/no-op content: `6`
- source-grounded content corrections: `7`
- rejected: `0`

The seven corrections may update only the existing open draft revision content fields (`prompt`, `options`, answer fields, and explanation/method only when supplied by the reviewed artifact). Existing item identity, lesson links, source links, source checksums and provenance remain preserved. No new Question Bank items or parallel revisions are created by this batch dry-run.

The database review/publication lifecycle is not bypassed. This dry-run does not manufacture reviewer/publisher actors. Question rows stay non-published until an authorized controlled apply/review step supplies valid lifecycle actors/timestamps.

## Exact dry-run effect counts

### Inserts

- curriculum sections: **1 max** (`1` under the verified pre-state of zero matching sections)
- lessons: **0**
- lesson assets: **0**
- media assets: **0**
- media variants: **0**
- question bank items: **0**
- question bank revisions: **0**
- revision lesson links: **0**
- revision source links: **0**
- quiz rows: **0**

### Updates

- reused lessons requiring curated structural reconciliation: **4**
- lesson assets: **0**
- media/source rows: **0**
- existing question draft revisions with semantic correction: **7**
- existing question revisions with no content change: **6**

Expected direct content/structure row mutations under the verified pre-state: **12 rows total** = 1 section insert + 4 lesson updates + 7 question-revision updates.

This count intentionally excludes audit/event rows that a future controlled apply may be required to append by the application service contract. Those must be enumerated by the apply implementation before mutation; they are not silently omitted from rollback planning.

### Explicitly unchanged

- remaining legacy-import lesson rows outside the four page identities: **untouched**
- remaining question rows outside the reviewed 13: **untouched**
- all 4 lesson assets: **unchanged / draft**
- all 4 ready media assets: **unchanged**
- RAW/source assets/checksums: **unchanged**
- publication state: **unchanged / closed**

No row is archived/deactivated/deleted merely to make the old 62 count disappear.

## Idempotency keys / matching rules

The controlled apply must resolve before mutation by:

1. exact active `class_slug=grade-9` + `subject_slug=english` offering;
2. section unique key `(class_id, subject_id, slug)`;
3. lesson identity by the verified legacy page/source provenance, then enforce the curated slug;
4. media identity by exact `content_source_asset` path/checksum linkage;
5. question identity by existing revision source linkage for the exact source page plus the reviewed question locator/order.

If any identity resolves to zero or multiple candidate rows, the apply must abort rather than insert a replacement opportunistically.

## Rollback scope

Because the four lessons and thirteen question items pre-exist, rollback must restore values rather than delete those identities.

Rollback for a future apply is bounded to:

- delete the newly inserted section **only after** restoring the four lesson `section_id` values;
- restore the pre-apply values of the four reused lesson structural fields;
- restore the pre-apply content of the seven corrected draft question revisions;
- leave the six no-op revisions untouched;
- preserve all lesson assets, media assets, media variants, content source assets and RAW evidence.

Expected reversible business-row set: **12 rows** under the verified pre-state. Any audit/event rows generated by the future apply are append-only evidence and must be accounted for separately rather than deleted to hide history.

## Media decision

Current display WebP files are larger than immutable JPEG sources (`549,794` vs `440,502` bytes, +24.81%). Therefore this dry-run performs **0 media transformations**. Existing derived variants are retained as evidence but are not claimed as optimization success. A later media profile is allowed only after measurable byte reduction and readability validation.

## Gate result

`MODERN_TARGET_DRY_RUN_PASS / APPLY_NOT_AUTHORIZED_YET`

The dry-run closes the duplicate-safe target-shape decision. Before PostgreSQL mutation, the next checkpoint must turn this plan into an executable controlled apply/rollback transaction and re-resolve all identities against the live database immediately before mutation. Any drift from the counts/identities above is a hard stop, not a reason to create duplicates.
