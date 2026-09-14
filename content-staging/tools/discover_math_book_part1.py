#!/usr/bin/env python3
import hashlib,json,re
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SID='1933807f-4cb0-40c9-9b29-3ef3d32c98dc'
RAW=ROOT/'content-staging/raw/legacy-supabase/subjects'/SID
MASTER=ROOT/'master-reference/الرياضيات ثالث ثانوي/02_الرياضيات_ثالث_ثانوي'
OUT=ROOT/'content-staging/reconstruction/educational'/f'{SID}-discovery.json'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''): h.update(b)
 return h.hexdigest()
manifest=json.loads((RAW/'manifest.json').read_text(encoding='utf-8'))
pages=json.loads((RAW/'pages.json').read_text(encoding='utf-8'))
master=json.loads((MASTER/'manifest.json').read_text(encoding='utf-8'))
by_source={int(x['source_page']):x for x in master}
page_by_id={x['id']:x for x in pages}
rows=[]; failures=[]
sha_counts=Counter(x['sha256'] for x in manifest['images'])
for ordinal,im in enumerate(manifest['images'],1):
 obj=im.get('storage_object_path','')
 m=re.search(r'page_(\d+)\.',obj)
 source_page=int(m.group(1)) if m else None
 ref=by_source.get(source_page)
 raw=ROOT/'content-staging'/im['raw_path']
 master_file=MASTER/ref['relative_path'] if ref else None
 same=False
 if ref and raw.is_file() and master_file.is_file(): same=sha(raw)==sha(master_file)==im['sha256']
 if not same: failures.append({'ordinal':ordinal,'legacy_page_id':im['legacy_page_id'],'stored_page_number':im['page_number'],'source_page':source_page,'reason':'identity_mismatch_or_missing_reference'})
 pg=page_by_id.get(im['legacy_page_id'],{})
 rows.append({'ordinal':ordinal,'stored_page_number':im['page_number'],'source_page':source_page,'legacy_page_id':im['legacy_page_id'],'section':ref.get('section') if ref else None,'title':ref.get('title') if ref else None,'book_page':ref.get('book_page') if ref else None,'raw_sha256':im['sha256'],'master_relative_path':ref.get('relative_path') if ref else None,'exact_sha_identity':same,'legacy_question_count':len(pg.get('ai_questions') or [])})
sections=[]
for r in rows:
 if not sections or sections[-1]['section']!=r['section']:
  sections.append({'section':r['section'],'start_stored_page':r['stored_page_number'],'end_stored_page':r['stored_page_number'],'start_source_page':r['source_page'],'end_source_page':r['source_page'],'title_runs':[]})
 s=sections[-1]; s['end_stored_page']=r['stored_page_number']; s['end_source_page']=r['source_page']
 if not s['title_runs'] or s['title_runs'][-1]['title']!=r['title']:
  s['title_runs'].append({'title':r['title'],'start_stored_page':r['stored_page_number'],'end_stored_page':r['stored_page_number'],'start_source_page':r['source_page'],'end_source_page':r['source_page']})
 else:
  s['title_runs'][-1]['end_stored_page']=r['stored_page_number']; s['title_runs'][-1]['end_source_page']=r['source_page']
report={'schema_version':1,'operation':'math_book_part1_identity_and_structure_discovery','subject_id':SID,'source_name':'كتاب الرياضيات - الجزء الأول','classification':'educational_source','raw_image_count':len(manifest['images']),'legacy_question_count':sum(len((p.get('ai_questions') or [])) for p in pages),'master_reference_path':'الرياضيات ثالث ثانوي/02_الرياضيات_ثالث_ثانوي','master_manifest_entries':len(master),'matched_source_page_min':min(r['source_page'] for r in rows if r['source_page'] is not None),'matched_source_page_max':max(r['source_page'] for r in rows if r['source_page'] is not None),'exact_sha_identity_count':sum(1 for r in rows if r['exact_sha_identity']),'identity_failures':failures,'identity_status':'VERIFIED' if not failures and all(r['exact_sha_identity'] for r in rows) else 'NOT VERIFIED','within_source_duplicate_sha_groups':[{'sha256':k,'count':v} for k,v in sha_counts.items() if v>1],'sections':sections,'page_map':rows,'structure_status':'DISCOVERY_ONLY','note':'Sections and contiguous title runs are copied only after exact SHA identity to the trusted master reference. Final unit/lesson/review promotion requires a separate evidence-backed finalization pass.','raw_mutations':0}
OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'identity_status':report['identity_status'],'raw_images':report['raw_image_count'],'exact_sha_identity_count':report['exact_sha_identity_count'],'source_page_range':[report['matched_source_page_min'],report['matched_source_page_max']],'sections':len(sections),'title_runs':sum(len(s['title_runs']) for s in sections),'legacy_questions':report['legacy_question_count'],'duplicate_sha_groups':len(report['within_source_duplicate_sha_groups']),'output':str(OUT.relative_to(ROOT))},ensure_ascii=False))
if report['identity_status']!='VERIFIED': raise SystemExit(2)
