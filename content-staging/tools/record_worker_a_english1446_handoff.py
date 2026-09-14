#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / "content-staging/CONTENT_RECONSTRUCTION_AUTOMATION_LOG.md"
RUN_MARKER = "## RUN 2026-09-14T11:39:30+03:00 — Worker A"

active = """## 10. ACTIVE CHECKPOINT

- state: `READY`
- branch: `content/corpus-inventory-20260914`
- latest verified work HEAD before this handoff commit: `52e2ac53841e5a53ecb4deac85e6e2bdb777fc8a`
- last completed source: `062f0aa0-ae21-454e-ad9a-c390df6e4a08 — الانجليزي نماذج وزارية 1446`
- current source: `da6fc228-1ada-4627-8306-80d9d3401490 — الانجليزي نماذج وزارية 1447`
- current source baseline from live manifest: `42 images/pages; 234 legacy questions; duplicate page numbers recorded at 18, 27, 29; no missing-image/malformed-image anomalies recorded`
- current operation: `read live manifest/pages preserving duplicate page-number identities -> technically verify all 42 images -> inspect source-record order, SHA/title/storage evidence -> generate complete visual evidence -> resolve Individual Exam Model/correction boundaries only from English 1447 evidence -> isolate any numbering/title ambiguity as review_required rather than normalizing it -> map all 234 legacy questions only where structurally evidenced -> assert global 25,755 invariant -> checkpoint`
- next source: `NOT YET RESOLVED — derive only after English 1447 from live MASTER_CONTENT_MANIFEST`
- blockers: `none`
- owner decision required now: `no`
"""

run = """
## RUN 2026-09-14T11:39:30+03:00 — Worker A

- state: COMPLETE
- start HEAD: `e7d9de180e32cd0315b97831b2376d169a2fe2b4`
- end HEAD before handoff-log commit: `52e2ac53841e5a53ecb4deac85e6e2bdb777fc8a`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `062f0aa0-ae21-454e-ad9a-c390df6e4a08 — الانجليزي نماذج وزارية 1446`
- completed in this run:
  - verified Worker B's English 1445 finalization against live branch state and shared handoff;
  - completed 39/39 non-destructive technical verification for English 1446: existence/readability/byte-size/SHA-256/MIME all match and page sequence 1..39 is contiguous;
  - generated and visually inspected complete contact sheets covering all 39 source pages;
  - independently resolved thirteen source-local three-page exam occurrences, each with two question-paper pages followed by its matching correction/result page;
  - preserved visible correction-form codes as source evidence without promoting them to official model codes;
  - finalized 13 unique Individual Exam Models / 39 finalized Exam Pages / 13 correction-result candidates / 0 verified standalone Answer Keys;
  - preserved the source's 0 legacy questions without fabrication or synthetic mapping;
  - updated MASTER_CONTENT_MANIFEST and canonical reconstruction/status/handoff/inventory/validation/import/continuation reports through exact-head GitHub Actions finalization.
- evidence produced/verified:
  - discovery workflow run `34823356315`: success; artifact `10338234805`, digest `sha256:98637b8b6283b83b0513eeef86f05d46ce132e326f4596ceda3d19a0abf2d49f`;
  - complete visual sheets reviewed: `001-012`, `013-024`, `025-036`, `037-039`;
  - technical report: `content-staging/reconstruction/technical/062f0aa0-ae21-454e-ad9a-c390df6e4a08.json`;
  - discovery report: `content-staging/reconstruction/exams/source-groups/062f0aa0-ae21-454e-ad9a-c390df6e4a08-discovery.json`;
  - final reconstruction: `content-staging/reconstruction/exams/source-groups/062f0aa0-ae21-454e-ad9a-c390df6e4a08.json`;
  - finalization workflow run `34823771285`: success with `ENGLISH_1446_FINALIZATION_VERIFY_PASS`;
  - final artifact `10339383045`, digest `sha256:d42e8508475e4a6a848a634abad3047eab8dfd569b0dd022831f72361712b850`;
  - finalized reconstruction bot commit: `52e2ac53841e5a53ecb4deac85e6e2bdb777fc8a`;
  - within-source duplicate SHA groups: 0.
- ambiguity/review_required:
  - model boundaries: none after full source-local metadata + visual review;
  - standalone official Answer Keys: `NOT VERIFIED`; thirteen correction/result pages remain candidates only;
  - official model codes/titles/term beyond explicit evidence: `NOT VERIFIED`;
  - source legacy questions: 0, so no semantic question mapping was fabricated.
- invariant result: PASS (`2,236 + 733 + 351 + 22,435 = 25,755`)
- Sources processed: 11/58
- Educational: 3/26
- Books / Units / Lessons / Lesson Pages: 3 / 25 / 110 / 413
- Exam Source Groups: 8/32
- Individual Exam Models: 122
- Exam Pages: 416/2,286
- Verified Answer Keys: 0
- Source images technical: 908/5,273
- WebP generated / accepted / rejected: 0 / 0 / 0
- Legacy Questions: 25,755
- Lesson-linked: 2,236
- Exam-linked: 733
- Review-required: 351
- Unclassified: 22,435
- Duplicate groups classified: 0/99
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `062f0aa0-ae21-454e-ad9a-c390df6e4a08 — الانجليزي نماذج وزارية 1446`
- current source: `da6fc228-1ada-4627-8306-80d9d3401490 — الانجليزي نماذج وزارية 1447`
- exact next operation: `Fetch English 1447 live manifest/pages and preserve duplicate page-number identities at 18, 27 and 29; technically verify all 42 image records; inspect sequence/SHA/title/storage evidence and render complete contact sheets; resolve model/correction boundaries only from English 1447 evidence; map all 234 legacy questions only where structurally evidenced; quarantine unresolved records as review_required; assert global invariant; checkpoint.`
- next source: `NOT YET RESOLVED — derive after English 1447 from live MASTER_CONTENT_MANIFEST`
- blockers: `none`
- handoff note: `Worker B should re-fetch live HEAD and this baton, confirm English 1446 finalization is complete, then treat English 1447's duplicate page-number records as provenance to investigate rather than normalize. Do not inherit the 13x3 English 1446 pattern without new evidence.`
"""

text = PATH.read_text(encoding="utf-8")
if RUN_MARKER in text:
    raise SystemExit("handoff already recorded")
pattern = re.compile(r"## 10\. ACTIVE CHECKPOINT\n.*?\n---\n\n### Shared handoff rule", re.S)
replacement = active.rstrip() + "\n\n---\n\n### Shared handoff rule"
text2, count = pattern.subn(replacement, text, count=1)
if count != 1:
    raise SystemExit(f"ACTIVE CHECKPOINT replacement count={count}")
PATH.write_text(text2.rstrip() + "\n\n" + run.strip() + "\n", encoding="utf-8")
print("WORKER_A_ENGLISH_1446_HANDOFF_RECORDED")
