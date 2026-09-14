#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_ID = "62d827b3-8ab6-4c2b-8ff2-de6156947276"
RECON_PATH = ROOT / "content-staging/reconstruction/exams/source-groups" / f"{SOURCE_ID}.json"
MASTER_PATH = ROOT / "content-staging/manifests/MASTER_CONTENT_MANIFEST.json"
START = "<!-- BIOLOGY_EXAM_1446_CHECKPOINT_START -->"
END = "<!-- BIOLOGY_EXAM_1446_CHECKPOINT_END -->"


def replace_block(path: Path, body: str):
    text = path.read_text(encoding="utf-8")
    block = f"{START}\n{body.rstrip()}\n{END}"
    if START in text and END in text:
        before = text.split(START, 1)[0].rstrip()
        after = text.split(END, 1)[1].lstrip()
        text = before + "\n\n" + block + ("\n\n" + after if after else "\n")
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    path.write_text(text, encoding="utf-8")


def is_processed(source):
    status = str(source.get("review_status") or "")
    return status.startswith("processed_") or status == "reconstructed_verified"


def next_unprocessed_source(master, current_index):
    sources = master.get("sources") or []
    for item in sources[current_index + 1:] + sources[:current_index]:
        if not is_processed(item):
            return item
    return None


def main():
    recon = json.loads(RECON_PATH.read_text(encoding="utf-8"))
    if recon.get("individual_exam_model_count") != 25 or recon.get("finalized_exam_page_count") != 100:
        raise SystemExit("Biology 1446 model/page count not finalized")
    qmap = recon.get("question_mapping") or {}
    if int(qmap.get("exam_linked_structural", -1)) != 200 or int(qmap.get("review_required", -1)) != 0 or int(qmap.get("unassigned_within_source", -1)) != 0:
        raise SystemExit("Biology 1446 question accounting mismatch")

    master = json.loads(MASTER_PATH.read_text(encoding="utf-8"))
    sources = master.get("sources") or []
    current_index = next((i for i, s in enumerate(sources) if s.get("id") == SOURCE_ID), None)
    if current_index is None:
        raise SystemExit("Biology 1446 source missing from master")
    source = sources[current_index]
    old_processed = is_processed(source)
    old_exam = source.get("exam_reconstruction") if isinstance(source.get("exam_reconstruction"), dict) else {}
    old_tech = source.get("technical_verification") if isinstance(source.get("technical_verification"), dict) else {}
    old_models = int(old_exam.get("individual_exam_models") or 0)
    old_pages = int(old_exam.get("finalized_exam_pages") or old_exam.get("exam_pages") or 0)
    old_corrections = int(old_exam.get("correction_sheet_candidates") or 0)
    old_linked = int(old_exam.get("exam_linked_questions") or 0)
    old_review = int(old_exam.get("review_required_questions") or 0)
    old_images = int(old_tech.get("images_verified") or 0)

    source.update({
        "classification": "exam_source_group",
        "classification_evidence": "legacy exam label + 100/100 technical verification + complete 100-page visual review resolving twenty-five source-local four-page question/question/question/correction occurrences",
        "review_status": "processed_boundary_verified_questions_structurally_linked_answer_keys_not_verified",
        "exam_models": 25,
        "answer_keys": "NOT VERIFIED",
        "technical_verification": {
            "status": "verified",
            "report_path": f"content-staging/reconstruction/technical/{SOURCE_ID}.json",
            "images_verified": 100,
            "readable": 100,
            "sha256_match_manifest": 100,
            "mime_match_manifest": 100,
            "duplicate_sha_groups_within_source": 6,
            "duplicate_disposition": "preserved_as_distinct_source_occurrences_no_merge_no_raw_mutation"
        },
        "exam_reconstruction": {
            "status": recon["status"],
            "path": f"content-staging/reconstruction/exams/source-groups/{SOURCE_ID}.json",
            "source_blocks_reviewed": 25,
            "verified_source_occurrences": 25,
            "review_required_blocks": 0,
            "individual_exam_models": 25,
            "source_pages": 100,
            "finalized_exam_pages": 100,
            "review_required_pages": 0,
            "pages_per_source_block": 4,
            "question_pages_per_verified_occurrence": 3,
            "correction_sheet_candidates": 25,
            "verified_answer_keys": 0,
            "answer_key_status": "NOT VERIFIED",
            "exam_linked_questions": 200,
            "review_required_questions": 0,
            "associated_legacy_questions": 200,
            "semantic_question_correctness": "NOT VERIFIED",
            "duplicate_sha_groups_within_source": 6,
            "raw_mutations": 0
        }
    })

    progress = master.setdefault("reconstruction_progress", {})
    progress["sources_completed"] = int(progress.get("sources_completed") or 0) + (0 if old_processed else 1)
    progress["exam_source_groups_completed"] = int(progress.get("exam_source_groups_completed") or 0) + (0 if old_processed else 1)
    progress["individual_exam_models"] = int(progress.get("individual_exam_models") or 0) + (25 - old_models)
    progress["exam_pages_completed"] = int(progress.get("exam_pages_completed") or 0) + (100 - old_pages)
    progress["correction_sheet_candidates"] = int(progress.get("correction_sheet_candidates") or 0) + (25 - old_corrections)
    progress["source_images_technically_verified"] = int(progress.get("source_images_technically_verified") or 0) + (100 - old_images)
    progress["exam_linked_to_individual_model"] = int(progress.get("exam_linked_to_individual_model") or 0) + (200 - old_linked)
    progress["review_required"] = int(progress.get("review_required") or 0) + (0 - old_review)
    progress["unclassified"] = int(progress.get("unclassified") or 0) - ((200 - old_linked) + (0 - old_review))
    for key, value in {
        "sources_total": 58, "educational_sources_total": 26, "exam_source_groups_total": 32,
        "exam_pages_total": 2286, "source_images_total": 5273, "legacy_questions_total": 25755,
        "duplicate_fingerprint_groups_total": 99, "raw_mutations": 0, "unrelated_mutations": 0,
        "new_imports": 0, "new_publications": 0
    }.items():
        progress[key] = value
    invariant = sum(int(progress.get(k) or 0) for k in ("lesson_linked_structural", "exam_linked_to_individual_model", "review_required", "unclassified"))
    if invariant != 25755:
        raise SystemExit(f"global question invariant failed: {invariant}")

    master["status"] = "RECONSTRUCTION_IN_PROGRESS_NOT_IMPORT_READY"
    next_source = next_unprocessed_source(master, current_index)
    next_id = next_source.get("id") if next_source else "NONE"
    next_name = (next_source.get("legacy_source") or {}).get("name") if next_source else "NONE"
    MASTER_PATH.write_text(json.dumps(master, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    p = progress
    body = f"""## Reconstruction checkpoint — Biology Ministry Exams 1446

- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Source `{SOURCE_ID}` — `الاحياء نماذج وزارية 1446` completed from source-local evidence.
- Technical verification: **100/100** images exist, readable, byte-size/SHA-256/MIME match; sequence **1..100** contiguous.
- Duplicate evidence: **6** SHA-256 duplicate groups (each two source occurrences) preserved exactly; no merge, renumber, deletion, or RAW mutation.
- Full visual review resolves **25** verified Individual Exam Model occurrences; each is three question pages + one correction/result sheet candidate.
- Finalized Exam Pages: **100**; review-required pages: **0**; correction-sheet candidates: **25**; verified standalone Answer Keys: **0 / NOT VERIFIED**.
- Source legacy questions: **200/200** structurally linked by verified page membership; semantic correctness remains **NOT VERIFIED**.
- Progress: Sources **{p['sources_completed']}/58**; Educational **{p.get('educational_sources_completed', 0)}/26**; Exam Groups **{p['exam_source_groups_completed']}/32**; Individual Exam Models **{p['individual_exam_models']}**; Exam Pages **{p['exam_pages_completed']}/2,286**; source images technical **{p['source_images_technically_verified']}/5,273**.
- Global questions: Lesson-linked **{p.get('lesson_linked_structural', 0)}**; Exam-linked **{p.get('exam_linked_to_individual_model', 0)}**; Review-required **{p.get('review_required', 0)}**; Unclassified **{p.get('unclassified', 0)}**; invariant **PASS = 25,755**.
- RAW/unrelated/import/publication mutations: **0/0/0/0**.
- Next source: `{next_id}` — `{next_name}`.
"""
    for filename in ("CONTENT_REBUILD_EXECUTION_STATUS.md", "CONTENT_REBUILD_HANDOFF.md", "CONTENT_INVENTORY.md", "CONTENT_VALIDATION_REPORT.md", "CONTENT_IMPORT_REPORT.md", "CONTENT_REBUILD_CONTINUATION_2026-09-14.md"):
        path = ROOT / "content-staging" / filename
        if path.exists():
            replace_block(path, body)

    print(json.dumps({"sources_completed": p["sources_completed"], "exam_source_groups_completed": p["exam_source_groups_completed"], "individual_exam_models": p["individual_exam_models"], "exam_pages_completed": p["exam_pages_completed"], "source_images_technically_verified": p["source_images_technically_verified"], "exam_linked": p.get("exam_linked_to_individual_model", 0), "review_required": p.get("review_required", 0), "unclassified": p.get("unclassified", 0), "next_source_id": next_id, "next_source_name": next_name, "invariant": invariant}, ensure_ascii=False))


if __name__ == "__main__":
    main()
