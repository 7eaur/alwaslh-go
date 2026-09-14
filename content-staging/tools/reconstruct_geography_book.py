#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SID = 'a7f1e94f-82d1-4146-af5b-4e9b51363f0b'
RAW = ROOT / 'content-staging/raw/legacy-supabase/subjects' / SID
MASTER = ROOT / 'master-reference/تاسع إجتماعيات/جغرافيا_تاسع'
OUT_DISC = ROOT / 'content-staging/reconstruction/educational' / f'{SID}-discovery.json'
OUT = ROOT / 'content-staging/reconstruction/educational' / f'{SID}.json'


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

manifest = json.loads((RAW / 'manifest.json').read_text(encoding='utf-8'))
pages = json.loads((RAW / 'pages.json').read_text(encoding='utf-8'))
master_manifest = json.loads((MASTER / 'manifest.json').read_text(encoding='utf-8'))

if manifest['counts']['pages'] != 104 or manifest['counts']['image_references'] != 104:
    raise SystemExit(f"unexpected geography source count: {manifest['counts']}")
if manifest['counts']['questions'] != 0:
    raise SystemExit('geography source unexpectedly contains legacy questions')
if any(manifest['anomalies'].get(k) for k in manifest['anomalies']):
    raise SystemExit(f"geography manifest anomalies must be reviewed first: {manifest['anomalies']}")

master_by_sha = {}
for ref in master_manifest:
    fp = MASTER / ref['relative_path']
    if not fp.is_file():
        raise SystemExit(f'missing master reference file: {fp}')
    digest = sha256(fp)
    master_by_sha.setdefault(digest, []).append((ref, fp))

page_by_id = {p['id']: p for p in pages}
page_map = []
for image in sorted(manifest['images'], key=lambda x: (x['page_number'], x['image_index'])):
    raw_file = ROOT / 'content-staging' / image['raw_path']
    actual = sha256(raw_file)
    if actual != image['sha256']:
        raise SystemExit(f"RAW SHA drift on stored page {image['page_number']}")
    matches = master_by_sha.get(actual, [])
    if len(matches) != 1:
        raise SystemExit(f"exact master identity not unique for stored page {image['page_number']}: {len(matches)} matches")
    ref, _ = matches[0]
    page = page_by_id.get(image['legacy_page_id'])
    if page is None:
        raise SystemExit(f"missing pages.json row for {image['legacy_page_id']}")
    page_map.append({
        'stored_page_number': image['page_number'],
        'legacy_page_id': image['legacy_page_id'],
        'raw_sha256': actual,
        'source_page': ref['source_page'],
        'book_page': ref.get('book_page'),
        'section': ref.get('section'),
        'title': ref.get('title'),
        'master_relative_path': ref['relative_path'],
        'legacy_question_count': len(page.get('ai_questions') or []),
        'content_equivalence_verified': True,
    })

if len(page_map) != 104:
    raise SystemExit('geography exact identity count is not 104')
stored = [r['stored_page_number'] for r in page_map]
source = [r['source_page'] for r in page_map]
if stored != list(range(min(stored), max(stored) + 1)):
    raise SystemExit('stored geography pages are not contiguous')
if source != list(range(min(source), max(source) + 1)):
    raise SystemExit('master geography source pages are not contiguous')
if any(r['legacy_question_count'] for r in page_map):
    raise SystemExit('pages.json contains unexpected geography AI questions')

sections = []
for row in page_map:
    if not sections or sections[-1]['section'] != row['section']:
        sections.append({
            'section': row['section'],
            'start_stored_page': row['stored_page_number'],
            'end_stored_page': row['stored_page_number'],
            'start_source_page': row['source_page'],
            'end_source_page': row['source_page'],
            'titles': [],
        })
    sec = sections[-1]
    sec['end_stored_page'] = row['stored_page_number']
    sec['end_source_page'] = row['source_page']
    if not sec['titles'] or sec['titles'][-1]['title'] != row['title']:
        sec['titles'].append({
            'title': row['title'],
            'start_stored_page': row['stored_page_number'],
            'end_stored_page': row['stored_page_number'],
            'start_source_page': row['source_page'],
            'end_source_page': row['source_page'],
        })
    else:
        sec['titles'][-1]['end_stored_page'] = row['stored_page_number']
        sec['titles'][-1]['end_source_page'] = row['source_page']

units = []
lessons = []
lesson_pages = []
unit_cover_pages = []
unit_review_pages = []
non_lesson_pages = []

