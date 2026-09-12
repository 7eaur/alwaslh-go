# Curriculum Reconstruction Policy

The staging repository must not promote legacy page rows directly to production lessons.

## Required hierarchy

```text
Canonical Class
  -> Canonical Subject
    -> Source Document
      -> Curriculum Section / Unit
        -> Reviewed Lesson
          -> Ordered Page Assets
          -> Reviewed Questions
```

## Raw vs curated

### Raw

Raw records preserve the legacy source without semantic rewriting. A legacy `lessons` row is a page/source record.

### Curated

Curated content may add/recover:

- canonical class and subject mapping;
- document identity/type/year;
- Unit/Section boundaries;
- reviewed Lesson boundaries;
- ordered page membership;
- normalized question type/options/answer status;
- OCR/summary metadata;
- optimized WebP derivatives.

Every curated entity must preserve source provenance.

## Lesson boundary rule

`same title + contiguous page number` is **candidate evidence only**. It is not sufficient by itself to declare a final Lesson.

A final Lesson must be supported by one or more of:

1. explicit source document structure (contents/manifest/unit mapping);
2. a reviewed curriculum mapping;
3. a deterministic rule documented for that document family;
4. human review when source structure is ambiguous.

Do not merge noncontiguous repeated titles automatically.

## Grade 9 English reconstruction

The existing `تاسع انجليزي/الانجليزي_تاسع/manifest.json` contains `section`, `title`, `source_page`, and `book_page` data. The 69 live Supabase rows correspond to book page numbers 1..69 and source image names page_0005..page_0073. Therefore this manifest is valid structural evidence for reconstructing Unit/Section membership, but page titles remain lesson/activity candidates until reviewed.

## Questions

Questions remain attached to their exact legacy page during staging.

Normalization must never invent answers:

- valid MCQ: preserve options and in-range correct index;
- semantic true/false: canonicalize representation while preserving meaning;
- unsupported/malformed: `review_required`;
- direct question without trusted answer: `unknown`.

Final question-to-lesson links are derived only after the page-to-lesson mapping is approved.

## Images

Raw image bytes are immutable evidence.

Optimized images:

- are derived from raw bytes;
- use WebP;
- preserve pixel dimensions by default;
- never upscale;
- must decode successfully after conversion;
- must record raw and optimized SHA-256;
- are rejected when size savings are negligible;
- must remain readable as textbook pages.

## Production gate

No curated batch is production-importable until all of these are true:

- hierarchy validated;
- no unresolved duplicate page positions;
- all page assets present and checksum-verified;
- image optimization report complete;
- questions normalized and unresolved cases enumerated;
- provenance complete;
- target mapping explicit;
- import dry-run is duplicate-safe and publication-safe.
