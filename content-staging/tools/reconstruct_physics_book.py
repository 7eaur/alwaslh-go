#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SID='4863bbf6-6cf3-4238-9407-75825724292a'
DISC=ROOT/'content-staging/reconstruction/educational'/f'{SID}-discovery.json'
PAGES=ROOT/'content-staging/raw/legacy-supabase/subjects'/SID/'pages.json'
OUT=ROOT/'content-staging/reconstruction/educational'/f'{SID}.json'
d=json.loads(DISC.read_text(encoding='utf-8')); pages=json.loads(PAGES.read_text(encoding='utf-8'))
if d.get('identity_status')!='VERIFIED_EXACT_SHA' or d.get('exact_sha_identity_count')!=207 or d.get('preferred_master_exact_sha_count')!=207: raise SystemExit('physics exact identity not verified')
labels={x['page_number']:x['label'] for x in d['page_labels']}; ids={x['page_number']:x['legacy_page_id'] for x in d['page_labels']}; all_pages=sorted(labels)
if all_pages!=list(range(9,216)) or any(labels[p] is None for p in all_pages): raise SystemExit('unexpected physics page range/labels')
runs=[]
for p in all_pages:
 t=labels[p]
 if not runs or runs[-1]['title']!=t: runs.append({'title':t,'start_page':p,'end_page':p})
 else: runs[-1]['end_page']=p
for r in runs:r['pages']=list(range(r['start_page'],r['end_page']+1))
unit_starts=[i for i,r in enumerate(runs) if r['title'].startswith('غلاف الوحدة -')]
if len(unit_starts)!=9: raise SystemExit(f'expected 9 unit covers, got {len(unit_starts)}')
page_records={p['page_number']:p for p in pages}; units=[]; lessons=[]; cover_pages=[]; review_pages=[]; lesson_pages=[]
for ui,ri in enumerate(unit_starts,1):
 next_ri=unit_starts[ui] if ui<len(unit_starts) else len(runs); section=runs[ri:next_ri]; cover=section[0]
 if cover['start_page']!=cover['end_page']: raise SystemExit(f'unit {ui} cover not one page')
 cover_pages.append(cover['start_page']); ul=[]; ur=[]
 for run in section[1:]:
  if run['title'].startswith('تقويم الوحدة'):
   review_pages.extend(run['pages']); ur.extend(run['pages']); continue
  lp=run['pages']; lesson_pages.extend(lp)
  lesson={'id':f'physics12-u{ui:02d}-l{len(ul)+1:02d}','unit_ordinal':ui,'lesson_ordinal':len(ul)+1,'title':run['title'],'stored_page_range':[lp[0],lp[-1]],'stored_pages':lp,'legacy_page_ids':[ids[x] for x in lp],'legacy_question_count':sum(len(page_records.get(x,{}).get('ai_questions') or []) for x in lp),'boundary_status':'verified_exact_master_title_run'}
  ul.append(lesson); lessons.append(lesson)
 title=cover['title'].split('-',1)[1].strip()
 units.append({'ordinal':ui,'title':title,'cover_label':cover['title'],'stored_page_range':[section[0]['start_page'],section[-1]['end_page']],'cover_page':cover['start_page'],'review_pages':ur,'lessons':ul})
if (len(units),len(lessons),len(lesson_pages),len(cover_pages),len(review_pages))!=(9,45,173,9,25): raise SystemExit(f'counts differ {len(units)}/{len(lessons)}/{len(lesson_pages)}/{len(cover_pages)}/{len(review_pages)}')
if set(lesson_pages)|set(cover_pages)|set(review_pages)!=set(all_pages) or len(lesson_pages)+len(cover_pages)+len(review_pages)!=207: raise SystemExit('page classification not exact')
lesson_by_page={p:l for l in lessons for p in l['stored_pages']}; links=[]; rr=[]; total=0
for p in all_pages:
 qs=page_records.get(p,{}).get('ai_questions') or []; total+=len(qs)
 for qi,q in enumerate(qs,1):
  base={'stored_page_number':p,'legacy_page_id':ids[p],'question_index':qi,'question':q.get('question'),'semantic_correctness':'NOT VERIFIED'}; l=lesson_by_page.get(p)
  if l: links.append({**base,'lesson_id':l['id'],'lesson_title':l['title'],'structural_link_status':'verified_page_within_exact_master_title_run'})
  else: rr.append({**base,'page_class':'unit_review' if p in review_pages else 'unit_cover','structural_link_status':'review_required_nonlesson_page'})
if total!=3101 or len(links)+len(rr)!=3101: raise SystemExit(f'question accounting mismatch {total}/{len(links)}/{len(rr)}')
report={'schema_version':1,'status':'reconstructed_verified','subject_id':SID,'source_name':'الفيزياء الكتاب المدرسي','classification':'educational_book_source','source_identity':{'status':'verified','master_reference_path':d['preferred_master_directory'],'raw_master_exact_sha_matches':207,'raw_images':207,'stored_page_range':[9,215]},'reconstructed_book':{'title':'الفيزياء الكتاب المدرسي','units':units,'unit_count':9,'lesson_count':45,'lesson_page_count':173,'unit_cover_page_count':9,'unit_review_page_count':25,'retained_pages':207,'legacy_retained_page_range':[9,215]},'page_classification':{'lesson_pages':lesson_pages,'unit_cover_pages':cover_pages,'unit_review_pages':review_pages,'appendix_pages':[]},'questions':{'legacy_questions':3101,'structurally_lesson_linked_questions':len(links),'review_required_questions':len(rr),'semantic_question_review':'NOT VERIFIED','links':links,'review_required':rr},'evidence':['207/207 retained RAW images are byte-identical by SHA-256 to one exact master reference directory.','Exact master filenames provide nine one-page unit covers, 45 content-title runs, and nine explicit unit-review runs across every retained page.','All 207 retained pages are classified exactly once from exact-master title-run evidence; question linkage is structural by verified page membership only.'],'visual_inspection_note':'Contact sheets were generated for all retained pages; structural promotion relies on deterministic exact-SHA master labels. Semantic correctness remains NOT VERIFIED.','raw_mutations':0,'imports_created':0,'publications_created':0}
OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':report['status'],'units':9,'lessons':45,'lesson_pages':173,'covers':9,'reviews':25,'questions_linked':len(links),'review_required':len(rr)},ensure_ascii=False))
