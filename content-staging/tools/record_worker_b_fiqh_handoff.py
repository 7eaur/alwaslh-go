#!/usr/bin/env python3
import json,re
from datetime import datetime,timezone,timedelta
from pathlib import Path
SID='6a8ea7f2-1e77-4654-a28c-0ea1b82b4830'; NEXT='0d4fa9fd-a93c-4d18-9dea-6dd22eb2e199'
baton=Path('content-staging/CONTENT_RECONSTRUCTION_AUTOMATION_LOG.md')
master=json.loads(Path('content-staging/manifests/MASTER_CONTENT_MANIFEST.json').read_text())
p=master['reconstruction_progress']; recon=json.loads(Path(f'content-staging/reconstruction/educational/{SID}.json').read_text())
assert recon['reconstructed_book']['lesson_count']==13 and recon['reconstructed_book']['lesson_member_page_count']==67
assert recon['questions']['structurally_lesson_linked_questions']==906
assert (p['sources_completed'],p['educational_sources_completed'],p['verified_books'],p['verified_units'],p['verified_lessons'],p['verified_lesson_pages'])==(20,10,10,33,196,877)
assert (p['source_images_technically_verified'],p['lesson_linked_structural'],p['exam_linked_to_individual_model'],p['review_required'],p['unclassified'])==(1542,6891,967,351,17546)
assert p['lesson_linked_structural']+p['exam_linked_to_individual_model']+p['review_required']+p['unclassified']==25755
assert p['raw_mutations']==p['unrelated_mutations']==p['new_imports']==p['new_publications']==0
ns=next(x for x in master['sources'] if x['id']==NEXT)
assert ns['counts']['pages']==42 and ns['counts']['images_downloaded']==42 and ns['counts']['questions']==28 and ns['counts']['image_download_failures']==0 and all(not v for v in ns['anomalies'].values())
text=baton.read_text()
checkpoint='''## 10. ACTIVE CHECKPOINT

- state: `READY_FOR_NEXT_SOURCE`
- branch: `content/corpus-inventory-20260914`
- latest verified work HEAD before this handoff commit: `dde5a8b873741eea058d91f9e0a25b9b2e8ab96f`
- last completed source: `6a8ea7f2-1e77-4654-a28c-0ea1b82b4830 — الفقه الكتاب المدرسي`
- current source: `0d4fa9fd-a93c-4d18-9dea-6dd22eb2e199 — الرياضيات نماذج وزارية 1445`
- current source baseline from live manifest: `42 pages/images, 28 legacy questions, 0 download failures; all manifest anomaly arrays are empty. Technical verification, exam-model boundaries, correction/answer-key status, and question placement remain NOT VERIFIED.`
- current operation: `Re-fetch live HEAD and baton; confirm no active/running workflow for 0d4fa9fd-a93c-4d18-9dea-6dd22eb2e199; technically verify all 42 immutable RAW images; generate complete ordered visual evidence; discover Individual Exam Model boundaries and correction/result/Answer-Key evidence only from Mathematics 1445 itself; structurally map 28 legacy questions only where page/model membership is proven; preserve uncertainty as review_required or NOT VERIFIED; reassert the 25,755 invariant.`
- next source: `Resolve from live MASTER_CONTENT_MANIFEST only after Mathematics 1445 is safely finalized.`
- blockers: `none at handoff; do not inherit any prior exam occurrence pattern into Mathematics 1445.`
- owner decision required now: `no`
'''
text,n=re.subn(r'## 10\. ACTIVE CHECKPOINT\n.*?\n---\n\n### Shared handoff rule',checkpoint+'\n---\n\n### Shared handoff rule',text,count=1,flags=re.S); assert n==1
now=datetime.now(timezone(timedelta(hours=3))).replace(microsecond=0).isoformat()
run=f'''

## RUN {now} — Worker B

- state: COMPLETE
- start HEAD: `c2852d76e355adc77496756657d5f5ad894a5469`
- end HEAD before handoff-log tooling commit: `dde5a8b873741eea058d91f9e0a25b9b2e8ab96f`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `6a8ea7f2-1e77-4654-a28c-0ea1b82b4830 — الفقه الكتاب المدرسي`
- completed in this run:
  - failed closed while Worker A's Seerah workflow was still mutating, then consumed the corrected live Seerah handoff before starting Fiqh;
  - technically verified **67/67** Fiqh RAW images and proved **67/67 exact SHA identity** with `master/التربية الاسلاميه ثالث ثانوي/كتاب الفقه/الصور`;
  - retained pages **8..74**, established **13 lessons**, and assigned **67/67** pages exactly once from explicit exact-SHA filename labels;
  - structurally mapped **906/906** legacy questions by proven page membership; semantic correctness remains `NOT VERIFIED`;
  - kept Unit hierarchy and independent review/evaluation subtype boundaries `NOT VERIFIED`; no unsupported structure was invented;
  - discovery run `34847979060` and finalization run `34848274718` completed successfully with live-HEAD safety gates;
  - updated reconstruction, MASTER, status/handoff/inventory/validation/import/continuation evidence only; no production import/publication.
- evidence produced/verified:
  - `content-staging/reconstruction/technical/{SID}.json`;
  - `content-staging/reconstruction/educational/{SID}-discovery.json`;
  - `content-staging/reconstruction/educational/{SID}.json`;
  - `fiqh-contact-sheets` artifact; evidence/status commit `dde5a8b873741eea058d91f9e0a25b9b2e8ab96f`.
- ambiguity/review_required:
  - Unit hierarchy: `NOT VERIFIED`; independent review/evaluation subtype boundaries: `NOT VERIFIED`; question semantic correctness: `NOT VERIFIED`.
- invariant result: PASS (`6,891 + 967 + 351 + 17,546 = 25,755`)
- Sources processed: 20/58
- Educational: 10/26
- Books / Units / Lessons / Lesson Pages: 10 / 33 / 196 / 877
- Exam Source Groups: 10/32
- Individual Exam Models: 166
- Exam Pages: 548/2,286
- Verified Answer Keys: 0
- Source images technical: 1,542/5,273
- WebP generated / accepted / rejected: 0 / 0 / 0
- Legacy Questions: 25,755
- Lesson-linked: 6,891
- Exam-linked: 967
- Review-required: 351
- Unclassified: 17,546
- Duplicate groups classified: 0/99
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `{SID} — الفقه الكتاب المدرسي`
- current source: `{NEXT} — الرياضيات نماذج وزارية 1445`
- exact next operation: `Verify no active Mathematics 1445 workflow; technically verify 42 images; inspect complete ordered visual evidence and discover model/correction boundaries from Mathematics 1445 only; map 28 questions only to proven model membership; preserve unsupported Answer Keys/semantics as NOT VERIFIED or review_required; assert global invariant and checkpoint.`
- next source: `NOT YET RESOLVED — derive only after Mathematics 1445 from live MASTER_CONTENT_MANIFEST`
- blockers: `none at handoff.`
- handoff note: `Worker A starts from Mathematics 1445 only after re-fetching live HEAD/baton. Do not rerun Fiqh absent fresh drift evidence; do not inherit prior exam grouping patterns.`
'''
baton.write_text(text.rstrip()+run+'\n')
print('WORKER_B_FIQH_HANDOFF_VERIFY_PASS')
