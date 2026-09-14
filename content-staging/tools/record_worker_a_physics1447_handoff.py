#!/usr/bin/env python3
import json
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path('.')
LOG_PATH = ROOT / 'content-staging/CONTENT_RECONSTRUCTION_AUTOMATION_LOG.md'
MASTER_PATH = ROOT / 'content-staging/manifests/MASTER_CONTENT_MANIFEST.json'
SOURCE_ID = 'bbc5c2e7-9b96-4502-a8b0-6a14d2f8782a'
NEXT_SOURCE_ID = 'd1a6b8f8-d81b-4824-86e1-d370ec28bdf1'
EVIDENCE_HEAD = 'a472b465c292ac55109bde64196a7b589ac0735b'
START_HEAD = 'c0fb023344ef6b002054f8b88bb5ed1148fb5004'


def source_name(item):
    return (item.get('legacy_source') or {}).get('name') or item.get('name') or 'UNKNOWN'


def main():
    master = json.loads(MASTER_PATH.read_text(encoding='utf-8'))
    src = next(s for s in master['sources'] if s.get('id') == SOURCE_ID)
    nxt = next(s for s in master['sources'] if s.get('id') == NEXT_SOURCE_ID)
    if src.get('review_status') != 'processed_boundary_verified_answer_keys_not_verified':
        raise SystemExit('Physics 1447 not canonically processed')

    p = master['reconstruction_progress']
    expected = {
        'sources_completed': 35,
        'educational_sources_completed': 16,
        'exam_source_groups_completed': 19,
        'individual_exam_models': 356,
        'exam_pages_completed': 1232,
        'source_images_technically_verified': 2979,
        'lesson_linked_structural': 13135,
        'exam_linked_to_individual_model': 1920,
        'review_required': 1229,
        'unclassified': 9471,
        'raw_mutations': 0,
        'unrelated_mutations': 0,
        'new_imports': 0,
        'new_publications': 0,
    }
    for key, value in expected.items():
        if int(p.get(key) or 0) != value:
            raise SystemExit(f'progress drift {key}: {p.get(key)} != {value}')
    if sum(int(p.get(k) or 0) for k in ('lesson_linked_structural','exam_linked_to_individual_model','review_required','unclassified')) != 25755:
        raise SystemExit('global invariant drift')

    manifest_path = ROOT / 'content-staging/raw/legacy-supabase/subjects' / NEXT_SOURCE_ID / 'manifest.json'
    nm = json.loads(manifest_path.read_text(encoding='utf-8'))
    c = nm['counts']; a = nm['anomalies']
    if (c.get('pages'), c.get('images_downloaded'), c.get('questions'), c.get('image_download_failures')) != (42, 42, 0, 0):
        raise SystemExit('next-source baseline drift')
    anomaly_keys = ('duplicate_page_numbers','invalid_subject_ids','malformed_ai_questions','malformed_image_urls','missing_images','multiple_images','null_or_invalid_page_numbers')
    if any(a.get(k) for k in anomaly_keys):
        raise SystemExit('next-source anomaly drift')

    trigger_head = subprocess.check_output(['git','rev-parse','HEAD'], text=True).strip()
    next_name = source_name(nxt)

    active = f'''## 10. ACTIVE CHECKPOINT

- state: `READY_NEXT_SOURCE`
- branch: `content/corpus-inventory-20260914`
- latest evidence HEAD before this handoff tooling: `{EVIDENCE_HEAD}`
- last completed source: `{SOURCE_ID} — الفيزياء نماذج وزاريه 1447`
- current source: `{NEXT_SOURCE_ID} — {next_name}`
- current source baseline from live manifest: `42 pages / 42 images / 0 legacy questions / 0 download failures; anomaly arrays empty.`
- current source verified work: `NOT STARTED; no Physics or prior Arabic packet size/boundary pattern may be inherited.`
- current operation: `Re-fetch live HEAD and baton; confirm no active/running workflow for this exact source; technically verify all 42 immutable RAW images; perform source-local duplicate scan and exam-boundary discovery; visually inspect complete source evidence; resolve occurrences, Individual Exam Models, correction/result candidates and Answer-Key evidence without inheriting prior-source patterns; there are 0 legacy questions so do not fabricate question mappings; use review_required/NOT VERIFIED when evidence is insufficient; assert global invariants; checkpoint.`
- next source: `Resolve only after Arabic 1447 finalization from live MASTER.`
- blockers: `none`
- completed Physics 1447 evidence: `124/124 immutable RAW images technically verified; sequence 1..124 contiguous; 9 duplicate SHA groups preserved; complete visual review proves 31 four-page occurrences, each three question pages plus one correction/result candidate; 31 Individual Exam Models / 124 Exam Pages finalized; 31 correction candidates; 0 verified standalone Answer Keys; 255/255 legacy questions structurally linked by verified page membership; semantic correctness NOT VERIFIED; RAW/unrelated/import/publication mutations 0.`
'''

    text = LOG_PATH.read_text(encoding='utf-8')
    marker = '## 10. ACTIVE CHECKPOINT'
    shared = '---\n\n### Shared handoff rule'
    if marker not in text or shared not in text:
        raise SystemExit('shared baton anchors missing')
    before = text.split(marker, 1)[0]
    after = text.split(shared, 1)[1]
    text = before + active + '\n---\n\n### Shared handoff rule' + after

    now = datetime.now(timezone(timedelta(hours=3))).isoformat(timespec='seconds')
    run = f'''\n\n## RUN {now} — Worker A

- state: `COMPLETE`
- start HEAD: `{START_HEAD}`
- evidence HEAD before handoff tooling: `{EVIDENCE_HEAD}`
- handoff-trigger HEAD: `{trigger_head}`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `{SOURCE_ID} — الفيزياء نماذج وزاريه 1447`
- completed in this run:
  - fetched live branch/baton first and verified the previous Physics 1446 handoff against live MASTER/manifests/evidence;
  - confirmed no active/running workflow for Physics 1447 before discovery/finalization;
  - technically verified **124/124** immutable RAW images with byte-size/SHA-256/MIME agreement, contiguous sequence **1..124**, **9** duplicate SHA groups preserved and **0** RAW mutations;
  - generated and visually inspected complete contact sheets covering all **124** pages;
  - independently resolved **31** source-local four-page occurrences, each three question pages followed by one correction/result-sheet candidate; all 124 pages finalized exactly once;
  - preserved the 9 SHA duplicate groups, which form three repeated question-sheet triplets, without collapsing complete occurrences solely from partial-page duplication;
  - finalized **31 Individual Exam Models / 124 Exam Pages**, **31 correction/result candidates**, **0 review-required pages**, and **0 verified standalone Answer Keys**;
  - structurally linked **255/255 legacy questions** to verified model membership; semantic correctness remains `NOT VERIFIED`;
  - updated canonical reconstruction, MASTER and evidence-backed status/handoff/inventory/validation/import/continuation files; no production import/publication was created;
  - discovery run `34909617398` and finalization run `34910199734` succeeded; finalization passed exact-live-HEAD gates before finalization, evidence write, and commit.
- evidence produced/verified:
  - `content-staging/reconstruction/technical/{SOURCE_ID}.json`;
  - `content-staging/reconstruction/exams/source-groups/{SOURCE_ID}-discovery.json`;
  - `content-staging/reconstruction/exams/source-groups/{SOURCE_ID}.json`;
  - discovery artifact `physics-exam-1447-discovery-evidence` id `10374510074`;
  - final artifact `physics-exam-1447-final-evidence` id `10374346533`;
  - canonical evidence commit `{EVIDENCE_HEAD}`.
- ambiguity/review_required:
  - source boundary ambiguity: none after complete visual review;
  - standalone official Answer Keys: `NOT VERIFIED`; correction/result pages remain candidates only;
  - official model codes/titles/term: `NOT VERIFIED`;
  - semantic correctness of all 255 legacy questions/answers: `NOT VERIFIED`.
- invariant result: PASS (`13,135 + 1,920 + 1,229 + 9,471 = 25,755`)
- Sources processed: 35/58
- Educational: 16/26
- Books / Units / Lessons / Lesson Pages: 14 / 57 / 328 / 1,527
- Exam Source Groups: 19/32
- Individual Exam Models: 356
- Exam Pages: 1,232/2,286
- Verified Answer Keys: 0
- Source images technical: 2,979/5,273
- WebP generated / accepted / rejected: 0 / 0 / 0
- Legacy Questions: 25,755
- Lesson-linked: 13,135
- Exam-linked: 1,920
- Review-required: 1,229
- Unclassified: 9,471
- Duplicate groups classified: 0/99
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `{SOURCE_ID} — الفيزياء نماذج وزاريه 1447`
- current source: `{NEXT_SOURCE_ID} — {next_name}`
- exact next operation: `Re-fetch live HEAD/baton; verify no active workflow for {NEXT_SOURCE_ID}; technically verify all 42 immutable RAW images; independently discover Arabic 1447 duplicate/model/correction boundaries from complete source-local evidence; do not inherit prior-source packet sizes; there are 0 legacy questions, so do not invent mappings; quarantine uncertainty as review_required/NOT VERIFIED; assert the 25,755 invariant; checkpoint.`
- next source: `Resolve only after Arabic 1447 finalization from live MASTER.`
- blockers: `none`
- handoff note: `Worker B should start only from {NEXT_SOURCE_ID} after re-fetching live HEAD and this baton. Do not rerun/finalize Physics 1447 absent fresh drift evidence and do not promote correction/result candidates to standalone official Answer Keys without explicit evidence.`
'''
    LOG_PATH.write_text(text.rstrip() + run + '\n', encoding='utf-8')
    print(json.dumps({'handoff_trigger_head': trigger_head, 'next_source_id': NEXT_SOURCE_ID, 'next_source_name': next_name, 'invariant': 25755}, ensure_ascii=False))


if __name__ == '__main__':
    main()
