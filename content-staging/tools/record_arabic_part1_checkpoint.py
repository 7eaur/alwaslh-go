#!/usr/bin/env python3
import json, os
from datetime import datetime, timezone, timedelta
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SID='ab701a9e-3efb-409a-8ed1-9752d41c4771'
RECON=ROOT/'content-staging/reconstruction/educational'/f'{SID}.json'
MASTER=ROOT/'content-staging/manifests/MASTER_CONTENT_MANIFEST.json'
LOG=ROOT/'content-staging/CONTENT_RECONSTRUCTION_AUTOMATION_LOG.md'
START='<!-- ARABIC_PART1_CHECKPOINT_START -->'; END='<!-- ARABIC_PART1_CHECKPOINT_END -->'

def repl(path,body):
    text=path.read_text(encoding='utf-8'); block=f'{START}\n{body.rstrip()}\n{END}'
    if START in text and END in text:
        before=text.split(START,1)[0].rstrip(); after=text.split(END,1)[1].lstrip(); text=before+'\n\n'+block+('\n\n'+after if after.strip() else '\n')
    else: text=text.rstrip()+'\n\n'+block+'\n'
    path.write_text(text,encoding='utf-8')

r=json.loads(RECON.read_text(encoding='utf-8')); c=r['counts']
assert (c['books'],c['units'],c['semantic_instructional_lessons'],c['unique_lesson_physical_pages'],c['unit_cover_or_intro_pages'],c['assessment_pages'],c['tail_pages'])==(1,12,60,114,35,18,2)
assert c['unique_lesson_physical_pages']+c['unit_cover_or_intro_pages']+c['assessment_pages']+c['tail_pages']==169
m=json.loads(MASTER.read_text(encoding='utf-8')); s=next(x for x in m['sources'] if x['id']==SID); p=m['reconstruction_progress']
already=s.get('review_status')=='reconstructed_verified'
if not already:
    p['sources_completed']+=1; p['educational_sources_completed']+=1; p['verified_books']+=1; p['verified_units']+=12; p['verified_lessons']+=60; p['verified_lesson_pages']+=114; p['source_images_technically_verified']+=169
s['classification']='educational_book_source'
s['classification_evidence']='169/169 immutable RAW technical verification + complete visual review + exact lesson-header evidence + shared physical lesson-page policy'
s['review_status']='reconstructed_verified'
s['technical_verification']={'status':'verified','report_path':f'content-staging/reconstruction/technical/{SID}.json','images_verified':169,'readable':169,'sha256_match_manifest':169,'mime_match_manifest':169,'duplicate_sha_groups_within_source':0}
s['reconstruction']={'status':'verified','path':f'content-staging/reconstruction/educational/{SID}.json','book_title':'كتاب العربي - الجزء الأول','retained_page_range':[9,177],'retained_pages':169,'units':12,'lessons':60,'lesson_pages':114,'unit_cover_or_intro_pages':35,'assessment_pages':18,'tail_pages':2,'shared_physical_lesson_pages':r['shared_lesson_pages'],'legacy_questions':0,'semantic_question_review':'NOT APPLICABLE — 0 legacy questions','raw_mutations':0}
m['status']='RECONSTRUCTION_IN_PROGRESS_NOT_IMPORT_READY'
assert (p['sources_completed'],p['educational_sources_completed'],p['verified_books'],p['verified_units'],p['verified_lessons'],p['verified_lesson_pages'],p['source_images_technically_verified'])==(37,17,15,69,388,1641,3190)
assert p['lesson_linked_structural']+p['exam_linked_to_individual_model']+p['review_required']+p['unclassified']==25755
assert all(p[k]==0 for k in ('raw_mutations','unrelated_mutations','new_imports','new_publications'))
MASTER.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def done(x):
    rs=str(x.get('review_status','')).lower(); rec=(x.get('reconstruction') or {}).get('status'); er=(x.get('exam_reconstruction') or {}).get('status','')
    return rec=='verified' or 'verified_empty' in rs or 'reconstructed_verified' in rs or str(er).startswith('processed_')
sources=m['sources']; idx=next(i for i,x in enumerate(sources) if x['id']==SID); n=next((x for x in sources[idx+1:]+sources[:idx] if not done(x)),None)
nid=n['id'] if n else 'NONE'; nn=((n.get('legacy_source') or {}).get('name') or n.get('name') or 'UNKNOWN') if n else 'NONE'
body=f'''## Reconstruction checkpoint — Arabic book part 1

- Sources processed: **{p['sources_completed']}/{p['sources_total']}**; Educational: **{p['educational_sources_completed']}/{p['educational_sources_total']}**; Exam groups: **{p['exam_source_groups_completed']}/{p['exam_source_groups_total']}**.
- Books / Units / Lessons / unique physical Lesson pages: **{p['verified_books']} / {p['verified_units']} / {p['verified_lessons']} / {p['verified_lesson_pages']}**.
- Arabic Part 1: **169/169** technical; **12 Units / 60 semantic Lessons / 114 unique physical lesson pages / 35 intro-cover / 18 assessment / 2 tail**.
- Shared physical lesson pages are preserved semantically without double-counting: **{len(r['shared_lesson_pages'])}**.
- Questions unchanged: **{p['lesson_linked_structural']} + {p['exam_linked_to_individual_model']} + {p['review_required']} + {p['unclassified']} = 25,755**.
- Technical images: **{p['source_images_technically_verified']}/{p['source_images_total']}**. RAW/unrelated/import/publication mutations **0/0/0/0**.
- Last completed: `{SID} — كتاب العربي - الجزء الأول`. Next: `{nid} — {nn}`.
'''
for f in ['CONTENT_REBUILD_EXECUTION_STATUS.md','CONTENT_REBUILD_HANDOFF.md','CONTENT_INVENTORY.md','CONTENT_VALIDATION_REPORT.md','CONTENT_IMPORT_REPORT.md','CONTENT_REBUILD_CONTINUATION_2026-09-14.md']:
    path=ROOT/'content-staging'/f
    if path.exists(): repl(path,body)

