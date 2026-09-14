#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_ID = "3d91d812-ab78-476a-b2fc-dc2c31152e1a"
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
        if checks.get(key) != 60:
            raise SystemExit(f"expected 60 for {key}")
    if checks.get("failures") != 0 or tech.get("raw_mutations") != 0:
        raise SystemExit("technical failures or RAW mutation detected")
    seq = tech.get("page_sequence", {})
    if seq.get("first_page_number") != 1 or seq.get("last_page_number") != 60 or seq.get("missing_page_numbers") or seq.get("duplicate_page_numbers"):
        raise SystemExit("unexpected page sequence")
    if tech.get("duplicate_sha256_groups_within_subject"):
        raise SystemExit("unexpected within-source duplicate SHA groups")
    counts = manifest.get("counts", {})
    if counts.get("pages") != 60 or counts.get("images_downloaded") != 60 or counts.get("questions") != 0 or counts.get("image_download_failures") != 0:
        raise SystemExit("unexpected manifest baseline")
    if discovery.get("page_sequence", {}).get("count") != 60 or not discovery.get("page_sequence", {}).get("contiguous"):
        raise SystemExit("discovery sequence mismatch")
    if not isinstance(pages, list) or len(pages) != 60:
        raise SystemExit("pages.json is not the expected 60-record list")
    by_page = {int(p["page_number"]): p for p in pages}
    if sorted(by_page) != list(range(1, 61)):
        raise SystemExit("pages.json not exact 1..60")
    if any((p.get("ai_questions") or []) for p in pages):
        raise SystemExit("unexpected legacy questions")
    images = {int(x["page_number"]): x for x in manifest.get("images", [])}
    if sorted(images) != list(range(1, 61)):
        raise SystemExit("manifest images not exact 1..60")

    models = []
    for ordinal in range(1, 21):
        first = (ordinal - 1) * 3 + 1
        nums = [first, first + 1, first + 2]
        records = [images[n] for n in nums]
        models.append({
            "id": f"biology-1445-exam-{ordinal:02d}",
            "internal_ordinal": ordinal,
            "source_model_label": f"source occurrence {ordinal}",
            "official_model_code": "NOT VERIFIED",
            "official_title": "NOT VERIFIED",
            "academic_year_hijri": "1445",
            "academic_year_gregorian": "2023-2024",
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
                "reason": "The third page is visibly a correction/result sheet paired with the preceding two question pages, but available evidence does not establish it as a standalone official Answer Key."
            },
            "boundary_evidence": [
                "All 60 source pages were visually reviewed in complete contact sheets generated from this Biology 1445 source.",
                f"Pages {first} and {first+1} are question sheets and page {first+2} is the paired correction/result sheet; the same source-local semantic sequence was verified independently for all 20 occurrences.",
                "The boundary decision is source-local and was not inherited from another subject or exam group."
            ],
            "review_status": "boundary_verified_answer_key_unverified"
        })

    output = {
        "schema_version": 1,
        "source_group_id": SOURCE_ID,
        "source_group_name": subject["subject"]["name"],
        "class_id": subject["class"]["id"],
        "class_name": subject["class"]["name"],
        "subject": "الأحياء",
        "classification": "exam_source_group",
        "academic_year_hijri": "1445",
        "academic_year_gregorian": "2023-2024",
        "source_pages": 60,
        "source_questions": 0,
        "source_blocks_reviewed": 20,
        "verified_source_occurrence_count": 20,
        "review_required_block_count": 0,
        "individual_exam_model_count": 20,
        "finalized_exam_page_count": 60,
        "review_required_page_count": 0,
        "correction_sheet_candidate_count": 20,
        "verified_answer_key_count": 0,
        "duplicate_sha256_groups_within_source": 0,
        "models": models,
        "question_mapping": {
            "exam_linked_structural": 0,
            "review_required": 0,
            "unassigned_within_source": 0,
            "semantic_correctness": "NOT VERIFIED",
            "records": []
        },
        "evidence": {
            "technical_report": f"content-staging/reconstruction/technical/{SOURCE_ID}.json",
            "discovery_report": f"content-staging/reconstruction/exams/source-groups/{SOURCE_ID}-discovery.json",
            "visual_review": "all 60 pages reviewed in contact sheets 001-012, 013-024, 025-036, 037-048, 049-060",
            "visual_discovery_workflow_run": 34888260549,
            "visual_discovery_artifact_id": 10365571987,
            "reference_identity": "60/60 RAW binaries match the repository reference directory الأحياء ثالث ثانوي/نماذج وزاريه 1445/الاحياء نماذج وزاريه 1445 by page-aligned Git blob identity",
            "storage_identity_used_as_final_boundary": False,
            "raw_mutations": 0
        },
        "status": "boundary_verified_zero_legacy_questions_answer_keys_not_verified"
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"source_group_id": SOURCE_ID, "models": 20, "exam_pages": 60, "questions_exam_linked": 0, "correction_candidates": 20, "verified_answer_keys": 0, "raw_mutations": 0}, ensure_ascii=False))


if __name__ == "__main__":
    main()
