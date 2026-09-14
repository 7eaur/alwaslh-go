#!/usr/bin/env python3
from pathlib import Path
import re

LOG=Path('content-staging/CONTENT_RECONSTRUCTION_AUTOMATION_LOG.md')
text=LOG.read_text(encoding='utf-8')
start='34581917c67d839d333577b0ab593df16b10b04d'
evidence_head='24489484ddf719597ceee6d021e8ca19d6c69152'
current_id='62d827b3-8ab6-4c2b-8ff2-de6156947276'
current_name='الاحياء نماذج وزارية 1446'

checkpoint=f'''## 10. ACTIVE CHECKPOINT

- state: `READY_NEXT_SOURCE`
- branch: `content/corpus-inventory-20260914`
- latest evidence HEAD before this handoff tooling: `{evidence_head}`
- last completed source: `3d91d812-ab78-476a-b2fc-dc2c31152e1a — الاحياء نماذج وزارية 1445`
- current source: `{current_id} — {current_name}`
- current source baseline from live manifest: `100 pages / 100 images / 200 legacy questions / 0 download failures; anomaly arrays empty.`
- current source verified work: `NOT STARTED; do not inherit the 1445 three-page occurrence pattern or any other exam-source structure.`
- current operation: `Re-fetch live HEAD and baton; confirm no active/running workflow for this exact source; technically verify all 100 immutable RAW images, perform source-local exam boundary discovery and complete visual inspection, resolve Individual Exam Model/correction/Answer-Key evidence without guessing, structurally map the 200 legacy questions only where verified page membership permits, assert global invariants, then checkpoint.`
- next source: `Resolve only after Biology Exams 1446 finalization from live MASTER.`
- blockers: `none`
- completed 1445 evidence: `60/60 technical; 60/60 page-aligned repository-reference binary identity; all 60 pages visually reviewed; 20 verified source-local Individual Exam Models x 3 pages; 20 correction/result-sheet candidates; 0 verified standalone Answer Keys; 0 legacy questions; no mappings invented.`
'''
pat=r'## 10\. ACTIVE CHECKPOINT\n.*?\n---\n\n### Shared handoff rule'
m=re.search(pat,text,flags=re.S)
if not m:
    raise SystemExit('ACTIVE CHECKPOINT block not found; fail closed')
text=text[:m.start()]+checkpoint+'\n---\n\n### Shared handoff rule'+text[m.end():]

run='''

## RUN 2026-09-14T22:46:15+03:00 — Worker A

- state: COMPLETE
- start HEAD: `34581917c67d839d333577b0ab593df16b10b04d`
- end HEAD before handoff-log commit: `24489484ddf719597ceee6d021e8ca19d6c69152`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `3d91d812-ab78-476a-b2fc-dc2c31152e1a — الاحياء نماذج وزارية 1445`
- completed in this run:
  - read live baton first and verified the prior Biology textbook closure against live manifests/evidence; no newer conflicting source mutation was present;
  - verified no same-source active/queued workflow before starting Biology 1445 work;
  - established a page-aligned repository reference containing the same 60 source binaries and verified immutable RAW media with 60/60 existence/readability/byte-size/SHA-256/MIME success, contiguous pages 1..60, 0 failures, and 0 within-source duplicate SHA groups;
  - generated five complete contact sheets and visually inspected all 60 pages from this source itself;
  - independently resolved twenty repeated semantic occurrences, each consisting of two question pages followed by a paired correction/result sheet; no boundary was inherited from another subject/source;
  - finalized 20 Individual Exam Models / 60 Exam Pages / 20 correction-sheet candidates; standalone official Answer Keys remain `NOT VERIFIED` and verified Answer Keys remain 0;
  - source contains 0 legacy questions, so no question mapping was invented and global question buckets remain unchanged;
  - guarded finalization reverified RAW/discovery, reconstructed the source, updated MASTER and all reconstruction/status/handoff/inventory/validation/import/continuation files, passed exact-live-HEAD gates and global invariant checks, then committed canonical evidence;
  - no production import/publication was created.
- evidence produced/verified:
  - `content-staging/reconstruction/technical/3d91d812-ab78-476a-b2fc-dc2c31152e1a.json`;
  - `content-staging/reconstruction/exams/source-groups/3d91d812-ab78-476a-b2fc-dc2c31152e1a-discovery.json`;
  - `content-staging/reconstruction/exams/source-groups/3d91d812-ab78-476a-b2fc-dc2c31152e1a.json`;
  - discovery workflow run `34888260549` success; artifact `10365571987` covers all 60 pages;
  - initial discovery run `34888105159` reached successful RAW verification/discovery but failed only in a newly written schema assertion before artifact upload; it produced no canonical evidence mutation and was corrected;
  - finalization workflow run `34888823441` passed technical verification, reconstruction, global invariant, exact-head gates, artifact upload, and canonical evidence commit;
  - canonical Biology 1445 evidence commit `24489484ddf719597ceee6d021e8ca19d6c69152`.
- ambiguity/review_required:
  - official individual model codes/titles and term remain `NOT VERIFIED` where not independently established;
  - the third page of each occurrence is retained as a correction/result-sheet candidate and is not promoted to a standalone official Answer Key;
  - source has 0 legacy questions, so semantic question correctness is `NOT VERIFIED` but no source question records require mapping.
- invariant result: PASS
- Sources processed: 29/58
- Educational: 15/26
- Books / Units / Lessons / Lesson Pages: 13 / 48 / 283 / 1,354
- Exam Source Groups: 14/32
- Individual Exam Models: 226
- Exam Pages: 728/2,286
- Verified Answer Keys: 0
- Source images technical: 2,260/5,273
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
- last completed source: `3d91d812-ab78-476a-b2fc-dc2c31152e1a — الاحياء نماذج وزارية 1445`
- current source: `62d827b3-8ab6-4c2b-8ff2-de6156947276 — الاحياء نماذج وزارية 1446`
- exact next operation: `Worker B must re-fetch live HEAD/baton, ensure no active workflow for source 62d827b3-8ab6-4c2b-8ff2-de6156947276, technically verify its 100 RAW images, perform complete source-local visual boundary discovery, classify model/correction/Answer-Key relations without inheriting Biology 1445 structure, then map its 200 legacy questions structurally only where page membership is verified and checkpoint.`
- next source: `NOT YET RESOLVED — resolve only after Biology Exams 1446 from live MASTER.`
- blockers: `none`
- handoff note: `Biology Exams 1445 is closed and must not be rerun absent new drift evidence. Biology Exams 1446 live baseline is 100 pages/images, 200 legacy questions, 0 download failures, and all anomaly arrays empty. Never assume its page/model block size from 1445.`
'''
text=text.rstrip()+run+'\n'
LOG.write_text(text,encoding='utf-8')
print('BIOLOGY_1445_AUTOMATION_HANDOFF_READY')
