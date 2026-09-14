#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SID = 'a7f1e94f-82d1-4146-af5b-4e9b51363f0b'
NEXT_ID = '516f1c1d-acc0-4b1c-8e50-8f92a7c737e0'
LOG = ROOT / 'content-staging/CONTENT_RECONSTRUCTION_AUTOMATION_LOG.md'
MASTER = ROOT / 'content-staging/manifests/MASTER_CONTENT_MANIFEST.json'

p = json.loads(MASTER.read_text(encoding='utf-8'))
x = p['reconstruction_progress']
expected = {
    'sources_completed': 15,
    'educational_sources_completed': 6,
    'verified_books': 6,
    'verified_units': 33,
    'verified_lessons': 151,
    'verified_lesson_pages': 602,
    'source_images_technically_verified': 1174,
    'lesson_linked_structural': 2374,
    'exam_linked_to_individual_model': 967,
    'review_required': 351,
    'unclassified': 22063,
}
for k, v in expected.items():
    if x.get(k) != v:
        raise SystemExit(f'geography handoff progress drift: {k}={x.get(k)} expected={v}')
if x['lesson_linked_structural'] + x['exam_linked_to_individual_model'] + x['review_required'] + x['unclassified'] != 25755:
    raise SystemExit('global question invariant failed')
if any(x.get(k) != 0 for k in ('raw_mutations', 'unrelated_mutations', 'new_imports', 'new_publications')):
    raise SystemExit('mutation invariant failed')

r = json.loads((ROOT / f'content-staging/reconstruction/educational/{SID}.json').read_text(encoding='utf-8'))
if r['status'] != 'reconstructed_verified' or r['source_identity']['raw_master_exact_sha_matches'] != 104:
    raise SystemExit('geography reconstruction identity not verified')
b = r['reconstructed_book']
if (b['unit_count'], b['lesson_count'], b['lesson_page_count'], b['unit_cover_page_count'], b['unit_review_page_count'], b['non_lesson_page_count']) != (4, 18, 94, 4, 6, 0):
    raise SystemExit('geography structure drift')

nm = json.loads((ROOT / f'content-staging/raw/legacy-supabase/subjects/{NEXT_ID}/manifest.json').read_text(encoding='utf-8'))
if nm['counts']['pages'] != 65 or nm['counts']['image_references'] != 65 or nm['counts']['questions'] != 976 or nm['counts']['image_download_failures'] != 0:
    raise SystemExit(f'next-source baseline drift: {nm["counts"]}')
if any(nm['anomalies'].get(k) for k in nm['anomalies']):
    raise SystemExit(f'next-source anomalies changed: {nm["anomalies"]}')

text = LOG.read_text(encoding='utf-8')
if '## RUN 2026-09-14T14:02:00+03:00 — Worker B' in text:
    raise SystemExit('Worker B geography RUN already present; fail closed')

checkpoint = '''## 10. ACTIVE CHECKPOINT

- state: `COMPLETE`
- branch: `content/corpus-inventory-20260914`
- latest verified work HEAD before this handoff commit: `8c93e3846375ec0188c938dcc3fd8e1f25c83e6e`
- last completed source: `a7f1e94f-82d1-4146-af5b-4e9b51363f0b — كتاب الجغرافيا`
- current source: `516f1c1d-acc0-4b1c-8e50-8f92a7c737e0 — الإيمان الكتاب المدرسي`
- current source baseline from live evidence: `65 pages / 65 image references / 976 legacy questions / 0 image download failures; manifest anomaly arrays are empty. Technical byte/SHA/MIME verification, exact identity and lesson/question boundaries are NOT VERIFIED.`
- current operation: `Geography finalized from exact evidence: 104/104 technical images and 104/104 unique exact SHA identities against master/تاسع إجتماعيات/جغرافيا_تاسع; retained stored/source pages 8..111; 4 units, 18 lessons, 94 lesson pages, 4 unit covers, 6 unit reviews, 0 legacy questions. Next: technically verify الإيمان's 65 immutable images, establish exact identity only from its own evidence, reconstruct its book/unit/lesson/review boundaries, and structurally map the 976 questions only where page membership is proven; semantic correctness remains NOT VERIFIED.`
- next source: `NOT YET RESOLVED — derive after الإيمان الكتاب المدرسي from live MASTER_CONTENT_MANIFEST`
- blockers: `none`
- owner decision required now: `no`
'''
pattern = r'## 10\. ACTIVE CHECKPOINT\n.*?\n---\n\n### Shared handoff rule'
replacement = checkpoint + '\n---\n\n### Shared handoff rule'
new, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
if count != 1:
    raise SystemExit(f'ACTIVE CHECKPOINT replacement count={count}')

