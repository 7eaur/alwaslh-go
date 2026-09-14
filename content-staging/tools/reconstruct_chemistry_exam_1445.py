#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_ID = "e101d097-7a14-44e5-b242-cdeb9a312b77"
SUBJECT_DIR = ROOT / "content-staging" / "raw" / "legacy-supabase" / "subjects" / SOURCE_ID
TECH_PATH = ROOT / "content-staging" / "reconstruction" / "technical" / f"{SOURCE_ID}.json"
DISCOVERY_PATH = ROOT / "content-staging" / "reconstruction" / "exams" / "source-groups" / f"{SOURCE_ID}-discovery.json"
OUT_PATH = ROOT / "content-staging" / "reconstruction" / "exams" / "source-groups" / f"{SOURCE_ID}.json"


def main():
    subject = json.loads((SUBJECT_DIR / "subject.json").read_text(encoding="utf-8"))
    manifest = json.loads((SUBJECT_DIR / "manifest.json").read_text(encoding="utf-8"))
    tech = json.loads(TECH_PATH.read_text(encoding="utf-8"))
    discovery = json.loads(DISCOVERY_PATH.read_text(encoding="utf-8"))

    if not tech.get("all_images_technically_verified"):
        raise SystemExit("Technical verification is not green")
    checks = tech.get("checks", {})
    for key in ("existing_files", "readable_images", "sha256_matches", "byte_size_matches", "mime_matches"):
        if checks.get(key) != 60:
            raise SystemExit(f"Expected 60 for {key}, got {checks.get(key)}")
    seq = tech.get("page_sequence", {})
    if seq.get("first_page_number") != 1 or seq.get("last_page_number") != 60 or seq.get("missing_page_numbers") or seq.get("duplicate_page_numbers"):
        raise SystemExit("Unexpected page sequence")
    if discovery.get("storage_lesson_identity_runs") != 1:
        raise SystemExit("Expected one storage lesson identity run")
    if manifest.get("counts", {}).get("pages") != 60 or manifest.get("counts", {}).get("questions") != 0:
        raise SystemExit("Unexpected source-group baseline")

    by_page = {int(item["page_number"]): item for item in manifest["images"]}
    if sorted(by_page) != list(range(1, 61)):
        raise SystemExit("Manifest is not exact 1..60")

    models = []
    for ordinal in range(1, 21):
        first = (ordinal - 1) * 3 + 1
        question_pages = [first, first + 1]
        correction_page = first + 2
        ordered = [first, first + 1, first + 2]
        records = [by_page[n] for n in ordered]
        models.append({
            "id": f"chemistry-1445-exam-{ordinal:02d}",
            "internal_ordinal": ordinal,
            "official_model_code": "NOT VERIFIED",
            "official_title": "NOT VERIFIED",
            "academic_year_hijri": "1445",
            "academic_year_gregorian": "2023-2024",
            "term": "NOT VERIFIED",
            "exam_type": "وزاري",
            "first_page": first,
            "last_page": first + 2,
            "page_count": 3,
            "ordered_page_numbers": ordered,
            "ordered_legacy_page_ids": [r.get("legacy_page_id") for r in records],
            "raw_paths": [r.get("raw_path") for r in records],
            "question_pages": question_pages,
            "correction_sheet_candidate_page": correction_page,
            "answer_key": {
                "status": "NOT VERIFIED",
                "reason": "The third page is visually a correction/electronic-answer sheet linked to the two preceding question pages, but available evidence does not explicitly establish it as an official answer key."
            },
            "associated_legacy_questions": 0,
            "boundary_status": "verified",
            "boundary_evidence": [
                "All 60 pages visually inspected in five complete 12-page contact sheets.",
                "The pattern repeats consistently: two question pages followed by one correction/electronic-answer sheet.",
                "Each question pair restarts the exam-question sequence and the following correction sheet covers the corresponding response set.",
                "The 60-page source therefore resolves into 20 contiguous three-page exam models."
            ],
            "review_status": "boundary_verified_answer_key_unverified"
        })

    output = {
        "schema_version": 1,
        "source_group_id": SOURCE_ID,
        "source_group_name": subject["subject"]["name"],
        "class_id": subject["class"]["id"],
        "class_name": subject["class"]["name"].strip(),
        "subject": "الكيمياء",
        "classification": "exam_source_group",
        "academic_year_hijri": "1445",
        "academic_year_gregorian": "2023-2024",
        "source_pages": 60,
        "source_questions": 0,
        "individual_exam_model_count": 20,
        "exam_page_count": 60,
        "verified_answer_key_count": 0,
        "correction_sheet_candidate_count": 20,
        "models": models,
        "technical_verification": checks,
        "duplicate_sha256_groups_within_source": len(tech.get("duplicate_sha256_groups_within_subject") or []),
        "evidence": {
            "technical_report": str(TECH_PATH.relative_to(ROOT)).replace("\\", "/"),
            "discovery_report": str(DISCOVERY_PATH.relative_to(ROOT)).replace("\\", "/"),
            "visual_review": "all pages reviewed in contact sheets 001-012, 013-024, 025-036, 037-048, 049-060",
            "storage_lesson_identity_runs": 1,
            "storage_identity_used_as_final_boundary": False,
            "raw_mutations": 0
        },
        "status": "processed_boundary_verified_answer_keys_not_verified",
        "notes": [
            "The legacy 60-page source group is not treated as one exam.",
            "20 Individual Exam Models are verified by repeated visual page structure, three pages per model.",
            "Third pages are retained as correction-sheet candidates; official Answer Key status remains NOT VERIFIED.",
            "Official model numbers/titles and term remain NOT VERIFIED rather than inferred from source order.",
            "No RAW file was modified and no import/publication was performed."
        ]
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "source_group_id": SOURCE_ID,
        "individual_exam_models": 20,
        "exam_pages": 60,
        "correction_sheet_candidates": 20,
        "verified_answer_keys": 0,
        "legacy_questions": 0,
        "raw_mutations": 0
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
