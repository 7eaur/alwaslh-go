#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime,timezone,timedelta
import json,re
ROOT=Path(__file__).resolve().parents[2]
LOG=ROOT/'content-staging/CONTENT_RECONSTRUCTION_AUTOMATION_LOG.md'
MASTER=ROOT/'content-staging/manifests/MASTER_CONTENT_MANIFEST.json'
SID='f25891fe-ea52-481b-baf2-ff4764c79bde'
START_HEAD='405c424792ff31dd66311328213dd23d10dc673e'
END_HEAD='f404c5749fc3f96c27ed163ebdec095723df6711'
p=json.loads(MASTER.read_text(encoding='utf-8')); pr=p['reconstruction_progress']
i=next(i for i,x in enumerate(p['sources']) if x['id']==SID); s=p['sources'][i]
assert s['review_status']=='processed_boundary_verified_duplicates_preserved_answer_keys_not_verified'
assert pr['sources_completed']==17 and pr['educational_sources_completed']==7 and pr['exam_source_groups_completed']==10
assert pr['individual_exam_models']==166 and pr['exam_pages_completed']==548 and pr['source_images_technically_verified']==1332
assert pr['lesson_linked_structural']==3350 and pr['exam_linked_to_individual_model']==967 and pr['review_required']==351 and pr['unclassified']==21087
assert sum(pr[k] for k in ('lesson_linked_structural','exam_linked_to_individual_model','review_required','unclassified'))==25755
n=p['sources'][i+1]; nid=n['id']; nname=n['legacy_source']['name']; nc=n['counts']; na=n['anomalies']
next_baseline=f"{nc['pages']} pages/images, {nc['questions']} legacy questions, {nc['image_download_failures']} download failures; manifest anomalies: duplicate_page_numbers={len(na['duplicate_page_numbers'])}, missing_images={len(na['missing_images'])}, multiple_images={len(na['multiple_images'])}, malformed_ai_questions={len(na['malformed_ai_questions'])}. Technical verification / source identity / reconstruction remain NOT VERIFIED unless live evidence says otherwise."
text=LOG.read_text(encoding='utf-8')
checkpoint=f'''## 10. ACTIVE CHECKPOINT

- state: `READY_FOR_NEXT_SOURCE`
- branch: `content/corpus-inventory-20260914`
- latest verified work HEAD before this handoff commit: `{END_HEAD}`
- last completed source: `{SID} — الاسلاميه ثانوي نماذج وزاريه 1447`
- current source: `{nid} — {nname}`
- current source baseline from live manifest: `{next_baseline}`
- current operation: `Re-fetch live HEAD and baton; confirm no active/running workflow for this source; technically verify immutable media first; establish educational identity/structure only from source-specific evidence; structurally map its 1,483 legacy questions only where page membership proves placement; quarantine uncertainty as review_required/NOT VERIFIED; reassert the 25,755 invariant.`
- next source: `Resolve from live manifest only after the current source is safely finalized.`
- blockers: `none at handoff; do not inherit Islamic-exam three-page boundaries into the educational source.`
- owner decision required now: `no`
'''
text,count=re.subn(r'## 10\. ACTIVE CHECKPOINT\n.*?\n---\n',checkpoint+'\n---\n',text,count=1,flags=re.S)
if count!=1: raise SystemExit('ACTIVE CHECKPOINT block not found exactly once')
ts=datetime.now(timezone(timedelta(hours=3))).replace(microsecond=0).isoformat()
run=f'''## RUN {ts} — Worker A

- state: COMPLETE_SOURCE_HANDOFF
- start HEAD: `{START_HEAD}`
- end HEAD before handoff-log commit: `{END_HEAD}`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `{SID} — الاسلاميه ثانوي نماذج وزاريه 1447`
- completed in this run:
  - re-fetched live branch/baton and verified the preceding Geography/Faith state rather than redoing completed work;
  - confirmed no active/queued workflow for this source before starting;
  - technically verified **93/93** immutable RAW images (exist/readable/byte-size/SHA-256/MIME), sequence **1..93** contiguous;
  - generated and visually reviewed complete contact-sheet evidence for all **93** pages;
  - established **31** source-local three-page exam occurrences, each two question pages followed by one correction/result page, covering all 93 pages exactly once;
  - preserved **6 exact-SHA duplicate groups** as provenance occurrences and did not merge or mutate RAW;
  - finalized **31 Individual Exam Models / 93 Exam Pages**, **31 correction/result candidates**, **0 review-required pages**, and **0 verified standalone Answer Keys**; official model-code transcription remains `NOT VERIFIED`;
  - source has **0 legacy questions**, so no question records were fabricated or mapped;
  - updated master manifest plus evidence-backed status/handoff/validation/import-report documents; no production import/publication was created;
  - discovery run `34840720032` and finalization run `34841162130` succeeded; both live-HEAD safety gates and global invariants passed.
- evidence/artifacts:
  - `content-staging/reconstruction/technical/{SID}.json`;
  - `content-staging/reconstruction/exams/source-groups/{SID}-discovery.json`;
  - `content-staging/reconstruction/exams/source-groups/{SID}.json`;
  - discovery workflow run `34840720032` (artifact `islamic-exam-1447-discovery-evidence`);
  - finalization workflow run `34841162130` (success);
  - final evidence/status commit `{END_HEAD}`.
- ambiguity/review_required:
  - standalone official Answer Keys: `NOT VERIFIED`;
  - official model codes/titles/term transcription: `NOT VERIFIED`;
  - exact-SHA duplicate question pages are preserved as distinct source occurrences inside visually complete exam blocks, not silently deduplicated;
  - source legacy-question semantics: `NOT APPLICABLE — 0 legacy questions`.
- invariant result: PASS (`3,350 + 967 + 351 + 21,087 = 25,755`)
- Sources processed: 17/58
- Educational: 7/26
- Books / Units / Lessons / Lesson Pages: 7 / 33 / 161 / 667
- Exam Source Groups: 10/32
- Individual Exam Models: 166
- Exam Pages: 548/2,286
- Source images technical: 1,332/5,273
- Legacy Questions: 25,755
- Lesson-linked: 3,350
- Exam-linked: 967
- Review-required: 351
- Unclassified: 21,087
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `{SID} — الاسلاميه ثانوي نماذج وزاريه 1447`
- current/next source: `{nid} — {nname}`
- current source live baseline: `{next_baseline}`
- exact next operation: `Re-fetch live HEAD/baton; verify no active workflow for {nid}; technically verify all 62 images; prove source identity/lesson or unit boundaries from its own evidence; map 1,483 questions only where page membership is proven; preserve uncertainty as review_required/NOT VERIFIED; assert the global invariant; checkpoint.`
- blockers: `none at handoff.`
- handoff note: `Worker B should start only from {nid} after re-fetching live HEAD and this baton. Do not rerun Islamic 1447 absent new drift evidence, and do not treat the six duplicate SHA groups as permission to delete or merge provenance.`
'''
marker='— Worker A\n\n- state: COMPLETE_SOURCE_HANDOFF\n- start HEAD: `'+START_HEAD+'`'
if marker not in text: text=text.rstrip()+'\n\n'+run.strip()+'\n'
LOG.write_text(text,encoding='utf-8')
print(json.dumps({'next_source_id':nid,'next_source_name':nname,'next_baseline':next_baseline,'run_timestamp':ts},ensure_ascii=False))
