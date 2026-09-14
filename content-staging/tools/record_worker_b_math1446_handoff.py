#!/usr/bin/env python3
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
LOG=ROOT/'content-staging/CONTENT_RECONSTRUCTION_AUTOMATION_LOG.md'
MASTER=ROOT/'content-staging/manifests/MASTER_CONTENT_MANIFEST.json'
SID='85c13f3f-fe85-47c3-affb-fb437d10d908'
NEXT='fef5e58f-21df-42e3-81ae-6966cd7bad10'
WORK_HEAD='1d7892e49460ed1c48e31436bacaeec2939ae7c1'
START_HEAD='d9d9739cbd39fd23c63912940837d8a7b2e68591'

def main():
    text=LOG.read_text(encoding='utf-8')
    assert '- current source: `85c13f3f-fe85-47c3-affb-fb437d10d908 — الرياضيات نماذج وزارية 1446`' in text, 'baton drift: current source is no longer Math 1446'
    m=json.loads(MASTER.read_text(encoding='utf-8')); p=m['reconstruction_progress']
    expected={'sources_completed':22,'educational_sources_completed':10,'verified_books':10,'verified_units':33,'verified_lessons':196,'verified_lesson_pages':877,'exam_source_groups_completed':12,'individual_exam_models':192,'exam_pages_completed':626,'answer_keys':0,'source_images_technically_verified':1623,'lesson_linked_structural':6891,'exam_linked_to_individual_model':1020,'review_required':351,'unclassified':17493,'duplicate_fingerprint_groups_classified':0,'raw_mutations':0,'unrelated_mutations':0,'new_imports':0,'new_publications':0,'correction_sheet_candidates':197}
    for k,v in expected.items(): assert p.get(k)==v,(k,p.get(k),v)
    assert p['lesson_linked_structural']+p['exam_linked_to_individual_model']+p['review_required']+p['unclassified']==25755
    src=next(x for x in m['sources'] if x['id']==SID); assert src['review_status']=='processed_boundary_verified_numbering_anomalies_preserved_answer_keys_not_verified'
    nxt=next(x for x in m['sources'] if x['id']==NEXT); nm=nxt['legacy_source']['name']; c=nxt['counts']; a=nxt['anomalies']
    active=f'''## 10. ACTIVE CHECKPOINT

- state: `READY_FOR_NEXT_SOURCE`
- branch: `content/corpus-inventory-20260914`
- latest verified work HEAD before this handoff commit: `{WORK_HEAD}`
- last completed source: `{SID} — الرياضيات نماذج وزارية 1446`
- current source: `{NEXT} — {nm}`
- current source baseline from live manifest: `{c['pages']} pages, {c['images_downloaded']} images, {c['questions']} legacy questions, {c['image_download_failures']} download failures; anomaly arrays preserved: {json.dumps(a,ensure_ascii=False,sort_keys=True)}`
- current operation: `Re-fetch live HEAD and baton; confirm no active/running workflow for {NEXT}; technically verify all immutable RAW; scan within-source SHA duplicates; generate complete visual boundary evidence; resolve Individual Exam Models and correction/Answer-Key evidence only from Math 1447 source-local metadata/visuals; map {c['questions']} legacy questions only where model membership is proven; quarantine uncertainty as review_required/NOT VERIFIED; assert 25,755 invariant; checkpoint and continue.`
- next source: `Resolve from live MASTER_CONTENT_MANIFEST only after the current source is safely finalized.`
- blockers: `none for forward progress; Math 1446 duplicate source page numbers 16 and 29 are preserved provenance anomalies and must never be silently normalized or merged.`
- owner decision required now: `no`
'''
    pattern=r'## 10\. ACTIVE CHECKPOINT\n.*?(?=\n---\n\n### Shared handoff rule)'
    new,n=re.subn(pattern,active.rstrip(),text,flags=re.S); assert n==1,n
    run=f'''

## RUN 2026-09-14T17:40:15+03:00 — Worker B

- state: COMPLETE
- start HEAD: `{START_HEAD}`
- end HEAD before handoff-log commit: `{WORK_HEAD}`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `{SID} — الرياضيات نماذج وزارية 1446`
- completed in this run:
  - consumed and verified Worker A's Math 1445 finalization/handoff instead of racing its active shared-log workflow;
  - technically verified all 39/39 Math 1446 immutable RAW images;
  - preserved duplicate source page numbers 16 and 29 as distinct legacy-page occurrences rather than normalizing identity;
  - generated occurrence-safe metadata and four complete visual contact sheets and visually reviewed all 39 occurrences;
  - verified 13 complete Individual Exam Models from explicit source titles plus visual evidence, each with two question pages and one correction/result candidate;
  - structurally linked all 25/25 source legacy questions to verified model 1 through unique legacy_page_id membership;
  - finalized reconstruction, MASTER manifest, and all checkpoint/status reports through exact-head guarded GitHub Actions run `34857025941`.
- evidence produced/verified:
  - `content-staging/reconstruction/technical/{SID}.json` — 39 existing/readable/SHA/byte-size/MIME matches, 0 failures, 0 duplicate SHA groups;
  - `content-staging/reconstruction/exams/source-groups/{SID}-metadata-evidence.json` — occurrence-safe identities and duplicate-number provenance;
  - `content-staging/reconstruction/exams/source-groups/{SID}-visual-review.json` — complete 39-occurrence visual adjudication;
  - `content-staging/reconstruction/exams/source-groups/{SID}.json` — 13 models / 39 finalized exam pages / 13 correction candidates;
  - workflow `34856438569` discovery success and workflow `34857025941` finalization success with `MATH_1446_FINALIZATION_VERIFY_PASS`.
- ambiguity/review_required:
  - source page-number anomalies 16 and 29 are provenance-only anomalies; no model membership remains ambiguous because explicit title + unique legacy_page_id + visual review establish membership;
  - standalone official Answer Keys: `NOT VERIFIED`; correction/result pages remain candidates only;
  - semantic correctness of legacy questions: `NOT VERIFIED`.
- invariant result: PASS
- Sources processed: 22/58
- Educational: 10/26
- Books / Units / Lessons / Lesson Pages: 10 / 33 / 196 / 877
- Exam Source Groups: 12/32
- Individual Exam Models: 192
- Exam Pages: 626/2,286
- Verified Answer Keys: 0
- Source images technical: 1,623/5,273
- WebP generated / accepted / rejected: 0 / 0 / 0
- Legacy Questions: 25,755
- Lesson-linked: 6,891
- Exam-linked: 1,020
- Review-required: 351
- Unclassified: 17,493
- Duplicate groups classified: 0/99
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `{SID} — الرياضيات نماذج وزارية 1446`
- current source: `{NEXT} — {nm}`
- exact next operation: `Technically verify the {c['pages']} Math 1447 immutable image occurrences, then discover its model/correction boundaries from its own metadata and complete visual evidence; map its {c['questions']} questions only after membership is proven.`
- next source: `NOT YET RESOLVED — resolve only after Math 1447 finalization from live MASTER_CONTENT_MANIFEST`
- blockers: `none`
- handoff note: `Math 1446 is closed. Do not normalize duplicate page numbers 16 or 29; legacy_page_id/source-record occurrence is the preserved identity. Worker A should start only from Math 1447 live evidence and must not inherit the 1446 numbering pattern.`
'''
    LOG.write_text(new.rstrip()+run+'\n',encoding='utf-8')
    print(json.dumps({'next_source_id':NEXT,'next_source_name':nm,'progress':expected,'invariant':25755},ensure_ascii=False))
if __name__=='__main__': main()
