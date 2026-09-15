#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SID = "dcc316bc-b7b8-4a9f-9022-ecc1e7762a9e"
RAW = ROOT / "content-staging/raw/legacy-supabase/subjects" / SID
TECH = ROOT / "content-staging/reconstruction/technical" / f"{SID}.json"
DISCOVERY = ROOT / "content-staging/reconstruction/exams/source-groups" / f"{SID}-discovery.json"
OUT = ROOT / "content-staging/reconstruction/exams/source-groups" / f"{SID}.json"


def main():
    subject = json.loads((RAW / "subject.json").read_text(encoding="utf-8"))
    manifest = json.loads((RAW / "manifest.json").read_text(encoding="utf-8"))
    pages = json.loads((RAW / "pages.json").read_text(encoding="utf-8"))
    tech = json.loads(TECH.read_text(encoding="utf-8"))
    discovery = json.loads(DISCOVERY.read_text(encoding="utf-8"))
    checks = tech.get("checks", {})
    assert tech.get("all_images_technically_verified") is True
    assert all(checks.get(key) == 124 for key in ("manifest_image_count", "existing_files", "readable_images", "sha256_matches", "byte_size_matches", "mime_matches"))
    assert checks.get("failures") == 0 and tech.get("raw_mutations") == 0
    assert tech.get("page_sequence") == {"first_page_number": 1, "last_page_number": 124, "unique_page_numbers": 124, "missing_page_numbers": [], "duplicate_page_numbers": []}
    duplicate_groups = tech.get("duplicate_sha256_groups_within_subject") or []
    assert len(duplicate_groups) == 9 and all(group.get("count") == 2 for group in duplicate_groups)
    assert manifest.get("counts") == {"pages": 124, "image_references": 124, "images_downloaded": 124, "image_download_failures": 0, "questions": 454}
    assert discovery.get("page_sequence") == {"first": 1, "last": 124, "count": 124, "contiguous": True}
    assert isinstance(pages, list) and len(pages) == 124
    by_page = {int(page["page_number"]): page for page in pages}
    images = {int(image["page_number"]): image for image in manifest.get("images", [])}
    assert sorted(by_page) == sorted(images) == list(range(1, 125))
    question_pages = {number for number, page in by_page.items() if page.get("ai_questions")}
    expected_question_pages = {number for number in range(1, 40) if number % 4 != 0}
    assert question_pages == expected_question_pages
    assert sum(len(page.get("ai_questions") or []) for page in pages) == 454

    models, question_records = [], []
    for ordinal in range(1, 32):
        first = (ordinal - 1) * 4 + 1
        numbers = list(range(first, first + 4))
        records = [images[number] for number in numbers]
        model_id = f"calculus-1447-exam-{ordinal:02d}"
        associated = 0
        for number in numbers:
            page = by_page[number]
            for qidx, _question in enumerate(page.get("ai_questions") or [], start=1):
                associated += 1
                question_records.append({
                    "source_page_number": number,
                    "legacy_page_id": page.get("id") or images[number].get("legacy_page_id"),
                    "source_question_ordinal_on_page": qidx,
                    "individual_exam_model_id": model_id,
                    "mapping_status": "structural_page_membership_verified",
                    "semantic_correctness": "NOT VERIFIED",
                })
        models.append({
            "id": model_id,
            "internal_ordinal": ordinal,
            "source_model_label": f"source occurrence {ordinal}",
            "official_model_code": "NOT VERIFIED",
            "official_title": "NOT VERIFIED",
            "academic_year_hijri": "1447",
            "academic_year_gregorian": "2025-2026",
            "term": "NOT VERIFIED",
            "exam_type": "وزاري",
            "first_page": first,
            "last_page": first + 3,
            "page_count": 4,
            "question_pages": numbers[:3],
            "correction_sheet_candidate_page": numbers[3],
            "ordered_page_numbers": numbers,
            "ordered_legacy_page_ids": [record.get("legacy_page_id") for record in records],
            "raw_paths": [record.get("raw_path") for record in records],
            "sha256": [record.get("sha256") for record in records],
            "associated_legacy_questions": associated,
            "boundary_status": "verified",
            "answer_key": {"status": "NOT VERIFIED", "reason": "The fourth page is visibly a correction/result sheet paired with the preceding three question pages, but available evidence does not establish it as a standalone official Answer Key."},
            "boundary_evidence": [
                "All 124 source pages were directly reviewed in eleven complete source-local contact sheets.",
                f"Pages {first}..{first + 2} are question sheets and page {first + 3} is the paired correction/result sheet; this four-page sequence was checked for this occurrence.",
                "The boundary decision is source-local and was not inherited from another Calculus source.",
            ],
            "review_status": "boundary_verified_answer_key_unverified",
        })
    assert len(question_records) == 454
    assert [model["associated_legacy_questions"] for model in models[:10]] == [80, 54] + [40] * 8
    assert not any(model["associated_legacy_questions"] for model in models[10:])

    output = {
        "schema_version": 1,
        "source_group_id": SID,
        "source_group_name": subject["subject"]["name"],
        "class_id": subject["class"]["id"],
        "class_name": subject["class"]["name"],
        "subject": "التفاضل والتكامل",
        "classification": "exam_source_group",
        "academic_year_hijri": "1447",
        "academic_year_gregorian": "2025-2026",
        "source_pages": 124,
        "source_questions": 454,
        "source_blocks_reviewed": 31,
        "verified_source_occurrence_count": 31,
        "review_required_block_count": 0,
        "individual_exam_model_count": 31,
        "finalized_exam_page_count": 124,
        "review_required_page_count": 0,
        "correction_sheet_candidate_count": 31,
        "verified_answer_key_count": 0,
        "duplicate_sha256_groups_within_source": 9,
        "duplicate_sha256_groups": duplicate_groups,
        "duplicate_disposition": "preserved_as_distinct_source_occurrences_no_merge_no_raw_mutation",
        "models": models,
        "question_mapping": {"exam_linked_structural": 454, "review_required": 0, "unassigned_within_source": 0, "semantic_correctness": "NOT VERIFIED", "records": question_records},
        "evidence": {
            "technical_report": f"content-staging/reconstruction/technical/{SID}.json",
            "discovery_report": f"content-staging/reconstruction/exams/source-groups/{SID}-discovery.json",
            "visual_review": "all 124 pages directly reviewed in contact sheets 001-012 through 121-124",
            "visual_discovery_workflow_run": "NOT APPLICABLE — direct local source review",
            "storage_identity_used_as_final_boundary": False,
            "raw_mutations": 0,
        },
        "status": "boundary_verified_legacy_questions_structurally_linked_answer_keys_not_verified",
    }
    OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"source_group_id": SID, "models": 31, "exam_pages": 124, "questions_exam_linked": 454, "correction_candidates": 31, "verified_answer_keys": 0, "duplicate_sha_groups": 9, "raw_mutations": 0}, ensure_ascii=False))


if __name__ == "__main__":
    main()
