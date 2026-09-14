#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_ID = "f25891fe-ea52-481b-baf2-ff4764c79bde"
SUBJECT_DIR = ROOT / "content-staging/raw/legacy-supabase/subjects" / SOURCE_ID
TECH_PATH = ROOT / "content-staging/reconstruction/technical" / f"{SOURCE_ID}.json"
DISCOVERY_PATH = ROOT / "content-staging/reconstruction/exams/source-groups" / f"{SOURCE_ID}-discovery.json"
OUT_PATH = ROOT / "content-staging/reconstruction/exams/source-groups" / f"{SOURCE_ID}.json"

# These 31 three-page blocks were visually reviewed in the complete 93-page
# contact-sheet evidence produced by run 34840720032. Each block is two
# ministry-question pages followed by one electronic correction/result sheet.
# This is source-local evidence; it is not inherited from another subject.
VERIFIED_BLOCKS = [[n, n + 1, n + 2] for n in range(1, 94, 3)]


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

    if manifest.get("counts", {}).get("pages") != 93 or manifest.get("counts", {}).get("questions") != 0:
        raise SystemExit("unexpected Islamic 1447 manifest baseline")
    if not tech.get("all_images_technically_verified"):
        raise SystemExit("technical verification not green")
    checks = tech.get("checks", {})
    for key in ("existing_files", "readable_images", "sha256_matches", "byte_size_matches", "mime_matches"):
        if checks.get(key) != 93:
            raise SystemExit(f"expected 93 for {key}")
    seq = tech.get("page_sequence", {})
    if seq.get("first_page_number") != 1 or seq.get("last_page_number") != 93 or seq.get("missing_page_numbers") or seq.get("duplicate_page_numbers"):
        raise SystemExit("unexpected technical page sequence")
    if discovery.get("page_sequence", {}).get("count") != 93 or not discovery.get("page_sequence", {}).get("contiguous"):
        raise SystemExit("discovery page sequence mismatch")
    if discovery.get("individual_exam_models") != "NOT VERIFIED" or discovery.get("answer_keys") != "NOT VERIFIED":
        raise SystemExit("discovery must remain pre-finalization")

    duplicate_groups = tech.get("duplicate_sha256_groups_within_subject") or []
    if len(duplicate_groups) != 6:
        raise SystemExit(f"expected six exact-SHA duplicate groups from technical evidence, got {len(duplicate_groups)}")

    images = {int(x["page_number"]): x for x in manifest.get("images", [])}
    if sorted(images) != list(range(1, 94)):
        raise SystemExit("manifest images not exact 1..93")
    pages = load_pages()
    by_page = {int(p["page_number"]): p for p in pages if isinstance(p.get("page_number"), int)}
    if sorted(by_page) != list(range(1, 94)):
        raise SystemExit("pages.json not exact 1..93")
    if any((p.get("ai_questions") or []) for p in by_page.values()):
        raise SystemExit("unexpected legacy questions in Islamic 1447 source")
    if any(p.get("content_type") != "exam_model" for p in by_page.values()):
        raise SystemExit("unexpected non-exam_model page metadata")

    # Preserve duplicate evidence exactly. Duplicated question-page images are
    # not silently merged: they occur in different visually verified source
    # blocks with distinct following correction/result sheets.
    duplicate_page_pairs = []
    for group in duplicate_groups:
        nums = []
        for raw_path in group.get("raw_paths") or []:
            name = Path(raw_path).name
            try:
                nums.append(int(name.split("-")[1]))
            except Exception as exc:
                raise SystemExit(f"cannot parse duplicate page number from {name}: {exc}")
        duplicate_page_pairs.append(sorted(nums))
    duplicate_page_pairs.sort()

    models = []
    for ordinal, nums in enumerate(VERIFIED_BLOCKS, 1):
        first, second, correction = nums
        records = [images[n] for n in nums]
        models.append({
            "id": f"islamic-1447-exam-{ordinal:02d}",
            "internal_ordinal": ordinal,
            "source_model_label": f"source block {ordinal}",
            "official_model_code": "NOT VERIFIED",
            "official_title": "NOT VERIFIED",
            "academic_year_hijri": "1447",
            "academic_year_gregorian": "2025-2026",
            "term": "NOT VERIFIED",
            "exam_type": "وزاري",
            "first_page": first,
            "last_page": correction,
            "page_count": 3,
            "question_pages": [first, second],
            "correction_sheet_candidate_page": correction,
            "ordered_page_numbers": nums,
            "ordered_legacy_page_ids": [r.get("legacy_page_id") for r in records],
            "raw_paths": [r.get("raw_path") for r in records],
            "sha256": [r.get("sha256") for r in records],
            "associated_legacy_questions": 0,
            "boundary_status": "verified",
            "answer_key": {
                "status": "NOT VERIFIED",
                "reason": "The third page is visibly an electronic correction/result sheet belonging to the immediately preceding two ministry-question pages, but the evidence does not establish a standalone official Answer Key artifact."
            },
            "boundary_evidence": [
                "All 93 source pages were visually reviewed in complete contact sheets.",
                f"Pages {first}-{second} are visibly ministry-question pages and page {correction} is the following electronic correction/result sheet.",
                "The source-local repeating three-page boundary pattern is complete across 31 blocks and was verified for Islamic 1447 itself.",
                "Exact-SHA duplicate question pages, where present, are preserved as source occurrences rather than silently merged."
            ],
            "review_status": "boundary_verified_answer_key_unverified"
        })

    output = {
        "schema_version": 1,
        "source_group_id": SOURCE_ID,
        "source_group_name": subject["subject"]["name"],
        "class_id": subject["class"]["id"],
        "class_name": subject["class"]["name"],
        "subject": "الإسلامية",
        "classification": "exam_source_group",
        "academic_year_hijri": "1447",
        "academic_year_gregorian": "2025-2026",
        "source_pages": 93,
        "source_questions": 0,
        "source_blocks_reviewed": 31,
        "verified_source_occurrence_count": 31,
        "review_required_block_count": 0,
        "individual_exam_model_count": 31,
        "finalized_exam_page_count": 93,
        "review_required_page_count": 0,
        "correction_sheet_candidate_count": 31,
        "verified_answer_key_count": 0,
        "duplicate_sha256_groups_within_source": 6,
        "duplicate_page_pairs_preserved": duplicate_page_pairs,
        "duplicate_interpretation": "repeated source-page content preserved within separate visually verified three-page exam occurrences; no deduplication or RAW mutation",
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
            "visual_review": "all 93 pages reviewed in contact sheets 001-012, 013-024, 025-036, 037-048, 049-060, 061-072, 073-084, 085-093",
            "discovery_workflow_run": 34840720032,
            "storage_identity_used_as_final_boundary": False,
            "official_model_codes": "NOT VERIFIED",
            "raw_mutations": 0
        },
        "status": "boundary_verified_no_legacy_questions_duplicates_preserved_answer_keys_not_verified"
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "source_group_id": SOURCE_ID,
        "source_occurrences": 31,
        "individual_exam_models": 31,
        "exam_pages": 93,
        "questions_exam_linked": 0,
        "correction_candidates": 31,
        "verified_answer_keys": 0,
        "duplicate_sha_groups_preserved": 6,
        "raw_mutations": 0
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
