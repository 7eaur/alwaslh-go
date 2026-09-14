#!/usr/bin/env python3
import hashlib, json, re
from collections import Counter, defaultdict
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw

SID='67d4ffae-68e1-42e8-9c3b-72329973c93d'
ROOT=Path('content-staging')
SRC=ROOT/'raw/legacy-supabase/subjects'/SID
MANIFEST=SRC/'manifest.json'
MASTER=Path('master-reference')
OUT=ROOT/'reconstruction/educational'/f'{SID}-discovery.json'
SHEETS=Path('/tmp/biology-contact-sheets')

m=json.loads(MANIFEST.read_text())
imgs=sorted(m['images'], key=lambda x:(x.get('page_number') is None, x.get('page_number') or -1, x.get('image_index',0)))
assert len(imgs)==214 and m['counts']['questions']==3304
source=[]
for r in imgs:
    p=SRC/'images'/Path(r['raw_path']).name
    assert p.exists(), p
    b=p.read_bytes(); h=hashlib.sha256(b).hexdigest()
    assert h==r['sha256'], (r['page_number'],h,r['sha256'])
    source.append((r,p,h))

exts={'.png','.jpg','.jpeg','.webp','.gif','.bmp','.tif','.tiff'}
master_by_sha=defaultdict(list)
for p in MASTER.rglob('*'):
    if p.is_file() and p.suffix.lower() in exts:
        try: h=hashlib.sha256(p.read_bytes()).hexdigest()
        except OSError: continue
        master_by_sha[h].append(str(p.relative_to(MASTER)))

matches=[]; dir_counts=Counter()
for r,p,h in source:
    paths=master_by_sha.get(h,[])
    for mp in paths: dir_counts[str(Path(mp).parent)]+=1
    matches.append({'page_number':r['page_number'],'legacy_page_id':r['legacy_page_id'],'sha256':h,'master_exact_sha_paths':paths})
matched=[x for x in matches if x['master_exact_sha_paths']]
unmatched=[x['page_number'] for x in matches if not x['master_exact_sha_paths']]
preferred_dir=None
if dir_counts:
    preferred_dir, preferred_count=dir_counts.most_common(1)[0]
else:
    preferred_count=0

def label_from_path(mp):
    stem=Path(mp).stem
    mm=re.match(r'^(?:ص|صفحة)?\s*\d+\s*-\s*(.*)$',stem)
    return (mm.group(1) if mm else stem).strip()

page_labels=[]
for x in matches:
    paths=[p for p in x['master_exact_sha_paths'] if preferred_dir and str(Path(p).parent)==preferred_dir]
    label=label_from_path(paths[0]) if len(paths)==1 else None
    page_labels.append({'page_number':x['page_number'],'legacy_page_id':x['legacy_page_id'],'label':label,'preferred_master_path':paths[0] if len(paths)==1 else None,'preferred_path_count':len(paths)})

runs=[]
for row in page_labels:
    if not runs or runs[-1]['label']!=row['label']:
        runs.append({'label':row['label'],'start_page':row['page_number'],'end_page':row['page_number'],'page_count':1})
    else:
        runs[-1]['end_page']=row['page_number']; runs[-1]['page_count']+=1
unit_candidates=[r for r in runs if r['label'] and r['label'].startswith('الوحدة')]
nonlesson_terms=('اختبار','تقويم','مراجعة','تمارين','أسئلة','نشاط عام','المحتويات','مقدمة','غلاف','تصدير')
nonlesson_candidates=[r for r in runs if r['label'] and any(t in r['label'] for t in nonlesson_terms)]

SHEETS.mkdir(parents=True,exist_ok=True)
for batch_start in range(0,len(source),12):
    batch=source[batch_start:batch_start+12]; cells=[]
    for r,p,h in batch:
        with Image.open(p) as im:
            im=ImageOps.exif_transpose(im).convert('RGB'); im.thumbnail((260,360))
            cell=Image.new('RGB',(280,410),'white'); cell.paste(im,((280-im.width)//2,15))
            ImageDraw.Draw(cell).text((8,385),f"storage page {r['page_number']}",fill='black'); cells.append(cell)
    rows=(len(cells)+3)//4; sheet=Image.new('RGB',(1120,410*rows),'white')
    for i,c in enumerate(cells): sheet.paste(c,((i%4)*280,(i//4)*410))
    lo=batch[0][0]['page_number']; hi=batch[-1][0]['page_number']; sheet.save(SHEETS/f'biology-pages-{lo:03d}-{hi:03d}.jpg',quality=88)

identity='VERIFIED_EXACT_SHA' if len(matched)==214 and preferred_count==214 else 'NOT VERIFIED'
out={
 'source_id':SID,'source_name':'الأحياء الكتاب المدرسي','status':'discovery_complete_not_finalized',
 'source_pages':214,'legacy_questions':3304,'retained_storage_page_range':[min(r['page_number'] for r in imgs),max(r['page_number'] for r in imgs)],
 'technical_source_sha_rechecked':214,'identity_status':identity,'exact_sha_identity_count':len(matched),'unmatched_storage_pages':unmatched,
 'candidate_master_directories':[{'path':k,'exact_sha_matches':v} for k,v in dir_counts.most_common()],
 'preferred_master_directory':preferred_dir,'preferred_master_exact_sha_count':preferred_count,
 'page_exact_sha_matches':matches,'page_labels':page_labels,'title_runs':runs,'unit_banner_candidates':unit_candidates,'nonlesson_title_candidates':nonlesson_candidates,
 'lesson_boundaries_status':'NOT VERIFIED','unit_boundaries_status':'NOT VERIFIED','question_linkage_status':'NOT VERIFIED','semantic_question_review':'NOT VERIFIED',
 'raw_mutations':0,'imports_created':0,'publications_created':0,
 'next_operation':'Inspect exact-master filename/title runs plus all contact sheets. Promote only evidence-backed units/lessons/non-lesson pages; otherwise retain NOT VERIFIED/review_required.'
}
OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'identity_status':identity,'exact_sha_identity_count':len(matched),'preferred_master_directory':preferred_dir,'preferred_count':preferred_count,'title_run_count':len(runs),'unit_candidates':unit_candidates,'nonlesson_candidates':nonlesson_candidates},ensure_ascii=False))
