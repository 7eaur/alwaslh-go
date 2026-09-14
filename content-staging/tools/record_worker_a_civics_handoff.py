#!/usr/bin/env python3
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[2]
LOG=ROOT/'content-staging/CONTENT_RECONSTRUCTION_AUTOMATION_LOG.md'
text=LOG.read_text(encoding='utf-8')
checkpoint='''## 10. ACTIVE CHECKPOINT

- state: `COMPLETE`
- branch: `content/corpus-inventory-20260914`
- latest verified work HEAD before this handoff commit: `c6497f06a2810915d39e58b249e8060932ec3932`
- last completed source: `7f02b242-5164-46d1-a82d-7f1023cfa8c9 — التربية الوطنية`
- current source: `a7f1e94f-82d1-4146-af5b-4e9b51363f0b — كتاب الجغرافيا`
- current source baseline from live evidence: `104 pages / 104 image references / 0 legacy questions / 0 image download failures; manifest anomaly arrays are empty. Technical byte/SHA/MIME verification for Geography has NOT YET been run.`
- current operation: `Civics finalized from exact source evidence: 59/59 technical images and 59/59 unique exact SHA identities against master/تاسع إجتماعيات/التربية_الوطنية_تاسع; retained stored pages 6..64 map exactly to master source pages 7..65; 4 units, 14 lessons, 48 lesson pages, 4 unit covers, 7 unit reviews, 0 legacy questions. Next: technically verify Geography's 104 immutable images and establish identity/boundaries only from Geography evidence. Candidate master/تاسع إجتماعيات/جغرافيا_تاسع exists, but equivalence is NOT VERIFIED until the identity gate passes.`
- next source: `NOT YET RESOLVED — derive after كتاب الجغرافيا from live MASTER_CONTENT_MANIFEST`
- blockers: `none`
- owner decision required now: `no`
'''
text,n=re.subn(r'## 10\. ACTIVE CHECKPOINT\n.*?\n---\n',checkpoint+'\n---\n',text,count=1,flags=re.S)
if n!=1: raise SystemExit('ACTIVE CHECKPOINT block not found exactly once')
run='''
## RUN 2026-09-14T13:40:00+03:00 — Worker A

- state: COMPLETE
- start HEAD: `1d11d21d75bd73b641b1f97c677b38f4a5f26583`
- end verified work HEAD before handoff tooling/log commit: `c6497f06a2810915d39e58b249e8060932ec3932`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `7f02b242-5164-46d1-a82d-7f1023cfa8c9 — التربية الوطنية`
- completed in this run:
  - verified Worker B's History completion against the live baton, manifest and evidence, then continued exactly from التربية الوطنية;
  - confirmed Civics baseline: 59 pages/images, 0 legacy questions, no manifest anomalies;
  - required unique exact SHA identity before using the explicit master Civics reference;
  - technically verified all 59 immutable RAW images: existence/readability/size/SHA-256/MIME 59/59, contiguous stored sequence 6..64, duplicate SHA groups 0;
  - established 59/59 unique byte-identical master matches, mapping stored 6..64 exactly to source pages 7..65;
  - reconstructed 4 units / 14 lessons / 48 lesson pages / 4 unit covers / 7 unit-review pages, with every retained page classified exactly once;
  - kept master-only source pages 1..6 and 66 reference-only rather than fabricating them;
  - confirmed 0 legacy questions; no question was fabricated or linked; semantic question review `NOT APPLICABLE`;
  - updated MASTER_CONTENT_MANIFEST and canonical status/inventory/validation/import/continuation evidence; no production import/publication;
  - fail-closed probe run `34833981327` stopped before any derived commit because a status guard did not recognize baseline `review_needed`; evidence stages had passed and no semantic state was written;
  - after verifying no prior technical/reconstruction finalization existed, successful run `34834237115` passed source reconstruction, both live-HEAD conflict gates and `CIVICS_FINALIZATION_VERIFY_PASS`, producing `c6497f06a2810915d39e58b249e8060932ec3932`.
- evidence produced/verified:
  - `content-staging/reconstruction/technical/7f02b242-5164-46d1-a82d-7f1023cfa8c9.json`;
  - `content-staging/reconstruction/educational/7f02b242-5164-46d1-a82d-7f1023cfa8c9-discovery.json`;
  - `content-staging/reconstruction/educational/7f02b242-5164-46d1-a82d-7f1023cfa8c9.json`;
  - exact reference: `master/تاسع إجتماعيات/التربية_الوطنية_تاسع`;
  - successful workflow run: `34834237115`;
  - final checkpoint commit: `c6497f06a2810915d39e58b249e8060932ec3932`.
- ambiguity/review_required:
  - Civics source ambiguity requiring quarantine: 0;
  - source questions: 0; no semantic claims invented;
  - Geography identity/lesson boundaries remain `NOT VERIFIED` until its own gates pass.
- invariant result: PASS (`2,374 + 967 + 351 + 22,063 = 25,755`)
- Sources processed: 14/58
- Educational: 5/26
- Books / Units / Lessons / Lesson Pages: 5 / 29 / 133 / 508
- Exam Source Groups: 9/32
- Individual Exam Models: 135
- Exam Pages: 455/2,286
- Verified Answer Keys: 0
- Correction/report candidates: 140
- Source images technical: 1,070/5,273
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
- last completed source: `7f02b242-5164-46d1-a82d-7f1023cfa8c9 — التربية الوطنية`
- current source: `a7f1e94f-82d1-4146-af5b-4e9b51363f0b — كتاب الجغرافيا`
- current source baseline: `104 pages/images; 0 legacy questions; no manifest anomalies; technical verification NOT YET RUN.`
- exact next operation: `Re-fetch live HEAD/log; technically verify all 104 Geography RAW images and sequence/SHA/MIME; test identity against the explicit Geography reference only by exact/source evidence; reconstruct unit/lesson/review boundaries only after identity is proven; preserve any missing slice as reference-only; assert 25,755 invariant; checkpoint.`
- next source: `NOT YET RESOLVED — derive after Geography from live MASTER_CONTENT_MANIFEST`
- blockers: `none`
- handoff note: `Worker B should start with Geography from its own live evidence. Do not reopen Civics absent drift evidence and do not assume the Civics unit/title-run pattern applies to Geography.`
'''
marker='## RUN 2026-09-14T13:40:00+03:00 — Worker A'
if marker not in text:
    text=text.rstrip()+'\n\n'+run.strip()+'\n'
LOG.write_text(text,encoding='utf-8')
print('WORKER_A_CIVICS_HANDOFF_RECORDED')
