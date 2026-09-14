#!/usr/bin/env python3
import json, subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
LOG=ROOT/'content-staging/CONTENT_RECONSTRUCTION_AUTOMATION_LOG.md'
MASTER=ROOT/'content-staging/manifests/MASTER_CONTENT_MANIFEST.json'
SID='41e5a81c-3b93-479c-9b76-33815cae9430'
NEXT='0b28dc73-7e43-45f1-99c8-14825dcf3ded'
START_HEAD='6ee295cad286e397a428335663e9b1d0a1a0410f'
EVIDENCE_HEAD='26c703fe11d4e9de9381b6cbf48bed5c8ec995ed'

m=json.loads(MASTER.read_text(encoding='utf-8'))
p=m['reconstruction_progress']
sources=m['sources']
src=next(s for s in sources if s.get('id')==SID)
nxt=next(s for s in sources if s.get('id')==NEXT)
if src.get('review_status')!='processed_boundary_verified_answer_keys_not_verified':
    raise SystemExit('Physics 1445 is not canonically processed')
expected={'sources_completed':33,'educational_sources_completed':16,'exam_source_groups_completed':17,'individual_exam_models':299,'exam_pages_completed':1004,'source_images_technically_verified':2751,'lesson_linked_structural':13135,'exam_linked_to_individual_model':1465,'review_required':1229,'unclassified':9926,'raw_mutations':0,'unrelated_mutations':0,'new_imports':0,'new_publications':0}
for k,v in expected.items():
    if int(p.get(k) or 0)!=v: raise SystemExit(f'progress drift {k}: {p.get(k)} != {v}')
if sum(int(p.get(k) or 0) for k in ('lesson_linked_structural','exam_linked_to_individual_model','review_required','unclassified'))!=25755:
    raise SystemExit('global invariant drift')
nm=json.loads((ROOT/'content-staging/raw/legacy-supabase/subjects'/NEXT/'manifest.json').read_text(encoding='utf-8'))
c=nm['counts']; a=nm['anomalies']
if (c.get('pages'),c.get('images_downloaded'),c.get('questions'),c.get('image_download_failures'))!=(104,104,200,0):
    raise SystemExit('next-source baseline drift')
if any(a.get(k) for k in ('duplicate_page_numbers','invalid_subject_ids','malformed_ai_questions','malformed_image_urls','missing_images','multiple_images','null_or_invalid_page_numbers')):
    raise SystemExit('next-source anomalies drift')
