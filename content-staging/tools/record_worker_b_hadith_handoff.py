#!/usr/bin/env python3
import json, os, re
from pathlib import Path

START_HEAD='1879f3fff54861d146d4eb8912f6ccaa81eee0f7'
VERIFIED_WORK_HEAD='feea37c84718e752372a95fed8140c0e3556bb3a'
DISCOVERY_RUN='34841797706'
FINALIZATION_RUN='34842156912'
SID='cae82d8f-64f9-4d2a-984f-6e6fd19fac5c'
SOURCE_NAME='الحديث والتهذيب الكتاب'

baton=Path('content-staging/CONTENT_RECONSTRUCTION_AUTOMATION_LOG.md')
manifest=Path('content-staging/manifests/MASTER_CONTENT_MANIFEST.json')
p=json.loads(manifest.read_text())
prog=p['reconstruction_progress']; sources=p['sources']
i=next(i for i,s in enumerate(sources) if s['id']==SID)
nxt=sources[i+1] if i+1<len(sources) else None
if nxt:
    next_id=nxt['id']; next_name=nxt.get('legacy_source',{}).get('name') or nxt.get('name') or 'NOT VERIFIED'
    legacy=nxt.get('legacy_source',{}); counts=legacy.get('counts') or nxt.get('counts') or {}
    img_count=counts.get('images',counts.get('pages','NOT VERIFIED')); q_count=counts.get('questions','NOT VERIFIED')
    baseline=f'{img_count} pages/images, {q_count} legacy questions; technical verification / exact identity / structure remain NOT VERIFIED until live evidence proves otherwise.'
else:
    next_id='NOT YET RESOLVED'; next_name='NOT YET RESOLVED'; baseline='NOT VERIFIED'
required={'sources_completed':18,'educational_sources_completed':8,'verified_books':8,'verified_lessons':171,'verified_lesson_pages':729,'source_images_technically_verified':1394,'lesson_linked_structural':4833,'exam_linked_to_individual_model':967,'review_required':351,'unclassified':19604}
for k,v in required.items(): assert prog.get(k)==v,(k,prog.get(k),v)
assert prog['lesson_linked_structural']+prog['exam_linked_to_individual_model']+prog['review_required']+prog['unclassified']==25755
assert prog['raw_mutations']==0 and prog['unrelated_mutations']==0 and prog['new_imports']==0 and prog['new_publications']==0

