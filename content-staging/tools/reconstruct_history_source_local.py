#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SID = "0a76f44b-0a4f-4e36-9ea9-badecf78bf23"
SOURCE = ROOT / "content-staging/raw/legacy-supabase/subjects" / SID
PAGES = SOURCE / "pages.json"
TECH = ROOT / "content-staging/reconstruction/technical" / f"{SID}.json"
VISUAL = ROOT / "content-staging/reconstruction/educational" / f"{SID}-visual-index.json"
OUT = ROOT / "content-staging/reconstruction/educational" / f"{SID}.json"

LESSONS = [
    (1, "الدولة الإسلامية بعد وفاة الرسول 11-40هـ", 10, 13, [13]),
    (2, "الدولة الأموية وسياساتها 41-132هـ", 14, 21, [21]),
    (3, "الثورات الإسلامية على الحكم الأموي", 22, 30, [29, 30]),
    (4, "قيام الدولة العباسية (132هـ)", 31, 35, [35]),
    (5, "سياسات الدولة العباسية", 36, 43, [42, 43]),
    (6, "أنواع الثورات على الحكم العباسي", 44, 48, [47, 48]),
    (7, "نماذج من الثورات التصحيحية في العصر العباسي", 49, 55, [55]),
    (8, "الدول المستقلة في العصر العباسي", 56, 63, [63]),
    (9, "دول المنافسة والنفوذ في العصر العباسي", 64, 68, [68]),
]


