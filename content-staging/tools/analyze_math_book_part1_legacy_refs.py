#!/usr/bin/env python3
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SID='1933807f-4cb0-40c9-9b29-3ef3d32c98dc'
RAW=ROOT/'content-staging/raw/legacy-supabase/subjects'/SID
OUT=ROOT/'content-staging/reconstruction/educational'/f'{SID}-legacy-reference-analysis.json'
pages=json.loads((RAW/'pages.json').read_text(encoding='utf-8'))
rows=[]; global_titles=Counter()
for ordinal,p in enumerate(pages,1):
    qs=p.get('ai_questions') or []
    titles=[]
    ref_pages=[]
    for q in qs:
        for ref in q.get('question_references') or []:
            title=(ref.get('lesson_title') or '').strip()
            if title:
                titles.append(title); global_titles[title]+=1
            pn=(ref.get('page_number') or '').strip()
            if pn: ref_pages.append(pn)
    tc=Counter(titles)
    rows.append({
        'ordinal':ordinal,
        'legacy_page_id':p.get('id'),
        'stored_page_number':p.get('page_number'),
        'question_count':len(qs),
        'lesson_title_candidates':[{'title':k,'reference_count':v} for k,v in tc.most_common()],
        'candidate_status':'NO_QUESTION_EVIDENCE' if not tc else ('SINGLE_TITLE_CANDIDATE' if len(tc)==1 else 'MULTI_TITLE_CONFLICT'),
        'reference_page_values':sorted(set(ref_pages)),
    })
runs=[]
for r in rows:
    title=r['lesson_title_candidates'][0]['title'] if r['candidate_status']=='SINGLE_TITLE_CANDIDATE' else None
    if title is None: continue
    if not runs or runs[-1]['title']!=title or runs[-1]['end_ordinal']+1!=r['ordinal']:
        runs.append({'title':title,'start_ordinal':r['ordinal'],'end_ordinal':r['ordinal'],'start_stored_page':r['stored_page_number'],'end_stored_page':r['stored_page_number']})
    else:
        runs[-1]['end_ordinal']=r['ordinal']; runs[-1]['end_stored_page']=r['stored_page_number']
report={
 'schema_version':1,
 'operation':'math_book_part1_legacy_question_reference_analysis',
 'subject_id':SID,
 'evidence_scope':'Legacy ai_questions.question_references only; generated/question semantics are NOT VERIFIED and this file MUST NOT be used alone to finalize lesson boundaries.',
 'page_count':len(pages),
 'question_count':sum(len(p.get('ai_questions') or []) for p in pages),
 'pages_with_question_evidence':sum(1 for r in rows if r['question_count']>0),
 'pages_without_question_evidence':sum(1 for r in rows if r['question_count']==0),
 'pages_single_title_candidate':sum(1 for r in rows if r['candidate_status']=='SINGLE_TITLE_CANDIDATE'),
 'pages_multi_title_conflict':sum(1 for r in rows if r['candidate_status']=='MULTI_TITLE_CONFLICT'),
 'distinct_lesson_title_candidates':len(global_titles),
 'lesson_title_reference_counts':[{'title':k,'reference_count':v} for k,v in global_titles.most_common()],
 'contiguous_single_title_runs':runs,
 'pages':rows,
 'boundary_status':'NOT VERIFIED',
 'semantic_correctness':'NOT VERIFIED',
 'raw_mutations':0,
}
OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ['page_count','question_count','pages_with_question_evidence','pages_without_question_evidence','pages_single_title_candidate','pages_multi_title_conflict','distinct_lesson_title_candidates','boundary_status']},ensure_ascii=False))
