#!/usr/bin/env python3
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[2]
LOG=ROOT/'content-staging/CONTENT_RECONSTRUCTION_AUTOMATION_LOG.md'
text=LOG.read_text(encoding='utf-8')
checkpoint='''## 10. ACTIVE CHECKPOINT

- state: `COMPLETE`
- branch: `content/corpus-inventory-20260914`
- latest verified work HEAD before this handoff commit: `fcbf85fde72e7b9d3a11d111f3ab01d00aeeee78`
- last completed source: `0a76f44b-0a4f-4e36-9ea9-badecf78bf23 — التاريخ الكتاب المدرسي`
- current source: `7f02b242-5164-46d1-a82d-7f1023cfa8c9 — التربية الوطنية`
- current source baseline from live evidence: `NOT YET TECHNICALLY VERIFIED in this checkpoint; fetch live manifest/pages before making any structural assumption.`
- current operation: `History is finalized from immutable source-local evidence: 61/61 technical images, page 8 explicit TOC, page 9 first-semester cover, 9 verified lessons, 47 lesson-content pages, 12 lesson-review pages, all 61 pages classified exactly once, and 138/138 legacy questions structurally lesson-linked. History master equivalence remains NOT VERIFIED and must not be retroactively substituted. Next: technically verify التربية الوطنية from its own live manifest/pages and reconstruct only evidence-backed boundaries.`
- next source: `NOT YET RESOLVED — derive after التربية الوطنية from live MASTER_CONTENT_MANIFEST`
- blockers: `none`
- owner decision required now: `no`
'''
text,n=re.subn(r'## 10\. ACTIVE CHECKPOINT\n.*?\n---\n',checkpoint+'\n---\n',text,count=1,flags=re.S)
if n!=1: raise SystemExit('ACTIVE CHECKPOINT block not found exactly once')
run='''
## RUN 2026-09-14T13:15:00+03:00 — Worker B

- state: COMPLETE
- start HEAD: `aa707183aa03e0d47de68b717d6d097d7149c976`
- end HEAD before handoff-log commit: `fcbf85fde72e7b9d3a11d111f3ab01d00aeeee78`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `0a76f44b-0a4f-4e36-9ea9-badecf78bf23 — التاريخ الكتاب المدرسي`
- completed in this run:
  - verified Worker A's partial History handoff against live technical/discovery evidence and preserved the rejection of non-equivalent master History references;
  - generated complete ordered source-local visual evidence directly from all 61 immutable RAW pages and visually reviewed stored pages 8..68;
  - verified page 8 as an explicit TOC and page 9 as the `الفصل الدراسي الأول` cover;
  - resolved nine source-local lesson boundaries and twelve lesson-review pages without inventing an explicit Unit layer;
  - classified all 61 retained pages exactly once: 1 TOC + 1 semester cover + 47 lesson-content pages + 12 lesson-review pages;
  - structurally mapped all 138/138 legacy questions by verified page membership; semantic correctness remains NOT VERIFIED;
  - finalized the History reconstruction and updated MASTER_CONTENT_MANIFEST plus canonical status/inventory/validation/import/continuation files;
  - corrected one validation-only baseline assertion after discovering MASTER_CONTENT_MANIFEST still held the pre-History technical-image counter 950; no RAW/semantic state was mutated by the failed run.
- evidence produced/verified:
  - technical report: `content-staging/reconstruction/technical/0a76f44b-0a4f-4e36-9ea9-badecf78bf23.json`;
  - diagnostic master-equivalence report: `content-staging/reconstruction/educational/0a76f44b-0a4f-4e36-9ea9-badecf78bf23-discovery.json`;
  - visual index: `content-staging/reconstruction/educational/0a76f44b-0a4f-4e36-9ea9-badecf78bf23-visual-index.json`;
  - final reconstruction: `content-staging/reconstruction/educational/0a76f44b-0a4f-4e36-9ea9-badecf78bf23.json`;
  - source-local visual run `34831599212`; artifact `10342118472`; digest `sha256:dbb6cc5f980b293920f378ef24587ab9d9df65787e250fa955d33fbb3323a169`;
  - initial finalization run `34832016086` failed closed only on stale aggregate counter expectation (expected 1011, live manifest 950);
  - corrected finalization run `34832127755` passed `HISTORY_SOURCE_LOCAL_FINALIZATION_VERIFY_PASS`;
  - final artifact `10342790603`; digest `sha256:9c3cde6996f3cbb29741ffa1e22c989671ed1f241dfc0e7e8bf44666c88df1ca`;
  - final checkpoint commit: `fcbf85fde72e7b9d3a11d111f3ab01d00aeeee78`.
- ambiguity/review_required:
  - current master History parts remain `NOT VERIFIED` as equivalent to this RAW and were not used for semantic mapping;
  - formal book title beyond the legacy source label remains `NOT VERIFIED`;
  - no explicit Unit construct was proven in the retained slice, so no units were invented;
  - question semantic correctness remains `NOT VERIFIED`; structural membership is verified;
  - source review-required questions: 0.
- invariant result: PASS (`2,374 + 967 + 351 + 22,063 = 25,755`)
- Sources processed: 13/58
- Educational: 4/26
- Books / Units / Lessons / Lesson Pages: 4 / 25 / 119 / 460
- Exam Source Groups: 9/32
- Individual Exam Models: 135
- Exam Pages: 455/2,286
- Verified Answer Keys: 0
- Correction/report candidates: 140
- Source images technical: 1,011/5,273
- WebP generated / accepted / rejected: 0 / 0 / 0
- Legacy Questions: 25,755
- Lesson-linked: 2,374
- Exam-linked: 967
- Review-required: 351
- Unclassified: 22,063
- Duplicate groups classified: 0/99
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `0a76f44b-0a4f-4e36-9ea9-badecf78bf23 — التاريخ الكتاب المدرسي`
- current source: `7f02b242-5164-46d1-a82d-7f1023cfa8c9 — التربية الوطنية`
- exact next operation: `Fetch التربية الوطنية live manifest/pages; technically verify every source image and source-local sequence/SHA/MIME; establish identity and book/section/unit/lesson/review boundaries only from its own evidence; map its legacy questions only where structurally proven; quarantine ambiguity as review_required; assert 25,755 invariant; checkpoint.`
- next source: `NOT YET RESOLVED — derive after التربية الوطنية from live MASTER_CONTENT_MANIFEST`
- blockers: `none`
- handoff note: `Worker A should re-fetch live HEAD and this baton, verify History final reconstruction at fcbf85f..., then begin التربية الوطنية from its own evidence. Do not reopen History absent new drift evidence and do not inherit its semester/lesson pattern.`
'''
if '## RUN 2026-09-14T13:15:00+03:00 — Worker B' not in text:
    text=text.rstrip()+'\n\n'+run.strip()+'\n'
LOG.write_text(text,encoding='utf-8')
print('WORKER_B_HISTORY_HANDOFF_RECORDED')
