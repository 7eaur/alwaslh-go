# Grade 9 English Unit 2 — Reviewed Publication Report

Date: **2026-09-14**

Status: **DONE / COMMITTED_STATE_VERIFIED_AND_PUBLISHED**

## Authorized scope

Only the two explicitly reviewed Unit 2 Lessons were authorized for publication. No other Grade 9 English Lesson, Lesson Asset, or Question Revision was authorized by this gate.

### Lesson 1

- slug: `curated-english9-pb3-u2-describing-people-and-animals`
- title: `Describing people and animals`
- source book pages: `5..8`
- published Lesson Assets: `4`
- reviewed Question Revisions: `12`

### Lesson 2

- slug: `curated-english9-pb3-u2-time-and-meeting`
- title: `Telling time and arranging a meeting`
- source book pages: `9..10`
- published Lesson Assets: `2`
- reviewed Question Revisions: `7`

## Question review

Total reviewed questions: `19`.

- approved unchanged: `18`
- corrected before publication: `1`

Corrected page-10 question:

- old prompt: `When is Rashid meeting mentioned in the dialogue?`
- reviewed prompt: `When is Fuad helping Dad on Saturday?`
- answer: `at six o'clock`
- reviewed explanation: `Fuad says he is helping Dad at six o'clock.`

The correction was applied while the revision was still Draft and before the publication gate. Source provenance was retained.

## Publication mechanics

Publication runner source commits:

- publisher: `ea5a19b7086eb8779701be2b1f47fc073b38aa12`
- reviewed correction wrapper/final head: `7d17e19bef37835d500de492053e728f0cdb9f1b`

Railway deployment:

`5024b218-32e0-49fe-b9f8-20ee82c5bcd0` — `SUCCESS`

The runner performs a fail-closed reviewed-state check, transaction/rollback gate, controlled publication apply, and committed-state post-verification. The final runtime markers were:

- `G9_U2_PUBLISH_APPLY_PASS`
- `G9_U2_PUBLISH_FULL_PASS`
- final status: `COMMITTED_STATE_VERIFIED_AND_PUBLISHED`

Post-verify result:

- newly published Lessons: `2`
- newly published Lesson Assets: `6`
- newly published Question Revisions: `19`
- target Reader-eligible published assets: `6`
- target published/known Question Revisions eligible for Quiz Builder: `19`
- Grade 9 English publication totals after this gate: Lessons `2`, Lesson Assets `6`, Question Revisions `19`

This exact total proves the remaining imported Grade 9 English corpus stayed unpublished.

## Student delivery meaning

The two target Lessons now satisfy the Student Reader publication predicates: active lesson, active section, non-null `published_at`, published Lesson Assets, and ready Media Assets. Normal entitlement/auth rules still apply per student.

The 19 reviewed questions are published Question Bank revisions with known answers and are linked to the two modern Lessons (`12 + 7`). They are available to Quiz Builder. This publication gate **does not claim that a standalone student Quiz/version was created or published**; that remains a separate product action if required.

## Isolation guarantees

- no other Lesson was published by this gate
- no other Lesson Asset was published by this gate
- no other Question Revision was published by this gate
- immutable RAW was not mutated
- media binaries were not mutated
- page 70 was not fabricated
- the prohibited `69 -> 62` heuristic was not used
- source/provenance identities were retained

After verification, the Railway content service was returned to an idle start command so later documentation commits cannot replay publication logic.
