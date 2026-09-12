# Legacy Supabase Source Inventory

Snapshot checked: 2026-09-13

Project ref: `zhbgbmqhonqmzpqfiehs`

Live source counts at the start of this reconstruction branch:

- classes: **15**
- subjects: **58**
- page records (`lessons`): **5,273**
- embedded `ai_questions`: **25,755**
- quizzes: **0**
- saved_questions: **0**
- subject_extra_classes: **0**

Important: the embedded question total is a live-source value and is higher than an earlier audit snapshot. The extraction pipeline therefore records a new export manifest/digest on every extraction and treats source drift as data to review, not as something to hide.

## First pilot

`تاسع انجليزي → انجليزي الكتاب`

- legacy subject ID: `1794eea5-4772-4c94-bd2b-b08e5815e733`
- pages: **69**
- embedded questions: **104**
- images expected from page records: **69**
- structure reference: `تاسع انجليزي/الانجليزي_تاسع/manifest.json`

The pilot is intentionally reconstructed before attempting the full source. The old `lessons` table is page-oriented and must not be copied 1:1 into the current application curriculum model.
