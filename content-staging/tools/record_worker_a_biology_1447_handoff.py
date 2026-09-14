#!/usr/bin/env python3
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PATH = Path('content-staging/CONTENT_RECONSTRUCTION_AUTOMATION_LOG.md')
MARKER = '<!-- WORKER_A_BIOLOGY_1447_HANDOFF_34893720640 -->'
SECTION_START = '## 10. ACTIVE CHECKPOINT'
SECTION_END = '\n---\n\n### Shared handoff rule'


def main():
    text = PATH.read_text(encoding='utf-8')
    if MARKER in text:
        print('handoff already present')
        return
    if SECTION_START not in text or SECTION_END not in text:
        raise SystemExit('baton markers not found')

    before, tail = text.split(SECTION_START, 1)
    _old_active, after = tail.split(SECTION_END, 1)
    active = '''## 10. ACTIVE CHECKPOINT

- state: `READY_NEXT_SOURCE`
- branch: `content/corpus-inventory-20260914`
- latest evidence HEAD before this handoff tooling: `05d57a4855064bd93de8b302813f03d6a37971de`
- last completed source: `3df6f57e-26cb-414e-97c5-ef6bd2ff4487 — الاحياء نماذج وزارية 1447`
- current source: `4863bbf6-6cf3-4238-9407-75825724292a — الفيزياء الكتاب المدرسي`
- current source baseline from live manifest: `207 pages / 207 images / 3,101 legacy questions / 0 download failures; anomaly arrays empty.`
- current source verified work: `NOT STARTED; do not inherit Biology exam packet structure or any earlier textbook unit/lesson boundaries.`
- current operation: `Re-fetch live HEAD and baton; confirm no active/running workflow for this exact source; technically verify all 207 immutable RAW images; establish textbook identity and reconstruct units/lessons/review or assessment boundaries only from Physics source-local evidence; preserve non-lesson pages explicitly; structurally map the 3,101 legacy questions only where verified page membership supports it; use review_required/NOT VERIFIED for insufficient evidence; assert global invariants; checkpoint.`
- next source: `Resolve only after Physics textbook finalization from live MASTER.`
- blockers: `none`
- completed Biology 1447 evidence: `124/124 technical verification; all 124 pages reviewed through 11 complete contact sheets; 31 four-page source blocks assessed; 29 verified source occurrences producing 28 unique Individual Exam Models and 116 finalized Exam Pages; 2 mismatched question/correction blocks (pages 37..40 and 45..48) preserved as review_required pages; 29 correction-sheet candidates; 0 verified standalone Answer Keys; all 50 legacy questions structurally linked because all occur on verified model pages; semantic correctness NOT VERIFIED; 9 within-source duplicate SHA groups preserved without RAW mutation or destructive normalization.`
'''

    text = before + active + SECTION_END + after
    now = datetime.now(ZoneInfo('Asia/Riyadh')).replace(microsecond=0).isoformat()
    run = f'''{MARKER}
## RUN {now} — Worker A

- state: COMPLETE
- start HEAD: `ed595a10f0280218fa12df0d00d86925a68fc44b`
- end HEAD before handoff-log commit: `05d57a4855064bd93de8b302813f03d6a37971de`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `3df6f57e-26cb-414e-97c5-ef6bd2ff4487 — الاحياء نماذج وزارية 1447`
- completed in this run:
  - re-fetched the live branch HEAD and baton before work and verified no queued/in-progress workflow was mutating this source;
  - added and ran source-local discovery run `34893245344`; verified **124/124** immutable RAW images as existing/readable with exact byte-size, SHA-256 and MIME matches, zero failures, contiguous page numbers 1..124, and zero RAW mutations;
  - generated and inspected all **11** contact sheets covering all 124 pages; discovered the four-page block topology from this Biology 1447 source itself, not by inheriting Biology 1446;
  - preserved **9** exact within-source SHA duplicate groups and resolved their relationships conservatively: P.8 repeated source occurrence retained as legitimate; duplicated question blocks paired with mismatching correction reports at pages **37..40** and **45..48** isolated as `review_required` rather than forced into a model;
  - finalized **29 verified source occurrences / 28 unique Individual Exam Models / 116 finalized Exam Pages / 8 review-required pages / 29 correction-sheet candidates**; standalone official Answer Keys remain `NOT VERIFIED`;
  - structurally linked **50/50 legacy questions** by verified page membership; source review-required question count is **0** because the 50 questions occur on verified model pages; semantic correctness remains `NOT VERIFIED`;
  - successful finalization run `34893720640` passed RAW re-verification, reconstruction validation, the 25,755-question global invariant, all exact-live-HEAD gates, final artifact upload, canonical evidence commit and push.
- evidence produced/verified:
  - technical report: `content-staging/reconstruction/technical/3df6f57e-26cb-414e-97c5-ef6bd2ff4487.json`;
  - discovery report: `content-staging/reconstruction/exams/source-groups/3df6f57e-26cb-414e-97c5-ef6bd2ff4487-discovery.json`;
  - final reconstruction: `content-staging/reconstruction/exams/source-groups/3df6f57e-26cb-414e-97c5-ef6bd2ff4487.json`;
  - discovery run `34893245344`, artifact `10368161081`;
  - finalization run `34893720640`, artifact `10367238633`;
  - canonical evidence commit: `05d57a4855064bd93de8b302813f03d6a37971de`.
- ambiguity/review_required:
  - pages `37..40`: duplicated P.61 question sheets followed by a visibly mismatching P.31 correction report — preserve and `review_required`;
  - pages `45..48`: duplicated P.28 question sheets followed by a visibly mismatching P.88 correction report — preserve and `review_required`;
  - standalone official Answer Keys: `NOT VERIFIED`; correction/result sheets remain candidates;
  - semantic correctness of legacy questions remains `NOT VERIFIED`.
- invariant result: PASS (`10,514 + 1,382 + 749 + 13,110 = 25,755`)
- Sources processed: 31/58
- Educational: 15/26
- Books / Units / Lessons / Lesson Pages: 13 / 48 / 283 / 1,354
- Exam Source Groups: 16/32
- Individual Exam Models: 279
- Exam Pages: 944/2,286
- Verified Answer Keys: 0
- Correction-sheet candidates: 285
- Source images technical: 2,484/5,273
- WebP generated / accepted / rejected: 0 / 0 / 0
- Legacy Questions: 25,755
- Lesson-linked: 10,514
- Exam-linked: 1,382
- Review-required: 749
- Unclassified: 13,110
- Duplicate groups classified: 0/99
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `3df6f57e-26cb-414e-97c5-ef6bd2ff4487 — الاحياء نماذج وزارية 1447`
- current source: `4863bbf6-6cf3-4238-9407-75825724292a — الفيزياء الكتاب المدرسي`
- exact next operation: `Re-fetch live HEAD and baton; verify no active workflow for Physics textbook; technically verify all 207 immutable RAW images; reconstruct book/unit/lesson/non-lesson boundaries only from Physics source-local evidence; structurally map 3,101 legacy questions only where verified membership supports it; keep uncertain pages/questions review_required or NOT VERIFIED; assert invariants and checkpoint.`
- next source: `Resolve only after Physics textbook finalization from live MASTER.`
- blockers: `none`
- handoff note: `Worker B should start from Physics textbook baseline 207 pages / 207 images / 3,101 legacy questions / 0 download failures with empty anomaly arrays. Do not inherit boundaries from any previous textbook or Biology exam source.`
'''
    PATH.write_text(text.rstrip() + '\n\n' + run.rstrip() + '\n', encoding='utf-8')
    print('WORKER_A_BIOLOGY_1447_HANDOFF_PREPARED')


if __name__ == '__main__':
    main()
