#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SID='1933807f-4cb0-40c9-9b29-3ef3d32c98dc'
SRC=ROOT/'content-staging/raw/legacy-supabase/subjects'/SID
TECH=ROOT/'content-staging/reconstruction/technical'/f'{SID}.json'
OUT=ROOT/'content-staging/reconstruction/educational'/f'{SID}.json'

def qref(pid,i,q):
    s=json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'))
    return f'{pid}:{i}:{hashlib.sha256(s.encode()).hexdigest()[:16]}'

def main():
    t=json.loads(TECH.read_text(encoding='utf-8'))
    pages=json.loads((SRC/'pages.json').read_text(encoding='utf-8'))
    assert t['all_images_technically_verified'] is True and t['checks']['manifest_image_count']==186
    pages=sorted(pages,key=lambda p:(p['page_number'],p['id']))
    assert len(pages)==186 and [p['page_number'] for p in pages]==list(range(7,193))
    bynum={p['page_number']:p for p in pages}
    assert sum(len(p.get('ai_questions') or []) for p in pages)==717

    unit_specs=[
      ('math9-p1-u1','المجموعات والعلاقات',7,58),
      ('math9-p1-u2','تحليل المقادير الجبرية',59,112),
      ('math9-p1-u3','المعادلات',113,164),
      ('math9-p1-u4','حساب المثلثات',165,192),
    ]
    lesson_specs=[
      (7,9),(10,16),(17,24),(25,31),(32,39),(40,47),(48,52),
      (61,72),(73,80),(81,85),(86,89),(90,98),(99,101),(102,107),
      (113,124),(125,140),(141,151),(152,159),
      (165,172),(173,183),(184,186),
    ]
    review_pages={59,60}
    exercise_pages=set(range(53,58))|set(range(108,112))|set(range(160,164))|set(range(187,192))
    test_pages={58,112,164,192}
    nonlesson=review_pages|exercise_pages|test_pages

    lessons=[]; lesson_page_to_id={}; lesson_assignments=[]
    for idx,(a,b) in enumerate(lesson_specs,1):
        nums=list(range(a,b+1)); titles={bynum[n].get('title') for n in nums}
        assert len(titles)==1 and None not in titles
        lid=f'math9-p1-l{idx:02d}'
        unit_id=next(uid for uid,_,ua,ub in unit_specs if ua<=a<=ub)
        refs=[]
        for n in nums:
            lesson_page_to_id[n]=lid
            p=bynum[n]
            for qi,q in enumerate(p.get('ai_questions') or []):
                r=qref(p['id'],qi,q); refs.append(r)
                lesson_assignments.append({'question_ref':r,'legacy_page_id':p['id'],'stored_page_number':n,'legacy_question_index':qi,'lesson_id':lid,'mapping_basis':'source-local page title continuity + direct RAW visual boundary verification','semantic_correctness':'NOT VERIFIED'})
        lessons.append({'id':lid,'unit_id':unit_id,'title':next(iter(titles)),'stored_page_range':[a,b],'stored_pages':nums,'page_count':len(nums),'legacy_question_count':len(refs),'question_refs':refs,'boundary_status':'verified_source_local_metadata_plus_direct_raw_visual_review'})

    review_assignments=[]
    for n in sorted(nonlesson):
        p=bynum[n]
        subtype='unit_review' if n in review_pages else ('general_exercises' if n in exercise_pages else 'unit_test')
        for qi,q in enumerate(p.get('ai_questions') or []):
            review_assignments.append({'question_ref':qref(p['id'],qi,q),'legacy_page_id':p['id'],'stored_page_number':n,'legacy_question_index':qi,'page_subtype':subtype,'classification':'review_required','reason':'question belongs to a proven non-lesson review/exercise/test page; no lesson mapping forced','semantic_correctness':'NOT VERIFIED'})

    lesson_pages=set(lesson_page_to_id)
    assert len(lesson_pages)==162 and len(nonlesson)==24 and lesson_pages.isdisjoint(nonlesson)
    assert lesson_pages|nonlesson==set(range(7,193))
    assert len(lesson_assignments)==620 and len(review_assignments)==97
    all_refs=[x['question_ref'] for x in lesson_assignments+review_assignments]
    assert len(all_refs)==717 and len(set(all_refs))==717

    units=[]
    for uid,title,a,b in unit_specs:
        unit_lessons=[x['id'] for x in lessons if x['unit_id']==uid]
        unit_nonlesson=[n for n in range(a,b+1) if n in nonlesson]
        units.append({'id':uid,'title':title,'stored_page_range':[a,b],'lesson_ids':unit_lessons,'nonlesson_pages':unit_nonlesson,'boundary_status':'verified_direct_raw_visual_unit_banner_and_closing_test'})

    out={
      'schema_version':1,
      'status':'reconstructed_verified_source_local_visual_structure',
      'subject_id':SID,
      'source_name':'كتاب الرياضيات - الجزء الأول',
      'classification':'educational_book_source',
      'source_identity':{
        'status':'verified_source_local_raw_sequence_and_visual_structure',
        'retained_page_range':[7,192],
        'retained_pages':186,
        'evidence':'immutable RAW + source-local pages.json title continuity + complete contact-sheet/direct RAW visual review',
        'rejected_reference':'الرياضيات ثالث ثانوي/02_الرياضيات_ثالث_ثانوي',
        'rejected_reference_reason':'0/186 exact SHA matches; expected-position unique visual nearest match only 1/186; no metadata transferred from it'
      },
      'reconstructed_book':{
        'book_title':'كتاب الرياضيات - الجزء الأول',
        'unit_count':4,'units':units,
        'lesson_count':21,'lesson_member_page_count':162,'lessons':lessons,
        'nonlesson_page_count':24,
        'review_pages':sorted(review_pages),
        'general_exercise_pages':sorted(exercise_pages),
        'unit_test_pages':sorted(test_pages)
      },
      'questions':{
        'legacy_questions':717,
        'structurally_lesson_linked_questions':620,
        'review_required_questions':97,
        'unclassified_questions':0,
        'semantic_correctness':'NOT VERIFIED',
        'lesson_assignments':lesson_assignments,
        'review_required_assignments':review_assignments
      },
      'invariants':{
        'all_186_pages_classified_exactly_once':True,
        'all_717_questions_structurally_accounted_for':True,
        'raw_mutations':0,'unrelated_mutations':0,'new_imports':0,'new_publications':0
      }
    }
    OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'units':4,'lessons':21,'lesson_pages':162,'nonlesson_pages':24,'lesson_linked':620,'review_required':97},ensure_ascii=False))
if __name__=='__main__': main()
