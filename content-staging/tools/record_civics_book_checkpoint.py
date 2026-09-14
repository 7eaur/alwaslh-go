#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SID = '7f02b242-5164-46d1-a82d-7f1023cfa8c9'
RECON = ROOT / 'content-staging/reconstruction/educational' / f'{SID}.json'
MASTER = ROOT / 'content-staging/manifests/MASTER_CONTENT_MANIFEST.json'
MARK = 'CIVICS_BOOK_CHECKPOINT'
START = f'<!-- {MARK}_START -->'
END = f'<!-- {MARK}_END -->'


def replace_block(path: Path, body: str):
    text = path.read_text(encoding='utf-8')
    block = f'{START}\n{body.rstrip()}\n{END}'
    if START in text and END in text:
        before = text.split(START, 1)[0].rstrip()
        after = text.split(END, 1)[1].lstrip()
        text = before + '\n\n' + block + ('\n\n' + after if after else '\n')
    else:
        text = text.rstrip() + '\n\n' + block + '\n'
    path.write_text(text, encoding='utf-8')


r = json.loads(RECON.read_text(encoding='utf-8'))
if r.get('status') != 'reconstructed_verified':
    raise SystemExit('civics reconstruction is not verified')
book = r['reconstructed_book']
if r['source_identity']['raw_master_exact_sha_matches'] != 59 or book['retained_pages'] != 59:
    raise SystemExit('civics exact identity/page count gate failed')
if r['questions']['legacy_questions'] != 0:
    raise SystemExit('civics question count drift')

p = json.loads(MASTER.read_text(encoding='utf-8'))
progress = p.get('reconstruction_progress') or {}
expected = {
    'sources_completed': 13,
    'educational_sources_completed': 4,
    'verified_books': 4,
    'verified_units': 25,
    'verified_lessons': 119,
    'verified_lesson_pages': 460,
    'exam_source_groups_completed': 9,
    'individual_exam_models': 135,
    'exam_pages_completed': 455,
    'source_images_technically_verified': 1011,
    'lesson_linked_structural': 2374,
    'exam_linked_to_individual_model': 967,
    'review_required': 351,
    'unclassified': 22063,
}
for key, value in expected.items():
    if progress.get(key) != value:
        raise SystemExit(f'live progress drift before civics finalization: {key}={progress.get(key)} expected={value}')

source_index = next(i for i, x in enumerate(p['sources']) if x['id'] == SID)
s = p['sources'][source_index]
if s.get('review_status') not in (None, 'inventory_only', 'NOT VERIFIED', 'not_verified'):
    raise SystemExit(f'civics source already appears finalized: {s.get("review_status")}')
next_source = p['sources'][source_index + 1] if source_index + 1 < len(p['sources']) else None
next_id = next_source['id'] if next_source else 'NOT YET RESOLVED'
next_name = next_source['legacy_source']['name'] if next_source else 'NOT YET RESOLVED'

s['classification'] = 'educational_book_source'
s['classification_evidence'] = '59/59 unique exact RAW/master SHA identity + exact master section/title runs'
s['review_status'] = 'reconstructed_verified'
s['technical_verification'] = {
    'status': 'verified',
    'report_path': f'content-staging/reconstruction/technical/{SID}.json',
    'images_verified': 59,
    'readable': 59,
    'sha256_match_manifest': 59,
    'mime_match_manifest': 59,
    'duplicate_sha_groups_within_source': 0,
}
s['reconstruction'] = {
    'status': 'verified',
    'path': f'content-staging/reconstruction/educational/{SID}.json',
    'book_title': 'التربية الوطنية',
    'retained_page_range': r['source_identity']['stored_page_range'],
    'source_reference_page_range': r['source_identity']['source_reference_page_range'],
    'retained_pages': 59,
    'units': book['unit_count'],
    'lessons': book['lesson_count'],
    'lesson_pages': book['lesson_page_count'],
    'unit_cover_pages': book['unit_cover_page_count'],
    'unit_review_pages': book['unit_review_page_count'],
    'non_lesson_pages': book['non_lesson_page_count'],
    'legacy_questions': 0,
    'structurally_lesson_linked_questions': 0,
    'review_required_questions': 0,
    'semantic_question_review': 'NOT APPLICABLE',
    'raw_mutations': 0,
}

