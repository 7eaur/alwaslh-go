#!/usr/bin/env python3
import hashlib, json
from collections import Counter, defaultdict
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw

SID='a89c6c5d-d3d2-4aed-b98c-2ef5224cdae8'
ROOT=Path('content-staging')
SRC=ROOT/'raw/legacy-supabase/subjects'/SID
MANIFEST=SRC/'manifest.json'
MASTER=Path('master-reference')
OUT=ROOT/'reconstruction/educational'/f'{SID}-discovery.json'
SHEETS=Path('/tmp/seerah-contact-sheets')

m=json.loads(MANIFEST.read_text())
imgs=sorted(m['images'], key=lambda x:(x.get('page_number') is None, x.get('page_number') or -1, x.get('image_index',0)))
assert len(imgs)==81, len(imgs)
assert m['counts']['questions']==1152, m['counts']['questions']
assert m['counts']['image_download_failures']==0
assert all(not v for v in m['anomalies'].values()), m['anomalies']
source=[]
for r in imgs:
    p=SRC/'images'/Path(r['raw_path']).name
    assert p.exists(), p
    h=hashlib.sha256(p.read_bytes()).hexdigest()
    assert h==r['sha256'], (r.get('page_number'),h,r.get('sha256'))
    source.append((r,p,h))
exts={'.png','.jpg','.jpeg','.webp','.gif','.bmp','.tif','.tiff'}
master_by_sha=defaultdict(list)
for p in MASTER.rglob('*'):
    if p.is_file() and p.suffix.lower() in exts:
        try: h=hashlib.sha256(p.read_bytes()).hexdigest()
        except OSError: continue
        master_by_sha[h].append(str(p.relative_to(MASTER)))
matches=[]
for r,p,h in source:
    matches.append({'page_number':r.get('page_number'),'legacy_page_id':r.get('legacy_page_id'),'sha256':h,'master_exact_sha_paths':master_by_sha.get(h,[])})
matched=[x for x in matches if x['master_exact_sha_paths']]
unmatched=[x['page_number'] for x in matches if not x['master_exact_sha_paths']]
dir_counts=Counter()
for x in matched:
    for mp in x['master_exact_sha_paths']: dir_counts[str(Path(mp).parent)]+=1
SHEETS.mkdir(parents=True,exist_ok=True)
for batch_start in range(0,len(source),12):
    batch=source[batch_start:batch_start+12]; cells=[]
    for r,p,h in batch:
        with Image.open(p) as im:
            im=ImageOps.exif_transpose(im).convert('RGB'); im.thumbnail((260,360))
            cell=Image.new('RGB',(280,400),'white'); cell.paste(im,((280-im.width)//2,20))
            ImageDraw.Draw(cell).text((8,378),f"storage page {r.get('page_number')}",fill='black'); cells.append(cell)
    sheet=Image.new('RGB',(280*4,400*3),'white')
    for i,c in enumerate(cells): sheet.paste(c,((i%4)*280,(i//4)*400))
    lo=batch[0][0].get('page_number'); hi=batch[-1][0].get('page_number')
    sheet.save(SHEETS/f'seerah-pages-{lo:03d}-{hi:03d}.jpg',quality=88)
identity='VERIFIED_EXACT_SHA' if len(matched)==81 else 'NOT VERIFIED'
out={'source_id':SID,'source_name':'السيرة النبوية الكتاب','status':'discovery_complete_not_finalized','source_pages':81,'legacy_questions':1152,'retained_storage_page_range':[min(r['page_number'] for r in imgs),max(r['page_number'] for r in imgs)],'technical_source_sha_rechecked':81,'identity_status':identity,'exact_sha_identity_count':len(matched),'unmatched_storage_pages':unmatched,'candidate_master_directories':[{'path':k,'exact_sha_matches':v} for k,v in dir_counts.most_common()],'page_exact_sha_matches':matches,'semantic_structure_status':'NOT VERIFIED','question_linkage_status':'NOT VERIFIED','semantic_question_review':'NOT VERIFIED','raw_mutations':0,'imports_created':0,'publications_created':0,'next_operation':'Use only the 81 exact source pages and exact-SHA master filename evidence to prove lesson boundaries; preserve any page subtype ambiguity as NOT VERIFIED; only then link legacy questions by verified page membership.'}
OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'identity_status':identity,'exact_sha_identity_count':len(matched),'unmatched':len(unmatched),'candidate_master_directories':out['candidate_master_directories'][:10]},ensure_ascii=False))
