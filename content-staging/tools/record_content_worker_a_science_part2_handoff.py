#!/usr/bin/env python3
import json,re
from datetime import datetime,timezone,timedelta
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sid='81e99fe6-1421-462b-9562-1c0c5053a809'
log=ROOT/'content-staging/CONTENT_RECONSTRUCTION_AUTOMATION_LOG.md'
r=json.loads((ROOT/f'content-staging/reconstruction/educational/{sid}.json').read_text(encoding='utf-8'))
m=json.loads((ROOT/'content-staging/manifests/MASTER_CONTENT_MANIFEST.json').read_text(encoding='utf-8'))
p=m['reconstruction_progress']
assert r['status']=='reconstructed_verified'
assert r['source_identity']['raw_master_exact_sha_matches']==145
assert r['reconstructed_book']['unit_count']==8
assert r['reconstructed_book']['lesson_count']==31
assert r['reconstructed_book']['lesson_page_count']==126
assert r['reconstructed_book']['unit_cover_page_count']==8
assert r['reconstructed_book']['unit_review_page_count']==11
assert r['questions']['legacy_questions']==0
assert p['sources_completed']==9 and p['educational_sources_completed']==3
assert p['verified_books']==3 and p['verified_units']==25 and p['verified_lessons']==110 and p['verified_lesson_pages']==413
assert p['source_images_technically_verified']==839
assert p['lesson_linked_structural']+p['exam_linked_to_individual_model']+p['review_required']+p['unclassified']==25755
assert p['raw_mutations']==0 and p['unrelated_mutations']==0 and p['new_imports']==0 and p['new_publications']==0
text=log.read_text(encoding='utf-8')
checkpoint='''## 10. ACTIVE CHECKPOINT

- state: `READY`
- branch: `content/corpus-inventory-20260914`
- latest verified work HEAD before this handoff commit: `30cca9916e801a1d1e8085b71bf6f3fbb8e9d41c`
- last completed source: `81e99fe6-1421-462b-9562-1c0c5053a809 — كتاب العلوم - الجزء الثاني`
- current source: `8489a487-91d9-47fb-80b8-35d0e7a074a4 — الانجليزي نماذج وزارية 1445`
- current source baseline from live manifest: `30 images/pages; 0 legacy questions; manifest anomaly arrays empty`
- current operation: `read live manifest/pages -> technically verify all 30 images -> scan source-local duplicate SHA/sequence -> generate full visual evidence -> resolve Individual Exam Model and correction/answer-key boundaries only from English 1445 evidence -> preserve NOT VERIFIED where evidence is insufficient -> assert global invariant -> checkpoint`
- next source: `NOT YET RESOLVED — derive only after English 1445 from live MASTER_CONTENT_MANIFEST`
- blockers: `none`
- owner decision required now: `no`
---

### Shared handoff rule'''
pattern=r'## 10\. ACTIVE CHECKPOINT\n.*?\n---\n\n### Shared handoff rule'
if not re.search(pattern,text,re.S): raise SystemExit('ACTIVE CHECKPOINT block not found')
text=re.sub(pattern,checkpoint,text,count=1,flags=re.S)
if 'source at start: `81e99fe6-1421-462b-9562-1c0c5053a809 — كتاب العلوم - الجزء الثاني`' not in text.split('## RUN')[-1]:
 ts=datetime.now(timezone(timedelta(hours=3))).isoformat(timespec='seconds')
 run=f'''\n\n## RUN {ts} — Worker A

- state: COMPLETE
- start HEAD: `5f6f0450e6c9c19a38579950e0e80cf34e690be2`
- end HEAD before handoff-log commit: `30cca9916e801a1d1e8085b71bf6f3fbb8e9d41c`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `81e99fe6-1421-462b-9562-1c0c5053a809 — كتاب العلوم - الجزء الثاني`
- completed in this run:
  - verified Worker B's Science Part 1 finalization against the live branch and shared handoff;
  - completed 145/145 non-destructive technical verification for Science Part 2;
  - established exact source identity against `master/تاسع علوم/علوم_تاسع_الجزء_الثاني`: 145/145 retained RAW images are exact SHA-256 matches;
  - proved retained stored pages 7..151 correspond to master source pages 8..152; master-only pages 1..7 and 153..154 remain reference-only;
  - reconstructed units 9..16 as 8 Units, 31 Lessons, 126 Lesson pages, 8 Unit-cover pages and 11 Unit-review pages from exact master section/title runs;
  - classified every retained page exactly once and finalized the educational reconstruction;
  - confirmed the source contains 0 legacy questions and fabricated no question links;
  - updated MASTER_CONTENT_MANIFEST and canonical execution/handoff/inventory/validation/import/continuation reports;
  - exact-head finalization workflow completed successfully with all final invariant steps green.
- evidence produced/verified:
  - technical report: `content-staging/reconstruction/technical/81e99fe6-1421-462b-9562-1c0c5053a809.json`;
  - identity/structure discovery: `content-staging/reconstruction/educational/81e99fe6-1421-462b-9562-1c0c5053a809-discovery.json`;
  - final reconstruction: `content-staging/reconstruction/educational/81e99fe6-1421-462b-9562-1c0c5053a809.json`;
  - discovery workflow run `34818641697`: success;
  - finalization workflow run `34818819467`: success including `SCIENCE_BOOK_PART2_FINALIZATION_VERIFY_PASS`;
  - master reference: `تاسع علوم/علوم_تاسع_الجزء_الثاني`;
  - within-source duplicate SHA groups: 0.
- ambiguity/review_required:
  - no retained structural page remains ambiguous after exact identity/title-run reconstruction;
  - source question review-required count: 0 because the source contains 0 questions;
  - master-only pages outside the retained slice were not fabricated.
- invariant result: PASS (`2,236 + 733 + 351 + 22,435 = 25,755`)
- Sources processed: 9/58
- Educational: 3/26
- Books / Units / Lessons / Lesson Pages: 3 / 25 / 110 / 413
- Exam Source Groups: 6/32
- Individual Exam Models: 99
- Exam Pages: 347/2,286
- Verified Answer Keys: 0
- Source images technical: 839/5,273
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
- last completed source: `81e99fe6-1421-462b-9562-1c0c5053a809 — كتاب العلوم - الجزء الثاني`
- current source: `8489a487-91d9-47fb-80b8-35d0e7a074a4 — الانجليزي نماذج وزارية 1445`
- exact next operation: `Fetch English 1445 live manifest/pages; technically verify all 30 images; scan source-local duplicate SHA/sequence; generate complete visual evidence; resolve exam-model and correction/answer-key boundaries only from English 1445 evidence; map its 0 current legacy questions without fabrication; assert the 25,755 invariant; checkpoint and continue.`
- next source: `NOT YET RESOLVED — derive after English 1445 from live MASTER_CONTENT_MANIFEST`
- blockers: `none`
- handoff note: `Worker B must re-fetch live HEAD and this baton, confirm Science Part 2 finalization is complete, then start English Ministry Exams 1445 from its own evidence. Do not inherit Science or Chemistry page/model patterns.`
'''
 text=text.rstrip()+run+'\n'
log.write_text(text,encoding='utf-8')
print('CONTENT_WORKER_A_SCIENCE_PART2_HANDOFF_PASS')