new_progress = dict(progress)
new_progress.update({
    'sources_completed': 14,
    'educational_sources_completed': 5,
    'verified_books': 5,
    'verified_units': 25 + book['unit_count'],
    'verified_lessons': 119 + book['lesson_count'],
    'verified_lesson_pages': 460 + book['lesson_page_count'],
    'source_images_technically_verified': 1070,
})
# Question and exam counters are unchanged for this zero-question educational source.
assert new_progress['lesson_linked_structural'] + new_progress['exam_linked_to_individual_model'] + new_progress['review_required'] + new_progress['unclassified'] == 25755
assert new_progress['source_images_technically_verified'] <= 5273
p['status'] = 'RECONSTRUCTION_IN_PROGRESS_NOT_IMPORT_READY'
p['reconstruction_progress'] = new_progress
MASTER.write_text(json.dumps(p, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

summary = f'''## Reconstruction checkpoint — Grade 9 Civics

- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Sources processed: **14/58**; Educational: **5/26**; Exam Source Groups: **9/32**.
- Books / Units / Lessons / Lesson pages: **5 / {new_progress['verified_units']} / {new_progress['verified_lessons']} / {new_progress['verified_lesson_pages']}**.
- Civics: **59/59** technically verified images and **59/59** unique exact RAW/master SHA identities.
- Exact retained mapping: stored pages **{r['source_identity']['stored_page_range'][0]}..{r['source_identity']['stored_page_range'][1]}** -> master source pages **{r['source_identity']['source_reference_page_range'][0]}..{r['source_identity']['source_reference_page_range'][1]}**.
- Reconstructed source: **1 Book, {book['unit_count']} Units, {book['lesson_count']} Lessons, {book['lesson_page_count']} Lesson pages, {book['unit_cover_page_count']} Unit-cover pages, {book['unit_review_page_count']} Unit-review pages, {book['non_lesson_page_count']} non-lesson pages**.
- Questions: source contains **0** legacy questions; no question records fabricated.
- Global questions unchanged: Lesson-linked **2,374**; Exam-linked **967**; Review-required **351**; Unclassified **22,063** = **25,755**.
- Individual Exam Models **135**; Exam Pages **455/2,286**; Verified Answer Keys **0**.
- Source images technical **1,070/5,273**; WebP **0/0/0**; Duplicate groups **0/99**.
- RAW / unrelated / imports / publications: **0/0/0/0**.
- Last completed: `{SID} — التربية الوطنية`.
- Next: `{next_id} — {next_name}`.
'''

replace_block(ROOT / 'content-staging/CONTENT_REBUILD_EXECUTION_STATUS.md', summary)
replace_block(ROOT / 'content-staging/CONTENT_REBUILD_HANDOFF.md', f'''## Active reconstruction handoff — Civics complete

- Last completed: `{SID} — التربية الوطنية`.
- Verified: **59/59** technical + unique exact master SHA identity; **{book['unit_count']} Units / {book['lesson_count']} Lessons / {book['lesson_page_count']} Lesson pages / {book['unit_cover_page_count']} covers / {book['unit_review_page_count']} reviews / {book['non_lesson_page_count']} non-lesson pages**.
- Questions: source contains **0 legacy questions**; no fabricated links; semantic question review `NOT APPLICABLE`.
- Current/next: `{next_id} — {next_name}`.
- Exact next operation: fetch that source's live manifest/pages, verify immutable media, then reconstruct only evidence-backed boundaries from its own exact source/master evidence.
- RAW/unrelated/import/publication mutations remain **0/0/0/0**.
''')
replace_block(ROOT / 'content-staging/CONTENT_INVENTORY.md', f'''## Verified reconstruction checkpoint — Grade 9 Civics

- Legacy source `{SID}` is exactly identified as `master/تاسع إجتماعيات/التربية_الوطنية_تاسع` for all **59 retained images** by SHA-256.
- Reconstructed structure: **{book['unit_count']} Units, {book['lesson_count']} Lessons, {book['lesson_page_count']} Lesson pages, {book['unit_cover_page_count']} Unit covers, {book['unit_review_page_count']} Unit reviews, {book['non_lesson_page_count']} non-lesson pages**.
- Source has **0** legacy questions in the verified manifest/pages dataset.
''')
replace_block(ROOT / 'content-staging/CONTENT_VALIDATION_REPORT.md', f'''## Grade 9 Civics reconstruction validation

- Technical verification: **59/59** files exist, readable, size/SHA/MIME match.
- Exact reference identity: **59/59** RAW images equal unique images in the exact Civics master reference by SHA-256.
- Structure: **{book['unit_count']} Units / {book['lesson_count']} Lessons / {book['lesson_page_count']} Lesson pages / {book['unit_cover_page_count']} covers / {book['unit_review_page_count']} reviews / {book['non_lesson_page_count']} non-lesson pages**; every retained page is classified exactly once.
- Questions: **0** source questions; no fabricated question links.
- RAW mutations: **0**.
''')
replace_block(ROOT / 'content-staging/CONTENT_IMPORT_REPORT.md', '''## Civics reconstruction checkpoint — no import performed

The reconstruction artifact is verified, but the corpus remains `RECONSTRUCTION_IN_PROGRESS_NOT_IMPORT_READY`.

- New imports: **0**; new publications: **0**; production mutations: **0**; RAW mutations: **0**.
- Import readiness remains deferred until corpus reconstruction/boundary discovery is complete.
''')
cont = ROOT / 'content-staging/CONTENT_REBUILD_CONTINUATION_2026-09-14.md'
if cont.exists():
    replace_block(cont, f'''## Continuation checkpoint — Civics complete

Continue with `{next_id} — {next_name}`; do not rerun Civics absent new drift evidence. Current verified global progress: **14/58 sources; 5/26 educational; 9/32 exam groups; 1,070/5,273 technical images; 2,374 lesson-linked; 967 exam-linked; 351 review-required; 22,063 unclassified**.
''')

print(json.dumps({
    'checkpoint': MARK,
    'sources': 14,
    'educational': 5,
    'books': 5,
    'units': new_progress['verified_units'],
    'lessons': new_progress['verified_lessons'],
    'lesson_pages': new_progress['verified_lesson_pages'],
    'images_verified': 1070,
    'next_source_id': next_id,
    'next_source_name': next_name,
    'invariant': 25755,
    'raw_mutations': 0,
}, ensure_ascii=False))
