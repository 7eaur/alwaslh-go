#!/usr/bin/env python3
import hashlib,json
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
SID='0a76f44b-0a4f-4e36-9ea9-badecf78bf23'
RAW=ROOT/'content-staging/raw/legacy-supabase/subjects'/SID
MASTER_ROOT=ROOT/'master-reference/تاسع إجتماعيات'
MASTER_PARTS=[
 ('part1',MASTER_ROOT/'تاريخ_تاسع_الجزء_الأول'),
 ('part2',MASTER_ROOT/'تاريخ_تاسع_الجزء_الثاني'),
]
OUT=ROOT/'content-staging/reconstruction/educational'/f'{SID}-discovery.json'

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''): h.update(b)
 return h.hexdigest()

manifest=json.loads((RAW/'manifest.json').read_text(encoding='utf-8'))
pages=json.loads((RAW/'pages.json').read_text(encoding='utf-8'))
page_by_id={x['id']:x for x in pages}

master_rows=[]
for part,base in MASTER_PARTS:
 m=json.loads((base/'manifest.json').read_text(encoding='utf-8'))
 for row in m:
  fp=base/row['relative_path']
  if not fp.is_file():
   continue
  master_rows.append({**row,'part':part,'master_path':str((Path('تاسع إجتماعيات')/base.name/row['relative_path']).as_posix()),'sha256':sha(fp)})

by_sha=defaultdict(list)
for r in master_rows: by_sha[r['sha256']].append(r)

rows=[]; failures=[]; ambiguities=[]
for im in manifest['images']:
 raw=ROOT/'content-staging'/im['raw_path']
 actual=sha(raw) if raw.is_file() else None
 candidates=by_sha.get(actual,[]) if actual else []
 exact_manifest=(actual==im['sha256'])
 unique=(len(candidates)==1)
 ref=candidates[0] if unique else None
 if not exact_manifest or not unique:
  failures.append({'legacy_page_id':im['legacy_page_id'],'stored_page_number':im['page_number'],'manifest_sha256':im['sha256'],'actual_sha256':actual,'master_match_count':len(candidates),'reason':'raw_manifest_mismatch' if not exact_manifest else 'master_identity_not_unique'})
 if len(candidates)>1:
  ambiguities.append({'legacy_page_id':im['legacy_page_id'],'stored_page_number':im['page_number'],'matches':[{'part':x['part'],'source_page':x['source_page'],'title':x['title']} for x in candidates]})
 pg=page_by_id.get(im['legacy_page_id'],{})
 rows.append({
  'stored_page_number':im['page_number'],'legacy_page_id':im['legacy_page_id'],'raw_sha256':im['sha256'],
  'exact_raw_manifest_sha':exact_manifest,'master_unique_identity':unique,
  'master_part':ref['part'] if ref else None,'source_page':ref['source_page'] if ref else None,'book_page':ref['book_page'] if ref else None,
  'section':ref['section'] if ref else None,'title':ref['title'] if ref else None,'master_relative_path':ref['master_path'] if ref else None,
  'legacy_question_count':len(pg.get('ai_questions') or [])
 })

matched=[r for r in rows if r['master_unique_identity'] and r['exact_raw_manifest_sha']]
parts={}
for part,_ in MASTER_PARTS:
 pr=[r for r in matched if r['master_part']==part]
 if not pr: continue
 pr=sorted(pr,key=lambda x:(x['source_page'],x['stored_page_number']))
 runs=[]
 for r in pr:
  key=(r['section'],r['title'])
  if not runs or runs[-1]['key']!=key or r['source_page']!=runs[-1]['end_source_page']+1:
   runs.append({'key':key,'section':r['section'],'title':r['title'],'start_source_page':r['source_page'],'end_source_page':r['source_page'],'stored_pages':[r['stored_page_number']], 'legacy_question_count':r['legacy_question_count']})
  else:
   runs[-1]['end_source_page']=r['source_page']; runs[-1]['stored_pages'].append(r['stored_page_number']); runs[-1]['legacy_question_count']+=r['legacy_question_count']
 for x in runs: x.pop('key',None)
 parts[part]={'matched_pages':len(pr),'source_page_min':min(r['source_page'] for r in pr),'source_page_max':max(r['source_page'] for r in pr),'title_runs':runs}

report={
 'schema_version':1,'operation':'history_book_exact_identity_and_structure_discovery','subject_id':SID,'source_name':'التاريخ الكتاب المدرسي','classification':'educational_source',
 'raw_image_count':len(manifest['images']),'legacy_question_count':sum(len((p.get('ai_questions') or [])) for p in pages),
 'master_reference_paths':['تاسع إجتماعيات/تاريخ_تاسع_الجزء_الأول','تاسع إجتماعيات/تاريخ_تاسع_الجزء_الثاني'],
 'master_reference_images_indexed':len(master_rows),'exact_sha_identity_count':len(matched),'identity_failures':failures,'identity_ambiguities':ambiguities,
 'identity_status':'VERIFIED' if len(matched)==len(manifest['images']) and not failures and not ambiguities else 'NOT VERIFIED',
 'matched_parts':parts,'page_map':rows,'lesson_boundaries_status':'NOT VERIFIED',
 'semantic_question_review':'NOT VERIFIED','note':'Exact SHA identity against both trusted History master parts. Section/title runs are discovery evidence only until final boundary classification.','raw_mutations':0
}
OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'identity_status':report['identity_status'],'raw_images':report['raw_image_count'],'exact_sha_identity_count':report['exact_sha_identity_count'],'parts':{k:{'matched_pages':v['matched_pages'],'source_page_range':[v['source_page_min'],v['source_page_max']]} for k,v in parts.items()},'legacy_questions':report['legacy_question_count'],'output':str(OUT.relative_to(ROOT))},ensure_ascii=False))
if report['identity_status']!='VERIFIED': raise SystemExit(2)
