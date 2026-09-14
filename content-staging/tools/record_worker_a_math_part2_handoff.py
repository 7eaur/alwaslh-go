#!/usr/bin/env python3
from __future__ import annotations
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT=Path(__file__).resolve().parents[2]
LOG=ROOT/'content-staging/CONTENT_RECONSTRUCTION_AUTOMATION_LOG.md'
text=LOG.read_text(encoding='utf-8')
old_current='- current source: `b80cbba1-410a-4346-9446-c3f01c4f9e56 — كتاب الرياضيات - الجزء الثاني`'
if old_current not in text:
    raise SystemExit('BATON_DRIFT: expected Math Part 2 active checkpoint not found')
if '## RUN 2026-09-14T19:20:21+03:00 — Worker B' not in text:
    raise SystemExit('BATON_DRIFT: expected latest Worker B run not found')

start=text.index('## 10. ACTIVE CHECKPOINT')
marker='\n---\n\n### Shared handoff rule'
end=text.index(marker,start)
checkpoint='''## 10. ACTIVE CHECKPOINT

- state: `READY_NEXT_SOURCE`
- branch: `content/corpus-inventory-20260914`
- latest evidence HEAD before this handoff tooling: `f138cb2872ca8afdbcdd01776ab3c41d7e7b4e6d`
- last completed source: `b80cbba1-410a-4346-9446-c3f01c4f9e56 — كتاب الرياضيات - الجزء الثاني`
- current source: `b6ce737e-26d4-4219-a607-27bfb7d2f518 — كتاب الإسلامية - الجزء الأول`
- current source baseline from live manifest: `status=empty; 0 pages, 0 images, 0 legacy questions, 0 download failures; anomaly arrays preserved empty.`
- current source verified work: `Manifest-level emptiness VERIFIED. No Book/Unit/Lesson/page/question structure exists in the retained legacy payload and none may be invented from the source name.`
- current operation: `Re-fetch live HEAD and this baton; verify pages.json and subject.json are consistent with the manifest-level empty source; determine and apply only an evidence-backed canonical verified-empty source disposition if the live MASTER/status schema supports it. Do not count or invent a Book, Unit, Lesson, page, question mapping, import, or publication. If no canonical empty-source disposition is defined, leave this source active as NOT VERIFIED/review_required and document the schema-policy blocker rather than silently skipping it.`
- next source: `NOT YET RESOLVED — resolve from live MASTER only after the current empty source receives a canonical evidence-backed disposition.`
- blockers: `Content reconstruction blocker for current source: retained legacy payload is genuinely empty. No prior canonical verified-empty source pattern was found during this run; Worker B must fail closed if the live schema still lacks one.`
- owner decision required now: `no; continue source-by-source fail-closed`
'''
text=text[:start]+checkpoint+text[end:]

