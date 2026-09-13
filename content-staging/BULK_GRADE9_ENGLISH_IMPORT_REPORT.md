# Grade 9 English — Full Bulk Import Report

Date: 2026-09-13

## Result

`BULK-GRADE9-ENGLISH-IMPORT = DONE / FULL_ASSET_COVERAGE_VERIFIED / UNPUBLISHED`

The full Grade 9 English Pupil's Book 3 reconstruction scope is now present in modern PostgreSQL as draft content and has passed read-only inspection, rollback-only transaction gating, controlled apply, and committed-state verification.

## Source authority used

- Legacy Grade 9 English subject: `1794eea5-4772-4c94-bd2b-b08e5815e733`.
- Immutable reconstruction manifest: `content-staging/curated/grade-9/english/pupil-book-3/reconstruction-candidates.json`.
- Legacy source evidence: `content/legacy-supabase-reconstruction` page chunks and immutable RAW extraction.
- `master` contains the separate Third Secondary/Pupil's Book 6 corpus and was **not** used as Grade 9 evidence.
- No `69 -> 62` arithmetic/heuristic was used to derive curriculum truth.

## Manifest scope

- RAW pages: `69`
- RAW images: `69`
- Question revisions: `104`
- Sections/units: `8`
- Source-manifest-only pages: `1` (`Blank Final Page`, book page 70) — preserved as evidence only because it has no RAW identity.

Recovered units:

1. `Unit 1 - Revision`
2. `Unit 2 - Describing: Making plans`
3. `Unit 3 - Other countries`
4. `Unit 4 - Visiting Japan`
5. `Unit 5 - Safety`
6. `Unit 6 - Helping others`
7. `Unit 7 - Communications`
8. `Unit 8 - Winning medals`

## Runtime execution

Source commit: `9e58ab3e882b883bddd016099949881801eedc28`

Railway deployment: `de7f9883-b2f0-483d-a7c1-ffbfb15ac30c`

Deployment status: `SUCCESS`

Runtime markers, in order:

- `BULK_G9_EN_INSPECT_PASS`
- `BULK_G9_EN_TRANSACTION_GATE_PASS`
- `BULK_G9_EN_APPLY_PASS`
- `BULK_G9_EN_VERIFY_PASS`
- `BULK_G9_EN_RUNNER_PASS`

## Verified committed state

- Pages verified: `69/69`
- RAW images verified by checksum: `69/69`
- Content source identities: `69/69`
- Ready Media Assets: `69/69`
- Lesson Assets: `69/69`
- Sections verified: `8/8`
- Involved Lesson identities: `59`
- New Sections created by this bulk apply: `6`
- Existing Sections reused: `2`
- Lessons assigned to their recovered Section: `54`
- Lesson assignments already correct/reused: `5`
- Question revisions preserved: `104/104`
- Manifest-only page 70 preserved as evidence-only: `1`

The `59` Lesson identities are **not** derived from the prohibited `69 -> 62` heuristic. They are the live Lesson identities that own the 69 verified Lesson Assets after previously reviewed curation/reassignment. All 69 page/image identities remain represented exactly once.

## Mutation boundary

- RAW mutations: `0`
- Media binary mutations: `0`
- Question mutations: `0`
- Publication changes: `0`
- Unrelated mutations: `0`

The controlled mutation was limited to missing Section creation and assigning existing unpublished Lesson rows to their verified recovered Section.

## Publication state

- Published Lessons in this scope: `0`
- Published Lesson Assets: `0`
- Published Questions: `0`

This checkpoint **does not authorize publication**. Publication remains a separate review/product gate.

## Interpretation

The full Grade 9 English source corpus is now technically imported and structurally reachable in modern PostgreSQL: all 69 RAW-backed pages/images are present, linked through Media/Lesson Assets, assigned under the eight recovered units, and checksum/provenance verified.

This closes the data-completeness/import problem for the book. A later pedagogical curation pass may still choose to merge or rename Lesson identities for a cleaner learning experience, but that is a semantic refinement of already-imported content, not missing-page/media import work. It must not delete provenance, fabricate page 70, mutate RAW, or auto-publish legacy/AI content.
