#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
from PIL import Image
import imagehash

ROOT=Path(__file__).resolve().parents[2]
SID='0a76f44b-0a4f-4e36-9ea9-badecf78bf23'
RAW=ROOT/'content-staging/raw/legacy-supabase/subjects'/SID
MASTER_ROOT=ROOT/'master-reference/تاسع إجتماعيات'
MASTER_PARTS=[('part1',MASTER_ROOT/'تاريخ_تاسع_الجزء_الأول'),('part2',MASTER_ROOT/'تاريخ_تاسع_الجزء_الثاني')]
OUT=ROOT/'content-staging/reconstruction/educational'/f'{SID}-discovery.json'

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''): h.update(b)
 return h.hexdigest()
def hashes(p):
 with Image.open(p) as im:
  rgb=im.convert('RGB')
  return imagehash.phash(rgb), imagehash.dhash(rgb), imagehash.whash(rgb)
def score(a,b):
 return (int(a[0]-b[0]),int(a[1]-b[1]),int(a[2]-b[2]))

def total(s): return s[0]+s[1]+s[2]

manifest=json.loads((RAW/'manifest.json').read_text(encoding='utf-8'))
pages=json.loads((RAW/'pages.json').read_text(encoding='utf-8'))
page_by_id={x['id']:x for x in pages}
master_rows=[]
for part,base in MASTER_PARTS:
 for ref in json.loads((base/'manifest.json').read_text(encoding='utf-8')):
  fp=base/ref['relative_path']
  if fp.is_file():
   master_rows.append({'part':part,'base':base,**ref,'file':fp,'sha256':sha(fp),'hashes':hashes(fp)})

rows=[]
for im in manifest['images']:
 raw=ROOT/'content-staging'/im['raw_path']; actual=sha(raw); rh=hashes(raw)
 ranked=[]
 for ref in master_rows:
  sc=score(rh,ref['hashes'])
  ranked.append((total(sc),sc,ref))
 ranked.sort(key=lambda x:(x[0],x[1],x[2]['part'],x[2]['source_page']))
 top=ranked[:5]; best=top[0]; second=top[1] if len(top)>1 else None
 pg=page_by_id.get(im['legacy_page_id'],{})
 rows.append({'stored_page_number':im['page_number'],'legacy_page_id':im['legacy_page_id'],'raw_sha256':im['sha256'],'raw_sha_verified':actual==im['sha256'],'legacy_question_count':len(pg.get('ai_questions') or []),'top_candidates':[{'part':x[2]['part'],'source_page':x[2]['source_page'],'book_page':x[2]['book_page'],'section':x[2]['section'],'title':x[2]['title'],'relative_path':x[2]['relative_path'],'phash_distance':x[1][0],'dhash_distance':x[1][1],'whash_distance':x[1][2],'combined_distance':x[0],'exact_sha':actual==x[2]['sha256']} for x in top],'best_part':best[2]['part'],'best_source_page':best[2]['source_page'],'best_book_page':best[2]['book_page'],'best_section':best[2]['section'],'best_title':best[2]['title'],'best_relative_path':best[2]['relative_path'],'best_combined_distance':best[0],'runner_up_combined_distance':second[0] if second else None,'best_exact_sha':actual==best[2]['sha256']})

# Sequence evidence: find whether best candidates form a single-part monotonic consecutive run.
ordered=sorted(rows,key=lambda r:r['stored_page_number'])
parts=[r['best_part'] for r in ordered]; src=[r['best_source_page'] for r in ordered]
one_part=len(set(parts))==1
consecutive=all(src[i+1]==src[i]+1 for i in range(len(src)-1)) if src else False
best_distances=[r['best_combined_distance'] for r in ordered]
runner_margins=[(r['runner_up_combined_distance']-r['best_combined_distance']) for r in ordered if r['runner_up_combined_distance'] is not None]
# Conservative automatic verification: exact monotonic sequence in one part AND every page has a clearly better candidate.
strong_pages=[r for r in ordered if r['best_combined_distance']<=24 and (r['runner_up_combined_distance'] is None or r['runner_up_combined_distance']-r['best_combined_distance']>=4)]
sequence_verified=one_part and consecutive and len(strong_pages)==len(ordered)

mapped=[]
if sequence_verified:
 for r in ordered:
  ref=next(x for x in master_rows if x['part']==r['best_part'] and x['source_page']==r['best_source_page'])
  mapped.append({**r,'master_part':ref['part'],'source_page':ref['source_page'],'book_page':ref['book_page'],'section':ref['section'],'title':ref['title'],'master_relative_path':ref['relative_path'],'content_equivalence_verified':True})
else:
 for r in ordered: mapped.append({**r,'master_part':None,'source_page':None,'book_page':None,'section':None,'title':None,'master_relative_path':None,'content_equivalence_verified':False})

parts_summary={}
if sequence_verified:
 part=parts[0]
 runs=[]
 for r in mapped:
  key=(r['section'],r['title'])
  if not runs or runs[-1]['key']!=key or r['source_page']!=runs[-1]['end_source_page']+1:
   runs.append({'key':key,'section':r['section'],'title':r['title'],'start_source_page':r['source_page'],'end_source_page':r['source_page'],'stored_pages':[r['stored_page_number']],'legacy_question_count':r['legacy_question_count']})
  else:
   runs[-1]['end_source_page']=r['source_page']; runs[-1]['stored_pages'].append(r['stored_page_number']); runs[-1]['legacy_question_count']+=r['legacy_question_count']
 for x in runs: x.pop('key',None)
 parts_summary[part]={'matched_pages':len(mapped),'source_page_min':src[0],'source_page_max':src[-1],'title_runs':runs}

report={'schema_version':3,'operation':'history_book_global_visual_identity_and_structure_discovery','subject_id':SID,'source_name':'التاريخ الكتاب المدرسي','classification':'educational_source','raw_image_count':len(rows),'legacy_question_count':sum(len((p.get('ai_questions') or [])) for p in pages),'raw_sha_verified_count':sum(1 for r in rows if r['raw_sha_verified']),'master_reference_images_indexed':len(master_rows),'exact_master_sha_count':sum(1 for r in rows if r['best_exact_sha']),'global_matching':{'one_part_best_matches':one_part,'best_match_part':parts[0] if one_part and parts else None,'best_source_pages_consecutive':consecutive,'best_source_page_min':min(src) if src else None,'best_source_page_max':max(src) if src else None,'max_best_combined_distance':max(best_distances) if best_distances else None,'min_runner_up_margin':min(runner_margins) if runner_margins else None,'strong_page_count':len(strong_pages),'sequence_verified':sequence_verified},'content_equivalence_verified_count':len(mapped) if sequence_verified else 0,'identity_status':'VERIFIED' if sequence_verified else 'NOT VERIFIED','identity_method':'global pHash+dHash+wHash ranking across every page in both trusted master History parts, then monotonic-sequence and candidate-margin gate','matched_parts':parts_summary,'page_map':mapped,'lesson_boundaries_status':'NOT VERIFIED','semantic_question_review':'NOT VERIFIED','raw_mutations':0}
OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'identity_status':report['identity_status'],'raw_images':len(rows),'raw_sha_verified':report['raw_sha_verified_count'],'exact_master_sha':report['exact_master_sha_count'],'content_equivalence_verified':report['content_equivalence_verified_count'],'global_matching':report['global_matching'],'legacy_questions':report['legacy_question_count']},ensure_ascii=False))
