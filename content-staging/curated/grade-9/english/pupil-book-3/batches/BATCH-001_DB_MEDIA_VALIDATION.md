# BATCH-001 — DB / Media / Provenance Validation

Batch: `BATCH-001-G9-EN-PB3-U1`

Validation date: 2026-09-13

Source branch checkpoint inspected: `a4ec103a0bb36a40f144a65ee6635a70f15f059a`

Railway inspector deployment: `00e69a2d-05f4-4e22-9449-5d82f80c8849`

Mode: **read-only**. No PostgreSQL writes or publication changes were performed by this validation.

## Scope verified

Target curriculum scope resolves to active `grade-9` + active `english` + active subject/class offering.

The smallest coherent first batch is Unit 1 — Revision, book pages 1–4:

| # | Lesson candidate | RAW bytes | Display WebP bytes | Media | Questions |
|---|---|---:|---:|---|---:|
| 1 | Presents from London | 103,737 | 128,642 | ready | 4 |
| 2 | What's my job? | 125,483 | 158,586 | ready | 4 |
| 3 | The holidays | 109,229 | 129,316 | ready | 3 |
| 4 | A postcard from London | 102,053 | 133,250 | ready | 2 |

Totals: 4 source pages, 4 lesson candidates, 4 ready media assets, 13 question revisions.

## Boundary evidence

The reviewed structural manifest assigns book pages 1–4 to the same section, `Unit 1 - Revision`, and assigns each page a distinct title. The four selected rows have independent source page IDs and independent question groups. No repeated-title continuation occurs inside this four-page slice.

Decision for **this batch only**: model the four pages as four lessons inside one curriculum section. This does not establish a global one-page-equals-one-lesson rule.

## Provenance verification

Each of the four current source rows resolves through:

`lesson_asset -> media_asset -> content_source_asset`

and preserves:

- legacy subject ID `1794eea5-4772-4c94-bd2b-b08e5815e733`;
- legacy record/page ID;
- legacy storage bucket/object;
- source page number/position;
- immutable source checksum SHA-256;
- source byte size.

Each of the 13 question revisions is still draft and has a `question_bank_revision_sources` link to the matching source page/media asset with the same input checksum. No question revision is published.

## Publication state

- Existing four legacy lessons: active but `published_at = NULL`.
- Existing four lesson assets: `publication_status = draft` and no asset publication timestamp.
- 13 question revisions: `status = draft`, not submitted/published.
- No curriculum section currently exists for this scope.
- Two active student entitlements exist, but the batch remains invisible because lesson/asset/question publication gates are not satisfied.

This validation does **not** authorize publication.

## Media-size decision

The current display WebP variants are valid derived assets, but they are not a size optimization for this batch:

- page 1: +24.01% versus RAW JPEG;
- page 2: +26.38%;
- page 3: +18.39%;
- page 4: +30.57%;
- combined RAW JPEG: 440,502 bytes;
- combined display WebP: 549,794 bytes;
- combined display increase: +24.81%.

Therefore BATCH-001 must **not** claim a successful size reduction from the existing display WebP variants. RAW remains immutable. A new derived WebP profile may be attempted later only if it is measurably smaller while preserving page readability; otherwise the smaller readable source may remain the preferred delivery candidate according to the application media contract.

Thumbnail/AI variants are not replacements for the canonical readable lesson page.

## Question gate

Database shape/provenance is verified for 13 questions, but semantic review against the page pixels/source text is **not yet closed** by this report. All 13 remain review-required. Answer fields must not be promoted solely because `answer_status = known` in the legacy-derived data.

## Current gate result

`DB_MEDIA_PROVENANCE_VALIDATED / CONTENT_REVIEW_PENDING`

Safe next action:

1. Review the 13 prompts/options/answers against the four source pages.
2. Record per-question decision (`approved`, `corrected`, or `rejected`) with source evidence.
3. Build the modern target dry-run for one section + four curated lesson slugs while accounting for the existing unpublished legacy import; do not create duplicates blindly.
4. Only after the question gate and target dry-run pass may controlled PostgreSQL mutation be considered.
