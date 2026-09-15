from pathlib import Path
import re, json
p=Path('content-staging/CONTENT_RECONSTRUCTION_AUTOMATION_LOG.md')
s=p.read_text()
sid='ab701a9e-3efb-409a-8ed1-9752d41c4771'
tech=json.loads(Path(f'content-staging/reconstruction/technical/{sid}.json').read_text())
assert tech['technical_verified_images']==169 and not tech['technical_failures'] and tech['page_sequence']['missing']==[]
checkpoint="""## 10. ACTIVE CHECKPOINT

- state: `PARTIAL_SAFE_HANDOFF`
- branch: `content/corpus-inventory-20260914`
- latest evidence HEAD before this handoff tooling: `3701f19266b7125977bc03395b0fda54ec21e9fb`
- last completed source: `d1a6b8f8-d81b-4824-86e1-d370ec28bdf1 — العربي نماذج وزارية 1447`
- current source: `ab701a9e-3efb-409a-8ed1-9752d41c4771 — كتاب العربي - الجزء الأول`
- current source baseline from live manifest: `169 pages / 169 images / 0 legacy questions / 0 download failures; anomaly arrays empty.`
- current source verified work: `169/169 immutable RAW images technically verified by byte-size/SHA-256/MIME; retained page sequence 9..177 contiguous; 0 duplicate SHA groups; 45 contiguous legacy metadata title-runs extracted. Metadata explicitly contains تقويم الوحدة الأولى through تقويم الوحدة الثانية عشرة, but Book/Unit/Lesson semantic finalization and visual semantic inspection remain NOT VERIFIED.`
- current operation: `Do not repeat technical verification absent drift. Establish exact source identity and inspect source-local visual/master evidence for pages 9..177; validate whether the 12 explicit unit-assessment title runs safely delimit 12 units and whether the intervening title runs are lesson boundaries. Preserve assessment pages separately; source has 0 legacy questions, so do not fabricate mappings. Finalize only after evidence is sufficient; otherwise retain NOT VERIFIED/review_required.`
- next source: `Resolve only after Arabic book part 1 finalization from live MASTER.`
- blockers: `Semantic Book/Unit/Lesson structure and visual page semantics are not yet verified; metadata title evidence is strong but was intentionally not promoted to canonical structure without the next evidence gate.`

---"""
s2=re.sub(r'## 10\. ACTIVE CHECKPOINT\n.*?\n---',checkpoint,s,count=1,flags=re.S)
assert s2!=s
run="""

## RUN 2026-09-15T03:17:30+03:00 — Worker A

- state: PARTIAL_SAFE_HANDOFF
- start HEAD: `06f266eaa801be9cd90e1908fabf31fca79c5bb6`
- end HEAD before handoff-log commit: `3701f19266b7125977bc03395b0fda54ec21e9fb`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `ab701a9e-3efb-409a-8ed1-9752d41c4771 — كتاب العربي - الجزء الأول`
- completed in this run:
  - reviewed the live Arabic 1447 finalization and reconciled MASTER progress before advancing;
  - verified 169/169 immutable RAW images for Arabic book part 1 by byte-size, SHA-256 and MIME;
  - verified retained page sequence 9..177 is contiguous with no missing pages and 0 duplicate SHA groups;
  - extracted 45 contiguous source-local metadata title runs without promoting them to semantic structure;
  - confirmed explicit metadata assessment titles from `تقويم الوحدة الأولى` through `تقويم الوحدة الثانية عشرة`;
  - created technical evidence only; no production import/publication and no RAW mutation.
- evidence produced/verified:
  - `content-staging/reconstruction/technical/ab701a9e-3efb-409a-8ed1-9752d41c4771.json`;
  - GitHub Actions run `34912501125` completed successfully;
  - evidence commit `3701f19266b7125977bc03395b0fda54ec21e9fb`.
- ambiguity/review_required:
  - exact Book/Unit/Lesson semantic structure: `NOT VERIFIED` pending visual/exact-reference evidence;
  - visual semantic inspection: `NOT VERIFIED`;
  - source has 0 legacy questions, therefore no mappings were invented.
- invariant result: PASS
- Sources processed: 36/58
- Educational: 16/26
- Books / Units / Lessons / Lesson Pages: 14 / 57 / 328 / 1,527
- Exam Source Groups: 20/32
- Individual Exam Models: 370
- Exam Pages: 1,274/2,286
- Verified Answer Keys: 0
- Source images technical: 3,190/5,273
- WebP generated / accepted / rejected: 0 / 0 / 0
- Legacy Questions: 25,755
- Lesson-linked: 13,135
- Exam-linked: 1,920
- Review-required: 1,229
- Unclassified: 9,471
- Duplicate groups classified: 0/99
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `d1a6b8f8-d81b-4824-86e1-d370ec28bdf1 — العربي نماذج وزارية 1447`
- current source: `ab701a9e-3efb-409a-8ed1-9752d41c4771 — كتاب العربي - الجزء الأول`
- exact next operation: `Use the already-verified technical report; establish exact source identity and inspect source-local visual/master evidence for pages 9..177, then validate or reject the apparent 12-unit / title-run lesson boundaries before canonical finalization.`
- next source: `NOT YET RESOLVED`
- blockers: `semantic structure/visual evidence gate only; no technical blocker`
- handoff note: `Worker B must not rerun Arabic 1447 or repeat the 169-image technical pass absent drift. Continue Arabic book part 1 from the semantic/visual evidence gate. Metadata title runs are evidence, not permission to guess; keep NOT VERIFIED where exact identity or boundaries remain insufficient.`
"""
p.write_text(s2.rstrip()+run+'\n')
