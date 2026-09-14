#!/usr/bin/env python3
import json,re,subprocess
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
LOG=ROOT/'content-staging/CONTENT_RECONSTRUCTION_AUTOMATION_LOG.md'
STATUS=ROOT/'content-staging/CONTENT_REBUILD_EXECUTION_STATUS.md'
HANDOFF=ROOT/'content-staging/CONTENT_REBUILD_HANDOFF.md'
MASTER=ROOT/'content-staging/manifests/MASTER_CONTENT_MANIFEST.json'
SID='1933807f-4cb0-40c9-9b29-3ef3d32c98dc'
START_HEAD='8c0d26a855229a7c1def2a758400d19020a88a25'
EVIDENCE_HEAD='d07fbe0fb1c7169f4641efa06afa7b6379e5cbdf'

def main():
    text=LOG.read_text(encoding='utf-8')
    assert '- current source: `1933807f-4cb0-40c9-9b29-3ef3d32c98dc — كتاب الرياضيات - الجزء الأول`' in text, 'baton drift: current source changed'
    current_head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    m=json.loads(MASTER.read_text(encoding='utf-8')); p=m['reconstruction_progress']
    expected={'sources_completed':23,'educational_sources_completed':10,'verified_books':10,'verified_units':33,'verified_lessons':196,'verified_lesson_pages':877,'exam_source_groups_completed':13,'individual_exam_models':206,'exam_pages_completed':668,'answer_keys':0,'source_images_technically_verified':1665,'lesson_linked_structural':6891,'exam_linked_to_individual_model':1132,'review_required':351,'unclassified':17381,'duplicate_fingerprint_groups_classified':0,'raw_mutations':0,'unrelated_mutations':0,'new_imports':0,'new_publications':0}
    for k,v in expected.items(): assert p.get(k)==v,(k,p.get(k),v)
    assert p['lesson_linked_structural']+p['exam_linked_to_individual_model']+p['review_required']+p['unclassified']==25755
    src=next(x for x in m['sources'] if x['id']==SID); c=src['counts']; a=src['anomalies']; nm=src['legacy_source']['name']
    assert c['pages']==186 and c['images_downloaded']==186 and c['questions']==717 and c['image_download_failures']==0
    tech=json.loads((ROOT/f'content-staging/reconstruction/technical/{SID}.json').read_text(encoding='utf-8'))
    disc=json.loads((ROOT/f'content-staging/reconstruction/educational/{SID}-discovery.json').read_text(encoding='utf-8'))
    vis=json.loads((ROOT/f'content-staging/reconstruction/educational/{SID}-visual-identity-diagnostic.json').read_text(encoding='utf-8'))
    q=json.loads((ROOT/f'content-staging/reconstruction/educational/{SID}-legacy-reference-analysis.json').read_text(encoding='utf-8'))
    assert tech['all_images_technically_verified'] is True and tech['checks']['manifest_image_count']==186
    assert disc['exact_sha_identity_count']==0 and disc['identity_status']=='NOT VERIFIED'
    assert vis['intended_unique_best_count']==1 and vis['all_intended_unique_best'] is False
    assert q['page_count']==186 and q['question_count']==717 and q['boundary_status']=='NOT VERIFIED'
    assert q['pages_with_question_evidence']==60 and q['pages_without_question_evidence']==126
    assert q['pages_single_title_candidate']==57 and q['pages_multi_title_conflict']==3 and q['distinct_lesson_title_candidates']==45
    active=f'''## 10. ACTIVE CHECKPOINT

- state: `PARTIAL_SAFE_HANDOFF_SOURCE_IDENTITY_BLOCKER`
- branch: `content/corpus-inventory-20260914`
- latest evidence HEAD before this handoff tooling: `{EVIDENCE_HEAD}`
- last completed source: `fef5e58f-21df-42e3-81ae-6966cd7bad10 — الرياضيات نماذج وزارية 1447`
- current source: `{SID} — {nm}`
- current source baseline from live manifest: `{c['pages']} pages, {c['images_downloaded']} images, {c['questions']} legacy questions, {c['image_download_failures']} download failures; anomaly arrays preserved: {json.dumps(a,ensure_ascii=False,sort_keys=True)}`
- current source verified work: `186/186 immutable RAW images technically PASS. The initially tested master reference (الرياضيات ثالث ثانوي/02_الرياضيات_ثالث_ثانوي) is REJECTED as an identity source: 0/186 exact SHA matches and only 1/186 expected source-page positions is the unique visual nearest match across all 255 reference pages. No book/unit/lesson/review boundary or question mapping has been promoted.`
- current operation: `Re-fetch live HEAD and this baton; confirm no active/running workflow for {SID}; keep the current source active. Establish the actual source identity from RAW/source-local evidence first. Generate and inspect occurrence-safe visual contact sheets or another deterministic page-level reference for the 186 RAW pages; do not reuse the rejected Third Secondary master metadata. Use legacy question_references only as weak candidates: they cover 60/186 pages, leave 126 pages without question evidence, include 3 multi-title conflicts, and remain semantically NOT VERIFIED. Only after source identity/page boundaries are independently evidenced may units/lessons/reviews and the 717 structural links be finalized.`
- next source: `NOT YET RESOLVED — do not advance until {SID} is either safely finalized or explicitly quarantined by an evidence-backed decision.`
- blockers: `SOURCE IDENTITY NOT VERIFIED. Rejected reference evidence: exact SHA 0/186; all-v-all visual diagnostic expected-position unique-best 1/186. Legacy AI question-reference candidates are insufficient alone (60 pages with evidence / 126 without; 57 single-title pages / 3 conflicts; 45 distinct candidate titles).`
- owner decision required now: `no; continue evidence discovery fail-closed`
'''
    pattern=r'## 10\. ACTIVE CHECKPOINT\n.*?(?=\n---\n\n### Shared handoff rule)'
    new,n=re.subn(pattern,active.rstrip(),text,flags=re.S); assert n==1,n
    ts=datetime.now(ZoneInfo('Asia/Riyadh')).isoformat(timespec='seconds')
    run=f'''

## RUN {ts} — Worker A

- state: `PARTIAL_SAFE_HANDOFF_SOURCE_IDENTITY_BLOCKER`
- start HEAD: `{START_HEAD}`
- end HEAD before handoff-log commit: `{current_head}`
- evidence HEAD before handoff tooling: `{EVIDENCE_HEAD}`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start/current: `{SID} — {nm}`
- completed in this run:
  - consumed the live Worker B Math 1447 baton and verified the active source from live manifest/evidence;
  - technically verified **186/186** immutable RAW images with the repository verifier; RAW remained unchanged;
  - tested the apparent Third Secondary master reference and failed closed instead of inheriting its structure: **0/186 exact SHA identities**;
  - performed an independent all-vs-all grayscale page diagnostic against all **255** pages of that reference; only **1/186** RAW occurrences had the expected page position as a unique nearest visual match, proving that the apparent reference must not be used to transfer titles/boundaries;
  - analyzed all **717** legacy question references as weak source-local candidates only: 60/186 pages have question evidence, 126 have none, 57 pages have one candidate title, 3 pages have conflicting candidate titles, and 45 distinct candidate lesson titles exist;
  - intentionally did **not** promote a book identity, unit/lesson/review boundaries, question links, source completion, imports, or publications because independent source identity remains insufficient.
- evidence produced/verified:
  - `content-staging/reconstruction/technical/{SID}.json` — 186/186 technical media PASS;
  - `content-staging/reconstruction/educational/{SID}-discovery.json` — exact master identity diagnostic, 0/186 SHA matches, identity `NOT VERIFIED`;
  - `content-staging/reconstruction/educational/{SID}-visual-identity-diagnostic.json` — all-vs-all 186x255 visual diagnostic, expected-position unique-best 1/186;
  - `content-staging/reconstruction/educational/{SID}-legacy-reference-analysis.json` — question-reference candidate coverage/conflicts, boundaries explicitly `NOT VERIFIED`;
  - discovery workflow `34863674270` PASS for technical/diagnostic invariants; earlier fail-closed runs `34862933212` and `34863089370` caused no finalization or RAW mutation.
- ambiguity/review_required:
  - actual book/edition/grade identity: `NOT VERIFIED`;
  - book/unit/lesson/review boundaries: `NOT VERIFIED`;
  - all 717 question structural links for this source: unchanged/unclassified pending independent page membership evidence;
  - semantic correctness of legacy question titles/content: `NOT VERIFIED`.
- invariant result: PASS — canonical classifications unchanged: 6,891 + 1,132 + 351 + 17,381 = 25,755
- canonical progress remains: Sources 23/58; Educational 10/26; Books/Units/Lessons/Lesson Pages 10/33/196/877; Exam Source Groups 13/32; Individual Exam Models 206; Exam Pages 668/2,286; Answer Keys 0; Source images promoted in MASTER 1,665/5,273; Duplicate groups classified 0/99.
- run-local technical evidence: current source images verified 186/186; not promoted to canonical completed-source counter while source identity is unresolved.
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `fef5e58f-21df-42e3-81ae-6966cd7bad10 — الرياضيات نماذج وزارية 1447`
- current source: `{SID} — {nm}`
- exact next operation: `Keep this source active. Build/inspect occurrence-safe visual contact sheets directly from its 186 RAW images (or locate a deterministic exact reference for this edition), establish page/book identity independently, then reconstruct only evidence-backed unit/lesson/review boundaries. Treat the 45 legacy lesson-title candidates as hints only, not truth. Map the 717 questions only after page membership is independently proven; otherwise leave them unclassified/review_required.`
- next source: `NOT YET RESOLVED`
- blockers: `Source identity mismatch with the apparent Third Secondary master reference; no safe structural finalization yet.`
- handoff note: `Worker B must not repeat or force the rejected master mapping. Continue from the diagnostic artifacts above, keeping source {SID} active until identity/boundaries are independently evidenced.`
'''
    LOG.write_text(new.rstrip()+run+'\n',encoding='utf-8')
    note=f'''\n\n## Partial source-identity checkpoint — {ts}\n\n- Source: `{SID} — {nm}`\n- 186/186 RAW images technically verified.\n- Apparent Third Secondary master reference rejected: 0/186 exact SHA matches and expected page position unique-best in only 1/186 all-vs-all visual comparisons.\n- 717 legacy question references are candidate evidence only: 60 pages covered, 126 uncovered, 3 pages with title conflicts, 45 distinct candidate titles.\n- Source/book/unit/lesson/review identity and boundaries remain `NOT VERIFIED`; canonical reconstruction counters and the 25,755 classification invariant are unchanged.\n- No RAW/unrelated/import/publication mutations.\n- Next: independently identify/visually inspect this exact RAW edition before any structural promotion.\n'''
    for path in (STATUS,HANDOFF):
        s=path.read_text(encoding='utf-8')
        marker=f'Partial source-identity checkpoint — {ts}'
        assert marker not in s
        path.write_text(s.rstrip()+note+'\n',encoding='utf-8')
    print(json.dumps({'current_head':current_head,'source':SID,'technical_verified':'186/186','sha_identity':'0/186','visual_expected_unique_best':'1/186','legacy_pages_with_evidence':60,'legacy_pages_without_evidence':126,'invariant':25755},ensure_ascii=False))
if __name__=='__main__': main()
