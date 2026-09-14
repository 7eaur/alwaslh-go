#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, timezone, timedelta
import json,re
ROOT=Path(__file__).resolve().parents[2]
LOG=ROOT/'content-staging/CONTENT_RECONSTRUCTION_AUTOMATION_LOG.md'
MASTER=ROOT/'content-staging/manifests/MASTER_CONTENT_MANIFEST.json'
SID='516f1c1d-acc0-4b1c-8e50-8f92a7c737e0'
START_HEAD='90e6580845197880eb0c20ee137be3484cb18259'
END_HEAD='556ffc76d0fb3d3fa632cbf0c1f678b986f8d4d7'
p=json.loads(MASTER.read_text(encoding='utf-8')); pr=p['reconstruction_progress']
i=next(i for i,x in enumerate(p['sources']) if x['id']==SID); s=p['sources'][i]
assert s['review_status']=='reconstructed_verified_exact_sha_lesson_membership'
assert pr['sources_completed']==16 and pr['educational_sources_completed']==7 and pr['verified_books']==7
assert pr['lesson_linked_structural']==3350 and pr['unclassified']==21087 and pr['source_images_technically_verified']==1239
assert pr['lesson_linked_structural']+pr['exam_linked_to_individual_model']+pr['review_required']+pr['unclassified']==25755
n=p['sources'][i+1]; nid=n['id']; nname=n['legacy_source']['name']; nc=n['counts']; na=n['anomalies']
next_baseline=f"{nc['pages']} pages/images, {nc['questions']} legacy questions, {nc['image_download_failures']} download failures; manifest anomalies: duplicate_page_numbers={len(na['duplicate_page_numbers'])}, missing_images={len(na['missing_images'])}, multiple_images={len(na['multiple_images'])}, malformed_ai_questions={len(na['malformed_ai_questions'])}. Technical verification / source identity / reconstruction remain NOT VERIFIED unless live evidence says otherwise."
text=LOG.read_text(encoding='utf-8')
checkpoint=f'''## 10. ACTIVE CHECKPOINT

- state: `READY_FOR_NEXT_SOURCE`
- branch: `content/corpus-inventory-20260914`
- latest verified work HEAD before this handoff commit: `{END_HEAD}`
- last completed source: `{SID} — الإيمان الكتاب المدرسي`
- current source: `{nid} — {nname}`
- current source baseline from live manifest: `{next_baseline}`
- current operation: `Re-fetch live HEAD and baton; confirm no active/running workflow for this source; read its immutable manifest/pages/evidence; run technical verification first; establish source identity and book/exam boundaries only from source-specific evidence; structurally map questions only where page/model membership is proven; quarantine uncertainty as review_required/NOT VERIFIED.`
- next source: `Resolve from live manifest only after the current source is safely finalized.`
- blockers: `none at handoff; the current source itself is NOT VERIFIED and must not inherit Faith structure.`
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
- source at start: `{SID} — الإيمان الكتاب المدرسي`
- completed in this run:
  - re-fetched live branch and consumed Worker B's Geography handoff from the shared baton;
  - confirmed no duplicate/active Faith finalization workflow before starting;
  - technically verified all **65/65** immutable Faith RAW images (exist/readable/byte-size/SHA-256/MIME) without RAW mutation;
  - proved **65/65 exact SHA-256 identities** against `master/التربية الاسلاميه ثالث ثانوي/كتاب الإيمان/الصور`, with zero unmatched retained pages;
  - generated complete contact-sheet visual evidence for the retained pages 8..72;
  - used only exact-SHA master filename evidence to establish **10 lesson groups** and assign **65/65 retained pages** exactly once to a lesson; no Unit layer was invented (`NOT VERIFIED`);
  - structurally linked **976/976 legacy questions** to the evidence-backed lesson containing their immutable legacy page; question semantic correctness remains `NOT VERIFIED`;
  - updated the master manifest and evidence-backed status/handoff/validation/import-report documents; no production import/publication was created;
  - passed `FAITH_RECONSTRUCTION_VERIFY_PASS` and `FAITH_FINALIZATION_VERIFY_PASS`; both live-HEAD safety gates passed immediately before finalization/write.
- evidence/artifacts:
  - `content-staging/reconstruction/technical/{SID}.json`;
  - `content-staging/reconstruction/educational/{SID}-discovery.json`;
  - `content-staging/reconstruction/educational/{SID}.json`;
  - discovery workflow run `34839217675` (success; contact-sheet artifact `faith-contact-sheets`);
  - finalization workflow run `34839580526` (success);
  - final evidence/status commit `{END_HEAD}`.
- ambiguity/review_required:
  - Faith Unit hierarchy: `NOT VERIFIED`; no unit layer was asserted;
  - lesson membership is verified from exact page identity + explicit reference filename lesson labels;
  - page subtype/review-boundary semantics beyond lesson membership: `NOT VERIFIED`;
  - semantic correctness of all 976 question texts/answers: `NOT VERIFIED`;
  - no forced semantic claims were made.
- invariant result: PASS (`3,350 + 967 + 351 + 21,087 = 25,755`)
- Sources processed: 16/58
- Educational: 7/26
- Books / Units / Lessons / Lesson Pages: 7 / {pr['verified_units']} / {pr['verified_lessons']} / {pr['verified_lesson_pages']}
- Exam Source Groups: {pr.get('exam_source_groups_completed',9)}/32
- Individual Exam Models: {pr.get('individual_exam_models',135)}
- Exam Pages: {pr.get('exam_pages_verified',455)}/2,286
- Source images technical: 1,239/5,273
- Legacy Questions: 25,755
- Lesson-linked: 3,350
- Exam-linked: 967
- Review-required: 351
- Unclassified: 21,087
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `{SID} — الإيمان الكتاب المدرسي`
- current/next source: `{nid} — {nname}`
- current source live baseline: `{next_baseline}`
- exact next operation: `Re-fetch live HEAD/baton; verify no active workflow for {nid}; read its live manifest/pages; run full technical verification; establish identity/structure from its own source-specific evidence; then link questions only where evidence proves membership and reassert the 25,755 global invariant.`
- blockers: `none at handoff.`
- handoff note: `Worker B should start from {nid} only after re-fetching live HEAD and this baton. Do not rerun/finalize Faith unless new drift evidence appears. Preserve Faith's unit hierarchy and semantic question review as NOT VERIFIED; do not upgrade those claims without new evidence.`
'''
marker='— Worker A\n\n- state: COMPLETE_SOURCE_HANDOFF\n- start HEAD: `'+START_HEAD+'`'
if marker not in text:
    text=text.rstrip()+'\n\n'+run.strip()+'\n'
LOG.write_text(text,encoding='utf-8')
print(json.dumps({'next_source_id':nid,'next_source_name':nname,'next_baseline':next_baseline,'run_timestamp':ts},ensure_ascii=False))
