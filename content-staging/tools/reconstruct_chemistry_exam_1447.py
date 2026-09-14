#!/usr/bin/env python3
import json
from collections import OrderedDict, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_ID = "e7c8291c-e904-4e8c-9cd8-2753818cedf3"
SUBJECT_DIR = ROOT / "content-staging/raw/legacy-supabase/subjects" / SOURCE_ID
TECH_PATH = ROOT / "content-staging/reconstruction/technical" / f"{SOURCE_ID}.json"
DISCOVERY_PATH = ROOT / "content-staging/reconstruction/exams/source-groups" / f"{SOURCE_ID}-discovery.json"
OUT_PATH = ROOT / "content-staging/reconstruction/exams/source-groups" / f"{SOURCE_ID}.json"

# Full visual review of all 124 source pages. Each tuple is:
# first_page, question_model_code, correction_report_model_code, status.
BLOCKS = [
    (1, "P.28", "P.28", "verified"),
    (5, "P.63", "P.63", "verified"),
    (9, "P.10", "P.10", "verified"),
    (13, "P.2", "P.2", "verified"),
    (17, "P.84", "P.84", "verified"),
    (21, "P.23", "P.23", "verified"),
    (25, "P.97", "P.97", "verified"),
    (29, "P.55", "P.55", "verified"),
    (33, "P.30", "P.30", "verified"),
    (37, "P.61", "P.31", "review_required"),
    (41, "P.7", "P.7", "verified"),
    (45, "P.28", "P.88", "review_required"),
    (49, "P.8", "P.8", "verified"),
    (53, "P.45", "P.45", "verified"),
    (57, "P.8", "P.8", "verified"),
    (61, "P.80", "P.80", "verified"),
    (65, "P.61", "P.61", "verified"),
    (69, "P.71", "P.71", "verified"),
    (73, "P.6", "P.6", "verified"),
    (77, "P.44", "P.44", "verified"),
    (81, "P.57", "P.57", "verified"),
    (85, "P.106", "P.106", "verified"),
    (89, "P.89", "P.89", "verified"),
    (93, "P.77", "P.77", "verified"),
    (97, "P.19", "P.19", "verified"),
    (101, "P.18", "P.18", "verified"),
    (105, "P.21", "P.21", "verified"),
    (109, "P.64", "P.64", "verified"),
    (113, "P.56", "P.56", "verified"),
    (117, "P.12", "P.12", "verified"),
    (121, "P.9", "P.9", "verified"),
]