text=baton.read_text()
checkpoint=f'''## 10. ACTIVE CHECKPOINT

- state: `READY_FOR_NEXT_SOURCE`
- branch: `content/corpus-inventory-20260914`
- latest verified work HEAD before this handoff commit: `{VERIFIED_WORK_HEAD}`
- last completed source: `{SID} — {SOURCE_NAME}`
- current source: `{next_id} — {next_name}`
- current source baseline from live manifest: `{baseline}`
- current operation: `Re-fetch live HEAD and baton; confirm no active/running workflow for {next_id}; read its immutable manifest/pages/evidence; technically verify RAW first; establish exact educational identity and lesson/unit boundaries only from source-specific evidence; map legacy questions only where page membership proves placement; preserve unresolved semantics/subtypes as NOT VERIFIED or review_required; reassert the 25,755 invariant.`
- next source: `Resolve from live manifest only after the current source is safely finalized.`
- blockers: `none at handoff; do not inherit Hadith lesson titles, ranges, or ten-lesson count into the next source.`
- owner decision required now: `no`
'''
pat=r'## 10\. ACTIVE CHECKPOINT\n.*?\n---\n\n### Shared handoff rule'
text2,n=re.subn(pat,checkpoint+'\n---\n\n### Shared handoff rule',text,count=1,flags=re.S)
assert n==1,'ACTIVE CHECKPOINT block not uniquely found'
run=f'''

## RUN 2026-09-14T15:13:12+03:00 — Worker B

- state: COMPLETE
- start HEAD: `{START_HEAD}`
- end HEAD: `{VERIFIED_WORK_HEAD}`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `{SID} — {SOURCE_NAME}`
- completed in this run:
  - consumed Worker A's live Islamic-1447 handoff and verified there was no active conflicting source workflow before mutation;
  - technically verified **62/62** immutable RAW images for Hadith and Refinement;
  - proved **62/62 exact SHA-256 identity** against the single master reference directory `التربية الاسلاميه ثالث ثانوي/كتاب الحديث والتهذيب/الصور`;
  - generated and reviewed complete contact-sheet coverage for stored pages **9..70**;
  - used explicit exact-master filename evidence to establish **10 lessons** and assign **62/62 retained pages** exactly once to a lesson;
  - structurally mapped **1,483/1,483 legacy questions** by proven page membership; semantic correctness remains `NOT VERIFIED`;
  - intentionally did not invent a Unit layer and did not claim page subtype/review boundaries; both remain `NOT VERIFIED`;
  - updated MASTER_CONTENT_MANIFEST and evidence-backed status/handoff/inventory/validation/import/continuation files;
  - discovery run `{DISCOVERY_RUN}` and finalization run `{FINALIZATION_RUN}` both completed successfully with live-HEAD fail-closed gates.
- evidence produced/verified:
  - `content-staging/reconstruction/technical/{SID}.json`;
  - `content-staging/reconstruction/educational/{SID}-discovery.json`;
  - `content-staging/reconstruction/educational/{SID}.json`;
  - contact-sheet artifact `hadith-contact-sheets` (artifact id `10346576550`), covering pages 009..070;
  - discovery workflow run `{DISCOVERY_RUN}` success;
  - finalization workflow run `{FINALIZATION_RUN}` success and `HADITH_FINALIZATION_VERIFY_PASS`;
  - final evidence/status commit `{VERIFIED_WORK_HEAD}`.
- ambiguity/review_required:
  - unit hierarchy: `NOT VERIFIED`; no unit layer asserted;
  - page subtype/review/evaluation boundaries: `NOT VERIFIED`; not needed to prove lesson membership;
  - semantic correctness of all 1,483 legacy questions: `NOT VERIFIED`;
  - source-level review-required question count added in this run: 0 because structural page-to-lesson membership is fully proven.
- invariant result: PASS (`4,833 + 967 + 351 + 19,604 = 25,755`)
- Sources processed: 18/58
- Educational: 8/26
- Books / Units / Lessons / Lesson Pages: 8 / 33 / 171 / 729
- Exam Source Groups: 10/32
- Individual Exam Models: 166
- Exam Pages: 548/2,286
- Verified Answer Keys: 0
- Source images technical: 1,394/5,273
- WebP generated / accepted / rejected: 0 / 0 / 0
- Legacy Questions: 25,755
- Lesson-linked: 4,833
- Exam-linked: 967
- Review-required: 351
- Unclassified: 19,604
- Duplicate groups classified: 0/99
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `{SID} — {SOURCE_NAME}`
- current source: `{next_id} — {next_name}`
- exact next operation: `Re-fetch live HEAD/baton; verify no active workflow for {next_id}; read its live manifest/pages; run full technical verification; establish identity and educational structure only from its own exact evidence; map questions only by proven page membership; leave semantic/subtype uncertainty NOT VERIFIED/review_required; assert global invariants and checkpoint.`
- next source: `Resolve from live manifest after {next_id} is finalized.`
- blockers: `none at handoff.`
- handoff note: `Worker A must start from {next_id} only after re-fetching the live branch and baton. Do not rerun Hadith absent new drift evidence and do not inherit its 10-lesson pattern or page range into Seerah.`
'''
if f'end HEAD: `{VERIFIED_WORK_HEAD}`' in text2[-8000:] and '— Worker B' in text2[-8000:]: raise SystemExit('handoff already appears present')
baton.write_text(text2.rstrip()+run+'\n')
print(json.dumps({'next_source_id':next_id,'next_source_name':next_name,'baseline':baseline,'progress':required},ensure_ascii=False))
