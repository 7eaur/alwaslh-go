#!/usr/bin/env python3
import hashlib,json,re
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
def ph(p):
 with Image.open(p) as im: return imagehash.phash(im.convert('RGB'))

manifest=json.loads((RAW/'manifest.json').read_text(encoding='utf-8'))
pages=json.loads((RAW/'pages.json').read_text(encoding='utf-8'))
page_by_id={x['id']:x for x in pages}
master={}
for part,base in MASTER_PARTS:
 rows=json.loads((base/'manifest.json').read_text(encoding='utf-8'))
 master[part]={int(x['source_page']):{**x,'file':base/x['relative_path']} for x in rows}

rows=[]; failures=[]
for im in manifest['images']:
 raw=ROOT/'content-staging'/im['raw_path']; actual=sha(raw)
 m=re.search(r'-(\d+)\.(?:jpe?g|png|webp)$',im.get('storage_object_path',''),re.I)
 source_page=int(m.group(1)) if m else None
 cand=[]
 raw_ph=ph(raw)
 for part,_ in MASTER_PARTS:
  ref=master[part].get(source_page)
  if ref and ref['file'].is_file():
   cand.append((int(raw_ph-ph(ref['file'])),part,ref,sha(ref['file'])))
 cand.sort(key=lambda x:x[0])
 best=cand[0] if cand else None; second=cand[1] if len(cand)>1 else None
 strong=bool(best and best[0]<=8 and (second is None or second[0]-best[0]>=4))
 if not strong: failures.append({'legacy_page_id':im['legacy_page_id'],'stored_page_number':im['page_number'],'derived_source_page':source_page,'candidates':[{'part':c[1],'phash_distance':c[0]} for c in cand],'reason':'perceptual_identity_not_strong'})
 ref=best[2] if strong else None; part=best[1] if strong else None
 pg=page_by_id.get(im['legacy_page_id'],{})
 rows.append({'stored_page_number':im['page_number'],'legacy_page_id':im['legacy_page_id'],'storage_object_path':im.get('storage_object_path'),'derived_source_page':source_page,'raw_sha256':im['sha256'],'raw_sha_verified':actual==im['sha256'],'master_part':part,'source_page':ref['source_page'] if ref else None,'book_page':ref['book_page'] if ref else None,'section':ref['section'] if ref else None,'title':ref['title'] if ref else None,'master_relative_path':ref['relative_path'] if ref else None,'master_sha256':best[3] if strong else None,'exact_master_sha':bool(strong and actual==best[3]),'phash_distance':best[0] if best else None,'runner_up_phash_distance':second[0] if second else None,'content_equivalence_verified':strong,'legacy_question_count':len(pg.get('ai_questions') or [])})

verified=[r for r in rows if r['content_equivalence_verified'] and r['raw_sha_verified']]
parts={}
for part,_ in MASTER_PARTS:
 pr=sorted([r for r in verified if r['master_part']==part],key=lambda r:r['source_page'])
 if not pr: continue
 runs=[]
 for r in pr:
  key=(r['section'],r['title'])
  if not runs or runs[-1]['key']!=key or r['source_page']!=runs[-1]['end_source_page']+1:
   runs.append({'key':key,'section':r['section'],'title':r['title'],'start_source_page':r['source_page'],'end_source_page':r['source_page'],'stored_pages':[r['stored_page_number']],'legacy_question_count':r['legacy_question_count']})
  else:
   runs[-1]['end_source_page']=r['source_page']; runs[-1]['stored_pages'].append(r['stored_page_number']); runs[-1]['legacy_question_count']+=r['legacy_question_count']
 for x in runs: x.pop('key',None)
 parts[part]={'matched_pages':len(pr),'source_page_min':min(r['source_page'] for r in pr),'source_page_max':max(r['source_page'] for r in pr),'title_runs':runs}

status='VERIFIED' if len(verified)==len(rows) and not failures else 'NOT VERIFIED'
report={'schema_version':2,'operation':'history_book_perceptual_identity_and_structure_discovery','subject_id':SID,'source_name':'التاريخ الكتاب المدرسي','classification':'educational_source','raw_image_count':len(rows),'legacy_question_count':sum(len((p.get('ai_questions') or [])) for p in pages),'raw_sha_verified_count':sum(1 for r in rows if r['raw_sha_verified']),'exact_master_sha_count':sum(1 for r in rows if r['exact_master_sha']),'content_equivalence_verified_count':sum(1 for r in rows if r['content_equivalence_verified']),'identity_status':status,'identity_method':'storage-object source-page provenance + perceptual hash against both trusted master History parts; exact master SHA intentionally not required because master derivatives differ bytewise','failures':failures,'matched_parts':parts,'page_map':rows,'lesson_boundaries_status':'NOT VERIFIED','semantic_question_review':'NOT VERIFIED','raw_mutations':0}
OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'identity_status':status,'raw_images':len(rows),'raw_sha_verified':report['raw_sha_verified_count'],'exact_master_sha':report['exact_master_sha_count'],'content_equivalence_verified':report['content_equivalence_verified_count'],'parts':{k:{'matched_pages':v['matched_pages'],'source_page_range':[v['source_page_min'],v['source_page_max']]} for k,v in parts.items()},'legacy_questions':report['legacy_question_count'],'failure_count':len(failures)},ensure_ascii=False))