next_name=(nxt.get('legacy_source') or {}).get('name') or nxt.get('name') or 'UNKNOWN'
trigger_head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
active=f'''## 10. ACTIVE CHECKPOINT

- state: `READY_NEXT_SOURCE`
- branch: `content/corpus-inventory-20260914`
- latest evidence HEAD before this handoff tooling: `{EVIDENCE_HEAD}`
- last completed source: `{SID} — الفيزياء نماذج وزاريه 1445`
- current source: `{NEXT} — {next_name}`
- current source baseline from live manifest: `104 pages / 104 images / 200 legacy questions / 0 download failures; anomaly arrays empty.`
- current source verified work: `NOT STARTED; do not inherit the Physics 1445 three-page packet or any prior exam-source pattern.`
- current operation: `Re-fetch live HEAD and baton; confirm no active/running workflow for this exact source; technically verify all 104 immutable RAW images; perform source-local duplicate scan and exam-boundary discovery; visually inspect complete source evidence; resolve source occurrences, unique Individual Exam Models, correction/report candidates and Answer-Key evidence without inheriting the 1445 pattern; structurally map the 200 legacy questions only where verified page membership supports it; use review_required/NOT VERIFIED where evidence is insufficient; assert global invariants; checkpoint.`
- next source: `Resolve only after Physics 1446 exam-source finalization from live MASTER.`
- blockers: `none`
- completed Physics 1445 evidence: `60/60 immutable RAW technically verified; page sequence 1..60 contiguous; duplicate SHA groups 0; complete source-local visual review proves 20 three-page occurrences (two question pages + one correction/result candidate); 20 Individual Exam Models / 60 Exam Pages; 20 correction candidates; 0 standalone verified Answer Keys; 83/83 legacy questions structurally linked; semantic correctness NOT VERIFIED; RAW/unrelated/import/publication mutations 0/0/0/0.`
'''
text=LOG.read_text(encoding='utf-8')
marker='## 10. ACTIVE CHECKPOINT'
shared='---\n\n### Shared handoff rule'
if marker not in text or shared not in text: raise SystemExit('baton anchors missing')
before=text.split(marker,1)[0]
after=text.split(shared,1)[1]
text=before+active+'\n---\n\n### Shared handoff rule'+after
now=datetime.now(timezone(timedelta(hours=3))).isoformat(timespec='seconds')
run=f'''\n\n## RUN {now} — Worker A

- state: COMPLETE
- start HEAD: `{START_HEAD}`
- end HEAD before handoff-log commit: `{EVIDENCE_HEAD}`
- handoff tooling HEAD: `{trigger_head}`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `{SID} — الفيزياء نماذج وزاريه 1445`
- completed in this run:
  - consumed and verified the live baton and Physics-textbook checkpoint before touching this source;
  - confirmed no active/running same-source workflow at startup;
  - technically verified **60/60** immutable RAW images with byte-size/SHA-256/MIME/readability agreement, contiguous pages **1..60**, **0** failures, **0** duplicate SHA groups and **0** RAW mutations;
  - generated and visually inspected complete contact sheets covering all **60** source pages;
  - independently discovered **20** source-local three-page occurrences, each two question pages followed by one correction/result-sheet candidate; all pages finalized exactly once;
  - finalized **20 Individual Exam Models / 60 Exam Pages / 20 correction candidates / 0 review-required pages / 0 verified standalone Answer Keys**;
  - structurally linked **83/83 legacy questions** by verified model-page membership; semantic question/answer correctness remains `NOT VERIFIED`;
  - updated canonical reconstruction, MASTER and evidence-backed status/handoff/inventory/validation/import/continuation files; no production import/publication;
  - finalization run `34901788759` passed re-verification, reconstruction, global invariant and both exact-live-HEAD gates.
- evidence produced/verified:
  - `content-staging/reconstruction/technical/{SID}.json`;
  - `content-staging/reconstruction/exams/source-groups/{SID}-discovery.json`;
  - `content-staging/reconstruction/exams/source-groups/{SID}.json`;
  - discovery run `34901457816`, artifact id `10371445766`;
  - finalization run `34901788759`; canonical evidence commit `{EVIDENCE_HEAD}`.
- ambiguity/review_required:
  - source model boundaries: none after complete source-local visual review;
  - standalone official Answer Keys, official model codes/titles/term and semantic correctness: `NOT VERIFIED`.
- invariant result: PASS (`13,135 + 1,465 + 1,229 + 9,926 = 25,755`)
- Sources processed: 33/58
- Educational: 16/26
- Books / Units / Lessons / Lesson Pages: 14 / 57 / 328 / 1,527
- Exam Source Groups: 17/32
- Individual Exam Models: 299
- Exam Pages: 1,004/2,286
- Verified Answer Keys: 0
- Source images technical: 2,751/5,273
- WebP generated / accepted / rejected: 0 / 0 / 0
- Legacy Questions: 25,755
- Lesson-linked: 13,135
- Exam-linked: 1,465
- Review-required: 1,229
- Unclassified: 9,926
- Duplicate groups classified: 0/99
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `{SID} — الفيزياء نماذج وزاريه 1445`
- current source: `{NEXT} — {next_name}`
- exact next operation: `Re-fetch live HEAD/baton; verify no active workflow for {NEXT}; technically verify 104 immutable RAW images; independently discover Physics 1446 duplicate/model/correction boundaries from complete source-local visual evidence; do not inherit Physics 1445's three-page packet; structurally map 200 legacy questions only where membership is proven; quarantine uncertainty as review_required/NOT VERIFIED; assert invariant; checkpoint.`
- next source: `NOT YET RESOLVED — derive only after Physics 1446 finalization from live MASTER_CONTENT_MANIFEST`
- blockers: `none`
- handoff note: `Worker B starts only from {NEXT} after re-fetching live HEAD and baton. Physics 1445 is closed absent new drift evidence; do not upgrade correction/result candidates to official standalone Answer Keys without explicit evidence.`
'''
LOG.write_text(text.rstrip()+run+'\n',encoding='utf-8')
print(json.dumps({'next_source_id':NEXT,'next_source_name':next_name,'evidence_head':EVIDENCE_HEAD,'trigger_head':trigger_head},ensure_ascii=False))
