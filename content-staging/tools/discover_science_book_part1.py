#!/usr/bin/env python3
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SID='f4b6708c-027f-4883-9e85-e6e7acb52ecc'
RAW=ROOT/'content-staging/raw/legacy-supabase/subjects'/SID
MASTER=ROOT/'master-reference/تاسع علوم/علوم_تاسع_الجزء_الأول'
OUT=ROOT/'content-staging/reconstruction/educational'/f'{SID}-discovery.json'
def sha(p):
 h=hashlib.sha256();
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''): h.update(b)
 return h.hexdigest()
manifest=json.loads((RAW/'manifest.json').read_text(encoding='utf-8'))
pages=json.loads((RAW/'pages.json').read_text(encoding='utf-8'))
master=json.loads((MASTER/'manifest.json').read_text(encoding='utf-8'))
by_source={int(x['source_page']):x for x in master}
page_by_id={x['id']:x for x in pages}
rows=[]; failures=[]
for im in manifest['images']:
 obj=im.get('storage_object_path','')
 m=re.search(r'page_(\d+)\.',obj)
 source_page=int(m.group(1)) if m else None
 ref=by_source.get(source_page)
 raw=ROOT/'content-staging'/im['raw_path']
 master_file=MASTER/ref['relative_path'] if ref else None
 same=False
 if ref and raw.is_file() and master_file.is_file(): same=sha(raw)==sha(master_file)==im['sha256']
 if not same: failures.append({'legacy_page_id':im['legacy_page_id'],'stored_page_number':im['page_number'],'source_page':source_page,'reason':'identity_mismatch_or_missing_reference'})
 pg=page_by_id.get(im['legacy_page_id'],{})
 rows.append({'stored_page_number':im['page_number'],'source_page':source_page,'legacy_page_id':im['legacy_page_id'],'section':ref.get('section') if ref else None,'title':ref.get('title') if ref else None,'book_page':ref.get('book_page') if ref else None,'raw_sha256':im['sha256'],'master_relative_path':ref.get('relative_path') if ref else None,'exact_sha_identity':same,'legacy_question_count':len(pg.get('ai_questions') or [])})
sections=[]
for r in rows:
 if not sections or sections[-1]['section']!=r['section']:
  sections.append({'section':r['section'],'start_stored_page':r['stored_page_number'],'end_stored_page':r['stored_page_number'],'start_source_page':r['source_page'],'end_source_page':r['source_page'],'titles':[]})
 s=sections[-1]; s['end_stored_page']=r['stored_page_number']; s['end_source_page']=r['source_page']
 if r['title'] and (not s['titles'] or s['titles'][-1]['title']!=r['title']): s['titles'].append({'title':r['title'],'start_stored_page':r['stored_page_number'],'end_stored_page':r['stored_page_number']})
 else:
  if s['titles']: s['titles'][-1]['end_stored_page']=r['stored_page_number']
report={'schema_version':1,'operation':'science_book_part1_identity_and_structure_discovery','subject_id':SID,'source_name':'كتاب العلوم - الجزء الأول','classification':'educational_source','raw_image_count':len(manifest['images']),'legacy_question_count':sum(len((p.get('ai_questions') or [])) for p in pages),'master_reference_path':'تاسع علوم/علوم_تاسع_الجزء_الأول','master_manifest_entries':len(master),'matched_source_page_min':min(r['source_page'] for r in rows if r['source_page'] is not None),'matched_source_page_max':max(r['source_page'] for r in rows if r['source_page'] is not None),'exact_sha_identity_count':sum(1 for r in rows if r['exact_sha_identity']),'identity_failures':failures,'identity_status':'VERIFIED' if not failures and all(r['exact_sha_identity'] for r in rows) else 'NOT VERIFIED','sections':sections,'page_map':rows,'lesson_boundaries_status':'NOT VERIFIED','note':'Section/title runs are evidence-backed discovery candidates from exact master identity. They are not automatically promoted to finalized Lesson boundaries.','raw_mutations':0}
OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'identity_status':report['identity_status'],'raw_images':report['raw_image_count'],'exact_sha_identity_count':report['exact_sha_identity_count'],'source_page_range':[report['matched_source_page_min'],report['matched_source_page_max']],'sections':len(sections),'legacy_questions':report['legacy_question_count'],'output':str(OUT.relative_to(ROOT))},ensure_ascii=False))
if report['identity_status']!='VERIFIED': raise SystemExit(2)
