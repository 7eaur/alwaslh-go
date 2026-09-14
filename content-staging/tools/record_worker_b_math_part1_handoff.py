#!/usr/bin/env python3
import json,re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[2]
STAGING=ROOT/'content-staging'
LOG=STAGING/'CONTENT_RECONSTRUCTION_AUTOMATION_LOG.md'
MASTER=STAGING/'manifests/MASTER_CONTENT_MANIFEST.json'
CURRENT_ID='b80cbba1-410a-4346-9446-c3f01c4f9e56'
START_HEAD='6ed3971e2e2edfd276368f7ebf55f39d33a96610'
EVIDENCE_HEAD='f1202fbeedd500fc0d8fc2676b92485a46bf0570'

def main():
    master=json.loads(MASTER.read_text(encoding='utf-8')); prog=master['reconstruction_progress']
    current=next(x for x in master['sources'] if x['id']==CURRENT_ID)
    idx=next(i for i,x in enumerate(master['sources']) if x['id']==CURRENT_ID)
    nxt=master['sources'][idx+1] if idx+1<len(master['sources']) else None
    current_name=current['legacy_source']['name']
    next_desc=f"{nxt['id']} — {nxt['legacy_source']['name']}" if nxt else 'NOT YET RESOLVED'
    man=json.loads((STAGING/f'raw/legacy-supabase/subjects/{CURRENT_ID}/manifest.json').read_text(encoding='utf-8'))
    c=man['counts']; anomalies=man['anomalies']
    baseline=f"{c['pages']} pages, {c['images_downloaded']} images, {c['questions']} legacy questions, {c['image_download_failures']} download failures; anomaly arrays preserved: {json.dumps(anomalies,ensure_ascii=False,sort_keys=True)}"
    active=f'''## 10. ACTIVE CHECKPOINT

- state: `READY_NEXT_SOURCE`
- branch: `content/corpus-inventory-20260914`
- latest evidence HEAD before this handoff tooling: `{EVIDENCE_HEAD}`
- last completed source: `1933807f-4cb0-40c9-9b29-3ef3d32c98dc — كتاب الرياضيات - الجزء الأول`
- current source: `{CURRENT_ID} — {current_name}`
- current source baseline from live manifest: `{baseline}`
- current source verified work: `NOT STARTED in this handoff. No structural assumptions inherited from Part 1.`
- current operation: `Re-fetch live HEAD and this baton; confirm no active/running workflow for {CURRENT_ID}; technically verify all {c['images_downloaded']} immutable RAW images first; establish Part 2 identity and Unit/Lesson/non-lesson boundaries only from its own deterministic evidence; because this source has 0 legacy questions, do not invent question mappings; preserve ambiguity as NOT VERIFIED/review_required; checkpoint only after page classification and invariants pass.`
- next source: `{next_desc}`
- blockers: `none for handoff; Part 2 technical/identity/structure evidence is NOT VERIFIED until Worker A inspects it.`
- owner decision required now: `no; continue source-by-source fail-closed`
'''
    text=LOG.read_text(encoding='utf-8')
    pat=r'## 10\. ACTIVE CHECKPOINT\n.*?\n---\n\n### Shared handoff rule'
    replacement=active.rstrip()+'\n---\n\n### Shared handoff rule'
    text,n=re.subn(pat,replacement,text,count=1,flags=re.S)
    if n!=1: raise SystemExit(f'ACTIVE CHECKPOINT replace count={n}')
    ts=datetime.now(ZoneInfo('Asia/Riyadh')).replace(microsecond=0).isoformat()
    run=f'''\n\n## RUN {ts} — Worker B

- state: COMPLETE
- start HEAD: `{START_HEAD}`
- end HEAD before handoff-log tooling: `{EVIDENCE_HEAD}`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `1933807f-4cb0-40c9-9b29-3ef3d32c98dc — كتاب الرياضيات - الجزء الأول`
- completed in this run:
  - verified Worker A's last RUN and source-identity blocker against live HEAD/manifests/evidence;
  - preserved the rejected master reference as rejected and transferred no structure from it;
  - generated and inspected complete occurrence-safe contact sheets covering all 186 immutable RAW pages;
  - established 4 unit boundaries, 21 source-local lesson runs, 162 lesson pages, and 24 proven non-lesson pages (2 review, 18 general-exercise, 4 unit-test);
  - accounted for all 717 legacy questions: 620 on proven lesson pages structurally lesson-linked; 97 on proven non-lesson pages marked review_required rather than forced into lessons;
  - reran 186/186 technical verification, finalized reconstruction, updated MASTER and evidence-backed status files;
  - finalization passed all live-HEAD gates and the global question invariant.
- evidence produced/verified:
  - technical report: `content-staging/reconstruction/technical/1933807f-4cb0-40c9-9b29-3ef3d32c98dc.json`;
  - reconstruction: `content-staging/reconstruction/educational/1933807f-4cb0-40c9-9b29-3ef3d32c98dc.json`;
  - contact-sheet run `34866261877`, artifact digest `sha256:d0809a083d82ceccfdddaecaa757b53503fbc28ef4a23b542a31f894a8bf866b`;
  - structure-analysis run `34866749562`: 717 = 620 lesson + 23 review + 62 general-exercise + 12 unit-test questions;
  - finalization run `34867041504`: `MATH_PART1_RECONSTRUCTION_VERIFY_PASS` and `MATH_PART1_FINALIZATION_VERIFY_PASS`;
  - canonical evidence commit: `{EVIDENCE_HEAD}`;
  - initial handoff workflow run `34867292456` failed at workflow configuration before any Job and made no baton/evidence mutation; replaced by the guarded handoff path that produced this RUN.
- ambiguity/review_required:
  - rejected reference `الرياضيات ثالث ثانوي/02_الرياضيات_ثالث_ثانوي`: 0/186 exact SHA matches and expected-position unique visual nearest match only 1/186; it remains unusable for identity/structure;
  - 97 questions on review/exercise/test pages remain `review_required`;
  - semantic correctness of legacy AI questions: `NOT VERIFIED`.
- invariant result: PASS
- Sources processed: {prog['sources_completed']}/58
- Educational: {prog['educational_sources_completed']}/26
- Books / Units / Lessons / Lesson Pages: {prog['verified_books']} / {prog['verified_units']} / {prog['verified_lessons']} / {prog['verified_lesson_pages']}
- Exam Source Groups: {prog['exam_source_groups_completed']}/32
- Individual Exam Models: {prog['individual_exam_models']}
- Exam Pages: {prog['finalized_exam_pages']}/2,286
- Verified Answer Keys: 0
- Source images technical: {prog['source_images_technically_verified']}/5,273
- WebP generated / accepted / rejected: 0 / 0 / 0
- Legacy Questions: 25,755
- Lesson-linked: {prog['lesson_linked_structural']}
- Exam-linked: {prog['exam_linked_to_individual_model']}
- Review-required: {prog['review_required']}
- Unclassified: {prog['unclassified']}
- Duplicate groups classified: 0/99
- RAW mutations: {prog['raw_mutations']}
- Unrelated mutations: {prog['unrelated_mutations']}
- New imports: {prog['new_imports']}
- New publications: {prog['new_publications']}
- last completed source: `1933807f-4cb0-40c9-9b29-3ef3d32c98dc — كتاب الرياضيات - الجزء الأول`
- current source: `{CURRENT_ID} — {current_name}`
- exact next operation: `Technically verify 135/135 Part 2 RAW images, establish identity/title evidence and complete visual boundaries from Part 2 itself, reconstruct its own Units/Lessons/non-lesson pages without inheriting Part 1 structure, assert 0-question accounting and global invariant, checkpoint, then continue.`
- next source: `{next_desc}`
- blockers: `none`
- handoff note: `Worker A must start Part 2 from its live manifest/RAW. Do not assume Part 1's unit count, page ranges, lesson count, or rejected-reference behavior applies. Part 2 baseline has 0 legacy questions, so invent no question mappings.`
'''
    LOG.write_text(text.rstrip()+run+'\n',encoding='utf-8')
    print(json.dumps({'timestamp':ts,'current':CURRENT_ID,'current_name':current_name,'next':next_desc,'counts':c},ensure_ascii=False))
if __name__=='__main__': main()
