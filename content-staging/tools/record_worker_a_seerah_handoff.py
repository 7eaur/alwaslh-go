#!/usr/bin/env python3
import json,re
from pathlib import Path
SID='a89c6c5d-d3d2-4aed-b98c-2ef5224cdae8'; NEXT='6a8ea7f2-1e77-4654-a28c-0ea1b82b4830'
baton=Path('content-staging/CONTENT_RECONSTRUCTION_AUTOMATION_LOG.md')
master=json.loads(Path('content-staging/manifests/MASTER_CONTENT_MANIFEST.json').read_text())
recon=json.loads(Path(f'content-staging/reconstruction/educational/{SID}.json').read_text()); p=master['reconstruction_progress']
assert recon['reconstructed_book']['lesson_count']==12 and recon['reconstructed_book']['lesson_member_page_count']==81 and recon['questions']['structurally_lesson_linked_questions']==1152
assert (p['sources_completed'],p['educational_sources_completed'],p['verified_books'],p['verified_units'],p['verified_lessons'],p['verified_lesson_pages'])==(19,9,9,33,183,810)
assert (p['source_images_technically_verified'],p['lesson_linked_structural'],p['exam_linked_to_individual_model'],p['review_required'],p['unclassified'])==(1475,5985,967,351,18452)
assert p['lesson_linked_structural']+p['exam_linked_to_individual_model']+p['review_required']+p['unclassified']==25755
ns=next(x for x in master['sources'] if x['id']==NEXT)
assert ns['counts']['pages']==67 and ns['counts']['images_downloaded']==67 and ns['counts']['questions']==906 and ns['counts']['image_download_failures']==0 and all(not v for v in ns['anomalies'].values())
text=baton.read_text()
assert 'a89c6c5d-d3d2-4aed-b98c-2ef5224cdae8' in text
checkpoint="""## 10. ACTIVE CHECKPOINT

- state: `READY_FOR_NEXT_SOURCE`
- branch: `content/corpus-inventory-20260914`
- latest verified work HEAD before this handoff commit: `3dac08e4cf470bd0846a55011518947672459c46`
- last completed source: `a89c6c5d-d3d2-4aed-b98c-2ef5224cdae8 — السيرة النبوية الكتاب`
- current source: `6a8ea7f2-1e77-4654-a28c-0ea1b82b4830 — الفقه الكتاب المدرسي`
- current source baseline from live manifest: `67 pages/images, 906 legacy questions, 0 download failures; manifest anomaly arrays are empty. Technical verification / exact identity / structure / question placement remain NOT VERIFIED until live evidence proves otherwise.`
- current operation: `Re-fetch live HEAD and baton; confirm no active/running workflow for 6a8ea7f2-1e77-4654-a28c-0ea1b82b4830; read its immutable manifest/pages/evidence; technically verify all 67 RAW images first; establish exact educational identity and lesson/unit/review boundaries only from Fiqh-specific evidence; map the 906 legacy questions only where page membership proves placement; preserve unresolved semantics/subtypes as NOT VERIFIED or review_required; reassert the 25,755 invariant.`
- next source: `Resolve from live MASTER_CONTENT_MANIFEST only after Fiqh is safely finalized.`
- blockers: `none at handoff; do not inherit Seerah lesson count, ranges, or page subtype assumptions into Fiqh.`
- owner decision required now: `no`
"""
text,n=re.subn(r'## 10\. ACTIVE CHECKPOINT\n.*?\n---\n\n### Shared handoff rule',checkpoint+'\n---\n\n### Shared handoff rule',text,count=1,flags=re.S)
assert n==1
run="""

## RUN 2026-09-14T16:09:00+03:00 — Worker A

- state: COMPLETE
- start HEAD: `ed4d73d0b95c35310a8a3794cfe811f1bb95af23`
- end HEAD before handoff-log tooling commit: `3dac08e4cf470bd0846a55011518947672459c46`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `a89c6c5d-d3d2-4aed-b98c-2ef5224cdae8 — السيرة النبوية الكتاب`
- completed in this run:
  - consumed Worker B's live Hadith handoff and confirmed no active/queued conflicting source workflow;
  - technically verified **81/81** immutable Seerah RAW images and regenerated complete contact-sheet evidence;
  - proved **81/81 exact SHA-256 identity** against `التربية الاسلاميه ثالث ثانوي/كتاب السيرة النبوية/الصور`, retained pages **8..88**, zero unmatched;
  - established **12 lessons** from exact-SHA filename lesson labels and assigned **81/81** retained pages exactly once; Unit layer remains `NOT VERIFIED`;
  - preserved subtype uncertainty: page **88** explicitly contains `التقويم والخاتمة`; other subtype/review boundaries remain `NOT VERIFIED`;
  - structurally mapped **1,152/1,152** legacy questions by proven page membership; semantic correctness remains `NOT VERIFIED`;
  - updated MASTER/content status evidence only; no production import/publication;
  - discovery run `34847083098` and finalization run `34847345410` succeeded, including `SEERAH_FINALIZATION_VERIFY_PASS` and live-HEAD safety gates.
- evidence produced/verified:
  - `content-staging/reconstruction/technical/a89c6c5d-d3d2-4aed-b98c-2ef5224cdae8.json`;
  - `content-staging/reconstruction/educational/a89c6c5d-d3d2-4aed-b98c-2ef5224cdae8-discovery.json`;
  - `content-staging/reconstruction/educational/a89c6c5d-d3d2-4aed-b98c-2ef5224cdae8.json`;
  - artifact `seerah-contact-sheets`; final evidence/status commit `3dac08e4cf470bd0846a55011518947672459c46`.
- ambiguity/review_required:
  - Unit hierarchy: `NOT VERIFIED`;
  - page 88 explicit evaluation/conclusion filename evidence; other subtype boundaries `NOT VERIFIED`;
  - semantic correctness of 1,152 questions: `NOT VERIFIED`; no question was forced into review_required because structural lesson membership is complete.
- invariant result: PASS (`5,985 + 967 + 351 + 18,452 = 25,755`)
- Sources processed: 19/58
- Educational: 9/26
- Books / Units / Lessons / Lesson Pages: 9 / 33 / 183 / 810
- Exam Source Groups: 10/32
- Individual Exam Models: 166
- Exam Pages: 548/2,286
- Verified Answer Keys: 0
- Source images technical: 1,475/5,273
- WebP generated / accepted / rejected: 0 / 0 / 0
- Legacy Questions: 25,755
- Lesson-linked: 5,985
- Exam-linked: 967
- Review-required: 351
- Unclassified: 18,452
- Duplicate groups classified: 0/99
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `a89c6c5d-d3d2-4aed-b98c-2ef5224cdae8 — السيرة النبوية الكتاب`
- current source: `6a8ea7f2-1e77-4654-a28c-0ea1b82b4830 — الفقه الكتاب المدرسي`
- exact next operation: `Re-fetch live HEAD/baton; verify no active Fiqh workflow; technically verify all 67 images; prove identity and lesson/unit/review boundaries from Fiqh evidence only; structurally map 906 questions only where page membership proves placement; preserve uncertainty as review_required/NOT VERIFIED; assert global invariant; checkpoint.`
- next source: `NOT YET RESOLVED — derive only after Fiqh from live MASTER_CONTENT_MANIFEST`
- blockers: `none at handoff.`
- handoff note: `Worker B starts only from Fiqh after re-fetching live HEAD/baton. Do not rerun Seerah absent fresh drift evidence; do not inherit Seerah's 12-lesson structure or ranges.`
"""
baton.write_text(text.rstrip()+run+'\n')
print('WORKER_A_SEERAH_HANDOFF_VERIFY_PASS')