run = '''

## RUN 2026-09-14T14:02:00+03:00 — Worker B

- state: COMPLETE
- start HEAD: `16064f06bf374f9b0875e6690a12775757fd45a8`
- end HEAD before handoff-log commit: `8c93e3846375ec0188c938dcc3fd8e1f25c83e6e`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `a7f1e94f-82d1-4146-af5b-4e9b51363f0b — كتاب الجغرافيا`
- completed in this run:
  - verified Worker A's Civics completion against the live branch, baton and canonical status evidence;
  - confirmed Geography baseline at 104 pages/images, 0 legacy questions and no manifest anomalies;
  - added a source-local fail-closed Geography reconstruction tool and exact-head finalization workflow;
  - technically verified 104/104 immutable RAW images without mutation;
  - established 104/104 unique exact SHA-256 identities against `master/تاسع إجتماعيات/جغرافيا_تاسع`;
  - proved the retained contiguous slice is stored/source pages 8..111; master-only pages 1..7 and 112..114 remain reference-only;
  - reconstructed 4 Units / 18 Lessons / 94 Lesson pages / 4 Unit covers / 6 Unit reviews / 0 non-lesson pages from exact section/title runs;
  - classified every retained page exactly once and preserved the zero-question source without fabrication;
  - updated MASTER_CONTENT_MANIFEST and canonical status/inventory/validation/import/continuation evidence;
  - GitHub Actions run `34835911183` completed successfully and pushed the verified checkpoint commit.
- evidence produced/verified:
  - `content-staging/reconstruction/technical/a7f1e94f-82d1-4146-af5b-4e9b51363f0b.json`;
  - `content-staging/reconstruction/educational/a7f1e94f-82d1-4146-af5b-4e9b51363f0b-discovery.json`;
  - `content-staging/reconstruction/educational/a7f1e94f-82d1-4146-af5b-4e9b51363f0b.json`;
  - exact reference: `master/تاسع إجتماعيات/جغرافيا_تاسع`;
  - workflow run `34835911183`: success; final checkpoint commit `8c93e3846375ec0188c938dcc3fd8e1f25c83e6e`;
  - next source manifest: 65 pages/images, 976 questions, 0 download failures, empty anomaly arrays.
- ambiguity/review_required:
  - Geography structural ambiguity requiring quarantine: 0;
  - Geography source questions: 0; semantic review `NOT APPLICABLE`;
  - الإيمان identity, structure, question semantics and page-to-lesson mapping remain `NOT VERIFIED` until its own evidence gates pass.
- invariant result: PASS (`2,374 + 967 + 351 + 22,063 = 25,755`)
- Sources processed: 15/58
- Educational: 6/26
- Books / Units / Lessons / Lesson Pages: 6 / 33 / 151 / 602
- Exam Source Groups: 9/32
- Individual Exam Models: 135
- Exam Pages: 455/2,286
- Verified Answer Keys: 0
- Source images technical: 1,174/5,273
- WebP generated / accepted / rejected: 0 / 0 / 0
- Legacy Questions: 25,755
- Lesson-linked: 2,374
- Exam-linked: 967
- Review-required: 351
- Unclassified: 22,063
- Duplicate groups classified: 0/99
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `a7f1e94f-82d1-4146-af5b-4e9b51363f0b — كتاب الجغرافيا`
- current source: `516f1c1d-acc0-4b1c-8e50-8f92a7c737e0 — الإيمان الكتاب المدرسي`
- exact next operation: `Fetch the live الإيمان manifest/pages and any explicit master candidate; technically verify all 65 images and source-local sequence/SHA/MIME; require exact/source evidence before accepting master equivalence; reconstruct book/unit/lesson/review boundaries only from proven evidence; structurally map all 976 questions only where their source-page membership proves a lesson or review location; use review_required/NOT VERIFIED for unresolved evidence; assert the 25,755 invariant; checkpoint.`
- next source: `NOT YET RESOLVED — derive only after الإيمان الكتاب المدرسي from live MASTER_CONTENT_MANIFEST`
- blockers: `none`
- handoff note: `Worker A must re-fetch live HEAD and baton, verify Geography checkpoint 8c93e384..., then start الإيمان from its own evidence. Do not inherit Geography/Civics title-run assumptions unless the Faith source proves the same structure.`
'''
LOG.write_text(new.rstrip() + run + '\n', encoding='utf-8')
print('WORKER_B_GEOGRAPHY_HANDOFF_READY')
