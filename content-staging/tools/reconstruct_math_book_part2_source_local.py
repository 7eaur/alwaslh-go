#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SID='b80cbba1-410a-4346-9446-c3f01c4f9e56'
SRC=ROOT/'content-staging/raw/legacy-supabase/subjects'/SID
TECH=ROOT/'content-staging/reconstruction/technical'/f'{SID}.json'
OUT=ROOT/'content-staging/reconstruction/educational'/f'{SID}.json'

def main():
    tech=json.loads(TECH.read_text(encoding='utf-8'))
    pages=json.loads((SRC/'pages.json').read_text(encoding='utf-8'))
    assert tech['all_images_technically_verified'] is True
    assert tech['checks']['manifest_image_count']==135
    pages=sorted(pages,key=lambda p:(p['page_number'],p['id']))
    assert len(pages)==135 and [p['page_number'] for p in pages]==list(range(7,142))
    assert sum(len(p.get('ai_questions') or []) for p in pages)==0
    bynum={p['page_number']:p for p in pages}

    unit_specs=[
      ('math9-p2-u5','الهندسة',7,64),
      ('math9-p2-u6','الهندسة الإحداثية والتحويلات',65,110),
      ('math9-p2-u7','الإحصاء',111,141),
    ]
    lesson_specs=[
      (7,9),(10,15),(16,21),(22,26),(27,29),(30,35),(36,42),(43,51),(52,60),
      (65,68),(69,72),(73,83),(84,89),(90,96),(97,105),
      (111,119),(120,122),(123,128),(129,137),
    ]
    exercise_pages=set(range(61,63))|set(range(106,109))|set(range(138,140))
    test_pages=set(range(63,65))|set(range(109,111))|set(range(140,142))
    nonlesson=exercise_pages|test_pages

    lessons=[]; lesson_page_to_id={}
    for idx,(a,b) in enumerate(lesson_specs,1):
        nums=list(range(a,b+1)); titles={bynum[n].get('title') for n in nums}
        assert len(titles)==1 and None not in titles
        assert all(len(p.get('ai_questions') or [])==0 for p in (bynum[n] for n in nums))
        lid=f'math9-p2-l{idx:02d}'
        uid=next(uid for uid,_,ua,ub in unit_specs if ua<=a<=ub)
        for n in nums: lesson_page_to_id[n]=lid
        lessons.append({
          'id':lid,'unit_id':uid,'title':next(iter(titles)),
          'stored_page_range':[a,b],'stored_pages':nums,'page_count':len(nums),
          'legacy_question_count':0,'question_refs':[],
          'boundary_status':'verified_source_local_metadata_plus_complete_contact_sheet_visual_review'
        })

    expected_nonlesson_titles={
      **{n:'general_exercises' for n in exercise_pages},
      **{n:'unit_test' for n in test_pages},
    }
    for n,subtype in expected_nonlesson_titles.items():
        title=bynum[n].get('title') or ''
        if subtype=='unit_test': assert title=='اختبار الوحدة'
        else: assert title in {'تمارين ومسائل عامة','تمارين عامة ومسائل'}
        assert len(bynum[n].get('ai_questions') or [])==0

    lesson_pages=set(lesson_page_to_id)
    assert len(lesson_pages)==122 and len(nonlesson)==13
    assert lesson_pages.isdisjoint(nonlesson)
    assert lesson_pages|nonlesson==set(range(7,142))

    units=[]
    for uid,title,a,b in unit_specs:
        unit_lessons=[x['id'] for x in lessons if x['unit_id']==uid]
        unit_nonlesson=[n for n in range(a,b+1) if n in nonlesson]
        units.append({
          'id':uid,'title':title,'stored_page_range':[a,b],
          'lesson_ids':unit_lessons,'nonlesson_pages':unit_nonlesson,
          'boundary_status':'verified_complete_contact_sheet_visual_unit_banner_and_closing_test'
        })

    out={
      'schema_version':1,
      'status':'reconstructed_verified_source_local_visual_structure',
      'subject_id':SID,
      'source_name':'كتاب الرياضيات - الجزء الثاني',
      'classification':'educational_book_source',
      'source_identity':{
        'status':'verified_source_local_raw_sequence_and_visual_structure',
        'retained_page_range':[7,141],
        'retained_pages':135,
        'evidence':'immutable RAW + source-local pages.json title continuity + complete 12-sheet contact-sheet visual review of all 135 retained pages',
        'visual_evidence':{
          'workflow_run_id':34869811987,
          'artifact_id':10358975418,
          'artifact_digest':'sha256:2c029bac25b762f9b37f4c8d0e43f32c7091845e008c91bef006c8955950d6a8',
          'sheets_reviewed':12,
          'pages_reviewed':135
        },
        'inherited_structure_from_part1':False,
        'external_reference_used_for_structure':False
      },
      'reconstructed_book':{
        'book_title':'كتاب الرياضيات - الجزء الثاني',
        'unit_count':3,'units':units,
        'lesson_count':19,'lesson_member_page_count':122,'lessons':lessons,
        'nonlesson_page_count':13,
        'review_pages':[],
        'general_exercise_pages':sorted(exercise_pages),
        'unit_test_pages':sorted(test_pages)
      },
      'questions':{
        'legacy_questions':0,
        'structurally_lesson_linked_questions':0,
        'review_required_questions':0,
        'unclassified_questions':0,
        'semantic_correctness':'NOT APPLICABLE — source has zero legacy questions',
        'lesson_assignments':[],
        'review_required_assignments':[]
      },
      'invariants':{
        'all_135_pages_classified_exactly_once':True,
        'all_0_questions_structurally_accounted_for':True,
        'raw_mutations':0,'unrelated_mutations':0,'new_imports':0,'new_publications':0
      }
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'units':3,'lessons':19,'lesson_pages':122,'nonlesson_pages':13,'legacy_questions':0},ensure_ascii=False))
if __name__=='__main__': main()
