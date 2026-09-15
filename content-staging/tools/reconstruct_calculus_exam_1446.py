#!/usr/bin/env python3
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_ID = "012196f1-a633-41cd-927b-d0b1b8845781"
SUBJECT_DIR = ROOT / "content-staging/raw/legacy-supabase/subjects" / SOURCE_ID
TECH_PATH = ROOT / "content-staging/reconstruction/technical" / f"{SOURCE_ID}.json"
DISCOVERY_PATH = ROOT / "content-staging/reconstruction/exams/source-groups" / f"{SOURCE_ID}-discovery.json"
OUT_PATH = ROOT / "content-staging/reconstruction/exams/source-groups" / f"{SOURCE_ID}.json"


def main():
    subject = json.loads((SUBJECT_DIR / "subject.json").read_text(encoding="utf-8"))
    manifest = json.loads((SUBJECT_DIR / "manifest.json").read_text(encoding="utf-8"))
    pages = json.loads((SUBJECT_DIR / "pages.json").read_text(encoding="utf-8"))
    tech = json.loads(TECH_PATH.read_text(encoding="utf-8"))
    discovery = json.loads(DISCOVERY_PATH.read_text(encoding="utf-8"))

    checks = tech.get("checks", {})
    if tech.get("all_images_technically_verified") is not True:
        raise SystemExit("technical verification not green")
    for key in (
        "manifest_image_count",
        "existing_files",
        "readable_images",
        "sha256_matches",
        "byte_size_matches",
        "mime_matches",
    ):
        if checks.get(key) != 100:
            raise SystemExit(f"expected 100 for {key}")
    if checks.get("failures") != 0 or tech.get("raw_mutations") != 0:
        raise SystemExit("technical failures or RAW mutation detected")
    sequence = tech.get("page_sequence", {})
    if (
        sequence.get("first_page_number") != 1
        or sequence.get("last_page_number") != 100
        or sequence.get("unique_page_numbers") != 100
        or sequence.get("missing_page_numbers")
        or sequence.get("duplicate_page_numbers")
    ):
        raise SystemExit("unexpected technical page sequence")
    duplicate_groups = tech.get("duplicate_sha256_groups_within_subject") or []
    if len(duplicate_groups) != 6 or any(int(group.get("count") or 0) != 2 for group in duplicate_groups):
        raise SystemExit("unexpected within-source duplicate SHA topology")

    counts = manifest.get("counts", {})
    if counts != {
        "pages": 100,
        "image_references": 100,
        "images_downloaded": 100,
        "image_download_failures": 0,
        "questions": 40,
    }:
        raise SystemExit("unexpected manifest baseline")
    discovery_sequence = discovery.get("page_sequence", {})
    if (
        discovery_sequence.get("count") != 100
        or discovery_sequence.get("first") != 1
        or discovery_sequence.get("last") != 100
        or not discovery_sequence.get("contiguous")
    ):
        raise SystemExit("discovery sequence mismatch")
    if not isinstance(pages, list) or len(pages) != 100:
        raise SystemExit("pages.json is not the expected 100-record list")
    by_page = {int(page["page_number"]): page for page in pages}
    if sorted(by_page) != list(range(1, 101)):
        raise SystemExit("pages.json not exact 1..100")
    question_distribution = {
        number: len(page.get("ai_questions") or [])
        for number, page in by_page.items()
        if page.get("ai_questions")
    }
    if question_distribution != {1: 21, 2: 13, 3: 6}:
        raise SystemExit(f"unexpected question distribution: {question_distribution}")
    images = {int(image["page_number"]): image for image in manifest.get("images", [])}
    if sorted(images) != list(range(1, 101)):
        raise SystemExit("manifest images not exact 1..100")

    models = []
    question_records = []
    total_questions = 0
    for ordinal in range(1, 26):
        first = (ordinal - 1) * 4 + 1
        numbers = [first, first + 1, first + 2, first + 3]
        records = [images[number] for number in numbers]
        model_id = f"calculus-1446-exam-{ordinal:02d}"
        associated = 0
        for number in numbers:
            page = by_page[number]
            legacy_page_id = page.get("id") or images[number].get("legacy_page_id")
            for question_ordinal, _question in enumerate(page.get("ai_questions") or [], start=1):
                associated += 1
                total_questions += 1
                question_records.append(
                    {
                        "source_page_number": number,
                        "legacy_page_id": legacy_page_id,
                        "source_question_ordinal_on_page": question_ordinal,
                        "individual_exam_model_id": model_id,
                        "mapping_status": "structural_page_membership_verified",
                        "semantic_correctness": "NOT VERIFIED",
                    }
                )
        models.append(
            {
                "id": model_id,
                "internal_ordinal": ordinal,
                "source_model_label": f"source occurrence {ordinal}",
                "official_model_code": "NOT VERIFIED",
                "official_title": "NOT VERIFIED",
                "academic_year_hijri": "1446",
                "academic_year_gregorian": "2024-2025",
                "term": "NOT VERIFIED",
                "exam_type": "وزاري",
                "first_page": first,
                "last_page": first + 3,
                "page_count": 4,
                "question_pages": [first, first + 1, first + 2],
                "correction_sheet_candidate_page": first + 3,
                "ordered_page_numbers": numbers,
                "ordered_legacy_page_ids": [record.get("legacy_page_id") for record in records],
                "raw_paths": [record.get("raw_path") for record in records],
                "sha256": [record.get("sha256") for record in records],
                "associated_legacy_questions": associated,
                "boundary_status": "verified",
                "answer_key": {
                    "status": "NOT VERIFIED",
                    "reason": "The fourth page is visibly a correction/result sheet paired with the preceding three question pages, but available evidence does not establish it as a standalone official Answer Key.",
                },
                "boundary_evidence": [
                    "All 100 source pages were directly reviewed in nine complete source-local contact sheets.",
                    f"Pages {first}..{first + 2} are question sheets and page {first + 3} is the paired correction/result sheet; this four-page sequence was checked for this occurrence.",
                    "The boundary decision is source-local and was not inherited from the Calculus 1445 source or another exam group.",
                ],
                "review_status": "boundary_verified_answer_key_unverified",
            }
        )

    if total_questions != 40 or len(question_records) != 40:
        raise SystemExit(f"expected 40 structurally mapped legacy questions, got {total_questions}")
    if models[0]["associated_legacy_questions"] != 40 or any(
        model["associated_legacy_questions"] for model in models[1:]
    ):
        raise SystemExit("question-to-model structural distribution mismatch")

    output = {
        "schema_version": 1,
        "source_group_id": SOURCE_ID,
        "source_group_name": subject["subject"]["name"],
        "class_id": subject["class"]["id"],
        "class_name": subject["class"]["name"],
        "subject": "التفاضل والتكامل",
        "classification": "exam_source_group",
        "academic_year_hijri": "1446",
        "academic_year_gregorian": "2024-2025",
        "source_pages": 100,
        "source_questions": 40,
        "source_blocks_reviewed": 25,
        "verified_source_occurrence_count": 25,
        "review_required_block_count": 0,
        "individual_exam_model_count": 25,
        "finalized_exam_page_count": 100,
        "review_required_page_count": 0,
        "correction_sheet_candidate_count": 25,
        "verified_answer_key_count": 0,
        "duplicate_sha256_groups_within_source": 6,
        "duplicate_sha256_groups": duplicate_groups,
        "duplicate_disposition": "preserved_as_distinct_source_occurrences_no_merge_no_raw_mutation",
        "models": models,
        "question_mapping": {
            "exam_linked_structural": 40,
            "review_required": 0,
            "unassigned_within_source": 0,
            "semantic_correctness": "NOT VERIFIED",
            "records": question_records,
        },
        "evidence": {
            "technical_report": f"content-staging/reconstruction/technical/{SOURCE_ID}.json",
            "discovery_report": f"content-staging/reconstruction/exams/source-groups/{SOURCE_ID}-discovery.json",
            "visual_review": "all 100 pages directly reviewed in contact sheets 001-012, 013-024, 025-036, 037-048, 049-060, 061-072, 073-084, 085-096, 097-100",
            "visual_discovery_workflow_run": "NOT APPLICABLE — direct local source review",
            "storage_identity_used_as_final_boundary": False,
            "raw_mutations": 0,
        },
        "status": "boundary_verified_legacy_questions_structurally_linked_answer_keys_not_verified",
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "source_group_id": SOURCE_ID,
                "models": 25,
                "exam_pages": 100,
                "questions_exam_linked": 40,
                "correction_candidates": 25,
                "verified_answer_keys": 0,
                "duplicate_sha_groups": 6,
                "raw_mutations": 0,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
