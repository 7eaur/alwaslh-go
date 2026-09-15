#!/usr/bin/env python3
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_ID = "6fa466f9-b930-437e-b091-947ee56407c4"
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
        if checks.get(key) != 80:
            raise SystemExit(f"expected 80 for {key}")
    if checks.get("failures") != 0 or tech.get("raw_mutations") != 0:
        raise SystemExit("technical failures or RAW mutation detected")
    sequence = tech.get("page_sequence", {})
    if (
        sequence.get("first_page_number") != 1
        or sequence.get("last_page_number") != 80
        or sequence.get("unique_page_numbers") != 80
        or sequence.get("missing_page_numbers")
        or sequence.get("duplicate_page_numbers")
    ):
        raise SystemExit("unexpected technical page sequence")
    if tech.get("duplicate_sha256_groups_within_subject"):
        raise SystemExit("unexpected within-source duplicate SHA groups")

    counts = manifest.get("counts", {})
    if counts != {
        "pages": 80,
        "image_references": 80,
        "images_downloaded": 80,
        "image_download_failures": 0,
        "questions": 0,
    }:
        raise SystemExit("unexpected manifest baseline")
    discovery_sequence = discovery.get("page_sequence", {})
    if (
        discovery_sequence.get("count") != 80
        or discovery_sequence.get("first") != 1
        or discovery_sequence.get("last") != 80
        or not discovery_sequence.get("contiguous")
    ):
        raise SystemExit("discovery sequence mismatch")
    if not isinstance(pages, list) or len(pages) != 80:
        raise SystemExit("pages.json is not the expected 80-record list")
    by_page = {int(page["page_number"]): page for page in pages}
    if sorted(by_page) != list(range(1, 81)):
        raise SystemExit("pages.json not exact 1..80")
    if any((page.get("ai_questions") or []) for page in pages):
        raise SystemExit("unexpected legacy questions")
    images = {int(image["page_number"]): image for image in manifest.get("images", [])}
    if sorted(images) != list(range(1, 81)):
        raise SystemExit("manifest images not exact 1..80")

    models = []
    for ordinal in range(1, 21):
        first = (ordinal - 1) * 4 + 1
        numbers = [first, first + 1, first + 2, first + 3]
        records = [images[number] for number in numbers]
        models.append(
            {
                "id": f"calculus-1445-exam-{ordinal:02d}",
                "internal_ordinal": ordinal,
                "source_model_label": f"source occurrence {ordinal}",
                "official_model_code": "NOT VERIFIED",
                "official_title": "NOT VERIFIED",
                "academic_year_hijri": "1445",
                "academic_year_gregorian": "2023-2024",
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
                "associated_legacy_questions": 0,
                "boundary_status": "verified",
                "answer_key": {
                    "status": "NOT VERIFIED",
                    "reason": "The fourth page is visibly a correction/result sheet paired with the preceding three question pages, but available evidence does not establish it as a standalone official Answer Key.",
                },
                "boundary_evidence": [
                    "All 80 source pages were directly reviewed in seven complete source-local contact sheets.",
                    f"Pages {first}..{first + 2} are question sheets and page {first + 3} is the paired correction/result sheet; this four-page sequence was checked for this occurrence.",
                    "The boundary decision is source-local and was not inherited from another subject or exam group.",
                ],
                "review_status": "boundary_verified_answer_key_unverified",
            }
        )

    output = {
        "schema_version": 1,
        "source_group_id": SOURCE_ID,
        "source_group_name": subject["subject"]["name"],
        "class_id": subject["class"]["id"],
        "class_name": subject["class"]["name"],
        "subject": "التفاضل والتكامل",
        "classification": "exam_source_group",
        "academic_year_hijri": "1445",
        "academic_year_gregorian": "2023-2024",
        "source_pages": 80,
        "source_questions": 0,
        "source_blocks_reviewed": 20,
        "verified_source_occurrence_count": 20,
        "review_required_block_count": 0,
        "individual_exam_model_count": 20,
        "finalized_exam_page_count": 80,
        "review_required_page_count": 0,
        "correction_sheet_candidate_count": 20,
        "verified_answer_key_count": 0,
        "duplicate_sha256_groups_within_source": 0,
        "models": models,
        "question_mapping": {
            "exam_linked_structural": 0,
            "review_required": 0,
            "unassigned_within_source": 0,
            "semantic_correctness": "NOT APPLICABLE — 0 legacy questions",
            "records": [],
        },
        "evidence": {
            "technical_report": f"content-staging/reconstruction/technical/{SOURCE_ID}.json",
            "discovery_report": f"content-staging/reconstruction/exams/source-groups/{SOURCE_ID}-discovery.json",
            "visual_review": "all 80 pages directly reviewed in contact sheets 001-012, 013-024, 025-036, 037-048, 049-060, 061-072, 073-080",
            "visual_discovery_workflow_run": "NOT APPLICABLE — direct local source review",
            "storage_identity_used_as_final_boundary": False,
            "raw_mutations": 0,
        },
        "status": "boundary_verified_zero_legacy_questions_answer_keys_not_verified",
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "source_group_id": SOURCE_ID,
                "models": 20,
                "exam_pages": 80,
                "questions_exam_linked": 0,
                "correction_candidates": 20,
                "verified_answer_keys": 0,
                "raw_mutations": 0,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
