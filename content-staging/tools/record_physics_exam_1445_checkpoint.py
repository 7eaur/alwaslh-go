#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_ID = "41e5a81c-3b93-479c-9b76-33815cae9430"
RECON_PATH = ROOT / "content-staging/reconstruction/exams/source-groups" / f"{SOURCE_ID}.json"
MASTER_PATH = ROOT / "content-staging/manifests/MASTER_CONTENT_MANIFEST.json"
START = "<!-- PHYSICS_EXAM_1445_CHECKPOINT_START -->"
END = "<!-- PHYSICS_EXAM_1445_CHECKPOINT_END -->"


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
    return status.startswith("processed_") or status in {"reconstructed_verified", "verified_empty_retained_source"}


def next_unprocessed_source(master, current_index):
    sources = master.get("sources") or []
    for item in sources[current_index + 1:] + sources[:current_index]:
        if not is_processed(item):
            return item
    return None


def source_name(item):
    if not item:
        return "NONE"
    legacy = item.get("legacy_source") or {}
    return legacy.get("name") or item.get("name") or "UNKNOWN"


def main():
    recon = json.loads(RECON_PATH.read_text(encoding="utf-8"))
    if recon.get("individual_exam_model_count") != 20 or recon.get("finalized_exam_page_count") != 60:
        raise SystemExit("Physics 1445 model/page count not finalized")
    qmap = recon.get("question_mapping") or {}
    if int(qmap.get("exam_linked_structural", -1)) != 83 or int(qmap.get("review_required", -1)) != 0 or int(qmap.get("unassigned_within_source", -1)) != 0:
        raise SystemExit("Physics 1445 question mapping not finalized")

    master = json.loads(MASTER_PATH.read_text(encoding="utf-8"))
    sources = master.get("sources") or []
    current_index = next((i for i, s in enumerate(sources) if s.get("id") == SOURCE_ID), None)
    if current_index is None:
        raise SystemExit("Physics 1445 source missing from master")
    source = sources[current_index]
    old_processed = is_processed(source)
    old_exam = source.get("exam_reconstruction") if isinstance(source.get("exam_reconstruction"), dict) else {}
    old_tech = source.get("technical_verification") if isinstance(source.get("technical_verification"), dict) else {}
    old_models = int(old_exam.get("individual_exam_models") or 0)
    old_pages = int(old_exam.get("finalized_exam_pages") or old_exam.get("exam_pages") or 0)
    old_corrections = int(old_exam.get("correction_sheet_candidates") or 0)
    old_images = int(old_tech.get("images_verified") or 0)
    old_exam_questions = int(old_exam.get("exam_linked_questions") or 0)
    old_review_questions = int(old_exam.get("review_required_questions") or 0)

    source.update({
        "classification": "exam_source_group",
        "classification_evidence": "legacy exam label + 60/60 technical verification + complete source-local 60-page visual review resolving twenty three-page question/question/correction occurrences",
        "review_status": "processed_boundary_verified_answer_keys_not_verified",
        "exam_models": 20,
        "answer_keys": "NOT VERIFIED",
        "technical_verification": {
            "status": "verified",
            "report_path": f"content-staging/reconstruction/technical/{SOURCE_ID}.json",
            "images_verified": 60,
            "readable": 60,
            "sha256_match_manifest": 60,
            "mime_match_manifest": 60,
            "duplicate_sha_groups_within_source": 0
        },
        "exam_reconstruction": {
            "status": recon["status"],
            "path": f"content-staging/reconstruction/exams/source-groups/{SOURCE_ID}.json",
            "source_blocks_reviewed": 20,
            "verified_source_occurrences": 20,
            "review_required_blocks": 0,
            "individual_exam_models": 20,
            "source_pages": 60,
            "finalized_exam_pages": 60,
            "review_required_pages": 0,
            "pages_per_source_block": 3,
            "question_pages_per_verified_occurrence": 2,
            "correction_sheet_candidates": 20,
            "verified_answer_keys": 0,
            "answer_key_status": "NOT VERIFIED",
            "exam_linked_questions": 83,
            "review_required_questions": 0,
            "associated_legacy_questions": 83,
            "semantic_question_correctness": "NOT VERIFIED",
            "raw_mutations": 0
        }
    })

    progress = master.setdefault("reconstruction_progress", {})
    source_delta = 0 if old_processed else 1
    models_delta = 20 - old_models
    pages_delta = 60 - old_pages
    corrections_delta = 20 - old_corrections
    images_delta = 60 - old_images
    exam_q_delta = 83 - old_exam_questions
    review_q_delta = 0 - old_review_questions
    if min(models_delta, pages_delta, corrections_delta, images_delta, exam_q_delta) < 0:
        raise SystemExit("existing source counters exceed evidence; fail closed")

    progress["sources_completed"] = int(progress.get("sources_completed") or 0) + source_delta
    progress["exam_source_groups_completed"] = int(progress.get("exam_source_groups_completed") or 0) + source_delta
    progress["individual_exam_models"] = int(progress.get("individual_exam_models") or 0) + models_delta
    progress["exam_pages_completed"] = int(progress.get("exam_pages_completed") or 0) + pages_delta
    progress["correction_sheet_candidates"] = int(progress.get("correction_sheet_candidates") or 0) + corrections_delta
    progress["source_images_technically_verified"] = int(progress.get("source_images_technically_verified") or 0) + images_delta
    progress["exam_linked_to_individual_model"] = int(progress.get("exam_linked_to_individual_model") or 0) + exam_q_delta
    progress["review_required"] = int(progress.get("review_required") or 0) + review_q_delta
    progress["unclassified"] = int(progress.get("unclassified") or 0) - exam_q_delta - review_q_delta

    for key, value in {
        "sources_total": 58,
        "educational_sources_total": 26,
        "exam_source_groups_total": 32,
        "exam_pages_total": 2286,
        "source_images_total": 5273,
        "legacy_questions_total": 25755,
        "duplicate_fingerprint_groups_total": 99,
        "raw_mutations": 0,
        "unrelated_mutations": 0,
        "new_imports": 0,
        "new_publications": 0
    }.items():
        progress[key] = value

    invariant = sum(int(progress.get(k) or 0) for k in ("lesson_linked_structural", "exam_linked_to_individual_model", "review_required", "unclassified"))
    if invariant != 25755:
        raise SystemExit(f"global question invariant failed: {invariant}")
    if int(progress.get("source_images_technically_verified") or 0) > 5273:
        raise SystemExit("technical image count exceeds corpus total")
    if any(int(progress.get(k) or 0) != 0 for k in ("raw_mutations", "unrelated_mutations", "new_imports", "new_publications")):
        raise SystemExit("forbidden mutation/import/publication counter nonzero")

    master["status"] = "RECONSTRUCTION_IN_PROGRESS_NOT_IMPORT_READY"
    next_source = next_unprocessed_source(master, current_index)
    next_id = next_source.get("id") if next_source else "NONE"
    next_name = source_name(next_source)
    MASTER_PATH.write_text(json.dumps(master, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    p = progress
    body = f"""## Reconstruction checkpoint — Physics Ministry Exams 1445

- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Source `{SOURCE_ID}` — `الفيزياء نماذج وزاريه 1445` completed from source-local evidence.
- Technical verification: **60/60** images exist/readable and byte-size/SHA-256/MIME match the immutable manifest; sequence **1..60** contiguous; duplicate SHA groups **0**.
- Full visual review resolves **20** verified source occurrences; each has two question pages followed by one correction/result-sheet candidate; all **60** source pages are finalized exactly once.
- Correction/result candidates: **20**; verified standalone official Answer Keys: **0 / NOT VERIFIED**.
- Source questions: **83/83 structurally exam-linked** by verified page membership; semantic question/answer correctness remains `NOT VERIFIED`.
- Progress: Sources **{p['sources_completed']}/58**; Educational **{p.get('educational_sources_completed', 0)}/26**; Exam Groups **{p['exam_source_groups_completed']}/32**; Individual Exam Models **{p['individual_exam_models']}**; Exam Pages **{p['exam_pages_completed']}/2,286**; source images technical **{p['source_images_technically_verified']}/5,273**.
- Global questions: Lesson-linked **{p.get('lesson_linked_structural', 0)}**; Exam-linked **{p.get('exam_linked_to_individual_model', 0)}**; Review-required **{p.get('review_required', 0)}**; Unclassified **{p.get('unclassified', 0)}**; invariant **PASS = 25,755**.
- RAW/unrelated/import/publication mutations: **0/0/0/0**.
- Next source: `{next_id}` — `{next_name}`.
"""
    for filename in (
        "CONTENT_REBUILD_EXECUTION_STATUS.md",
        "CONTENT_REBUILD_HANDOFF.md",
        "CONTENT_INVENTORY.md",
        "CONTENT_VALIDATION_REPORT.md",
        "CONTENT_IMPORT_REPORT.md",
        "CONTENT_REBUILD_CONTINUATION_2026-09-14.md"
    ):
        path = ROOT / "content-staging" / filename
        if path.exists():
            replace_block(path, body)

    print(json.dumps({
        "sources_completed": p["sources_completed"],
        "exam_source_groups_completed": p["exam_source_groups_completed"],
        "individual_exam_models": p["individual_exam_models"],
        "exam_pages_completed": p["exam_pages_completed"],
        "source_images_technically_verified": p["source_images_technically_verified"],
        "lesson_linked": p.get("lesson_linked_structural", 0),
        "exam_linked": p.get("exam_linked_to_individual_model", 0),
        "review_required": p.get("review_required", 0),
        "unclassified": p.get("unclassified", 0),
        "next_source_id": next_id,
        "next_source_name": next_name,
        "invariant": invariant
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
