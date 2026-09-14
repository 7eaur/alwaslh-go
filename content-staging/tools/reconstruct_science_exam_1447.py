#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_ID = "14ef15e0-5524-473a-bbdb-996df35ba535"
SUBJECT_DIR = ROOT / "content-staging/raw/legacy-supabase/subjects" / SOURCE_ID
TECH_PATH = ROOT / "content-staging/reconstruction/technical" / f"{SOURCE_ID}.json"
DISCOVERY_PATH = ROOT / "content-staging/reconstruction/exams/source-groups" / f"{SOURCE_ID}-discovery.json"
ANOMALY_PATH = ROOT / "content-staging/reconstruction/exams/source-groups" / f"{SOURCE_ID}-anomaly-evidence.json"
OUT_PATH = ROOT / "content-staging/reconstruction/exams/source-groups" / f"{SOURCE_ID}.json"

MODEL12_PAPER2_ID = "e5be5a57-1052-4193-b525-ffa11912a6b2"
MODEL12_CORRECTION_ID = "4e7b1edf-37cf-44d1-9801-091a396a86b0"


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
        raise SystemExit(f"Malformed ai_questions for {page.get('id')}")
    return len(questions)


def norm(value):
    return " ".join(str(value or "").split())


def main():
    subject = json.loads((SUBJECT_DIR / "subject.json").read_text(encoding="utf-8"))
    manifest = json.loads((SUBJECT_DIR / "manifest.json").read_text(encoding="utf-8"))
    tech = json.loads(TECH_PATH.read_text(encoding="utf-8"))
    discovery = json.loads(DISCOVERY_PATH.read_text(encoding="utf-8"))
    anomaly = json.loads(ANOMALY_PATH.read_text(encoding="utf-8"))
    pages = load_pages()
    images = manifest.get("images") or []

    if not tech.get("all_images_technically_verified"):
        raise SystemExit("technical verification not green")
    for key in ("existing_files", "readable_images", "sha256_matches", "byte_size_matches", "mime_matches"):
        if tech.get("checks", {}).get(key) != 42:
            raise SystemExit(f"expected 42 for {key}")
    seq = tech.get("page_sequence", {})
    if seq.get("first_page_number") != 1 or seq.get("last_page_number") != 42:
        raise SystemExit("unexpected sequence endpoints")
    if seq.get("missing_page_numbers") != [35] or seq.get("duplicate_page_numbers") != [36]:
        raise SystemExit("Science 1447 numbering anomaly changed")
    if tech.get("duplicate_sha256_groups_within_subject"):
        raise SystemExit("unexpected within-source duplicate SHA groups")
    if manifest.get("counts", {}).get("pages") != 42 or manifest.get("counts", {}).get("questions") != 262:
        raise SystemExit("unexpected manifest baseline")
    if len(pages) != 42 or len(images) != 42:
        raise SystemExit("source record count mismatch")
    if discovery.get("page_sequence", {}).get("count") != 42 or discovery.get("page_sequence", {}).get("contiguous"):
        raise SystemExit("discovery sequence mismatch")

    expected_numbers = list(range(1, 35)) + [36, 36] + list(range(37, 43))
    page_numbers_in_source_order = [p.get("page_number") for p in pages]
    if page_numbers_in_source_order != expected_numbers:
        raise SystemExit(f"unexpected pages.json source order: {page_numbers_in_source_order}")

    anomaly_records = anomaly.get("page_records_34_37_in_source_order") or []
    anomaly_ids = [x.get("legacy_page_id") for x in anomaly_records]
    expected_anomaly_ids = [
        "d37e4aea-1164-46c9-a52e-99f71c3da511",
        MODEL12_PAPER2_ID,
        MODEL12_CORRECTION_ID,
        "cc03f87b-5d73-40a3-a7eb-c09e7545c78c",
    ]
    if anomaly_ids != expected_anomaly_ids:
        raise SystemExit("anomaly identity/order changed")

    images_by_id = {x.get("legacy_page_id"): x for x in images}
    if len(images_by_id) != 42 or any(p.get("id") not in images_by_id for p in pages):
        raise SystemExit("page/image identity reconciliation failed")

    # Verify the ordinary blocks by source order. Model 12 is intentionally handled
    # separately because both stored page number and one metadata title are corrupted.
    for model in list(range(1, 12)) + [13, 14]:
        block = pages[(model - 1) * 3:model * 3]
        expected = [
            f"النموذج {model} الورقة 1",
            f"النموذج {model} الورقة 2",
            f"نموذج التصحيح النموذج {model}",
        ]
        if [norm(p.get("title")) for p in block] != [norm(x) for x in expected]:
            raise SystemExit(f"metadata block mismatch for model {model}")

    model12 = pages[33:36]
    if model12[0].get("page_number") != 34 or norm(model12[0].get("title")) != norm("النموذج 12 الورقة 1"):
        raise SystemExit("model 12 paper 1 mismatch")
    if model12[1].get("id") != MODEL12_PAPER2_ID or model12[2].get("id") != MODEL12_CORRECTION_ID:
        raise SystemExit("model 12 anomaly order mismatch")
    if [p.get("page_number") for p in model12] != [34, 36, 36]:
        raise SystemExit("model 12 stored page numbers changed")
    if norm(model12[1].get("title")) != norm("نموذج التصحيح النموذج 12") or norm(model12[2].get("title")) != norm("نموذج التصحيح النموذج 12"):
        raise SystemExit("model 12 duplicated metadata-title anomaly changed")

    if sum(qcount(p) for p in pages) != 262:
        raise SystemExit("question total mismatch")

    models = []
    mappings = []
    for model in range(1, 15):
        block = pages[(model - 1) * 3:model * 3]
        image_records = [images_by_id[p.get("id")] for p in block]
        model_id = f"science-1447-exam-{model:02d}"
        associated = sum(qcount(p) for p in block)
        question_records = block[:2]
        correction_record = block[2]
        source_positions = list(range((model - 1) * 3 + 1, model * 3 + 1))
        evidence = [
            "All 42 source image records were technically verified and visually reviewed in complete contact sheets.",
            "The source is resolved by its own metadata, source-record order, image identity and visual evidence; no prior-year page pattern is inherited.",
        ]
        anomaly_note = None
        if model == 12:
            anomaly_note = {
                "classification": "source_metadata_numbering_and_title_collision_preserved",
                "stored_page_numbers": [34, 36, 36],
                "missing_stored_page_number": 35,
                "duplicate_stored_page_number": 36,
                "paper2_legacy_page_id": MODEL12_PAPER2_ID,
                "correction_legacy_page_id": MODEL12_CORRECTION_ID,
                "metadata_title_issue": "Both stored page-36 records are titled as correction model 12 in pages.json.",
                "resolution": "Visual evidence shows the first duplicate-title record in source order (e5be...) is the second question-form page, while the following record (4e7b...) is the electronic correction/result sheet. Stored numbers/titles are preserved; no page 35 is fabricated.",
            }
            evidence.extend([
                "Model 12 source order is page record 34 (paper 1), e5be... stored as page 36 (visually paper 2), then 4e7b... stored as page 36 (visibly correction/result sheet).",
                "The two page-36 image records have distinct SHA-256 identities; the anomaly is metadata numbering/title corruption, not a duplicate binary.",
            ])
        else:
            evidence.append(
                f"Source metadata and visual evidence agree on model {model}: two question-form records followed by one electronic correction/result record."
            )

        model_entry = {
            "id": model_id,
            "internal_ordinal": model,
            "source_model_label": f"النموذج {model}",
            "official_model_code": "NOT VERIFIED",
            "official_title": "NOT VERIFIED",
            "academic_year_hijri": "1447",
            "academic_year_gregorian": "2025-2026",
            "term": "NOT VERIFIED",
            "exam_type": "وزاري",
            "page_count": 3,
            "source_sequence_positions": source_positions,
            "stored_page_numbers": [p.get("page_number") for p in block],
            "question_record_ids": [p.get("id") for p in question_records],
            "question_stored_page_numbers": [p.get("page_number") for p in question_records],
            "correction_sheet_candidate_record_id": correction_record.get("id"),
            "correction_sheet_candidate_stored_page_number": correction_record.get("page_number"),
            "ordered_legacy_page_ids": [p.get("id") for p in block],
            "raw_paths": [r.get("raw_path") for r in image_records],
            "sha256": [r.get("sha256") for r in image_records],
            "associated_legacy_questions": associated,
            "boundary_status": "verified",
            "answer_key": {
                "status": "NOT VERIFIED",
                "reason": "The correction/result sheet is visibly associated with the model, but available evidence does not establish it as a standalone official Answer Key."
            },
            "boundary_evidence": evidence,
            "review_status": "boundary_verified_answer_key_unverified",
        }
        if anomaly_note:
            model_entry["source_anomaly"] = anomaly_note
        models.append(model_entry)

        for source_pos, page in zip(source_positions, block):
            questions = page.get("ai_questions") or []
            for idx, question in enumerate(questions, 1):
                mappings.append({
                    "source_sequence_position": source_pos,
                    "stored_page_number": page.get("page_number"),
                    "legacy_page_id": page.get("id"),
                    "question_ordinal_on_page": idx,
                    "source_reference": question.get("source_reference") if isinstance(question, dict) else None,
                    "mapping_status": "exam_linked_structural",
                    "individual_exam_model_id": model_id,
                })

    if len(mappings) != 262:
        raise SystemExit("question mapping record count mismatch")

    output = {
        "schema_version": 1,
        "source_group_id": SOURCE_ID,
        "source_group_name": subject["subject"]["name"],
        "class_id": subject["class"]["id"],
        "class_name": subject["class"]["name"],
        "subject": "العلوم",
        "classification": "exam_source_group",
        "academic_year_hijri": "1447",
        "academic_year_gregorian": "2025-2026",
        "source_pages": 42,
        "source_questions": 262,
        "source_blocks_reviewed": 14,
        "verified_source_occurrence_count": 14,
        "review_required_block_count": 0,
        "individual_exam_model_count": 14,
        "finalized_exam_page_count": 42,
        "review_required_page_count": 0,
        "correction_sheet_candidate_count": 14,
        "verified_answer_key_count": 0,
        "duplicate_sha256_groups_within_source": 0,
        "source_numbering_anomalies": {
            "missing_page_numbers": [35],
            "duplicate_page_numbers": [36],
            "classification": "preserved_source_metadata_anomaly",
            "raw_or_metadata_rewrite_performed": False,
        },
        "models": models,
        "question_mapping": {
            "exam_linked_structural": 262,
            "review_required": 0,
            "unassigned_within_source": 0,
            "semantic_correctness": "NOT VERIFIED",
            "records": mappings,
        },
        "evidence": {
            "technical_report": f"content-staging/reconstruction/technical/{SOURCE_ID}.json",
            "discovery_report": f"content-staging/reconstruction/exams/source-groups/{SOURCE_ID}-discovery.json",
            "anomaly_evidence": f"content-staging/reconstruction/exams/source-groups/{SOURCE_ID}-anomaly-evidence.json",
            "visual_review": "all 42 image records reviewed in contact sheets 001-012, 013-024, 025-036, 037-042",
            "discovery_workflow_runs": [34814241092, 34814423651],
            "storage_identity_used_as_final_boundary": False,
            "raw_mutations": 0,
        },
        "status": "boundary_verified_questions_structurally_mapped_source_numbering_anomaly_preserved_answer_keys_not_verified"
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "source_group_id": SOURCE_ID,
        "models": 14,
        "exam_pages": 42,
        "questions_exam_linked": 262,
        "correction_candidates": 14,
        "verified_answer_keys": 0,
        "numbering_anomaly_preserved": {"missing": [35], "duplicate": [36]},
        "raw_mutations": 0,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
