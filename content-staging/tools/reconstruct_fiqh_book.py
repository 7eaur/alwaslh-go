#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SID='6a8ea7f2-1e77-4654-a28c-0ea1b82b4830'
SRC=ROOT/'content-staging/raw/legacy-supabase/subjects'/SID
DISC=ROOT/'content-staging/reconstruction/educational'/f'{SID}-discovery.json'
TECH=ROOT/'content-staging/reconstruction/technical'/f'{SID}.json'
OUT=ROOT/'content-staging/reconstruction/educational'/f'{SID}.json'
RX=re.compile(r'^ص(\d+)\s*-\s*(الدرس\s+[^-]+?)\s*-\s*(.+?)\.webp$')
def qref(pid,i,q):
    s=json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'))
    return f'{pid}:{i}:{hashlib.sha256(s.encode()).hexdigest()[:16]}'
def main():
    d=json.loads(DISC.read_text()); t=json.loads(TECH.read_text()); pages=json.loads((SRC/'pages.json').read_text())
    assert t['all_images_technically_verified'] is True and t['checks']['manifest_image_count']==67
    assert d['identity_status']=='VERIFIED_EXACT_SHA' and d['exact_sha_identity_count']==67 and not d['unmatched_storage_pages']
    pages=sorted(pages,key=lambda p:(p['page_number'],p['id']))
    assert len(pages)==67 and [p['page_number'] for p in pages]==list(range(8,75))
    bynum={p['page_number']:p for p in pages}
    assert sum(len(p.get('ai_questions') or []) for p in pages)==906
    labels={}; titles={}; evidence={}
    for x in d['page_exact_sha_matches']:
        assert len(x['master_exact_sha_paths'])==1
        path=x['master_exact_sha_paths'][0]; name=Path(path).name
        m=RX.match(name); assert m, name
        n=int(m.group(1)); assert n==x['page_number']
        labels[n]=m.group(2).strip(); titles[n]=m.group(3).strip(); evidence[n]=path
    assert set(labels)==set(range(8,75))
    groups=[]; cur=None
    for n in range(8,75):
        label=labels[n]
        if cur is None or cur['lesson_label']!=label:
            cur={'lesson_label':label,'title':titles[n],'stored_pages':[],'master_filename_evidence':[],'filename_title_variants':[]}; groups.append(cur)
        cur['stored_pages'].append(n); cur['master_filename_evidence'].append(evidence[n])
        if titles[n] not in cur['filename_title_variants']: cur['filename_title_variants'].append(titles[n])
    assert len(groups)==13, [(g['lesson_label'],g['title'],g['stored_pages']) for g in groups]
    assigns=[]
    for idx,g in enumerate(groups,1):
        g['id']=f'fiqh-third-secondary-l{idx:02d}'
        g['stored_page_range']=[g['stored_pages'][0],g['stored_pages'][-1]]
        g['boundary_status']='verified_exact_sha_master_filename_lesson_label_continuity'
        g['legacy_question_count']=0; refs=[]
        for n in g['stored_pages']:
            p=bynum[n]
            for qi,q in enumerate(p.get('ai_questions') or []):
                r=qref(p['id'],qi,q); refs.append(r); g['legacy_question_count']+=1
                assigns.append({'question_ref':r,'legacy_page_id':p['id'],'stored_page_number':n,'legacy_question_index':qi,'lesson_id':g['id'],'mapping_basis':'exact-SHA page identity + explicit master filename lesson label','semantic_correctness':'NOT VERIFIED'})
        g['question_refs']=refs
    assert sum(len(g['stored_pages']) for g in groups)==67
    assert len(assigns)==906 and len({a['question_ref'] for a in assigns})==906
    assert groups[0]['stored_page_range']==[8,13]
    assert groups[-1]['stored_page_range']==[68,74]
    explicit_eval=[n for n in range(8,75) if 'التقويم' in titles[n] or 'الخاتمة' in titles[n] or 'ختامية' in titles[n]]
    assert explicit_eval==[], explicit_eval
    out={'schema_version':1,'status':'reconstructed_verified_exact_sha_lesson_membership','subject_id':SID,'source_name':'الفقه الكتاب المدرسي','classification':'educational_book_source','source_identity':{'status':'verified_exact_sha','exact_sha_matches':67,'master_reference_directory':'التربية الاسلاميه ثالث ثانوي/كتاب الفقه/الصور','retained_page_range':[8,74],'front_and_back_matter_outside_retained_range':'reference-only; not invented in RAW'},'reconstructed_book':{'book_title':'كتاب الفقه','unit_count':0,'unit_status':'NOT VERIFIED','lesson_count':13,'lesson_member_page_count':67,'lessons':groups,'explicit_evaluation_or_conclusion_filename_pages':[],'other_page_subtype_review_boundaries':'NOT VERIFIED'},'questions':{'legacy_questions':906,'structurally_lesson_linked_questions':906,'review_required_questions':0,'unclassified_questions':0,'semantic_correctness':'NOT VERIFIED','assignments':assigns},'invariants':{'all_67_pages_assigned_exactly_once_to_evidence_lesson':True,'all_906_questions_structurally_accounted_for':True,'raw_mutations':0,'new_imports':0,'new_publications':0}}
    OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'lessons':13,'pages':67,'questions_linked':906},ensure_ascii=False))
if __name__=='__main__': main()
