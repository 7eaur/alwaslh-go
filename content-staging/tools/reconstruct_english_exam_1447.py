#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_ID = "da6fc228-1ada-4627-8306-80d9d3401490"
SUBJECT_DIR = ROOT / "content-staging/raw/legacy-supabase/subjects" / SOURCE_ID
TECH_PATH = ROOT / "content-staging/reconstruction/technical" / f"{SOURCE_ID}.json"
DISCOVERY_PATH = ROOT / "content-staging/reconstruction/exams/source-groups" / f"{SOURCE_ID}-discovery.json"
OUT_PATH = ROOT / "content-staging/reconstruction/exams/source-groups" / f"{SOURCE_ID}.json"

# Explicit source-record ordinals, derived from the 42-record source order and full visual review.
# Model 13 is intentionally absent because only paper 2 + correction are evidenced; paper 1 is NOT VERIFIED.
MODEL_RECORD_ORDINALS = {
    1: [1, 2, 3],
    2: [4, 5, 6],
    3: [7, 8, 9],
    4: [10, 11, 18],
    5: [12, 13, 14],
    6: [15, 16, 17],
    7: [19, 20, 21],
    8: [22, 23, 24],
    9: [25, 26, 27],
    10: [28, 30, 31],
    11: [32, 33, 34],
    12: [35, 36, 37],
    14: [40, 41, 42],
}
REVIEW_REQUIRED_ORDINALS = [29, 38, 39]
EXPECTED_IDS = {
    1: "1f773b62-9738-4238-b154-e98ca0de1153", 2: "98c76afe-d644-4c81-9dd8-1072e98ea554", 3: "ac865826-dc19-4dd7-8236-ac2923dad0d6",
    4: "faadb233-acfa-4df3-a56d-fffff1be8c0d", 5: "098291ff-b09d-4919-b8ab-50af8b61e149", 6: "31289e5c-05c0-4075-8e56-2ffe63dd487b",
    7: "adc5d37e-5bf9-453f-9e99-de83353da44f", 8: "2f1feda5-e6cb-4fc2-8809-35a62a02b1fb", 9: "c044f303-5a16-4515-9ef6-b24827de0545",
    10: "f1a2fdb6-6004-4ce3-9f5b-7da27e6b917c", 11: "f45aa643-9e52-48a3-9ca4-95721ddfc3d1", 12: "e1f1fa7f-e4f9-4ce0-affe-03eef000b718",
    13: "8e40da23-772a-4690-81d3-191933819d99", 14: "b0c4f6c7-7b88-4560-907b-8926ea3d562c", 15: "60d2291d-462b-4d24-a482-0251634ff6da",
    16: "b6a4b570-c27a-45d4-8993-2605f886a05c", 17: "bd66dfc3-8aaf-4d89-8432-2a6b009b0c96", 18: "135082c2-fb9a-4161-a76e-5272f6a30a03",
    19: "4f57f460-237e-4f56-9ae1-dbe8b5f1d266", 20: "c97c6e5d-f44b-4f4c-85e2-d5d2dabc392a", 21: "039d9554-ebdf-41bc-9ce0-4c26f9fdf705",
    22: "716fac6f-fd8c-4363-b0c9-c2341d092110", 23: "337aba63-1982-47c9-9d2c-52b9eb53fd70", 24: "773d4f77-e3bd-410c-a912-b45df5764f97",
    25: "c46915d1-cce3-483c-8124-378bb7763dc7", 26: "6f462e5f-6f32-4af3-8309-ff51314d5076", 27: "4beb2b12-6926-409b-8bbb-c3ccc446f156",
    28: "b8f07b26-f5de-48b0-9e9b-3a08b4578ead", 29: "73dc07ad-1f8f-44bc-849b-42ffd4cdfd53", 30: "5a19aec6-1b1a-488a-aacc-8a702965c1d2",
    31: "e58f2d63-a5b8-40b0-96fa-00a5df504fe6", 32: "963aef3f-bc01-4001-8bde-44520ba113cc", 33: "58c3c3f9-6d55-444d-8a0b-2598aa49d4ea",
    34: "bd04527f-27ed-485f-a36c-886a76a5e1cc", 35: "5166ebe2-090d-4084-863b-599ec27fe37e", 36: "532486e6-d635-4a8e-b76a-eb7a3cb8bcbd",
    37: "9a2d6479-2859-4b30-a16e-4d94a8362b65", 38: "4ea55b2b-2757-488f-b694-fe437a26980d", 39: "f7b58900-2bfc-45f5-a67f-fa3c4cbf3f98",
    40: "0e49553f-d2cf-44d3-b485-5ca262dbb09a", 41: "1f5f5bbd-cc93-444a-af3b-496cc47f7130", 42: "28f1d033-dd6c-403a-b0f0-fd493c16d454",
}


