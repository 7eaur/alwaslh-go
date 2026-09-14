#!/usr/bin/env python3
import json,re,math
from pathlib import Path
from PIL import Image,ImageOps
ROOT=Path(__file__).resolve().parents[2]
SID='1933807f-4cb0-40c9-9b29-3ef3d32c98dc'
RAW=ROOT/'content-staging/raw/legacy-supabase/subjects'/SID
MASTER=ROOT/'master-reference/الرياضيات ثالث ثانوي/02_الرياضيات_ثالث_ثانوي'
OUT=ROOT/'content-staging/reconstruction/educational'/f'{SID}-visual-identity-diagnostic.json'
manifest=json.loads((RAW/'manifest.json').read_text(encoding='utf-8'))
master=json.loads((MASTER/'manifest.json').read_text(encoding='utf-8'))
def sig(path):
 with Image.open(path) as im:
  im=ImageOps.exif_transpose(im).convert('L')
  im=ImageOps.fit(im,(48,64),method=Image.Resampling.LANCZOS)
  return list(im.getdata())
def mae(a,b): return sum(abs(x-y) for x,y in zip(a,b))/len(a)
master_sigs={int(x['source_page']):sig(MASTER/x['relative_path']) for x in master}
rows=[]
for ordinal,im in enumerate(manifest['images'],1):
 m=re.search(r'page_(\d+)\.',im.get('storage_object_path',''))
 intended=int(m.group(1)) if m else None
 raw_sig=sig(ROOT/'content-staging'/im['raw_path'])
 scores=sorted((mae(raw_sig,ms),sp) for sp,ms in master_sigs.items())
 best_mae,best_page=scores[0]; second_mae,second_page=scores[1]
 intended_mae=next((v for v,p in scores if p==intended),None)
 intended_rank=next((i+1 for i,(v,p) in enumerate(scores) if p==intended),None)
 rows.append({'ordinal':ordinal,'legacy_page_id':im['legacy_page_id'],'stored_page_number':im['page_number'],'intended_source_page':intended,'best_source_page':best_page,'best_mae':round(best_mae,6),'second_source_page':second_page,'second_mae':round(second_mae,6),'best_margin':round(second_mae-best_mae,6),'intended_mae':round(intended_mae,6) if intended_mae is not None else None,'intended_rank':intended_rank,'intended_is_unique_best':best_page==intended and best_mae < second_mae})
unique_best=sum(1 for r in rows if r['intended_is_unique_best'])
maes=[r['best_mae'] for r in rows]; margins=[r['best_margin'] for r in rows]
report={'schema_version':1,'operation':'math_book_part1_visual_identity_diagnostic','subject_id':SID,'comparison_method':'PIL grayscale EXIF-normalized ImageOps.fit 48x64 + mean absolute pixel error; each RAW compared against all 255 master pages','raw_count':len(rows),'master_count':len(master),'intended_unique_best_count':unique_best,'all_intended_unique_best':unique_best==len(rows),'best_mae_min':min(maes),'best_mae_max':max(maes),'best_mae_mean':round(sum(maes)/len(maes),6),'best_margin_min':min(margins),'best_margin_mean':round(sum(margins)/len(margins),6),'rows':rows,'interpretation':'Diagnostic only. This report does not promote master metadata or final structure by itself.','raw_mutations':0}
OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ['raw_count','master_count','intended_unique_best_count','all_intended_unique_best','best_mae_min','best_mae_max','best_mae_mean','best_margin_min','best_margin_mean']},ensure_ascii=False))
