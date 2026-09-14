#!/usr/bin/env python3
from pathlib import Path
import re

LOG=Path('content-staging/CONTENT_RECONSTRUCTION_AUTOMATION_LOG.md')
text=LOG.read_text(encoding='utf-8')
start='ce49a13c341abe1866a225a0255a88df50f1aa1a'
evidence_head='81b2f46773e109aa5edea0d56673912cfdf832e4'
current_id='3d91d812-ab78-476a-b2fc-dc2c31152e1a'
current_name='الاحياء نماذج وزارية 1445'

checkpoint=f'''## 10. ACTIVE CHECKPOINT

- state: `READY_NEXT_SOURCE`
- branch: `content/corpus-inventory-20260914`
- latest evidence HEAD before this handoff tooling: `{evidence_head}`
- last completed source: `67d4ffae-68e1-42e8-9c3b-72329973c93d — الأحياء الكتاب المدرسي`
- current source: `{current_id} — {current_name}`
- current source baseline from live manifest: `60 pages / 60 images / 0 legacy questions / 0 download failures; anomaly arrays empty.`
- current source verified work: `NOT STARTED; do not inherit Biology textbook structure or any prior exam-model pattern.`
- current operation: `Re-fetch live HEAD and baton; confirm no active/running workflow for this exact source; technically verify all 60 immutable RAW images, perform source-local exam boundary discovery and complete visual inspection, resolve Individual Exam Model occurrences and correction/Answer-Key evidence without guessing, map zero legacy questions (none exist), assert global invariants, then checkpoint.`
- next source: `Resolve only after Biology Exams 1445 finalization from live MASTER.`
- blockers: `none`
- biology textbook evidence: `214/214 technical + 214/214 exact SHA identity against master/الأحياء ثالث ثانوي/الاحياء الكتاب المدرسي/الصور; 8 units / 47 lessons / 193 lesson pages / 8 covers / 13 reviews; 3,003 lesson-linked + 301 review_required; semantic correctness NOT VERIFIED.`
- verified-empty policy: `content-staging/reconstruction/VERIFIED_EMPTY_SOURCE_DISPOSITION_POLICY.json — verified_empty_retained_source counts as processed source + processed educational source, but never as a verified Book/Unit/Lesson/page structure.`
'''
pat=r'## 10\. ACTIVE CHECKPOINT\n.*?\n---\n\n### Shared handoff rule'
m=re.search(pat,text,flags=re.S)
if not m:
    raise SystemExit('ACTIVE CHECKPOINT block not found; fail closed')
replacement=checkpoint+'\n---\n\n### Shared handoff rule'
text=text[:m.start()]+replacement+text[m.end():]

run='''

## RUN 2026-09-14T21:42:15+03:00 — Worker A

- state: COMPLETE
- start HEAD: `ce49a13c341abe1866a225a0255a88df50f1aa1a`
- end HEAD before handoff-log commit: `81b2f46773e109aa5edea0d56673912cfdf832e4`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `67d4ffae-68e1-42e8-9c3b-72329973c93d — الأحياء الكتاب المدرسي`
- completed in this run:
  - verified no conflicting active/queued workflow before Biology work;
  - technically reverified all 214/214 immutable RAW images, with contiguous stored pages 8..221, no missing/duplicate page numbers, 0 technical failures, and 0 within-source duplicate SHA groups;
  - established exact source identity: 214/214 RAW SHA-256 values match the single canonical master directory `الأحياء ثالث ثانوي/الاحياء الكتاب المدرسي/الصور`;
  - generated complete contact sheets and inspected unit/review transitions without using OCR or changing RAW;
  - reconstructed and verified 1 Book / 8 Units / 47 Lessons / 193 Lesson pages / 8 Unit-cover pages / 13 Unit-review pages; all 214 retained pages classified exactly once;
  - structurally accounted for all 3,304 legacy questions: 3,003 lesson-linked by verified page membership and 301 `review_required` on non-lesson cover/review pages; semantic correctness remains `NOT VERIFIED`;
  - ran guarded finalization with exact-live-HEAD gates before finalization and before evidence write; all invariant/finalization steps passed;
  - updated MASTER_CONTENT_MANIFEST and reconstruction/status/handoff/inventory/validation/import/continuation evidence; no production import/publication was created.
- evidence produced/verified:
  - `content-staging/reconstruction/technical/67d4ffae-68e1-42e8-9c3b-72329973c93d.json`;
  - `content-staging/reconstruction/educational/67d4ffae-68e1-42e8-9c3b-72329973c93d-discovery.json`;
  - `content-staging/reconstruction/educational/67d4ffae-68e1-42e8-9c3b-72329973c93d.json`;
  - discovery workflow run `34881574393` success; contact-sheet artifact `10363007798` covers all 214 pages;
  - finalization workflow run `34882293130` success; marker `BIOLOGY_FINALIZATION_VERIFY_PASS`;
  - canonical Biology evidence commit `81b2f46773e109aa5edea0d56673912cfdf832e4`.
- ambiguity/review_required:
  - 301 source questions reside on verified non-lesson unit-cover/review pages and remain `review_required` rather than being forced into lessons;
  - semantic correctness of all legacy questions/content remains `NOT VERIFIED`;
  - verified standalone official Answer Keys are not applicable to this textbook source;
  - initial discovery workflow configuration attempt failed before any job/evidence mutation and was corrected; no resulting data blocker remains.
- invariant result: PASS
- Sources processed: 28/58
- Educational: 15/26
- Books / Units / Lessons / Lesson Pages: 13 / 48 / 283 / 1,354
- Exam Source Groups: 13/32
- Individual Exam Models: 206
- Exam Pages: 668/2,286
- Verified Answer Keys: 0
- Source images technical: 2,200/5,273
- WebP generated / accepted / rejected: 0 / 0 / 0
- Legacy Questions: 25,755
- Lesson-linked: 10,514
- Exam-linked: 1,132
- Review-required: 749
- Unclassified: 13,360
- Duplicate groups classified: 0/99
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `67d4ffae-68e1-42e8-9c3b-72329973c93d — الأحياء الكتاب المدرسي`
- current source: `3d91d812-ab78-476a-b2fc-dc2c31152e1a — الاحياء نماذج وزارية 1445`
- exact next operation: `Worker B must re-fetch live HEAD/baton, ensure no active workflow for source 3d91d812-ab78-476a-b2fc-dc2c31152e1a, technically verify its 60 RAW images, discover/visually verify source-local Individual Exam Model boundaries and correction/Answer-Key relations, preserve all ambiguity as review_required/NOT VERIFIED, then checkpoint.`
- next source: `NOT YET RESOLVED — resolve only after Biology Exams 1445 from live MASTER.`
- blockers: `none`
- handoff note: `Biology textbook is closed and must not be rerun absent new drift evidence. Biology Exams 1445 has a live baseline of 60 pages/images, 0 legacy questions, 0 download failures, and empty anomaly arrays. Do not inherit textbook structure or previous exam-source page/model patterns.`
'''
text=text.rstrip()+run+'\n'
LOG.write_text(text,encoding='utf-8')
print('BIOLOGY_AUTOMATION_HANDOFF_READY')