def load_pages():
    payload = json.loads((SUBJECT_DIR / "pages.json").read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    for key in ("pages", "records", "items", "data"):
        value = payload.get(key) if isinstance(payload, dict) else None
        if isinstance(value, list):
            return value
    raise SystemExit("Unsupported pages.json shape")


def main():
    subject = json.loads((SUBJECT_DIR / "subject.json").read_text(encoding="utf-8"))
    manifest = json.loads((SUBJECT_DIR / "manifest.json").read_text(encoding="utf-8"))
    tech = json.loads(TECH_PATH.read_text(encoding="utf-8"))
    discovery = json.loads(DISCOVERY_PATH.read_text(encoding="utf-8"))
    pages = load_pages()

    if len(pages) != 42 or manifest.get("counts", {}).get("pages") != 42 or manifest.get("counts", {}).get("questions") != 234:
        raise SystemExit("unexpected English 1447 manifest/pages baseline")
    if not tech.get("all_images_technically_verified"):
        raise SystemExit("technical verification not green")
    for key in ("existing_files", "readable_images", "sha256_matches", "byte_size_matches", "mime_matches"):
        if tech.get("checks", {}).get(key) != 42:
            raise SystemExit(f"expected 42 for {key}")
    seq = tech.get("page_sequence", {})
    if seq.get("missing_page_numbers") != [12, 26, 37] or seq.get("duplicate_page_numbers") != [18, 27, 29]:
        raise SystemExit(f"unexpected preserved page-number anomaly: {seq}")
    if tech.get("duplicate_sha256_groups_within_subject"):
        raise SystemExit("unexpected within-source duplicate SHA groups")
    if discovery.get("counts", {}).get("pages") != 42:
        raise SystemExit("discovery page count mismatch")

    for ordinal, page in enumerate(pages, 1):
        if page.get("id") != EXPECTED_IDS[ordinal]:
            raise SystemExit(f"source record identity drift at ordinal {ordinal}")

    images = manifest.get("images") or []
    by_legacy_id = {x.get("legacy_page_id"): x for x in images}
    if len(by_legacy_id) != 42:
        raise SystemExit("manifest image identity count mismatch")

    q_total = sum(len(p.get("ai_questions") or []) for p in pages)
    if q_total != 234:
        raise SystemExit(f"source question total drift: {q_total}")

    models = []
    question_records = []
    finalized_ordinals = set()
    for model_no, ordinals in MODEL_RECORD_ORDINALS.items():
        finalized_ordinals.update(ordinals)
        recs = [pages[o - 1] for o in ordinals]
        imgs = [by_legacy_id[r["id"]] for r in recs]
        model_id = f"english-1447-exam-{model_no:02d}"
        q_count = 0
        for ordinal, rec in zip(ordinals[:2], recs[:2]):
            for qi, question in enumerate(rec.get("ai_questions") or [], 1):
                q_count += 1
                question_records.append({
                    "model_id": model_id,
                    "model_number": model_no,
                    "source_record_ordinal": ordinal,
                    "legacy_page_id": rec.get("id"),
                    "stored_page_number": rec.get("page_number"),
                    "question_index_within_page": qi,
                    "source_reference": question.get("source_reference"),
                    "status": "exam_linked_structural",
                    "semantic_correctness": "NOT VERIFIED"
                })
        models.append({
            "id": model_id,
            "internal_ordinal": model_no,
            "source_model_label": f"النموذج {model_no}",
            "official_model_code": "NOT VERIFIED",
            "official_title": "NOT VERIFIED",
            "academic_year_hijri": "1447",
            "academic_year_gregorian": "2025-2026",
            "term": "NOT VERIFIED",
            "exam_type": "وزاري",
            "source_record_ordinals": ordinals,
            "stored_page_numbers": [r.get("page_number") for r in recs],
            "ordered_legacy_page_ids": [r.get("id") for r in recs],
            "question_page_legacy_ids": [recs[0].get("id"), recs[1].get("id")],
            "correction_sheet_candidate_legacy_id": recs[2].get("id"),
            "raw_paths": [i.get("raw_path") for i in imgs],
            "sha256": [i.get("sha256") for i in imgs],
            "associated_legacy_questions": q_count,
            "boundary_status": "verified",
            "answer_key": {
                "status": "NOT VERIFIED",
                "reason": "The third record is visibly an electronic correction/result sheet associated with the model, but available evidence does not establish a standalone official Answer Key artifact."
            },
            "review_status": "boundary_verified_answer_key_unverified"
        })

    if finalized_ordinals & set(REVIEW_REQUIRED_ORDINALS):
        raise SystemExit("review-required ordinal leaked into finalized models")
    if finalized_ordinals | set(REVIEW_REQUIRED_ORDINALS) != set(range(1, 43)):
        raise SystemExit("not all 42 source records are accounted for exactly once")
    if len(question_records) != 234:
        raise SystemExit(f"expected all 234 questions to be structurally exam-linked, got {len(question_records)}")

    review_records = []
    reasons = {
        29: "Distinct second-paper image stored as page 29 and metadata-labeled model 9 paper 2, but model 9 is visually complete at source records 25..27 and model 10 uses the other page-29 paper 2. No evidence-backed first-paper/correction relation exists for this extra record.",
        38: "Visibly a question-paper second page and metadata-labeled model 13 paper 2. Model 13 paper 1 is NOT VERIFIED; numeric page label 37 is absent and the record metadata that claims model 13 paper 1 (ordinal 27) is visibly a correction sheet used in the completed model-9 occurrence.",
        39: "Visibly the model-13 correction/result candidate, but model 13 paper 1 is NOT VERIFIED, so the incomplete model cannot be finalized."
    }
    for ordinal in REVIEW_REQUIRED_ORDINALS:
        rec = pages[ordinal - 1]
        img = by_legacy_id[rec["id"]]
        review_records.append({
            "source_record_ordinal": ordinal,
            "legacy_page_id": rec.get("id"),
            "stored_page_number": rec.get("page_number"),
            "metadata_title": rec.get("title"),
            "raw_path": img.get("raw_path"),
            "sha256": img.get("sha256"),
            "question_count": len(rec.get("ai_questions") or []),
            "status": "review_required",
            "reason": reasons[ordinal]
        })

    output = {
        "schema_version": 1,
        "source_group_id": SOURCE_ID,
        "source_group_name": subject["subject"]["name"],
        "class_id": subject["class"]["id"],
        "class_name": subject["class"]["name"],
        "subject": "الإنجليزي",
        "classification": "exam_source_group",
        "academic_year_hijri": "1447",
        "academic_year_gregorian": "2025-2026",
        "source_pages": 42,
        "source_questions": 234,
        "source_records_visually_reviewed": 42,
        "nominal_model_labels_reviewed": 14,
        "verified_source_occurrence_count": 13,
        "review_required_block_count": 2,
        "individual_exam_model_count": 13,
        "finalized_exam_page_count": 39,
        "review_required_page_count": 3,
        "correction_sheet_candidate_count": 14,
        "model_matched_correction_sheet_candidate_count": 13,
        "verified_answer_key_count": 0,
        "duplicate_sha256_groups_within_source": 0,
        "preserved_page_number_anomaly": {
            "missing_numeric_labels": [12, 26, 37],
            "duplicate_numeric_labels": [18, 27, 29],
            "normalization_performed": False
        },
        "models": models,
        "review_required_records": review_records,
        "question_mapping": {
            "exam_linked_structural": 234,
            "review_required": 0,
            "unassigned_within_source": 0,
            "semantic_correctness": "NOT VERIFIED",
            "records": question_records
        },
        "anomaly_resolution": [
            {
                "source_record_ordinals": [10, 11, 18],
                "resolution": "verified_model_4_noncontiguous_occurrence",
                "evidence": "Records 10 and 11 are visibly model-4 question papers; record 18 is a distinct correction/result sheet metadata-labeled model-4 correction. The intervening model-5/6 records are preserved in source order."
            },
            {
                "source_record_ordinals": [25, 26, 27],
                "resolution": "verified_model_9_with_corrupted_metadata_titles",
                "evidence": "Full visual review shows question paper 1, question paper 2, correction/result in source order. Metadata titles for records 26/27 are inconsistent with the visible artifacts, so the visual/source-identity evidence governs without rewriting RAW metadata."
            },
            {
                "source_record_ordinals": [28, 30, 31],
                "resolution": "verified_model_10_using_second_duplicate_page_29_record",
                "evidence": "Record 28 is model-10 paper 1; record 30 is the matching paper 2 and metadata-labeled model-10 paper 2; record 31 is model-10 correction/result. Record 29 is a distinct extra paper-2 image and remains review_required."
            },
            {
                "source_record_ordinals": [38, 39],
                "resolution": "model_13_incomplete_review_required",
                "evidence": "Record 38 is visibly paper 2 and record 39 correction/result. Paper 1 is NOT VERIFIED; missing numeric label 37 is preserved and no page is fabricated."
            }
        ],
        "evidence": {
            "technical_report": f"content-staging/reconstruction/technical/{SOURCE_ID}.json",
            "discovery_report": f"content-staging/reconstruction/exams/source-groups/{SOURCE_ID}-discovery.json",
            "visual_review": "all 42 source records reviewed in complete contact sheets 001-013, 014-024, 025-035, 036-042",
            "successful_discovery_workflow_run": 34826307823,
            "visual_artifact_id": 10340652157,
            "visual_artifact_sha256": "358985b359cc04f8ae14693ddbd0a880b33d132c13a8a26f0eb249139fbe72cd",
            "storage_identity_used_as_final_boundary": False,
            "raw_mutations": 0
        },
        "status": "boundary_verified_with_three_review_required_pages_answer_keys_not_verified"
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "source_group_id": SOURCE_ID,
        "models": 13,
        "finalized_exam_pages": 39,
        "review_required_pages": 3,
        "questions_exam_linked": 234,
        "correction_candidates": 14,
        "verified_answer_keys": 0,
        "raw_mutations": 0
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
