# Alwaslh Legacy Content Staging

This directory is the controlled staging area for reconstructing educational content from the legacy Supabase source before any future import into the current Alwaslh PostgreSQL database.

## Authority and safety

- Legacy Supabase is **read-only source evidence**.
- `raw/` is immutable after extraction. Do not hand-edit raw records or raw images.
- `curated/` is the reviewed educational model that may later become an import source.
- Production PostgreSQL is not written from this repository until a curated batch passes validation and explicit import review.
- Never treat a legacy `lessons` row as a final lesson automatically. Legacy rows are page/source records unless a reviewed curriculum mapping says otherwise.

## Pipeline

```text
Legacy Supabase
  -> raw inventory + raw page records + raw images + SHA-256
  -> validation / duplicate analysis
  -> curriculum reconstruction
  -> Class -> Subject -> Document -> Section/Unit -> Lesson -> ordered pages
  -> question normalization and review flags
  -> WebP derivation from immutable raw images
  -> curated validation
  -> production dry-run/import in 7eaur/alwaslh
```

## Layout

```text
content-staging/
  raw/
    legacy-supabase/
      inventory/
      subjects/<legacy-subject-id>/
        subject.json
        pages.json
        images/
        manifest.json
  curated/
    <class>/<subject>/<document>/...
  reports/
  schemas/
  tools/
```

Raw image files are stored once. Optimized WebP files are derived outputs and must record both source and optimized SHA-256 values.

## Required environment for extraction

The extractor reads only from the legacy project:

- `LEGACY_SUPABASE_URL`
- `LEGACY_SUPABASE_PUBLISHABLE_KEY`

Do not commit keys or service-role credentials.

## Initial verified source

Legacy Supabase project ref: `zhbgbmqhonqmzpqfiehs`.

The first reconstruction target is legacy subject:

- class: `تاسع انجليزي`
- subject: `انجليزي الكتاب`
- subject id: `1794eea5-4772-4c94-bd2b-b08e5815e733`
- source page/image rows: 69
- embedded questions: 104

This source is intentionally extracted as pages first. Final Unit/Lesson structure is a separate curated decision.