EXPECTED_DUPLICATE_PAGE_PAIRS = {
    (1, 45), (2, 46), (3, 47),
    (37, 65), (38, 66), (39, 67),
    (49, 57), (50, 58), (51, 59),
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def load_pages():
    payload = json.loads((SUBJECT_DIR / "pages.json").read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("pages", "records", "items", "data"):
            if isinstance(payload.get(key), list):
                return payload[key]
    raise SystemExit("Unsupported pages.json shape")


def page_question_count(page):
    questions = page.get("ai_questions") or []
    if not isinstance(questions, list):
        raise SystemExit(f"Malformed ai_questions at page {page.get('page_number')}")
    return len(questions)


def page_payload(by_image, page_numbers):
    records = [by_image[n] for n in page_numbers]
    return {
        "ordered_page_numbers": page_numbers,
        "ordered_legacy_page_ids": [r.get("legacy_page_id") for r in records],
        "raw_paths": [r.get("raw_path") for r in records],
        "sha256": [r.get("sha256") for r in records],
    }


def model_id(code):
    return f"chemistry-1447-model-{code.lower().replace('.', '-')}"


def main():
    subject = json.loads((SUBJECT_DIR / "subject.json").read_text(encoding="utf-8"))
    manifest = json.loads((SUBJECT_DIR / "manifest.json").read_text(encoding="utf-8"))
    tech = json.loads(TECH_PATH.read_text(encoding="utf-8"))
    discovery = json.loads(DISCOVERY_PATH.read_text(encoding="utf-8"))

    checks = tech.get("checks", {})
    if not tech.get("all_images_technically_verified"):
        raise SystemExit("Technical verification is not green")
    for key in ("existing_files", "readable_images", "sha256_matches", "byte_size_matches", "mime_matches"):
        if checks.get(key) != 124:
            raise SystemExit(f"Expected 124 for {key}, got {checks.get(key)}")
    seq = tech.get("page_sequence", {})
    if seq.get("first_page_number") != 1 or seq.get("last_page_number") != 124 or seq.get("missing_page_numbers") or seq.get("duplicate_page_numbers"):
        raise SystemExit("Unexpected page sequence")
    if discovery.get("storage_lesson_identity_runs") != 1:
        raise SystemExit("Expected one storage lesson identity run")
    if manifest.get("counts", {}).get("pages") != 124 or manifest.get("counts", {}).get("questions") != 226:
        raise SystemExit("Unexpected source-group baseline")

    images = manifest.get("images") or []
    by_image = {int(x["page_number"]): x for x in images}
    if sorted(by_image) != list(range(1, 125)):
        raise SystemExit("Manifest is not exact 1..124")

    sha_pages = defaultdict(list)
    for n, record in by_image.items():
        sha_pages[record.get("sha256")].append(n)
    actual_pairs = {tuple(sorted(v)) for v in sha_pages.values() if len(v) > 1}
    if actual_pairs != EXPECTED_DUPLICATE_PAGE_PAIRS:
        raise SystemExit(f"Unexpected exact duplicate page groups: {sorted(actual_pairs)}")
    if len(tech.get("duplicate_sha256_groups_within_subject") or []) != 9:
        raise SystemExit("Expected 9 duplicate SHA groups")

    pages = load_pages()
    by_page = {int(p["page_number"]): p for p in pages if isinstance(p.get("page_number"), int)}
    if sorted(by_page) != list(range(1, 125)):
        raise SystemExit("pages.json is not exact 1..124")
    page_question_counts = {n: page_question_count(by_page[n]) for n in range(1, 125)}
    if sum(page_question_counts.values()) != 226:
        raise SystemExit("Question total does not equal manifest baseline 226")

    occurrences = []
    review_blocks = []
    valid_by_code = OrderedDict()
    page_to_model = {}
    review_pages = set()

    for ordinal, (first, q_code, correction_code, status) in enumerate(BLOCKS, 1):
        ordered = list(range(first, first + 4))
        payload = page_payload(by_image, ordered)
        q_count = sum(page_question_counts[n] for n in ordered)
        row = {
            "source_block_ordinal": ordinal,
            "first_page": first,
            "last_page": first + 3,
            "page_count": 4,
            **payload,
            "question_pages": ordered[:3],
            "correction_sheet_candidate_page": ordered[3],
            "question_model_code": q_code,
            "correction_report_model_code": correction_code,
            "source_block_question_count": q_count,
            "status": status,
        }
        if status == "verified":
            if q_code != correction_code:
                raise SystemExit(f"Verified block has mismatched codes at {first}")
            row["correction_relation"] = "verified_by_visual_model_code_and_contiguous_candidate_report"
            occurrences.append(row)
            valid_by_code.setdefault(q_code, []).append(row)
            for n in ordered:
                page_to_model[n] = model_id(q_code)
        else:
            if q_code == correction_code:
                raise SystemExit(f"Review block unexpectedly matches at {first}")
            row["review_reason"] = "question_model_code_and_correction_report_model_code_do_not_match"
            row["candidate_classification"] = "duplicate_source_import_candidate_review_required"
            review_blocks.append(row)
            review_pages.update(ordered)

    if len(occurrences) != 29 or len(valid_by_code) != 28 or len(review_blocks) != 2:
        raise SystemExit("Unexpected verified/review/model counts")
    if [x["first_page"] for x in review_blocks] != [37, 45]:
        raise SystemExit("Unexpected review-required block positions")
    if len(valid_by_code.get("P.8", [])) != 2:
        raise SystemExit("P.8 repeat not resolved")

    models = []
    for ordinal, (code, model_occurrences) in enumerate(valid_by_code.items(), 1):
        canonical = model_occurrences[0]
        associated_questions = sum(o["source_block_question_count"] for o in model_occurrences)
        model = {
            "id": model_id(code),
            "internal_ordinal": ordinal,
            "official_model_code": code,
            "official_title": "اختبار الشهادة الثانوية العامة (القسم العلمي) - الكيمياء",
            "academic_year_hijri": "1447",
            "academic_year_gregorian": "2025-2026",
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
            "source_occurrence_count": len(model_occurrences),
            "source_occurrences": model_occurrences,
            "associated_legacy_questions": associated_questions,
            "answer_key": {
                "status": "NOT VERIFIED",
                "reason": "The fourth page is a candidate-specific electronic correction report with answer/result data, but the source does not explicitly establish it as a standalone official Answer Key."
            },
            "boundary_status": "verified",
            "boundary_evidence": [
                "All 124 pages were visually inspected through eleven complete contact sheets.",
                "Verified source blocks contain three question pages followed by a contiguous candidate-specific electronic correction report with a matching visible model code.",
                "Academic year 1447 / 2025-2026 is visible in the source exam/correction headers.",
                "No 1445 or 1446 page-count rule was assumed; the four-page block structure is source-local evidence."
            ],
            "review_status": "boundary_verified_correction_relation_verified_answer_key_unverified"
        }
        if code == "P.8":
            model["repeat_classification"] = {
                "classification": "legitimate_repeated_exam_model_occurrence",
                "canonical_occurrence_pages": model_occurrences[0]["ordered_page_numbers"],
                "repeated_occurrence_pages": [o["ordered_page_numbers"] for o in model_occurrences[1:]],
                "reason": "Question pages 49..51 and 57..59 are exact-SHA duplicates with the same visible P.8 model code, while correction reports 52 and 60 are distinct candidate-specific reports for P.8."
            }
        if code == "P.28":
            model["related_review_required_block"] = [45, 46, 47, 48]
        if code == "P.61":
            model["related_review_required_block"] = [37, 38, 39, 40]
        models.append(model)

    linked_questions = sum(page_question_counts[n] for n in page_to_model)
    review_questions = sum(page_question_counts[n] for n in review_pages)
    if linked_questions + review_questions != 226:
        raise SystemExit("Not all 226 questions are structurally accounted for")

    mappings = []
    for n in range(1, 125):
        page = by_page[n]
        questions = page.get("ai_questions") or []
        for index, question in enumerate(questions, 1):
            if n in page_to_model:
                mappings.append({
                    "page_number": n,
                    "legacy_page_id": page.get("id"),
                    "question_ordinal_on_page": index,
                    "source_reference": question.get("source_reference") if isinstance(question, dict) else None,
                    "mapping_status": "exam_linked_structural",
                    "individual_exam_model_id": page_to_model[n],
                })
            else:
                mappings.append({
                    "page_number": n,
                    "legacy_page_id": page.get("id"),
                    "question_ordinal_on_page": index,
                    "source_reference": question.get("source_reference") if isinstance(question, dict) else None,
                    "mapping_status": "review_required",
                    "individual_exam_model_id": "NOT VERIFIED",
                    "reason": "source_block_question_and_correction_model_codes_mismatch",
                })
    if len(mappings) != 226:
        raise SystemExit("Question mapping record count mismatch")

    duplicate_resolution = [
        {
            "question_page_blocks": [[49, 50, 51], [57, 58, 59]],
            "model_code": "P.8",
            "classification": "legitimate_repeated_exam_model_occurrence",
            "correction_pages": [52, 60],
            "action": "preserve_both_occurrences_and_link_to_one_unique_model"
        },
        {
            "question_page_blocks": [[37, 38, 39], [65, 66, 67]],
            "model_code": "P.61",
            "classification": "review_required",
            "candidate_classification": "duplicate_source_import_candidate",
            "correction_pages": [40, 68],
            "evidence": "page 40 visibly reports P.31 while page 68 reports matching P.61",
            "action": "preserve_all_pages; finalize only 65..68 as P.61; isolate 37..40"
        },
        {
            "question_page_blocks": [[1, 2, 3], [45, 46, 47]],
            "model_code": "P.28",
            "classification": "review_required",
            "candidate_classification": "duplicate_source_import_candidate",
            "correction_pages": [4, 48],
            "evidence": "page 48 visibly reports P.88 while page 4 reports matching P.28",
            "action": "preserve_all_pages; finalize only 1..4 as P.28; isolate 45..48"
        }
    ]

    output = {
        "schema_version": 1,
        "source_group_id": SOURCE_ID,
        "source_group_name": subject["subject"]["name"],
        "class_id": subject["class"]["id"],
        "class_name": subject["class"]["name"].strip(),
        "subject": "الكيمياء",
        "classification": "exam_source_group",
        "academic_year_hijri": "1447",
        "academic_year_gregorian": "2025-2026",
        "term": "NOT VERIFIED",
        "source_pages": 124,
        "source_questions": 226,
        "source_blocks_reviewed": 31,
        "verified_source_occurrence_count": 29,
        "review_required_block_count": 2,
        "individual_exam_model_count": 28,
        "finalized_exam_page_count": 116,
        "review_required_page_count": 8,
        "verified_answer_key_count": 0,
        "correction_sheet_candidate_count": 31,
        "model_matched_correction_report_count": 29,
        "correction_only_mismatch_candidates": [
            {"page": 40, "visible_model_code": "P.31", "question_pages": "NOT VERIFIED", "relation": "NOT VERIFIED"},
            {"page": 48, "visible_model_code": "P.88", "question_pages": "NOT VERIFIED", "relation": "NOT VERIFIED"}
        ],
        "models": models,
        "verified_source_occurrences": occurrences,
        "review_required_blocks": review_blocks,
        "duplicate_resolution": duplicate_resolution,
        "question_mapping": {
            "legacy_questions": 226,
            "exam_linked_structural": linked_questions,
            "review_required": review_questions,
            "unassigned_within_source": 0,
            "page_question_counts": page_question_counts,
            "records": mappings,
            "semantic_correctness": "NOT VERIFIED"
        },
        "technical_verification": checks,
        "duplicate_sha256_groups_within_source": 9,
        "evidence": {
            "technical_report": rel(TECH_PATH),
            "discovery_report": rel(DISCOVERY_PATH),
            "visual_review": "all 124 pages reviewed in eleven contact sheets 001-012 through 121-124",
            "storage_lesson_identity_runs": 1,
            "storage_identity_used_as_final_boundary": False,
            "raw_mutations": 0
        },
        "status": "processed_boundary_verified_with_review_required_mismatches_answer_keys_not_verified",
        "notes": [
            "Twenty-nine source blocks have matching question/correction model codes and resolve to 28 unique Individual Exam Models because P.8 legitimately repeats.",
            "Blocks 37..40 (P.61 questions / P.31 correction) and 45..48 (P.28 questions / P.88 correction) are isolated as review_required; no missing question pages are fabricated.",
            "All 124 RAW pages are preserved. Only 116 pages belong to finalized verified model occurrences; 8 pages remain isolated for review.",
            "All 226 legacy questions are structurally accounted for by page membership; semantic correctness remains NOT VERIFIED.",
            "Official standalone Answer Keys remain NOT VERIFIED and no import/publication is performed."
        ]
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    discovery["individual_exam_models"] = 28
    discovery["answer_keys"] = "NOT VERIFIED"
    discovery["final_boundary_result"] = {
        "status": output["status"],
        "source_blocks_reviewed": 31,
        "verified_occurrences": 29,
        "unique_individual_exam_models": 28,
        "finalized_exam_pages": 116,
        "review_required_blocks": [[37, 40], [45, 48]],
        "review_required_pages": 8,
        "correction_sheet_candidates": 31,
        "verified_answer_keys": 0,
        "exam_linked_questions": linked_questions,
        "review_required_questions": review_questions,
        "reconstruction_path": rel(OUT_PATH)
    }
    discovery["raw_mutations"] = 0
    DISCOVERY_PATH.write_text(json.dumps(discovery, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps({
        "source_group_id": SOURCE_ID,
        "verified_occurrences": 29,
        "review_required_blocks": 2,
        "individual_exam_models": 28,
        "finalized_exam_pages": 116,
        "review_required_pages": 8,
        "correction_sheet_candidates": 31,
        "verified_answer_keys": 0,
        "legacy_questions": 226,
        "exam_linked_questions": linked_questions,
        "review_required_questions": review_questions,
        "raw_mutations": 0
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
