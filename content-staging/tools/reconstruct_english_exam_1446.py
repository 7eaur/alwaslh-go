#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_ID = "062f0aa0-ae21-454e-ad9a-c390df6e4a08"
SUBJECT_DIR = ROOT / "content-staging/raw/legacy-supabase/subjects" / SOURCE_ID
TECH_PATH = ROOT / "content-staging/reconstruction/technical" / f"{SOURCE_ID}.json"
DISCOVERY_PATH = ROOT / "content-staging/reconstruction/exams/source-groups" / f"{SOURCE_ID}-discovery.json"
OUT_PATH = ROOT / "content-staging/reconstruction/exams/source-groups" / f"{SOURCE_ID}.json"
VISIBLE_CORRECTION_CODES = ["97.51", "97.52", "97.14", "97.13", "97.40", "97.22", "97.107", "97.5", "97.9", "97.3", "97.53", "97.4", "97.41"]


def load_pages():
    payload = json.loads((SUBJECT_DIR / "pages.json").read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("pages", "records", "items", "data"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    raise SystemExit("Unsupported pages.json shape")


def main():
    subject = json.loads((SUBJECT_DIR / "subject.json").read_text(encoding="utf-8"))
    manifest = json.loads((SUBJECT_DIR / "manifest.json").read_text(encoding="utf-8"))
    tech = json.loads(TECH_PATH.read_text(encoding="utf-8"))
    discovery = json.loads(DISCOVERY_PATH.read_text(encoding="utf-8"))

    if not tech.get("all_images_technically_verified"):
        raise SystemExit("technical verification not green")
    for key in ("existing_files", "readable_images", "sha256_matches", "byte_size_matches", "mime_matches"):
        if tech.get("checks", {}).get(key) != 39:
            raise SystemExit(f"expected 39 for {key}")
    seq = tech.get("page_sequence", {})
    if seq.get("first_page_number") != 1 or seq.get("last_page_number") != 39 or seq.get("missing_page_numbers") or seq.get("duplicate_page_numbers"):
        raise SystemExit("unexpected page sequence")
    if tech.get("duplicate_sha256_groups_within_subject"):
        raise SystemExit("unexpected within-source duplicate SHA groups")
    if manifest.get("counts", {}).get("pages") != 39 or manifest.get("counts", {}).get("questions") != 0:
        raise SystemExit("unexpected manifest baseline")
    if discovery.get("page_sequence", {}).get("count") != 39 or not discovery.get("page_sequence", {}).get("contiguous"):
        raise SystemExit("discovery sequence mismatch")

    expected_titles = {}
    for model in range(1, 14):
        first = (model - 1) * 3 + 1
        expected_titles[first] = f"النموذج {model} الورقة 1"
        expected_titles[first + 1] = f"النموذج {model} الورقة 2"
        expected_titles[first + 2] = f"نموذج التصحيح النموذج {model}"
    actual_titles = {int(x["page_number"]): x["title"] for x in tech.get("metadata_boundary_candidates", [])}
    if actual_titles != expected_titles:
        raise SystemExit("page titles do not match the visually verified 13-model source-local sequence")

    images = {int(x["page_number"]): x for x in manifest.get("images", [])}
    if sorted(images) != list(range(1, 40)):
        raise SystemExit("manifest images not exact 1..39")
    pages = load_pages()
    by_page = {int(p["page_number"]): p for p in pages if isinstance(p.get("page_number"), int)}
    if sorted(by_page) != list(range(1, 40)):
        raise SystemExit("pages.json not exact 1..39")
    if any((p.get("ai_questions") or []) for p in by_page.values()):
        raise SystemExit("unexpected legacy questions in English 1446 source")

    models = []
    for model in range(1, 14):
        first = (model - 1) * 3 + 1
        nums = [first, first + 1, first + 2]
        records = [images[n] for n in nums]
        model_id = f"english-1446-exam-{model:02d}"
        models.append({
            "id": model_id,
            "internal_ordinal": model,
            "source_model_label": f"النموذج {model}",
            "visible_correction_form_code": VISIBLE_CORRECTION_CODES[model - 1],
            "official_model_code": "NOT VERIFIED",
            "official_title": "NOT VERIFIED",
            "academic_year_hijri": "1446",
            "academic_year_gregorian": "2024-2025",
            "term": "NOT VERIFIED",
            "exam_type": "وزاري",
            "first_page": first,
            "last_page": first + 2,
            "page_count": 3,
            "question_pages": [first, first + 1],
            "correction_sheet_candidate_page": first + 2,
            "ordered_page_numbers": nums,
            "ordered_legacy_page_ids": [r.get("legacy_page_id") for r in records],
            "raw_paths": [r.get("raw_path") for r in records],
            "sha256": [r.get("sha256") for r in records],
            "associated_legacy_questions": 0,
            "boundary_status": "verified",
            "answer_key": {
                "status": "NOT VERIFIED",
                "reason": "The third page is visibly an electronic correction/result sheet associated with the same source model, but available evidence does not establish a standalone official Answer Key artifact."
            },
            "boundary_evidence": [
                "All 39 source pages were visually reviewed in complete contact sheets.",
                f"Source metadata explicitly labels pages {first} and {first+1} as model {model} papers 1 and 2 and page {first+2} as the correction model for model {model}.",
                f"The correction/result page visibly carries form code {VISIBLE_CORRECTION_CODES[model - 1]}; it is recorded as visible evidence, not promoted to an official model code.",
                "The three-page occurrence is verified independently for English 1446 and is not inherited from English 1445 or another subject."
            ],
            "review_status": "boundary_verified_answer_key_unverified"
        })

    output = {
        "schema_version": 1,
        "source_group_id": SOURCE_ID,
        "source_group_name": subject["subject"]["name"],
        "class_id": subject["class"]["id"],
        "class_name": subject["class"]["name"],
        "subject": "الإنجليزي",
        "classification": "exam_source_group",
        "academic_year_hijri": "1446",
        "academic_year_gregorian": "2024-2025",
        "source_pages": 39,
        "source_questions": 0,
        "source_blocks_reviewed": 13,
        "verified_source_occurrence_count": 13,
        "review_required_block_count": 0,
        "individual_exam_model_count": 13,
        "finalized_exam_page_count": 39,
        "review_required_page_count": 0,
        "correction_sheet_candidate_count": 13,
        "verified_answer_key_count": 0,
        "duplicate_sha256_groups_within_source": 0,
        "models": models,
        "question_mapping": {
            "exam_linked_structural": 0,
            "review_required": 0,
            "unassigned_within_source": 0,
            "semantic_correctness": "NOT APPLICABLE — source has 0 legacy questions",
            "records": []
        },
        "evidence": {
            "technical_report": f"content-staging/reconstruction/technical/{SOURCE_ID}.json",
            "discovery_report": f"content-staging/reconstruction/exams/source-groups/{SOURCE_ID}-discovery.json",
            "visual_review": "all 39 pages reviewed in contact sheets 001-012, 013-024, 025-036, 037-039",
            "discovery_workflow_run": 34823356315,
            "visual_artifact_id": 10338234805,
            "storage_identity_used_as_final_boundary": False,
            "raw_mutations": 0
        },
        "status": "boundary_verified_no_legacy_questions_answer_keys_not_verified"
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "source_group_id": SOURCE_ID,
        "models": 13,
        "exam_pages": 39,
        "questions_exam_linked": 0,
        "correction_candidates": 13,
        "verified_answer_keys": 0,
        "raw_mutations": 0
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
