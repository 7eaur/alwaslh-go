#!/usr/bin/env python3
import json,re,subprocess
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
LOG=ROOT/'content-staging/CONTENT_RECONSTRUCTION_AUTOMATION_LOG.md'
MASTER=ROOT/'content-staging/manifests/MASTER_CONTENT_MANIFEST.json'
SID='fef5e58f-21df-42e3-81ae-6966cd7bad10'
NEXT='1933807f-4cb0-40c9-9b29-3ef3d32c98dc'
FINAL_HEAD='6fcd36a0bf7e5db93e7cfc531d2b9471c489d65f'
START_HEAD='c378c367405701ee9a79c53b464bd377bcf1b8fa'

def main():
    text=LOG.read_text(encoding='utf-8')
    assert '- current source: `fef5e58f-21df-42e3-81ae-6966cd7bad10 — الرياضيات نماذج وزارية 1447`' in text, 'baton drift: current source is no longer Math 1447'
    current_head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    m=json.loads(MASTER.read_text(encoding='utf-8')); p=m['reconstruction_progress']
    expected={'sources_completed':23,'educational_sources_completed':10,'verified_books':10,'verified_units':33,'verified_lessons':196,'verified_lesson_pages':877,'exam_source_groups_completed':13,'individual_exam_models':206,'exam_pages_completed':668,'answer_keys':0,'source_images_technically_verified':1665,'lesson_linked_structural':6891,'exam_linked_to_individual_model':1132,'review_required':351,'unclassified':17381,'duplicate_fingerprint_groups_classified':0,'raw_mutations':0,'unrelated_mutations':0,'new_imports':0,'new_publications':0,'correction_sheet_candidates':211}
    for k,v in expected.items(): assert p.get(k)==v,(k,p.get(k),v)
    assert p['lesson_linked_structural']+p['exam_linked_to_individual_model']+p['review_required']+p['unclassified']==25755
    src=next(x for x in m['sources'] if x['id']==SID); assert src['review_status']=='processed_boundary_verified_explicit_titles_visual_semantics_not_verified_answer_keys_not_verified'
    nxt=next(x for x in m['sources'] if x['id']==NEXT); nm=nxt['legacy_source']['name']; c=nxt['counts']; a=nxt['anomalies']
    assert c['pages']==186 and c['images_downloaded']==186 and c['questions']==717 and c['image_download_failures']==0
    active=f'''## 10. ACTIVE CHECKPOINT

- state: `READY_FOR_NEXT_SOURCE`
- branch: `content/corpus-inventory-20260914`
- latest verified work HEAD before this handoff tooling: `{FINAL_HEAD}`
- last completed source: `{SID} — الرياضيات نماذج وزارية 1447`
- current source: `{NEXT} — {nm}`
- current source baseline from live manifest: `{c['pages']} pages, {c['images_downloaded']} images, {c['questions']} legacy questions, {c['image_download_failures']} download failures; anomaly arrays preserved: {json.dumps(a,ensure_ascii=False,sort_keys=True)}`
- current operation: `Re-fetch live HEAD and baton; confirm no active/running workflow for {NEXT}; technically verify all {c['images_downloaded']} immutable RAW images and within-source SHA duplicates; establish Math Part 1 source identity only from its own live metadata/master/source-local evidence; reconstruct only evidence-backed book/unit/lesson/review boundaries; structurally map the {c['questions']} legacy questions only where page membership is proven; mark insufficient evidence review_required/NOT VERIFIED; assert 25,755 invariant; checkpoint and continue.`
- next source: `Resolve from live MASTER_CONTENT_MANIFEST only after the current source is safely finalized.`
- blockers: `none; Math 1447 visual contact sheets exist but semantic visual inspection remains NOT VERIFIED, standalone Answer Keys remain NOT VERIFIED, and those limitations must not be upgraded without new evidence.`
- owner decision required now: `no`
'''
    pattern=r'## 10\. ACTIVE CHECKPOINT\n.*?(?=\n---\n\n### Shared handoff rule)'
    new,n=re.subn(pattern,active.rstrip(),text,flags=re.S); assert n==1,n
    ts=datetime.now(ZoneInfo('Asia/Riyadh')).isoformat(timespec='seconds')
    run=f'''

## RUN {ts} — Worker B

- state: COMPLETE
- start HEAD: `{START_HEAD}`
- end HEAD before handoff-log commit: `{current_head}`
- verified finalization HEAD: `{FINAL_HEAD}`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `{SID} — الرياضيات نماذج وزارية 1447`
- completed in this run:
  - consumed and verified the live Math 1446 Worker B handoff at the starting HEAD rather than relying on conversation memory;
  - technically verified all **42/42** Math 1447 immutable RAW images with byte-size/SHA-256/MIME/readability checks and **0** failures / **0** duplicate SHA groups;
  - generated occurrence-safe source metadata and complete visual contact-sheet artifacts in discovery run `34859563356`;
  - proved **14** complete Individual Exam Model boundaries from explicit unique source-local titles and the exact contiguous 1..42 three-record sequence; semantic visual inspection was deliberately kept `NOT VERIFIED` rather than guessed;
  - classified all **42** pages into those 14 model occurrences, each as paper 1 + paper 2 + correction-sheet candidate, with **0** page-level review_required;
  - structurally linked all **112/112** legacy questions through their unique legacy-page membership; semantic correctness remains `NOT VERIFIED`;
  - finalized reconstruction, MASTER manifest, and all status/checkpoint reports through exact-head guarded finalization run `34860210260`.
- evidence produced/verified:
  - `content-staging/reconstruction/technical/{SID}.json` — 42/42 immutable media checks PASS, contiguous page sequence 1..42, 0 duplicate SHA groups;
  - `content-staging/reconstruction/exams/source-groups/{SID}-metadata-evidence.json` — 42 unique records and explicit model 1..14 title triplets;
  - `content-staging/reconstruction/exams/source-groups/{SID}.json` — 14 models / 42 finalized exam pages / 14 correction candidates / 112 structurally linked questions;
  - discovery workflow `34859563356` success; visual artifact `10354183123` digest `sha256:5f90b8cd574533183a76fe0ac2f6754cfc491ff55afec016f5d1fede99145e15`;
  - finalization workflow `34860210260` success with reconstruction/global invariant verification and both live-HEAD gates PASS.
- ambiguity/review_required:
  - semantic visual inspection of generated contact sheets: `NOT VERIFIED`;
  - standalone official Answer Keys: `NOT VERIFIED`; pages titled `نموذج التصحيح` remain correction-sheet candidates only;
  - official model codes / term metadata: `NOT VERIFIED`;
  - semantic correctness of legacy questions: `NOT VERIFIED`.
- invariant result: PASS
- Sources processed: 23/58
- Educational: 10/26
- Books / Units / Lessons / Lesson Pages: 10 / 33 / 196 / 877
- Exam Source Groups: 13/32
- Individual Exam Models: 206
- Exam Pages: 668/2,286
- Verified Answer Keys: 0
- Source images technical: 1,665/5,273
- WebP generated / accepted / rejected: 0 / 0 / 0
- Legacy Questions: 25,755
- Lesson-linked: 6,891
- Exam-linked: 1,132
- Review-required: 351
- Unclassified: 17,381
- Duplicate groups classified: 0/99
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `{SID} — الرياضيات نماذج وزارية 1447`
- current source: `{NEXT} — {nm}`
- current source baseline: `{c['pages']} pages / {c['images_downloaded']} images / {c['questions']} legacy questions / {c['image_download_failures']} download failures; anomalies {json.dumps(a,ensure_ascii=False,sort_keys=True)}`
- exact next operation: `Technically verify the 186 immutable Math Part 1 RAW images first, then establish source identity and book/unit/lesson/review boundaries only from that source's own live evidence; map 717 questions only where page membership is proven; quarantine every unresolved boundary or mapping as review_required/NOT VERIFIED; assert global invariant before checkpoint.`
- next source: `NOT YET RESOLVED — resolve only after Math Part 1 finalization from live MASTER_CONTENT_MANIFEST`
- blockers: `none`
- handoff note: `Math 1447 is safely closed. Do not upgrade visual semantics, standalone Answer Keys, official model codes, term metadata, or question correctness without new evidence. Worker A should begin from Math Part 1 live manifest/pages and not inherit exam-source structure into the educational book.`
'''
    LOG.write_text(new.rstrip()+run+'\n',encoding='utf-8')
    print(json.dumps({'current_head':current_head,'next_source_id':NEXT,'next_source_name':nm,'progress':expected,'invariant':25755},ensure_ascii=False))
if __name__=='__main__': main()