for sec in sections:
    label = sec['section'] or ''
    if not label.startswith('الوحدة'):
        non_lesson_pages.extend(range(sec['start_stored_page'], sec['end_stored_page'] + 1))
        continue
    runs = sec['titles']
    if not runs:
        raise SystemExit(f'empty title runs for {label}')
    cover = runs[0]
    if cover['start_stored_page'] != cover['end_stored_page']:
        raise SystemExit(f'unit cover is not a single exact title run page: {label}')
    unit_cover_pages.append(cover['start_stored_page'])
    unit_lessons = []
    reviews = []
    for run in runs[1:]:
        start, end = run['start_stored_page'], run['end_stored_page']
        pages_run = list(range(start, end + 1))
        title = run['title'] or ''
        if title.startswith('تقويم الوحدة') or title.startswith('مراجعة الوحدة'):
            unit_review_pages.extend(pages_run)
            reviews.extend(pages_run)
            continue
        lesson = {
            'id': f'geography9-u{len(units)+1:02d}-l{len(unit_lessons)+1:02d}',
            'unit_ordinal': len(units) + 1,
            'lesson_ordinal': len(unit_lessons) + 1,
            'title': title,
            'stored_page_range': [start, end],
            'stored_pages': pages_run,
            'source_page_range': [run['start_source_page'], run['end_source_page']],
            'legacy_page_ids': [next(r['legacy_page_id'] for r in page_map if r['stored_page_number'] == p) for p in pages_run],
            'legacy_question_count': 0,
            'boundary_status': 'verified_exact_master_title_run',
        }
        unit_lessons.append(lesson)
        lessons.append(lesson)
        lesson_pages.extend(pages_run)
    units.append({
        'ordinal': len(units) + 1,
        'title': label.split(':', 1)[1].strip() if ':' in label else label,
        'section_label': label,
        'stored_page_range': [sec['start_stored_page'], sec['end_stored_page']],
        'source_page_range': [sec['start_source_page'], sec['end_source_page']],
        'cover_page': cover['start_stored_page'],
        'review_pages': reviews,
        'lessons': unit_lessons,
    })

assigned = set(lesson_pages) | set(unit_cover_pages) | set(unit_review_pages) | set(non_lesson_pages)
if assigned != set(stored):
    raise SystemExit(f'geography page classification mismatch: missing={sorted(set(stored)-assigned)} extra={sorted(assigned-set(stored))}')
if len(assigned) != len(lesson_pages) + len(unit_cover_pages) + len(unit_review_pages) + len(non_lesson_pages):
    raise SystemExit('geography page classifications overlap')
if not units or not lessons:
    raise SystemExit('geography structure did not yield explicit units/lessons; manual review required')

master_only = sorted(set(r['source_page'] for r in master_manifest) - set(source))
discovery = {
    'schema_version': 1,
    'operation': 'geography_exact_master_identity_and_structure_discovery',
    'subject_id': SID,
    'source_name': 'كتاب الجغرافيا',
    'classification': 'educational_book_source',
    'raw_image_count': 104,
    'raw_sha_verified_count': 104,
    'master_reference_path': 'master/تاسع إجتماعيات/جغرافيا_تاسع',
    'master_manifest_entries': len(master_manifest),
    'exact_sha_identity_count': 104,
    'identity_status': 'VERIFIED',
    'stored_page_range': [min(stored), max(stored)],
    'source_reference_page_range': [min(source), max(source)],
    'master_only_source_pages_outside_retained_slice': master_only,
    'page_map': page_map,
    'sections': sections,
    'semantic_question_review': 'NOT APPLICABLE',
    'raw_mutations': 0,
}
OUT_DISC.parent.mkdir(parents=True, exist_ok=True)
OUT_DISC.write_text(json.dumps(discovery, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

report = {
    'schema_version': 1,
    'status': 'reconstructed_verified',
    'subject_id': SID,
    'source_name': 'كتاب الجغرافيا',
    'classification': 'educational_book_source',
    'source_identity': {
        'status': 'verified',
        'master_reference_path': discovery['master_reference_path'],
        'raw_master_exact_sha_matches': 104,
        'raw_images': 104,
        'stored_page_range': discovery['stored_page_range'],
        'source_reference_page_range': discovery['source_reference_page_range'],
        'master_manifest_entries': len(master_manifest),
        'master_only_source_pages_outside_retained_slice': master_only,
    },
    'reconstructed_book': {
        'title': 'كتاب الجغرافيا',
        'units': units,
        'unit_count': len(units),
        'lesson_count': len(lessons),
        'lesson_page_count': len(lesson_pages),
        'unit_cover_page_count': len(unit_cover_pages),
        'unit_review_page_count': len(unit_review_pages),
        'non_lesson_page_count': len(non_lesson_pages),
        'retained_pages': 104,
        'legacy_retained_page_range': discovery['stored_page_range'],
        'source_reference_page_range': discovery['source_reference_page_range'],
    },
    'page_classification': {
        'lesson_pages': lesson_pages,
        'unit_cover_pages': unit_cover_pages,
        'unit_review_pages': unit_review_pages,
        'non_lesson_pages': non_lesson_pages,
    },
    'questions': {
        'legacy_questions': 0,
        'structurally_lesson_linked_questions': 0,
        'review_required_questions': 0,
        'semantic_question_review': 'NOT APPLICABLE',
        'links': [],
    },
    'evidence': [
        '104/104 retained RAW images must be byte-identical by SHA-256 to unique images in the exact Geography master reference.',
        'Unit/lesson/review boundaries are derived only from exact master section/title runs after identity succeeds.',
        'The retained source contains 0 legacy AI questions; no question records are fabricated.',
    ],
    'raw_mutations': 0,
}
OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({
    'status': report['status'], 'images': 104,
    'stored_range': discovery['stored_page_range'],
    'source_range': discovery['source_reference_page_range'],
    'units': len(units), 'lessons': len(lessons),
    'lesson_pages': len(lesson_pages), 'covers': len(unit_cover_pages),
    'reviews': len(unit_review_pages), 'non_lesson': len(non_lesson_pages), 'questions': 0,
}, ensure_ascii=False))
