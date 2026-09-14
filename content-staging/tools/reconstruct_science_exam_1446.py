#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_ID = "004c02be-3f55-49e1-bbdc-b0824491bd68"
SUBJECT_DIR = ROOT / "content-staging/raw/legacy-supabase/subjects" / SOURCE_ID
TECH_PATH = ROOT / "content-staging/reconstruction/technical" / f"{SOURCE_ID}.json"
DISCOVERY_PATH = ROOT / "content-staging/reconstruction/exams/source-groups" / f"{SOURCE_ID}-discovery.json"
OUT_PATH = ROOT / "content-staging/reconstruction/exams/source-groups" / f"{SOURCE_ID}.json"


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


def qcount(page):
    questions = page.get("ai_questions") or []
    if not isinstance(questions, list):
        raise SystemExit(f"Malformed ai_questions at page {page.get('page_number')}")
    return len(questions)


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
    if manifest.get("counts", {}).get("pages") != 39 or manifest.get("counts", {}).get("questions") != 30:
        raise SystemExit("unexpected manifest baseline")
    if discovery.get("page_sequence", {}).get("count") != 39 or not discovery.get("page_sequence", {}).get("contiguous"):
        raise SystemExit("discovery sequence mismatch")

    expected_titles = {}
    for model in range(1, 14):
        first = (model - 1) * 3 + 1
        expected_titles[first] = f"النموذج {model} الورقة 1"
        expected_titles[first + 1] = f"النموذج {model} الورقة 2"
        expected_titles[first + 2] = f"نموذج التصحيح النموذج {model}"
    actual_titles = {int(x["page_number"]): str(x["title"]).strip() for x in tech.get("metadata_boundary_candidates", [])}
    expected_titles = {k: v.strip() for k, v in expected_titles.items()}
    if actual_titles != expected_titles:
        raise SystemExit("page titles do not match the verified 13-model source-local sequence")

    images = {int(x["page_number"]): x for x in manifest.get("images", [])}
    if sorted(images) != list(range(1, 40)):
        raise SystemExit("manifest images not exact 1..39")
    pages = load_pages()
    by_page = {int(p["page_number"]): p for p in pages if isinstance(p.get("page_number"), int)}
    if sorted(by_page) != list(range(1, 40)):
        raise SystemExit("pages.json not exact 1..39")
    page_qcounts = {n: qcount(by_page[n]) for n in range(1, 40)}
    if sum(page_qcounts.values()) != 30:
        raise SystemExit("question total mismatch")

    models = []
    mappings = []
    for model in range(1, 14):
        first = (model - 1) * 3 + 1
        nums = [first, first + 1, first + 2]
        records = [images[n] for n in nums]
        model_id = f"science-1446-exam-{model:02d}"
        associated = sum(page_qcounts[n] for n in nums)
        models.append({
            "id": model_id,
            "internal_ordinal": model,
            "source_model_label": f"النموذج {model}",
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
            "associated_legacy_questions": associated,
            "boundary_status": "verified",
            "answer_key": {
                "status": "NOT VERIFIED",
                "reason": "The third page is visibly an electronic correction/result sheet paired with the same source model, but available evidence does not establish it as a standalone official Answer Key."
            },
            "boundary_evidence": [
                "All 39 source pages were visually reviewed in complete contact sheets.",
                f"Source metadata explicitly labels pages {first} and {first+1} as model {model} papers 1 and 2 and page {first+2} as the correction model for model {model}.",
                "Visual review independently confirms two question-form pages followed by an electronic correction/result sheet for every one of the 13 source-local blocks.",
                "The source-local three-page pattern is verified independently for Science 1446 and is not inherited from Science 1445 or Chemistry."
            ],
            "review_status": "boundary_verified_answer_key_unverified"
        })
        for n in nums:
            page = by_page[n]
            questions = page.get("ai_questions") or []
            for idx, question in enumerate(questions, 1):
                mappings.append({
                    "page_number": n,
                    "legacy_page_id": page.get("id"),
                    "question_ordinal_on_page": idx,
                    "source_reference": question.get("source_reference") if isinstance(question, dict) else None,
                    "mapping_status": "exam_linked_structural",
                    "individual_exam_model_id": model_id,
                })

    if len(mappings) != 30:
        raise SystemExit("question mapping record count mismatch")

    output = {
        "schema_version": 1,
        "source_group_id": SOURCE_ID,
        "source_group_name": subject["subject"]["name"],
        "class_id": subject["class"]["id"],
        "class_name": subject["class"]["name"],
        "subject": "العلوم",
        "classification": "exam_source_group",
        "academic_year_hijri": "1446",
        "academic_year_gregorian": "2024-2025",
        "source_pages": 39,
        "source_questions": 30,
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
            "exam_linked_structural": 30,
            "review_required": 0,
            "unassigned_within_source": 0,
            "semantic_correctness": "NOT VERIFIED",
            "records": mappings,
        },
        "evidence": {
            "technical_report": f"content-staging/reconstruction/technical/{SOURCE_ID}.json",
            "discovery_report": f"content-staging/reconstruction/exams/source-groups/{SOURCE_ID}-discovery.json",
            "visual_review": "all 39 pages reviewed in contact sheets 001-012, 013-024, 025-036, 037-039",
            "discovery_workflow_run": 34811638024,
            "storage_identity_used_as_final_boundary": False,
            "raw_mutations": 0,
        },
        "status": "boundary_verified_questions_structurally_mapped_answer_keys_not_verified"
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "source_group_id": SOURCE_ID,
        "models": 13,
        "exam_pages": 39,
        "questions_exam_linked": 30,
        "correction_candidates": 13,
        "verified_answer_keys": 0,
        "raw_mutations": 0,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
