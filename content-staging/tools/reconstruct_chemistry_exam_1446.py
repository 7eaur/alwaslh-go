#!/usr/bin/env python3
import json
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_ID = "c09ce569-ea42-4f0b-997f-95b029a7e6ea"
SUBJECT_DIR = ROOT / "content-staging" / "raw" / "legacy-supabase" / "subjects" / SOURCE_ID
TECH_PATH = ROOT / "content-staging" / "reconstruction" / "technical" / f"{SOURCE_ID}.json"
DISCOVERY_PATH = ROOT / "content-staging" / "reconstruction" / "exams" / "source-groups" / f"{SOURCE_ID}-discovery.json"
OUT_PATH = ROOT / "content-staging" / "reconstruction" / "exams" / "source-groups" / f"{SOURCE_ID}.json"

# Human visual review of the five 12-page contact sheets produced by the repository runner.
# Each occurrence is 3 question pages (Q1-30, Q31-49, Q50) followed by a candidate-specific
# electronic correction report. The model code is visible on the exam header.
OCCURRENCES = [
    (1, "P.87"),
    (5, "P.45"),
    (9, "P.52"),
    (13, "P.9"),
    (17, "P.3"),
    (21, "P.27"),
    (25, "P.5"),
    (29, "P.41"),
    (33, "P.72"),
    (37, "P.107"),
    (41, "P.41"),
    (45, "P.25"),
    (49, "P.40"),
    (53, "P.34"),
    (57, "P.89"),
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def source_records(manifest):
    by_page = {int(item["page_number"]): item for item in manifest["images"]}
    if sorted(by_page) != list(range(1, 61)):
        raise SystemExit("Manifest is not exact 1..60")
    return by_page


def page_payload(by_page, page_numbers):
    records = [by_page[n] for n in page_numbers]
    return {
        "ordered_page_numbers": page_numbers,
        "ordered_legacy_page_ids": [r.get("legacy_page_id") for r in records],
        "raw_paths": [r.get("raw_path") for r in records],
        "sha256": [r.get("sha256") for r in records],
    }


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

    by_page = source_records(manifest)

    expected_duplicate_pairs = [(29, 41), (30, 42), (31, 43)]
    for left, right in expected_duplicate_pairs:
        if by_page[left].get("sha256") != by_page[right].get("sha256"):
            raise SystemExit(f"Expected exact duplicate pages {left} and {right}")
    if by_page[32].get("sha256") == by_page[44].get("sha256"):
        raise SystemExit("Correction reports 32 and 44 unexpectedly became byte-identical")

    occurrence_rows = []
    for occurrence_ordinal, (first, model_code) in enumerate(OCCURRENCES, start=1):
        ordered = list(range(first, first + 4))
        qpages = ordered[:3]
        correction_page = ordered[3]
        payload = page_payload(by_page, ordered)
        occurrence_rows.append({
            "occurrence_ordinal": occurrence_ordinal,
            "model_code": model_code,
            "first_page": first,
            "last_page": first + 3,
            "page_count": 4,
            **payload,
            "question_pages": qpages,
            "correction_sheet_candidate_page": correction_page,
            "boundary_status": "verified",
            "correction_relation": "verified_by_visual_model_code_and_contiguous_response_report",
        })

    grouped = OrderedDict()
    for occurrence in occurrence_rows:
        grouped.setdefault(occurrence["model_code"], []).append(occurrence)

    if len(grouped) != 14 or len(occurrence_rows) != 15 or len(grouped.get("P.41", [])) != 2:
        raise SystemExit("Unexpected unique-model/source-occurrence count")

    models = []
    for ordinal, (model_code, occurrences) in enumerate(grouped.items(), start=1):
        canonical = occurrences[0]
        repeated = occurrences[1:]
        model = {
            "id": f"chemistry-1446-model-{model_code.lower().replace('.', '-')}",
            "internal_ordinal": ordinal,
            "official_model_code": model_code,
            "official_title": "اختبار الشهادة الثانوية العامة (القسم العلمي) - الكيمياء",
            "academic_year_hijri": "1446",
            "academic_year_gregorian": "2024-2025",
            "term": "NOT VERIFIED",
            "exam_type": "وزاري",
            "first_page": canonical["first_page"],
            "last_page": canonical["last_page"],
            "page_count": 4,
            "ordered_page_numbers": canonical["ordered_page_numbers"],
            "ordered_legacy_page_ids": canonical["ordered_legacy_page_ids"],
            "raw_paths": canonical["raw_paths"],
            "question_pages": canonical["question_pages"],
            "correction_sheet_candidate_page": canonical["correction_sheet_candidate_page"],
            "source_occurrence_count": len(occurrences),
            "source_occurrences": occurrences,
            "answer_key": {
                "status": "NOT VERIFIED",
                "reason": "The fourth page is visibly a candidate-specific 'نموذج التصحيح الإلكتروني' containing a correct-answer column and response/score data, but the available source does not explicitly establish it as a standalone official Answer Key."
            },
            "associated_legacy_questions": 0,
            "boundary_status": "verified",
            "boundary_evidence": [
                "All 60 pages were visually inspected through five complete 12-page contact sheets.",
                "Each source occurrence begins with a page whose header visibly states the model code and the 1446 / 2024-2025 secondary-certificate science-section exam context.",
                "Each occurrence contains three question pages: questions 1-30, 31-49, then question 50, followed by a model-matched electronic correction report.",
                "The correction report visibly carries the matching model identifier with a '2' prefix and candidate-specific identity/result fields."
            ],
            "review_status": "boundary_verified_correction_relation_verified_answer_key_unverified"
        }
        if repeated:
            model["repeat_classification"] = {
                "classification": "legitimate_repeated_exam_model_occurrence",
                "reason": "The repeated P.41 occurrence has exact-SHA-identical question pages 29-31 == 41-43 and the same visible model code, while correction pages 32 and 44 are distinct candidate-specific correction reports. All source pages are preserved; the repeat is not counted as a second unique Individual Exam Model.",
                "canonical_occurrence_pages": canonical["ordered_page_numbers"],
                "repeated_occurrence_pages": [r["ordered_page_numbers"] for r in repeated]
            }
        models.append(model)

    duplicate_resolution = {
        "classification": "legitimate_repeated_exam_model_occurrence",
        "model_code": "P.41",
        "exact_sha_duplicate_pairs": [[29, 41], [30, 42], [31, 43]],
        "canonical_occurrence_pages": [29, 30, 31, 32],
        "repeated_occurrence_pages": [41, 42, 43, 44],
        "correction_pages_byte_identical": False,
        "reason": "Visual review shows P.41 on both exam occurrences; the three question pages are exact SHA duplicates. The two correction reports show the same model but different candidate identity/result records, establishing a legitimate repeated occurrence of one model rather than a second unique model or an accidental byte duplicate.",
        "action": "preserve_all_source_pages_and_link_both_occurrences_to_one_unique_model"
    }

    output = {
        "schema_version": 1,
        "source_group_id": SOURCE_ID,
        "source_group_name": subject["subject"]["name"],
        "class_id": subject["class"]["id"],
        "class_name": subject["class"]["name"].strip(),
        "subject": "الكيمياء",
        "classification": "exam_source_group",
        "academic_year_hijri": "1446",
        "academic_year_gregorian": "2024-2025",
        "term": "NOT VERIFIED",
        "source_pages": 60,
        "source_questions": 0,
        "source_occurrence_count": 15,
        "individual_exam_model_count": 14,
        "exam_page_count": 60,
        "canonical_model_page_count": 56,
        "verified_answer_key_count": 0,
        "correction_sheet_candidate_count": 15,
        "models": models,
        "source_occurrences": occurrence_rows,
        "duplicate_resolution": duplicate_resolution,
        "technical_verification": checks,
        "duplicate_sha256_groups_within_source": len(tech.get("duplicate_sha256_groups_within_subject") or []),
        "evidence": {
            "technical_report": rel(TECH_PATH),
            "discovery_report": rel(DISCOVERY_PATH),
            "visual_review": "all pages reviewed in contact sheets 001-012, 013-024, 025-036, 037-048, 049-060",
            "visual_model_codes": [row["model_code"] for row in occurrence_rows],
            "unique_visual_model_codes": list(grouped.keys()),
            "storage_lesson_identity_runs": 1,
            "storage_identity_used_as_final_boundary": False,
            "raw_mutations": 0
        },
        "status": "processed_boundary_verified_repeat_classified_answer_keys_not_verified",
        "notes": [
            "The legacy 60-page source group is not treated as one exam.",
            "Fifteen contiguous four-page source occurrences are verified from 1446 visual evidence only; no 1445 page-count rule was assumed.",
            "Four-page occurrence structure: three question pages followed by a candidate-specific electronic correction report.",
            "Fourteen unique Individual Exam Models are verified because model P.41 occurs twice.",
            "Pages 29-31 and 41-43 are exact SHA duplicates and share visible model code P.41; pages 32 and 44 are distinct candidate-specific correction reports for that same model.",
            "Correction-report relations are verified, but official standalone Answer Key status remains NOT VERIFIED.",
            "Term remains NOT VERIFIED; no term was inferred.",
            "No RAW file was modified and no import/publication was performed."
        ]
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    discovery["individual_exam_models"] = 14
    discovery["answer_keys"] = "NOT VERIFIED"
    discovery["final_boundary_result"] = {
        "status": output["status"],
        "source_occurrences": 15,
        "unique_individual_exam_models": 14,
        "pages_per_source_occurrence": 4,
        "question_pages_per_occurrence": 3,
        "correction_sheet_candidates": 15,
        "verified_answer_keys": 0,
        "visual_model_codes": [row["model_code"] for row in occurrence_rows],
        "duplicate_resolution": duplicate_resolution,
        "reconstruction_path": rel(OUT_PATH)
    }
    discovery["raw_mutations"] = 0
    DISCOVERY_PATH.write_text(json.dumps(discovery, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps({
        "source_group_id": SOURCE_ID,
        "source_occurrences": 15,
        "individual_exam_models": 14,
        "exam_pages": 60,
        "correction_sheet_candidates": 15,
        "verified_answer_keys": 0,
        "repeated_model": "P.41",
        "repeat_classification": "legitimate_repeated_exam_model_occurrence",
        "legacy_questions": 0,
        "raw_mutations": 0
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
