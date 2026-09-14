#!/usr/bin/env python3
import json, subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SID='0b28dc73-7e43-45f1-99c8-14825dcf3ded'; NEXT='bbc5c2e7-9b96-4502-a8b0-6a14d2f8782a'; EVIDENCE='bac8c301d6d66b2e159831392db4ee86b4bdc745'; START_HEAD='bfc1084d913c50292193977db28ce851444b43e9'
log=ROOT/'content-staging/CONTENT_RECONSTRUCTION_AUTOMATION_LOG.md'; master=json.loads((ROOT/'content-staging/manifests/MASTER_CONTENT_MANIFEST.json').read_text(encoding='utf-8'))
src=next(s for s in master['sources'] if s.get('id')==SID); nxt=next(s for s in master['sources'] if s.get('id')==NEXT)
if src.get('review_status')!='processed_boundary_verified_answer_keys_not_verified': raise SystemExit('Physics1446 not processed')
p=master['reconstruction_progress']; expected={'sources_completed':34,'educational_sources_completed':16,'exam_source_groups_completed':18,'individual_exam_models':325,'exam_pages_completed':1108,'source_images_technically_verified':2855,'lesson_linked_structural':13135,'exam_linked_to_individual_model':1665,'review_required':1229,'unclassified':9726,'raw_mutations':0,'unrelated_mutations':0,'new_imports':0,'new_publications':0}
for k,v in expected.items():
    if int(p.get(k) or 0)!=v: raise SystemExit(f'drift {k}: {p.get(k)} != {v}')
if sum(int(p.get(k) or 0) for k in ('lesson_linked_structural','exam_linked_to_individual_model','review_required','unclassified'))!=25755: raise SystemExit('question invariant drift')
nm=json.loads((ROOT/'content-staging/raw/legacy-supabase/subjects'/NEXT/'manifest.json').read_text(encoding='utf-8')); c=nm['counts']; a=nm['anomalies']
if (c.get('pages'),c.get('images_downloaded'),c.get('questions'),c.get('image_download_failures'))!=(124,124,255,0): raise SystemExit('next baseline drift')
if any(a.get(k) for k in ('duplicate_page_numbers','invalid_subject_ids','malformed_ai_questions','malformed_image_urls','missing_images','multiple_images','null_or_invalid_page_numbers')): raise SystemExit('next anomaly drift')
trigger=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(); name=(nxt.get('legacy_source') or {}).get('name') or nxt.get('name') or 'UNKNOWN'
active=f"""## 10. ACTIVE CHECKPOINT

- state: `READY_NEXT_SOURCE`
- branch: `content/corpus-inventory-20260914`
- latest evidence HEAD before this handoff tooling: `{EVIDENCE}`
- last completed source: `{SID} — الفيزياء نماذج وزاريه 1446`
- current source: `{NEXT} — {name}`
- current source baseline from live manifest: `124 pages / 124 images / 255 legacy questions / 0 download failures; anomaly arrays empty.`
- current source verified work: `NOT STARTED; no prior Physics packet size/boundary pattern may be inherited.`
- current operation: `Re-fetch live HEAD and baton; confirm no active workflow for this source; technically verify 124 immutable RAW images; perform source-local duplicate/boundary discovery and complete visual review; resolve occurrences/models/correction candidates/Answer-Key evidence; map 255 legacy questions only where page membership is proven; use review_required/NOT VERIFIED for uncertainty; assert invariants; checkpoint.`
- next source: `Resolve only after Physics 1447 finalization from live MASTER.`
- blockers: `none`
- completed Physics 1446 evidence: `104/104 RAW technically verified; sequence 1..104 contiguous; 6 duplicate SHA groups preserved; complete visual review proves 26 four-page occurrences (3 question + 1 correction/result candidate); 26 models / 104 exam pages / 26 correction candidates; 0 standalone Answer Keys verified; 200/200 legacy questions structurally linked; semantic correctness NOT VERIFIED; mutations/imports/publications 0.`
"""
text=log.read_text(encoding='utf-8'); marker='## 10. ACTIVE CHECKPOINT'; shared='---\n\n### Shared handoff rule'
if marker not in text or shared not in text: raise SystemExit('baton anchors missing')
text=text.split(marker,1)[0]+active+'\n---\n\n### Shared handoff rule'+text.split(shared,1)[1]
now=datetime.now(timezone(timedelta(hours=3))).isoformat(timespec='seconds')
run=f"""

## RUN {now} — Worker A

- state: `COMPLETE_SOURCE_HANDOFF`
- start HEAD: `{START_HEAD}`
- end/evidence HEAD: `{EVIDENCE}`
- handoff-trigger HEAD: `{trigger}`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `{SID} — الفيزياء نماذج وزاريه 1446`
- completed: verified 104/104 immutable RAW; generated/reviewed complete 104-page visual evidence; resolved 26 four-page occurrences with pages 1-3 question sheets and page 4 correction/result candidate per occurrence; preserved 6 partial duplicate SHA groups without merge; finalized 26 models / 104 exam pages / 26 correction candidates; standalone Answer Keys 0 / NOT VERIFIED; structurally linked 200/200 legacy questions; semantic correctness NOT VERIFIED; canonical evidence/status/MASTER files updated; no production import/publication.
- discovery run/artifact: `34904572614` / `10372551381` (`physics-exam-1446-discovery-evidence`).
- finalization run/artifact: `34905014753` / `10372671720` (`physics-exam-1446-final-evidence`).
- invariant: PASS (`13,135 + 1,665 + 1,229 + 9,726 = 25,755`).
- progress: Sources `34/58`; Educational `16/26`; Books/Units/Lessons/Lesson Pages `14/57/328/1,527`; Exam Groups `18/32`; Models `325`; Exam Pages `1,108/2,286`; Answer Keys `0`; technical images `2,855/5,273`; Legacy Questions `25,755`; Lesson-linked `13,135`; Exam-linked `1,665`; Review-required `1,229`; Unclassified `9,726`.
- invariants/mutations: RAW `0`; unrelated `0`; new imports `0`; new publications `0`.
- current/next source: `{NEXT} — {name}`.
- next source baseline: `124 pages/images; 255 legacy questions; 0 download failures; anomaly arrays empty; reconstruction NOT VERIFIED.`
- exact next operation: `Re-fetch live HEAD/baton; verify no active workflow; technically verify all 124 RAW; independently discover Physics 1447 boundaries from complete source-local evidence without inheriting 1445/1446 packet sizes; map 255 questions only where proven; quarantine uncertainty; assert invariant; checkpoint.`
- blockers: `none`.
- handoff for Worker B: `Start only from {NEXT}; do not rerun Physics 1446 absent new drift evidence and do not promote correction/result candidates to standalone Answer Keys without evidence.`
"""
log.write_text(text.rstrip()+run+'\n',encoding='utf-8')
print(json.dumps({'next_source_id':NEXT,'next_source_name':name,'trigger_head':trigger,'evidence_head':EVIDENCE},ensure_ascii=False))
