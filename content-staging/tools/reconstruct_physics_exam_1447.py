#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_ID = "bbc5c2e7-9b96-4502-a8b0-6a14d2f8782a"
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
    for key in ("manifest_image_count", "existing_files", "readable_images", "sha256_matches", "byte_size_matches", "mime_matches"):
        if checks.get(key) != 124:
            raise SystemExit(f"expected 124 for {key}, got {checks.get(key)}")
    if checks.get("failures") != 0 or tech.get("raw_mutations") != 0:
        raise SystemExit("technical failures or RAW mutation")
    seq = tech.get("page_sequence", {})
    if seq.get("first_page_number") != 1 or seq.get("last_page_number") != 124 or seq.get("missing_page_numbers") or seq.get("duplicate_page_numbers"):
        raise SystemExit("unexpected page sequence")
    duplicate_groups = tech.get("duplicate_sha256_groups_within_subject") or []
    if len(duplicate_groups) != 9:
        raise SystemExit(f"expected 9 duplicate SHA groups, got {len(duplicate_groups)}")
    counts = manifest.get("counts", {})
    if (counts.get("pages"), counts.get("images_downloaded"), counts.get("questions"), counts.get("image_download_failures")) != (124, 124, 255, 0):
        raise SystemExit("unexpected manifest baseline")
    dseq = discovery.get("page_sequence", {})
    if dseq.get("count") != 124 or not dseq.get("contiguous"):
        raise SystemExit("discovery sequence mismatch")
    if not isinstance(pages, list) or len(pages) != 124:
        raise SystemExit("unexpected pages.json")
    by_page = {int(p["page_number"]): p for p in pages}
    images = {int(x["page_number"]): x for x in manifest.get("images", [])}
    if sorted(by_page) != list(range(1, 125)) or sorted(images) != list(range(1, 125)):
        raise SystemExit("pages/images not exact 1..124")

    models = []
    question_records = []
    total_questions = 0
    for ordinal in range(1, 32):
        first = (ordinal - 1) * 4 + 1
        nums = [first, first + 1, first + 2, first + 3]
        records = [images[n] for n in nums]
        model_id = f"physics-1447-exam-{ordinal:02d}"
        associated = 0
        for n in nums:
            page = by_page[n]
            legacy_page_id = page.get("id") or images[n].get("legacy_page_id")
            for qidx, _ in enumerate(page.get("ai_questions") or [], start=1):
                associated += 1
                total_questions += 1
                question_records.append({
                    "source_page_number": n,
                    "legacy_page_id": legacy_page_id,
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
            "question_pages": [first, first + 1, first + 2],
            "correction_sheet_candidate_page": first + 3,
            "ordered_page_numbers": nums,
            "ordered_legacy_page_ids": [r.get("legacy_page_id") for r in records],
            "raw_paths": [r.get("raw_path") for r in records],
            "sha256": [r.get("sha256") for r in records],
            "associated_legacy_questions": associated,
            "boundary_status": "verified",
            "answer_key": {
                "status": "NOT VERIFIED",
                "reason": "The fourth page is visibly a correction/result sheet paired with the preceding three question pages, but available evidence does not establish it as a standalone official Answer Key.",
            },
            "boundary_evidence": [
                "All 124 Physics 1447 source pages were visually reviewed in complete source-local contact sheets.",
                f"Pages {first}-{first+2} are question sheets and page {first+3} is the paired correction/result sheet; the four-page semantic sequence was independently verified for all 31 occurrences.",
                "Nine within-source SHA duplicate groups form three repeated question-sheet triplets; their paired fourth-page correction/result occurrences remain separately preserved, so no occurrence was collapsed solely from partial-page duplication.",
                "The boundary decision is source-local and was not inherited from Physics 1445, Physics 1446, or any other exam source group.",
            ],
            "review_status": "boundary_verified_answer_key_unverified",
        })
    if total_questions != 255 or len(question_records) != 255:
        raise SystemExit(f"expected 255 mapped legacy questions, got {total_questions}")

    output = {
        "schema_version": 1,
        "source_group_id": SOURCE_ID,
        "source_group_name": subject["subject"]["name"],
        "class_id": subject["class"]["id"],
        "class_name": subject["class"]["name"],
        "subject": "الفيزياء",
        "classification": "exam_source_group",
        "academic_year_hijri": "1447",
        "academic_year_gregorian": "2025-2026",
        "source_pages": 124,
        "source_questions": 255,
        "source_blocks_reviewed": 31,
        "verified_source_occurrence_count": 31,
        "review_required_block_count": 0,
        "individual_exam_model_count": 31,
        "finalized_exam_page_count": 124,
        "review_required_page_count": 0,
        "correction_sheet_candidate_count": 31,
        "verified_answer_key_count": 0,
        "duplicate_sha256_groups_within_source": 9,
        "models": models,
        "question_mapping": {
            "exam_linked_structural": 255,
            "review_required": 0,
            "unassigned_within_source": 0,
            "semantic_correctness": "NOT VERIFIED",
            "records": question_records,
        },
        "evidence": {
            "technical_report": f"content-staging/reconstruction/technical/{SOURCE_ID}.json",
            "discovery_report": f"content-staging/reconstruction/exams/source-groups/{SOURCE_ID}-discovery.json",
            "visual_review": "all 124 pages reviewed in contact sheets 001-012 through 121-124",
            "visual_discovery_workflow_run": 34909617398,
            "visual_discovery_artifact_id": 10374510074,
            "storage_identity_used_as_final_boundary": False,
            "raw_mutations": 0,
        },
        "status": "boundary_verified_legacy_questions_structurally_linked_answer_keys_not_verified",
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "source_group_id": SOURCE_ID,
        "models": 31,
        "exam_pages": 124,
        "questions_exam_linked": 255,
        "correction_candidates": 31,
        "verified_answer_keys": 0,
        "duplicate_sha_groups": 9,
        "raw_mutations": 0,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
