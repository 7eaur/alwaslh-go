#!/usr/bin/env python3
from pathlib import Path
import re

LOG=Path('content-staging/CONTENT_RECONSTRUCTION_AUTOMATION_LOG.md')
EVIDENCE_HEAD='5ae76c89cb74828c9d446f7224202ca048433300'
NEXT_ID='41e5a81c-3b93-479c-9b76-33815cae9430'
NEXT_NAME='الفيزياء نماذج وزاريه 1445'
text=LOG.read_text(encoding='utf-8')
active=f'''## 10. ACTIVE CHECKPOINT

- state: `READY_NEXT_SOURCE`
- branch: `content/corpus-inventory-20260914`
- latest evidence HEAD before this handoff tooling: `{EVIDENCE_HEAD}`
- last completed source: `4863bbf6-6cf3-4238-9407-75825724292a — الفيزياء الكتاب المدرسي`
- current source: `{NEXT_ID} — {NEXT_NAME}`
- current source baseline from live manifest: `60 pages / 60 images / 83 legacy questions / 0 download failures; anomaly arrays empty.`
- current source verified work: `NOT STARTED; do not inherit Physics textbook unit/lesson boundaries or any prior exam-source packet pattern.`
- current operation: `Re-fetch live HEAD and baton; confirm no active/running workflow for this exact source; technically verify all 60 immutable RAW images; perform source-local duplicate scan and exam-boundary discovery; visually inspect the complete source evidence; resolve source occurrences, unique Individual Exam Models, correction/report candidates and Answer-Key evidence without inheriting a previous pattern; structurally map the 83 legacy questions only where verified page membership supports it; use review_required/NOT VERIFIED when evidence is insufficient; assert global invariants; checkpoint.`
- next source: `Resolve only after Physics 1445 exam-source finalization from live MASTER.`
- blockers: `none`
- completed Physics textbook evidence: `207/207 immutable RAW images technically reverified and byte-identical by SHA-256 to the single canonical master directory الفيزياء ثالث ثانوي/كتاب الفيزياء/الصور; retained pages 9..215; exact master title runs establish 9 Units, 45 Lessons, 173 Lesson pages, 9 unit-cover pages and 25 unit-review pages; all 207 retained pages classified exactly once; 2,621/3,101 legacy questions structurally lesson-linked and 480/3,101 review_required on non-lesson pages; semantic question correctness NOT VERIFIED; no production import/publication and no RAW mutation.`

---'''
new,n=re.subn(r'## 10\. ACTIVE CHECKPOINT\n.*?\n---',active,text,count=1,flags=re.S)
if n!=1: raise SystemExit(f'ACTIVE CHECKPOINT replacement count={n}')
run='''

## RUN 2026-09-15T00:49:00+03:00 — Worker A

- state: COMPLETE
- start HEAD: `e5557a2a2659b442972af7932f9922556fbccb76`
- end HEAD before handoff-log commit: `5ae76c89cb74828c9d446f7224202ca048433300`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `4863bbf6-6cf3-4238-9407-75825724292a — الفيزياء الكتاب المدرسي`
- completed in this run:
  - re-fetched the live HEAD and shared baton and verified no queued/in-progress source workflow before work;
  - rehashed **207/207** immutable RAW images and proved **207/207 exact SHA-256 identities** against one canonical Physics master directory;
  - generated complete contact sheets and deterministic exact-master filename/title-run evidence;
  - finalized **9 Units / 45 Lessons / 173 Lesson pages / 9 unit-cover pages / 25 unit-review pages**, classifying all **207** retained pages exactly once;
  - accounted for all **3,101** source questions: **2,621** structurally lesson-linked and **480** `review_required`; semantic correctness remains `NOT VERIFIED`;
  - updated reconstruction, MASTER and corpus status evidence; production import/publication remained forbidden and untouched;
  - finalization run `34900381099` passed all exact-head, technical, reconstruction and global-invariant gates.
- evidence produced/verified:
  - `content-staging/reconstruction/technical/4863bbf6-6cf3-4238-9407-75825724292a.json`;
  - `content-staging/reconstruction/educational/4863bbf6-6cf3-4238-9407-75825724292a-discovery.json`;
  - `content-staging/reconstruction/educational/4863bbf6-6cf3-4238-9407-75825724292a-structure-summary.json`;
  - `content-staging/reconstruction/educational/4863bbf6-6cf3-4238-9407-75825724292a.json`;
  - discovery run `34899745606`; structure-summary run `34900021804`; finalization run `34900381099`;
  - canonical exact-SHA reference: `الفيزياء ثالث ثانوي/كتاب الفيزياء/الصور`;
  - evidence commit: `5ae76c89cb74828c9d446f7224202ca048433300`.
- ambiguity/review_required:
  - **480** questions remain `review_required` because their proven pages are unit covers/reviews rather than Lessons;
  - semantic correctness of legacy questions remains `NOT VERIFIED`.
- invariant result: PASS
- Sources processed: 32/58
- Educational: 16/26
- Books / Units / Lessons / Lesson Pages: 14 / 57 / 328 / 1,527
- Exam Source Groups: 16/32
- Individual Exam Models: 279
- Exam Pages: 944/2,286
- Verified Answer Keys: 0
- Source images technical: 2,691/5,273
- WebP generated / accepted / rejected: 0 / 0 / 0
- Legacy Questions: 25,755
- Lesson-linked: 13,135
- Exam-linked: 1,382
- Review-required: 1,229
- Unclassified: 10,009
- Duplicate groups classified: 0/99
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `4863bbf6-6cf3-4238-9407-75825724292a — الفيزياء الكتاب المدرسي`
- current source: `41e5a81c-3b93-479c-9b76-33815cae9430 — الفيزياء نماذج وزاريه 1445`
- exact next operation: `Re-fetch live HEAD and baton; verify no active workflow for Physics 1445; technically verify 60 immutable RAW images; discover duplicate/model boundaries and correction/Answer-Key evidence from this source alone; visually inspect all pages; structurally map 83 legacy questions only to verified model membership; quarantine ambiguity as review_required/NOT VERIFIED; assert invariants and checkpoint.`
- next source: `Resolve only after Physics 1445 finalization from live MASTER.`
- blockers: `none`
- handoff note: `Worker B starts from Physics Ministry Exams 1445 baseline 60 pages / 60 images / 83 legacy questions / 0 download failures with empty anomaly arrays. Do not inherit textbook structure or any prior subject's packet size; discover this source independently and preserve all RAW/provenance.`
'''
if '## RUN 2026-09-15T00:49:00+03:00 — Worker A' in new: raise SystemExit('duplicate run')
LOG.write_text(new.rstrip()+run+'\n',encoding='utf-8')
for fn in ['CONTENT_REBUILD_EXECUTION_STATUS.md','CONTENT_REBUILD_HANDOFF.md','CONTENT_INVENTORY.md','CONTENT_VALIDATION_REPORT.md','CONTENT_IMPORT_REPORT.md','CONTENT_REBUILD_CONTINUATION_2026-09-14.md']:
    p=Path('content-staging')/fn
    if p.exists():
        s=p.read_text(encoding='utf-8').replace(f'{NEXT_ID} — UNKNOWN',f'{NEXT_ID} — {NEXT_NAME}')
        p.write_text(s,encoding='utf-8')
print('WORKER_A_PHYSICS_HANDOFF_PREPARED')