def stable_question_ref(page_id: str, index: int, q: dict) -> str:
    payload = json.dumps(q, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
    return f"{page_id}:{index}:{digest}"


def main() -> None:
    pages = json.loads(PAGES.read_text(encoding="utf-8"))
    tech = json.loads(TECH.read_text(encoding="utf-8"))
    visual = json.loads(VISUAL.read_text(encoding="utf-8"))

    assert tech["all_images_technically_verified"] is True
    assert tech["checks"]["manifest_image_count"] == 61
    assert tech["raw_mutations"] == 0
    assert visual["raw_image_count"] == 61
    assert visual["stored_page_range"] == [8, 68]
    assert visual["boundary_page_exports"] == [8, 9, 10, 14, 22, 31, 36, 44, 49, 56, 64, 68]

    pages = sorted(pages, key=lambda p: (p["page_number"], p["id"]))
    assert len(pages) == 61
    assert [p["page_number"] for p in pages] == list(range(8, 69))
    by_num = {p["page_number"]: p for p in pages}
    assert sum(len(p.get("ai_questions") or []) for p in pages) == 138
    assert len(by_num[8].get("ai_questions") or []) == 0
    assert len(by_num[9].get("ai_questions") or []) == 0

    classified_pages: dict[int, str] = {8: "table_of_contents", 9: "semester_cover"}
    lesson_records = []
    assignments = []
    total_lesson_pages = 0
    total_review_pages = 0

    for ordinal, title, start, end, review_pages in LESSONS:
        all_pages = list(range(start, end + 1))
        content_pages = [n for n in all_pages if n not in review_pages]
        total_lesson_pages += len(content_pages)
        total_review_pages += len(review_pages)
        lesson_id = f"history9-sem1-l{ordinal:02d}"
        for n in content_pages:
            assert n not in classified_pages
            classified_pages[n] = f"lesson:{lesson_id}"
        for n in review_pages:
            assert n not in classified_pages
            classified_pages[n] = f"lesson_review:{lesson_id}"

        qcount = 0
        question_refs = []
        for n in all_pages:
            p = by_num[n]
            for idx, q in enumerate(p.get("ai_questions") or []):
                ref = stable_question_ref(p["id"], idx, q)
                qcount += 1
                question_refs.append(ref)
                assignments.append({
                    "question_ref": ref,
                    "legacy_page_id": p["id"],
                    "stored_page_number": n,
                    "legacy_question_index": idx,
                    "lesson_id": lesson_id,
                    "mapping_basis": "verified source-local page membership within visually verified lesson/review boundary",
                    "semantic_correctness": "NOT VERIFIED",
                })

        lesson_records.append({
            "id": lesson_id,
            "lesson_ordinal": ordinal,
            "title": title,
            "title_evidence": "source-local visual: page 8 table of contents + lesson start page",
            "stored_page_range": [start, end],
            "stored_pages": all_pages,
            "content_pages": content_pages,
            "review_pages": review_pages,
            "legacy_page_ids": [by_num[n]["id"] for n in all_pages],
            "legacy_question_count": qcount,
            "question_refs": question_refs,
            "boundary_status": "verified_source_local_visual",
        })

    assert len(classified_pages) == 61
    assert set(classified_pages) == set(range(8, 69))
    assert total_lesson_pages == 47
    assert total_review_pages == 12
    assert len(assignments) == 138
    assert len({a["question_ref"] for a in assignments}) == 138

    out = {
        "schema_version": 1,
        "status": "reconstructed_verified_source_local",
        "subject_id": SID,
        "source_name": "التاريخ الكتاب المدرسي",
        "classification": "educational_book_source",
        "source_identity": {
            "status": "verified_source_local_only",
            "authority": "immutable RAW provenance + complete source-local visual review",
            "raw_images": 61,
            "stored_page_range": [8, 68],
            "master_reference_equivalence": "NOT VERIFIED",
            "master_reference_exact_sha_matches": 0,
            "master_reference_strong_visual_matches": 0,
            "note": "The current master History parts represent a different visual/source edition. No master-derived title or boundary was accepted."
        },
        "visual_evidence": {
            "workflow_run": 34831599212,
            "artifact_id": 10342118472,
            "artifact_digest": "sha256:dbb6cc5f980b293920f378ef24587ab9d9df65787e250fa955d33fbb3323a169",
            "coverage": "all stored pages 8..68",
            "toc_page": 8,
            "semester_cover_page": 9,
            "lesson_start_pages": [10, 14, 22, 31, 36, 44, 49, 56, 64],
            "review_pages": [13, 21, 29, 30, 35, 42, 43, 47, 48, 55, 63, 68],
            "review_status": "complete",
        },
        "reconstructed_book": {
            "source_label": "التاريخ الكتاب المدرسي",
            "book_title": "NOT VERIFIED",
            "retained_slice_status": "complete first-semester slice evidenced by source-local TOC and semester cover",
            "explicit_units": [],
            "unit_count": 0,
            "sections": [
                {
                    "ordinal": 1,
                    "title": "الفصل الدراسي الأول",
                    "cover_page": 9,
                    "stored_page_range": [9, 68],
                    "lesson_count": 9,
                    "lessons": lesson_records,
                }
            ],
            "section_count": 1,
            "lesson_count": 9,
            "lesson_page_count": total_lesson_pages,
            "lesson_review_page_count": total_review_pages,
            "table_of_contents_pages": [8],
            "section_cover_pages": [9],
            "classified_page_count": len(classified_pages),
            "page_classification": [{"stored_page_number": n, "class": classified_pages[n]} for n in sorted(classified_pages)],
        },
        "questions": {
            "legacy_questions": 138,
            "structurally_lesson_linked_questions": 138,
            "review_required_questions": 0,
            "unclassified_questions": 0,
            "semantic_correctness": "NOT VERIFIED",
            "assignments": assignments,
        },
        "invariants": {
            "all_61_pages_classified_exactly_once": True,
            "all_138_questions_structurally_accounted_for": True,
            "raw_mutations": 0,
            "new_imports": 0,
            "new_publications": 0,
        },
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": out["status"],
        "lessons": 9,
        "lesson_pages": total_lesson_pages,
        "lesson_review_pages": total_review_pages,
        "questions_linked": len(assignments),
        "pages_classified": len(classified_pages),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
