#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SID='f4b6708c-027f-4883-9e85-e6e7acb52ecc'
DISC=ROOT/'content-staging/reconstruction/educational'/f'{SID}-discovery.json'
PAGES=ROOT/'content-staging/raw/legacy-supabase/subjects'/SID/'pages.json'
OUT=ROOT/'content-staging/reconstruction/educational'/f'{SID}.json'
d=json.loads(DISC.read_text(encoding='utf-8'))
pages=json.loads(PAGES.read_text(encoding='utf-8'))
if d.get('identity_status')!='VERIFIED' or d.get('exact_sha_identity_count')!=161 or d.get('raw_image_count')!=161:
 raise SystemExit('science part1 exact identity is not fully verified')
page_map=d['page_map']
by_stored={r['stored_page_number']:r for r in page_map}
page_records={p['page_number']:p for p in pages}
units=[]; lessons=[]; cover_pages=[]; review_pages=[]; lesson_pages=[]
for ui,sec in enumerate(d['sections'],1):
 titles=sec['titles']
 if not titles: raise SystemExit(f'empty titles in unit {ui}')
 cover=titles[0]
 if cover['start_stored_page']!=cover['end_stored_page']:
  raise SystemExit(f'unit cover is not one page for unit {ui}')
 cover_pages.append(cover['start_stored_page'])
 unit_lessons=[]
 for title_run in titles[1:]:
  start,end=title_run['start_stored_page'],title_run['end_stored_page']
  if title_run['title']=='تقويم الوحدة':
   review_pages.extend(range(start,end+1)); continue
  lp=list(range(start,end+1)); lesson_pages.extend(lp)
  lesson={'id':f'science9-part1-u{ui:02d}-l{len(unit_lessons)+1:02d}','unit_ordinal':ui,'lesson_ordinal':len(unit_lessons)+1,'title':title_run['title'],'stored_page_range':[start,end],'stored_pages':lp,'source_page_range':[by_stored[start]['source_page'],by_stored[end]['source_page']],'legacy_page_ids':[by_stored[x]['legacy_page_id'] for x in lp],'legacy_question_count':sum(len(page_records.get(x,{}).get('ai_questions') or []) for x in lp),'boundary_status':'verified_exact_master_title_run'}
  unit_lessons.append(lesson); lessons.append(lesson)
 units.append({'ordinal':ui,'title':sec['section'].split(':',1)[1].strip() if ':' in sec['section'] else sec['section'],'section_label':sec['section'],'stored_page_range':[sec['start_stored_page'],sec['end_stored_page']],'source_page_range':[sec['start_source_page'],sec['end_source_page']],'cover_page':cover['start_stored_page'],'review_pages':[p for p in range(sec['start_stored_page'],sec['end_stored_page']+1) if p in review_pages],'lessons':unit_lessons})
all_pages=sorted(by_stored)
if all_pages!=list(range(7,168)): raise SystemExit('unexpected retained stored-page range')
if len(units)!=8 or len(lessons)!=22 or len(lesson_pages)!=138 or len(cover_pages)!=8 or len(review_pages)!=15:
 raise SystemExit('science part1 structural counts differ from exact title-run evidence')
assigned=set(lesson_pages)|set(cover_pages)|set(review_pages)
if assigned!=set(all_pages): raise SystemExit('not all retained pages are classified exactly once')
question_links=[]; total_questions=0
for lesson in lessons:
 for sp in lesson['stored_pages']:
  qs=page_records.get(sp,{}).get('ai_questions') or []
  total_questions+=len(qs)
  for qi,q in enumerate(qs,1):
   question_links.append({'stored_page_number':sp,'legacy_page_id':by_stored[sp]['legacy_page_id'],'question_index':qi,'lesson_id':lesson['id'],'lesson_title':lesson['title'],'question':q.get('question'),'structural_link_status':'verified_page_within_exact_lesson_title_run','semantic_correctness':'NOT VERIFIED'})
if total_questions!=11 or len(question_links)!=11: raise SystemExit('expected exactly 11 source questions')
if any(x['stored_page_number']!=8 or x['lesson_title']!='المحلول ومكوناته' for x in question_links):
 raise SystemExit('question placement does not match verified source evidence')
report={'schema_version':1,'status':'reconstructed_verified','subject_id':SID,'source_name':'كتاب العلوم - الجزء الأول','classification':'educational_book_source','source_identity':{'status':'verified','master_reference_path':d['master_reference_path'],'raw_master_exact_sha_matches':161,'raw_images':161,'stored_page_range':[7,167],'source_reference_page_range':[8,168],'master_manifest_entries':d['master_manifest_entries'],'master_only_source_pages_outside_retained_slice':[1,2,3,4,5,6,7,169,170]},'reconstructed_book':{'title':'كتاب العلوم - الجزء الأول','units':units,'unit_count':8,'lesson_count':22,'lesson_page_count':138,'unit_cover_page_count':8,'unit_review_page_count':15,'appendix_page_count':0,'retained_pages':161,'legacy_retained_page_range':[7,167],'source_reference_page_range':[8,168]},'page_classification':{'lesson_pages':lesson_pages,'unit_cover_pages':cover_pages,'unit_review_pages':review_pages,'appendix_pages':[]},'questions':{'legacy_questions':11,'structurally_lesson_linked_questions':11,'review_required_questions':0,'semantic_question_review':'NOT VERIFIED','links':question_links},'evidence':['161/161 retained RAW images are byte-identical by SHA-256 to the exact master reference path.','The master page-by-page manifest provides eight section/unit runs and exact repeated title runs for lesson content and unit reviews.','All 11 legacy questions reside on stored page 8, which is inside the exact master title run for lesson المحلول ومكوناته.'],'raw_mutations':0}
OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':report['status'],'units':8,'lessons':22,'lesson_pages':138,'covers':8,'reviews':15,'questions_linked':11,'output':str(OUT.relative_to(ROOT))},ensure_ascii=False))
