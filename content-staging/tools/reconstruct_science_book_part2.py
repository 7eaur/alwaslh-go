#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SID='81e99fe6-1421-462b-9562-1c0c5053a809'
DISC=ROOT/'content-staging/reconstruction/educational'/f'{SID}-discovery.json'
PAGES=ROOT/'content-staging/raw/legacy-supabase/subjects'/SID/'pages.json'
OUT=ROOT/'content-staging/reconstruction/educational'/f'{SID}.json'
d=json.loads(DISC.read_text(encoding='utf-8'))
pages=json.loads(PAGES.read_text(encoding='utf-8'))
if d.get('identity_status')!='VERIFIED' or d.get('exact_sha_identity_count')!=145 or d.get('raw_image_count')!=145:
 raise SystemExit('science part2 exact identity is not fully verified')
page_map=d['page_map']; by_stored={r['stored_page_number']:r for r in page_map}; page_records={p['page_number']:p for p in pages}
units=[]; lessons=[]; cover_pages=[]; review_pages=[]; lesson_pages=[]
for ui,sec in enumerate(d['sections'],9):
 titles=sec['titles']
 if not titles: raise SystemExit(f'empty titles in unit {ui}')
 cover=titles[0]
 if cover['start_stored_page']!=cover['end_stored_page']: raise SystemExit(f'unit cover is not one page for unit {ui}')
 cover_pages.append(cover['start_stored_page']); unit_lessons=[]
 for title_run in titles[1:]:
  start,end=title_run['start_stored_page'],title_run['end_stored_page']
  if title_run['title']=='تقويم الوحدة': review_pages.extend(range(start,end+1)); continue
  lp=list(range(start,end+1)); lesson_pages.extend(lp)
  lesson={'id':f'science9-part2-u{ui:02d}-l{len(unit_lessons)+1:02d}','unit_ordinal':ui,'lesson_ordinal':len(unit_lessons)+1,'title':title_run['title'],'stored_page_range':[start,end],'stored_pages':lp,'source_page_range':[by_stored[start]['source_page'],by_stored[end]['source_page']],'legacy_page_ids':[by_stored[x]['legacy_page_id'] for x in lp],'legacy_question_count':sum(len(page_records.get(x,{}).get('ai_questions') or []) for x in lp),'boundary_status':'verified_exact_master_title_run'}
  unit_lessons.append(lesson); lessons.append(lesson)
 units.append({'ordinal':ui,'title':sec['section'].split(':',1)[1].strip() if ':' in sec['section'] else sec['section'],'section_label':sec['section'],'stored_page_range':[sec['start_stored_page'],sec['end_stored_page']],'source_page_range':[sec['start_source_page'],sec['end_source_page']],'cover_page':cover['start_stored_page'],'review_pages':[p for p in range(sec['start_stored_page'],sec['end_stored_page']+1) if p in review_pages],'lessons':unit_lessons})
all_pages=sorted(by_stored)
if all_pages!=list(range(7,152)): raise SystemExit('unexpected retained stored-page range')
if len(units)!=8 or len(lessons)!=31 or len(lesson_pages)!=126 or len(cover_pages)!=8 or len(review_pages)!=11:
 raise SystemExit(f'science part2 structural counts differ from exact title-run evidence: units={len(units)} lessons={len(lessons)} lesson_pages={len(lesson_pages)} covers={len(cover_pages)} reviews={len(review_pages)}')
assigned=set(lesson_pages)|set(cover_pages)|set(review_pages)
if assigned!=set(all_pages): raise SystemExit('not all retained pages are classified exactly once')
source_questions=sum(len(p.get('ai_questions') or []) for p in pages)
if source_questions!=0: raise SystemExit(f'expected 0 source questions, got {source_questions}')
report={'schema_version':1,'status':'reconstructed_verified','subject_id':SID,'source_name':'كتاب العلوم - الجزء الثاني','classification':'educational_book_source','source_identity':{'status':'verified','master_reference_path':d['master_reference_path'],'raw_master_exact_sha_matches':145,'raw_images':145,'stored_page_range':[7,151],'source_reference_page_range':[8,152],'master_manifest_entries':d['master_manifest_entries'],'master_only_source_pages_outside_retained_slice':[1,2,3,4,5,6,7,153,154]},'reconstructed_book':{'title':'كتاب العلوم - الجزء الثاني','units':units,'unit_count':8,'lesson_count':31,'lesson_page_count':126,'unit_cover_page_count':8,'unit_review_page_count':11,'appendix_page_count':0,'retained_pages':145,'legacy_retained_page_range':[7,151],'source_reference_page_range':[8,152]},'page_classification':{'lesson_pages':lesson_pages,'unit_cover_pages':cover_pages,'unit_review_pages':review_pages,'appendix_pages':[]},'questions':{'legacy_questions':0,'structurally_lesson_linked_questions':0,'review_required_questions':0,'semantic_question_review':'NOT APPLICABLE','links':[]},'evidence':['145/145 retained RAW images are byte-identical by SHA-256 to the exact master reference path.','The master page-by-page manifest provides eight section/unit runs (units 9 through 16) and exact repeated title runs for lesson content and unit reviews.','The retained source pages.json contains zero legacy AI questions; no question records were fabricated.'],'raw_mutations':0}
OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':report['status'],'units':8,'lessons':31,'lesson_pages':126,'covers':8,'reviews':11,'questions_linked':0,'output':str(OUT.relative_to(ROOT))},ensure_ascii=False))
