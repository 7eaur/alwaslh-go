#!/usr/bin/env python3
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[2]
LOG=ROOT/'content-staging/CONTENT_RECONSTRUCTION_AUTOMATION_LOG.md'
text=LOG.read_text(encoding='utf-8')
checkpoint='''## 10. ACTIVE CHECKPOINT

- state: `PARTIAL_SAFE_HANDOFF`
- branch: `content/corpus-inventory-20260914`
- latest verified work HEAD before this handoff commit: `2b9460f218a7b3d1a410abda089040b0f510f92c`
- last completed source: `da6fc228-1ada-4627-8306-80d9d3401490 — الانجليزي نماذج وزارية 1447`
- current source: `0a76f44b-0a4f-4e36-9ea9-badecf78bf23 — التاريخ الكتاب المدرسي`
- current source baseline from live evidence: `61/61 images technically verified (exist/readable/byte-size/SHA-256/MIME), stored page numbers 8..68 contiguous, 138 legacy questions; source structure/lesson identity remains NOT VERIFIED.`
- current operation: `History technical gate is complete. Trusted master references at تاسع إجتماعيات/تاريخ_تاسع_الجزء_الأول and الجزء_الثاني are NOT content-identical to this RAW: exact SHA 0/61; global visual matching across 211 master pages found 0 strong page matches and no single-part consecutive sequence. Do not use those master sections/titles for this RAW. Next: generate complete source-local visual/contact-sheet evidence directly from the 61 immutable RAW pages; inspect the actual edition's book/unit/lesson/review boundaries; classify only evidence-backed boundaries; then map the 138 questions where structurally proven and quarantine uncertainty as review_required.`
- next source: `7f02b242-5164-46d1-a82d-7f1023cfa8c9 — التربية الوطنية`
- blockers: `History master identity is NOT VERIFIED and appears to represent a different visual edition/source. Structural reconstruction and question mapping are blocked on source-local visual inspection; this is an evidence blocker, not a RAW integrity failure.`
- owner decision required now: `no`
'''
text,new_count=re.subn(r'## 10\. ACTIVE CHECKPOINT\n.*?\n---\n',checkpoint+'\n---\n',text,count=1,flags=re.S)
if new_count!=1:
    raise SystemExit('ACTIVE CHECKPOINT block not found exactly once')
run='''
## RUN 2026-09-14T12:50:00+03:00 — Worker A

- state: PARTIAL_SAFE_HANDOFF
- start HEAD: `a4f6a268e8a62d526d3187ec0f476fbedfc0cccb`
- end HEAD before handoff-log commit: `2b9460f218a7b3d1a410abda089040b0f510f92c`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `0a76f44b-0a4f-4e36-9ea9-badecf78bf23 — التاريخ الكتاب المدرسي`
- completed in this run:
  - verified Worker B's English 1447 closure and consumed the live baton;
  - read the History 61-page/138-question immutable source manifest;
  - completed non-destructive technical verification for all 61 History images: existence/readability/byte-size/SHA-256/MIME = 61/61, no missing/duplicate stored page numbers, no within-source SHA duplicate groups;
  - identified both available trusted master History references under `تاسع إجتماعيات` and tested them rather than assuming either part matched;
  - rejected exact-SHA identity safely: 0/61 RAW images are byte-identical to the 211 master History reference images;
  - rejected a page-number/filename-offset mapping after source-local evidence showed no strong perceptual matches;
  - ran global pHash+dHash+wHash ranking for every RAW page against all 211 pages across both master History parts;
  - global matching also failed closed: 0 strong page matches, best candidates do not come from one master part and do not form a consecutive sequence; therefore no master-derived unit/lesson/title mapping was accepted;
  - committed technical and diagnostic discovery evidence without mutating RAW, questions, imports or publications.
- evidence produced/verified:
  - technical report: `content-staging/reconstruction/technical/0a76f44b-0a4f-4e36-9ea9-badecf78bf23.json`;
  - diagnostic discovery: `content-staging/reconstruction/educational/0a76f44b-0a4f-4e36-9ea9-badecf78bf23-discovery.json`;
  - discovery workflow run `34828958697`: technical gate passed, exact-master identity intentionally failed closed;
  - perceptual diagnostic run `34829150813`: technical gate passed, fixed-page mapping rejected and evidence committed;
  - global visual matching run `34829503083`: technical gate passed, global comparison completed and evidence committed at `2b9460f218a7b3d1a410abda089040b0f510f92c`; identity assertion failed because evidence remained NOT VERIFIED;
  - global report: `master_reference_images_indexed=211`, `exact_master_sha_count=0`, `content_equivalence_verified_count=0`, `strong_page_count=0`, `sequence_verified=false`.
- ambiguity/review_required:
  - source identity against current master History references: `NOT VERIFIED`;
  - Book/Unit/Lesson/review boundaries: `NOT VERIFIED`;
  - 138 legacy questions remain structurally unclassified in the global baseline; semantic correctness: `NOT VERIFIED`;
  - no question was force-linked and no master title/section was copied onto this RAW.
- invariant result: PASS (`2,236 + 967 + 351 + 22,201 = 25,755`)
- Sources processed: 12/58
- Educational: 3/26
- Books / Units / Lessons / Lesson Pages: 3 / 25 / 110 / 413
- Exam Source Groups: 9/32
- Individual Exam Models: 135
- Exam Pages: 455/2,286
- Verified Answer Keys: 0
- Source images technical: 1,011/5,273
- WebP generated / accepted / rejected: 0 / 0 / 0
- Legacy Questions: 25,755
- Lesson-linked: 2,236
- Exam-linked: 967
- Review-required: 351
- Unclassified: 22,201
- Duplicate groups classified: 0/99
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `da6fc228-1ada-4627-8306-80d9d3401490 — الانجليزي نماذج وزارية 1447`
- current source: `0a76f44b-0a4f-4e36-9ea9-badecf78bf23 — التاريخ الكتاب المدرسي`
- exact next operation: `Use the verified 61 RAW pages themselves as authority: generate complete ordered contact sheets/visual evidence for stored pages 8..68; inspect cover/TOC/unit/lesson/review boundaries and source edition markers; derive a source-local reconstruction without importing master titles unless an individual page equivalence is later proven; map the 138 questions only after page-to-lesson boundaries are evidenced; quarantine ambiguous pages/items as review_required; reassert global invariant; finalize History only then.`
- next source: `7f02b242-5164-46d1-a82d-7f1023cfa8c9 — التربية الوطنية`
- blockers: `Current master History parts are not proven equivalent to the immutable RAW; source-local visual reconstruction is required before structural/question finalization.`
- handoff note: `Worker B should not retry the rejected exact-SHA or fixed-offset assumptions. Re-fetch live HEAD and this baton, confirm the three diagnostic runs/evidence, then continue History from complete RAW visual evidence. Keep History active; do not advance to التربية الوطنية until History is either evidence-finalized or only irreducible ambiguities are quarantined.`
'''
if '## RUN 2026-09-14T12:50:00+03:00 — Worker A' not in text:
    text=text.rstrip()+"\n\n"+run.strip()+"\n"
LOG.write_text(text,encoding='utf-8')
print('HISTORY_PARTIAL_HANDOFF_RECORDED')