# Append this run and replace ACTIVE CHECKPOINT atomically in the checked-out live tree.
log=LOG.read_text(encoding='utf-8'); marker='\n## ACTIVE CHECKPOINT\n'
if marker in log: history=log.rsplit(marker,1)[0].rstrip()
else: history=log.rstrip()
start_head=os.environ.get('START_HEAD','NOT VERIFIED'); now=datetime.now(timezone(timedelta(hours=3))).isoformat(timespec='seconds')
run=f'''## RUN {now} — Worker A

- state: COMPLETE_SOURCE_HANDOFF
- start HEAD: `{start_head}`
- end HEAD before handoff-log commit: `WORKFLOW_COMMIT_PENDING`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `{SID} — كتاب العربي - الجزء الأول`
- completed in this run: applied the already validated evidence-backed Arabic Part 1 reconstruction to live MASTER/status; finalized 1 Book / 12 Units / 60 semantic Lessons / 114 unique physical Lesson pages; preserved 11 shared physical lesson pages without double-counting; updated aggregate evidence documents; resolved next source from live MASTER.
- evidence/artifacts: `{RECON.relative_to(ROOT)}`; canonical checkpoint evidence already validated on live branch; shared-page policy `{Path('content-staging/reconstruction/SHARED_PHYSICAL_LESSON_PAGE_POLICY.json')}`.
- ambiguity/review_required: exact bibliographic edition transcription remains `NOT VERIFIED`; question mapping `NOT APPLICABLE — 0 legacy questions`.
- invariant result: PASS (`{p['lesson_linked_structural']} + {p['exam_linked_to_individual_model']} + {p['review_required']} + {p['unclassified']} = 25,755`)
- Sources processed: {p['sources_completed']}/{p['sources_total']}; Educational: {p['educational_sources_completed']}/{p['educational_sources_total']}; Books / Units / Lessons / Lesson Pages: {p['verified_books']} / {p['verified_units']} / {p['verified_lessons']} / {p['verified_lesson_pages']}; Exam Source Groups: {p['exam_source_groups_completed']}/{p['exam_source_groups_total']}; Individual Exam Models: {p['individual_exam_models']}; Exam Pages: {p['exam_pages_completed']}/{p['exam_pages_total']}; Source images technical: {p['source_images_technically_verified']}/{p['source_images_total']}.
- invariants: RAW mutations 0; unrelated mutations 0; new imports 0; new publications 0.
- current/next source: `{nid} — {nn}`
- exact next operation: `Re-fetch live HEAD/baton; verify no active workflow for {nid}; read its live manifest/pages; execute source-local technical verification and reconstruction/boundary discovery without inheriting Arabic Part 1 structure; quarantine insufficient evidence as NOT VERIFIED/review_required; assert invariants; checkpoint.`
- blockers: none at handoff.
- handoff note: `Worker B must not rerun/finalize Arabic Part 1 absent drift evidence. Start {nid} from its own source evidence.`
'''
active=f'''## ACTIVE CHECKPOINT

- state: `COMPLETE_SOURCE_HANDOFF`
- branch: `content/corpus-inventory-20260914`
- latest validated source: `{SID} — كتاب العربي - الجزء الأول`
- progress: `{p['sources_completed']}/{p['sources_total']} sources; {p['educational_sources_completed']}/{p['educational_sources_total']} educational; {p['exam_source_groups_completed']}/{p['exam_source_groups_total']} exam groups; {p['verified_books']} books; {p['verified_units']} units; {p['verified_lessons']} lessons; {p['verified_lesson_pages']} unique physical lesson pages; {p['source_images_technically_verified']}/{p['source_images_total']} technical images.`
- invariant: `{p['lesson_linked_structural']} + {p['exam_linked_to_individual_model']} + {p['review_required']} + {p['unclassified']} = 25,755`; RAW/unrelated/import/publication mutations `0/0/0/0`.
- current source: `{nid} — {nn}`
- current operation: `Begin source-local verification/reconstruction for {nid}; do not inherit prior-source boundaries.`
- next source: `Resolve only after {nid} finalization from live MASTER.`
- blockers: `none known; source identity/structure remain NOT VERIFIED until its own evidence gates pass.`
'''
LOG.write_text(history+'\n\n'+run+'\n'+active,encoding='utf-8')
print(json.dumps({'already':already,'next_source_id':nid,'next_source_name':nn,'progress':p},ensure_ascii=False))