ts=datetime.now(ZoneInfo('Asia/Riyadh')).replace(microsecond=0).isoformat()
run=f'''\n\n## RUN {ts} — Worker A

- state: COMPLETE
- start HEAD: `d1ca881dc475a24cdce53f2a1b5b2a42661a5ef3`
- end HEAD before handoff-log tooling: `f138cb2872ca8afdbcdd01776ab3c41d7e7b4e6d`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `b80cbba1-410a-4346-9446-c3f01c4f9e56 — كتاب الرياضيات - الجزء الثاني`
- completed in this run:
  - consumed and verified the live Worker B Math Part 1 baton against the live branch, manifests, evidence, and workflow state; no conflicting active/queued workflow existed for Math Part 2 at startup;
  - technically verified all **135/135** immutable RAW images: readable, byte-size/SHA-256/MIME matched, page sequence **7..141** contiguous, **0** failures, **0** duplicate page numbers, and **0** duplicate SHA groups;
  - extracted 25 source-local title runs as evidence candidates without automatically promoting them to Book/Unit/Lesson boundaries;
  - generated occurrence-safe visual contact sheets and inspected **all 135 retained pages** across **12 sheets**;
  - independently verified Math Part 2 structure from its own evidence only: **3 units / 19 lessons / 122 lesson pages / 13 non-lesson pages**;
  - verified unit banners and ranges: **الوحدة الخامسة — الهندسة (7..64)**, **الوحدة السادسة — الهندسة الإحداثية والتحويلات (65..110)**, **الوحدة السابعة — الإحصاء (111..141)**;
  - verified non-lesson pages as **7 general-exercise pages + 6 unit-test pages**; no review page was invented;
  - confirmed the source contains **0 legacy questions**, so no question mappings, review-required question assignments, or semantic claims were invented;
  - reran technical verification during exact-head guarded finalization, reconstructed the source, updated MASTER and evidence-backed status files, and passed the global question invariant and zero-mutation gates;
  - inspected the next live source manifest and found `كتاب الإسلامية - الجزء الأول` is evidence-backed **empty** (0 pages/images/questions); did not fabricate content or count it as completed.
- evidence produced/verified:
  - `content-staging/reconstruction/technical/b80cbba1-410a-4346-9446-c3f01c4f9e56.json` — 135/135 technical PASS;
  - `content-staging/reconstruction/educational/b80cbba1-410a-4346-9446-c3f01c4f9e56.json` — verified source-local reconstruction;
  - source-analysis workflow run `34869618522` — source-local title-run / technical evidence PASS;
  - complete visual workflow run `34869811987`, artifact `10358975418`, digest `sha256:2c029bac25b762f9b37f4c8d0e43f32c7091845e008c91bef006c8955950d6a8`; **12/12 sheets and 135/135 pages inspected**;
  - finalization workflow run `34870377097` — `MATH_PART2_RECONSTRUCTION_VERIFY_PASS` and `MATH_PART2_FINALIZATION_VERIFY_PASS`; all live-HEAD drift gates PASS;
  - canonical evidence commit: `f138cb2872ca8afdbcdd01776ab3c41d7e7b4e6d`;
  - next-source manifest: `content-staging/raw/legacy-supabase/subjects/b6ce737e-26d4-4219-a607-27bfb7d2f518/manifest.json` — `status=empty`, 0/0/0 pages/images/questions.
- ambiguity/review_required:
  - Math Part 2: no unresolved page-boundary ambiguity remains in the retained 135-page source;
  - semantic question correctness: `NOT APPLICABLE` because the source contains 0 legacy questions;
  - no external/master reference was used to transfer Math Part 2 structure and no Part 1 unit/lesson counts were inherited;
  - next source `كتاب الإسلامية - الجزء الأول`: Book identity/structure beyond its legacy label is **NOT VERIFIED** because the retained payload is empty; no prior canonical empty-source disposition was found in the live workflow/schema search.
- invariant result: PASS
- Sources processed: 25/58
- Educational: 12/26
- Books / Units / Lessons / Lesson Pages: 12 / 40 / 236 / 1,161
- Exam Source Groups: 13/32
- Individual Exam Models: 206
- Exam Pages: 668/2,286
- Verified Answer Keys: 0
- Source images technical: 1,986/5,273
- WebP generated / accepted / rejected: 0 / 0 / 0
- Legacy Questions: 25,755
- Lesson-linked: 7,511
- Exam-linked: 1,132
- Review-required: 448
- Unclassified: 16,664
- Duplicate groups classified: 0/99
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `b80cbba1-410a-4346-9446-c3f01c4f9e56 — كتاب الرياضيات - الجزء الثاني`
- current source: `b6ce737e-26d4-4219-a607-27bfb7d2f518 — كتاب الإسلامية - الجزء الأول`
- exact next operation: `Verify current source pages.json and subject.json against its status=empty manifest, then record only a canonical verified-empty source disposition if the live MASTER/status schema supports one; never fabricate Book/Unit/Lesson/page/question content. If no canonical empty disposition exists, preserve this source ACTIVE as NOT VERIFIED/review_required and document that schema-policy blocker before resolving the following source.`
- next source: `NOT YET RESOLVED — resolve only after the current empty-source disposition is safely recorded from the live MASTER.`
- blockers: `Current source has no retained content (0 pages/images/questions), and no prior canonical verified-empty source pattern was found. This does not invalidate Math Part 2 completion; it constrains the next source only.`
- handoff note: `Math Part 2 is safely closed from its own RAW/source-local evidence. Worker B must not infer Islamic Part 1 content from its name or from any neighboring source. Treat the empty manifest as evidence, verify the companion empty files, and fail closed unless a canonical verified-empty disposition can be recorded without inventing educational structure.`
'''
LOG.write_text(text.rstrip()+run+'\n',encoding='utf-8')
print(ts)
