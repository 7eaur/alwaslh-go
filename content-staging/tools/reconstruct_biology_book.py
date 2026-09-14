#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
SID='67d4ffae-68e1-42e8-9c3b-72329973c93d'
DISC=ROOT/'content-staging/reconstruction/educational'/f'{SID}-discovery.json'
PAGES=ROOT/'content-staging/raw/legacy-supabase/subjects'/SID/'pages.json'
OUT=ROOT/'content-staging/reconstruction/educational'/f'{SID}.json'

d=json.loads(DISC.read_text(encoding='utf-8'))
pages=json.loads(PAGES.read_text(encoding='utf-8'))
if d.get('identity_status')!='VERIFIED_EXACT_SHA' or d.get('exact_sha_identity_count')!=214 or d.get('preferred_master_exact_sha_count')!=214:
    raise SystemExit('biology exact identity is not fully verified')

labels={x['page_number']:x['label'] for x in d['page_labels']}
ids={x['page_number']:x['legacy_page_id'] for x in d['page_labels']}
all_pages=sorted(labels)
if all_pages!=list(range(8,222)):
    raise SystemExit(f'unexpected retained page range: {all_pages[:1]}..{all_pages[-1:]} count={len(all_pages)}')
if any(labels[p] is None for p in all_pages):
    raise SystemExit('one or more retained pages lacks a unique exact-master label')

runs=[]
for p in all_pages:
    label=labels[p]
    if not runs or runs[-1]['title']!=label:
        runs.append({'title':label,'start_page':p,'end_page':p})
    else:
        runs[-1]['end_page']=p
for r in runs:
    r['pages']=list(range(r['start_page'],r['end_page']+1))

unit_starts=[i for i,r in enumerate(runs) if r['title'].startswith('الوحدة ')]
if len(unit_starts)!=8:
    raise SystemExit(f'expected 8 exact unit banners, found {len(unit_starts)}')

page_records={p['page_number']:p for p in pages}
units=[]; lessons=[]; unit_cover_pages=[]; review_pages=[]; lesson_pages=[]
for ui,ri in enumerate(unit_starts,1):
    next_ri=unit_starts[ui] if ui<len(unit_starts) else len(runs)
    section=runs[ri:next_ri]
    cover=section[0]
    if cover['start_page']!=cover['end_page']:
        raise SystemExit(f'unit {ui} cover is not one page')
    unit_cover_pages.append(cover['start_page'])
    unit_lessons=[]; unit_reviews=[]
    for run in section[1:]:
        if run['title'].startswith('تقويم الوحدة'):
            review_pages.extend(run['pages']); unit_reviews.extend(run['pages']); continue
        lp=run['pages']; lesson_pages.extend(lp)
        lesson={
            'id':f'biology12-u{ui:02d}-l{len(unit_lessons)+1:02d}',
            'unit_ordinal':ui,'lesson_ordinal':len(unit_lessons)+1,
            'title':run['title'],'stored_page_range':[lp[0],lp[-1]],'stored_pages':lp,
            'legacy_page_ids':[ids[x] for x in lp],
            'legacy_question_count':sum(len(page_records.get(x,{}).get('ai_questions') or []) for x in lp),
            'boundary_status':'verified_exact_master_title_run'
        }
        unit_lessons.append(lesson); lessons.append(lesson)
    title=cover['title'].split('-',1)[1].strip() if '-' in cover['title'] else cover['title']
    units.append({'ordinal':ui,'title':title,'cover_label':cover['title'],'stored_page_range':[section[0]['start_page'],section[-1]['end_page']],
                  'cover_page':cover['start_page'],'review_pages':unit_reviews,'lessons':unit_lessons})

if (len(units),len(lessons),len(lesson_pages),len(unit_cover_pages),len(review_pages))!=(8,47,193,8,13):
    raise SystemExit(f'structural counts differ: units={len(units)} lessons={len(lessons)} lesson_pages={len(lesson_pages)} covers={len(unit_cover_pages)} reviews={len(review_pages)}')
assigned=set(lesson_pages)|set(unit_cover_pages)|set(review_pages)
if assigned!=set(all_pages) or len(lesson_pages)+len(unit_cover_pages)+len(review_pages)!=214:
    raise SystemExit('retained pages are not classified exactly once')

lesson_by_page={p:l for l in lessons for p in l['stored_pages']}
question_links=[]; review_required=[]; total_questions=0
for p in all_pages:
    qs=page_records.get(p,{}).get('ai_questions') or []
    total_questions+=len(qs)
    for qi,q in enumerate(qs,1):
        base={'stored_page_number':p,'legacy_page_id':ids[p],'question_index':qi,'question':q.get('question'),'semantic_correctness':'NOT VERIFIED'}
        lesson=lesson_by_page.get(p)
        if lesson:
            question_links.append({**base,'lesson_id':lesson['id'],'lesson_title':lesson['title'],'structural_link_status':'verified_page_within_exact_master_title_run'})
        else:
            review_required.append({**base,'page_class':'unit_review' if p in review_pages else 'unit_cover','structural_link_status':'review_required_nonlesson_page'})
if total_questions!=3304 or len(question_links)+len(review_required)!=3304:
    raise SystemExit(f'question accounting mismatch: total={total_questions} links={len(question_links)} review={len(review_required)}')

report={
 'schema_version':1,'status':'reconstructed_verified','subject_id':SID,'source_name':'الأحياء الكتاب المدرسي','classification':'educational_book_source',
 'source_identity':{'status':'verified','master_reference_path':d['preferred_master_directory'],'raw_master_exact_sha_matches':214,'raw_images':214,'stored_page_range':[8,221]},
 'reconstructed_book':{'title':'الأحياء الكتاب المدرسي','units':units,'unit_count':8,'lesson_count':47,'lesson_page_count':193,'unit_cover_page_count':8,'unit_review_page_count':13,'retained_pages':214,'legacy_retained_page_range':[8,221]},
 'page_classification':{'lesson_pages':lesson_pages,'unit_cover_pages':unit_cover_pages,'unit_review_pages':review_pages,'appendix_pages':[]},
 'questions':{'legacy_questions':3304,'structurally_lesson_linked_questions':len(question_links),'review_required_questions':len(review_required),'semantic_question_review':'NOT VERIFIED','links':question_links,'review_required':review_required},
 'evidence':['214/214 retained RAW images are byte-identical by SHA-256 to one exact master reference directory.','Exact master filenames provide eight one-page unit banners, repeated content-title runs, and explicit unit-review runs across every retained page.','All 214 retained pages are classified exactly once from exact-master title-run evidence; question linkage is structural by verified page membership only.'],
 'visual_inspection_note':'Generated contact sheets were inspected around multiple unit/review transitions; semantic correctness of lesson content/questions remains NOT VERIFIED.',
 'raw_mutations':0,'imports_created':0,'publications_created':0
}
OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':report['status'],'units':8,'lessons':47,'lesson_pages':193,'covers':8,'reviews':13,'questions_linked':len(question_links),'review_required':len(review_required)},ensure_ascii=False))
