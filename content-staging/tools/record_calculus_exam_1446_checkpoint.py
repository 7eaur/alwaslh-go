#!/usr/bin/env python3
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_ID = "012196f1-a633-41cd-927b-d0b1b8845781"
SOURCE_NAME = "التفاضل والتكامل نماذج وزاريه 1446"
RECON_PATH = ROOT / "content-staging/reconstruction/exams/source-groups" / f"{SOURCE_ID}.json"
MASTER_PATH = ROOT / "content-staging/manifests/MASTER_CONTENT_MANIFEST.json"
LOG_PATH = ROOT / "content-staging/CONTENT_RECONSTRUCTION_AUTOMATION_LOG.md"
START = "<!-- CALCULUS_EXAM_1446_CHECKPOINT_START -->"
END = "<!-- CALCULUS_EXAM_1446_CHECKPOINT_END -->"


def replace_block(path, body):
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
    reconstruction = source.get("reconstruction") if isinstance(source.get("reconstruction"), dict) else {}
    exam = source.get("exam_reconstruction") if isinstance(source.get("exam_reconstruction"), dict) else {}
    return (
        status.startswith("processed_")
        or status == "reconstructed_verified"
        or reconstruction.get("status") == "verified"
        or str(exam.get("status") or "").startswith("boundary_verified")
    )


def next_unprocessed_source(master, current_index):
    sources = master.get("sources") or []
    for item in sources[current_index + 1 :] + sources[:current_index]:
        if not is_processed(item):
            return item
    return None


def main():
    recon = json.loads(RECON_PATH.read_text(encoding="utf-8"))
    if (
        recon.get("source_group_id") != SOURCE_ID
        or recon.get("individual_exam_model_count") != 25
        or recon.get("finalized_exam_page_count") != 100
        or recon.get("source_blocks_reviewed") != 25
        or recon.get("correction_sheet_candidate_count") != 25
        or recon.get("verified_answer_key_count") != 0
        or recon.get("duplicate_sha256_groups_within_source") != 6
        or recon.get("review_required_page_count") != 0
    ):
        raise SystemExit("Calculus 1446 reconstruction is not finalized as expected")
    models = recon.get("models") or []
    if len(models) != 25:
        raise SystemExit("expected exactly 25 models")
    if [page for model in models for page in model.get("ordered_page_numbers", [])] != list(range(1, 101)):
        raise SystemExit("model page coverage is not exact ordered 1..100")
    if any(
        model.get("page_count") != 4
        or len(model.get("question_pages") or []) != 3
        or model.get("answer_key", {}).get("status") != "NOT VERIFIED"
        for model in models
    ):
        raise SystemExit("model structure/Answer-Key invariant failed")
    if models[0].get("associated_legacy_questions") != 40 or any(
        model.get("associated_legacy_questions") for model in models[1:]
    ):
        raise SystemExit("model question distribution mismatch")
    qmap = recon.get("question_mapping") or {}
    if (
        int(qmap.get("exam_linked_structural", -1)) != 40
        or int(qmap.get("review_required", -1)) != 0
        or int(qmap.get("unassigned_within_source", -1)) != 0
        or len(qmap.get("records") or []) != 40
        or {record.get("source_page_number") for record in qmap.get("records", [])} != {1, 2, 3}
    ):
        raise SystemExit("Calculus 1446 question accounting mismatch")

    master = json.loads(MASTER_PATH.read_text(encoding="utf-8"))
    sources = master.get("sources") or []
    current_index = next((index for index, source in enumerate(sources) if source.get("id") == SOURCE_ID), None)
    if current_index is None:
        raise SystemExit("Calculus 1446 source missing from MASTER")
    source = sources[current_index]
    progress = master.get("reconstruction_progress") or {}
    already = source.get("review_status") == "processed_boundary_verified_questions_structurally_linked_answer_keys_not_verified"

    if not already:
        expected = {
            "sources_completed": 39,
            "exam_source_groups_completed": 21,
            "individual_exam_models": 390,
            "exam_pages_completed": 1354,
            "correction_sheet_candidates": 396,
            "source_images_technically_verified": 3448,
            "lesson_linked_structural": 13135,
            "exam_linked_to_individual_model": 1920,
            "review_required": 1240,
            "unclassified": 9460,
        }
        actual = {key: progress.get(key) for key in expected}
        if actual != expected:
            raise SystemExit(f"concurrency/drift gate failed: {actual}")
        progress["sources_completed"] += 1
        progress["exam_source_groups_completed"] += 1
        progress["individual_exam_models"] += 25
        progress["exam_pages_completed"] += 100
        progress["correction_sheet_candidates"] += 25
        progress["source_images_technically_verified"] += 100
        progress["exam_linked_to_individual_model"] += 40
        progress["unclassified"] -= 40

    source.update(
        {
            "classification": "exam_source_group",
            "classification_evidence": "legacy exam label + 100/100 immutable RAW technical verification + complete 100-page source-local visual review resolving twenty-five four-page question/question/question/correction occurrences",
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
                "duplicate_disposition": "preserved_as_distinct_source_occurrences_no_merge_no_raw_mutation",
                "page_sequence": "contiguous 1..100",
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
                "exam_linked_questions": 40,
                "review_required_questions": 0,
                "associated_legacy_questions": 40,
                "semantic_question_correctness": "NOT VERIFIED",
                "duplicate_sha_groups_within_source": 6,
                "raw_mutations": 0,
            },
        }
    )

    expected_final = {
        "sources_completed": 40,
        "exam_source_groups_completed": 22,
        "individual_exam_models": 415,
        "exam_pages_completed": 1454,
        "correction_sheet_candidates": 421,
        "source_images_technically_verified": 3548,
        "lesson_linked_structural": 13135,
        "exam_linked_to_individual_model": 1960,
        "review_required": 1240,
        "unclassified": 9420,
    }
    actual_final = {key: progress.get(key) for key in expected_final}
    if actual_final != expected_final:
        raise SystemExit(f"final counter invariant failed: {actual_final}")
    question_total = sum(
        int(progress.get(key) or 0)
        for key in (
            "lesson_linked_structural",
            "exam_linked_to_individual_model",
            "review_required",
            "unclassified",
        )
    )
    if question_total != progress.get("legacy_questions_total") or question_total != 25755:
        raise SystemExit(f"global question invariant failed: {question_total}")
    if any(
        progress.get(key) != 0
        for key in ("raw_mutations", "unrelated_mutations", "new_imports", "new_publications")
    ):
        raise SystemExit("unexpected mutation/import/publication counter")

    master["status"] = "RECONSTRUCTION_IN_PROGRESS_NOT_IMPORT_READY"
    next_source = next_unprocessed_source(master, current_index)
    next_id = next_source.get("id") if next_source else "NONE"
    next_name = ((next_source.get("legacy_source") or {}).get("name") if next_source else None) or "NONE"
    next_counts = next_source.get("counts", {}) if next_source else {}
    MASTER_PATH.write_text(json.dumps(master, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    body = f"""## Reconstruction checkpoint — Calculus Ministry Exams 1446

- Source `{SOURCE_ID}` — `{SOURCE_NAME}` completed from source-local technical and visual evidence.
- Technical verification: **100/100** images match byte-size/SHA-256/MIME; sequence **1..100** contiguous.
- Duplicate evidence: **6** SHA-256 groups, each containing two source occurrences, preserved without merge, deletion, renumbering, or RAW mutation.
- Complete visual review resolves **25** Individual Exam Model occurrences, each with three question pages plus one correction/result-sheet candidate.
- Finalized Exam Pages: **100**; review-required pages: **0**; correction candidates: **25**; verified standalone Answer Keys: **0 / NOT VERIFIED**.
- Source legacy questions: **40/40** structurally linked to the first model by their preserved page membership on pages **1..3**; semantic correctness remains **NOT VERIFIED**.
- Progress: Sources **{progress['sources_completed']}/58**; Educational **{progress['educational_sources_completed']}/26**; Exam Groups **{progress['exam_source_groups_completed']}/32**; Individual Models **{progress['individual_exam_models']}**; Exam Pages **{progress['exam_pages_completed']}/2,286**; technical images **{progress['source_images_technically_verified']}/5,273**.
- Global questions: **{progress['lesson_linked_structural']} + {progress['exam_linked_to_individual_model']} + {progress['review_required']} + {progress['unclassified']} = 25,755**.
- RAW/unrelated/import/publication mutations: **0/0/0/0**. Production PostgreSQL cleanup/import: **NOT EXECUTED**; corpus remains reconstruction-in-progress.
- Next source: `{next_id}` — `{next_name}`.
"""
    for filename in (
        "CONTENT_REBUILD_EXECUTION_STATUS.md",
        "CONTENT_REBUILD_HANDOFF.md",
        "CONTENT_INVENTORY.md",
        "CONTENT_VALIDATION_REPORT.md",
        "CONTENT_IMPORT_REPORT.md",
        "CONTENT_REBUILD_CONTINUATION_2026-09-14.md",
    ):
        path = ROOT / "content-staging" / filename
        if path.exists():
            replace_block(path, body)

    log = LOG_PATH.read_text(encoding="utf-8")
    active_marker = "\n## ACTIVE CHECKPOINT\n"
    history = log.rsplit(active_marker, 1)[0].rstrip() if active_marker in log else log.rstrip()
    start_head = os.environ.get("START_HEAD", "NOT VERIFIED")
    now = datetime.now(timezone(timedelta(hours=3))).isoformat(timespec="seconds")
    run = f"""## RUN {now} — Worker A

- state: COMPLETE_SOURCE_HANDOFF
- start HEAD: `{start_head}`
- end HEAD before handoff-log commit: `WORKTREE_PENDING_COMMIT`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `{SOURCE_ID} — {SOURCE_NAME}`
- completed in this run: verified 100/100 immutable RAW images; directly reviewed all 100 pages; resolved twenty-five source-local four-page exam occurrences; retained each fourth page only as a correction/result candidate; structurally linked all 40 legacy questions from pages 1..3 to the first verified model; preserved six duplicate-SHA groups without merging; updated MASTER/status evidence.
- evidence/artifacts: `content-staging/reconstruction/technical/{SOURCE_ID}.json`; `content-staging/reconstruction/exams/source-groups/{SOURCE_ID}-discovery.json`; `content-staging/reconstruction/exams/source-groups/{SOURCE_ID}.json`.
- ambiguity/review_required: semantic correctness of all 40 legacy questions and standalone official Answer Keys remain `NOT VERIFIED`; no guessed semantic promotion.
- invariant result: PASS (`{progress['lesson_linked_structural']} + {progress['exam_linked_to_individual_model']} + {progress['review_required']} + {progress['unclassified']} = 25,755`).
- Sources processed: {progress['sources_completed']}/{progress['sources_total']}
- Educational: {progress['educational_sources_completed']}/{progress['educational_sources_total']}
- Exam Source Groups: {progress['exam_source_groups_completed']}/{progress['exam_source_groups_total']}
- Individual Exam Models: {progress['individual_exam_models']}
- Exam Pages: {progress['exam_pages_completed']}/{progress['exam_pages_total']}
- Source images technical: {progress['source_images_technically_verified']}/{progress['source_images_total']}
- Legacy Questions: {progress['legacy_questions_total']}
- Lesson-linked: {progress['lesson_linked_structural']}
- Exam-linked: {progress['exam_linked_to_individual_model']}
- Review-required: {progress['review_required']}
- Unclassified: {progress['unclassified']}
- RAW/unrelated/import/publication mutations: 0/0/0/0
- last completed source: `{SOURCE_ID} — {SOURCE_NAME}`
- current source: `{next_id} — {next_name}`
- exact next operation: `Re-fetch live HEAD/baton; verify no active workflow for {next_id}; technically verify its {next_counts.get('pages', 'NOT VERIFIED')} immutable RAW page records; reconstruct only source-local structure; map its {next_counts.get('questions', 'NOT VERIFIED')} legacy questions only where proven; quarantine uncertainty; assert invariants; checkpoint.`
- next source: `Resolve only after {next_id} finalization from live MASTER.`
- blockers: `none for reconstruction continuation; production database cleanup/import remains gated until an import-ready batch and modern schema dry-run are verified.`
"""
    active = f"""## ACTIVE CHECKPOINT

- state: `COMPLETE_SOURCE_HANDOFF`
- branch: `content/corpus-inventory-20260914`
- latest validated source: `{SOURCE_ID} — {SOURCE_NAME}`
- progress: `{progress['sources_completed']}/{progress['sources_total']} sources; {progress['educational_sources_completed']}/{progress['educational_sources_total']} educational; {progress['exam_source_groups_completed']}/{progress['exam_source_groups_total']} exam groups; {progress['individual_exam_models']} individual models; {progress['exam_pages_completed']}/{progress['exam_pages_total']} exam pages; {progress['source_images_technically_verified']}/{progress['source_images_total']} technical images.`
- invariant: `{progress['lesson_linked_structural']} + {progress['exam_linked_to_individual_model']} + {progress['review_required']} + {progress['unclassified']} = 25,755`; RAW/unrelated/import/publication mutations `0/0/0/0`.
- current source: `{next_id} — {next_name}`
- current source baseline: `{next_counts.get('pages', 'NOT VERIFIED')} pages / {next_counts.get('image_references', 'NOT VERIFIED')} images / {next_counts.get('questions', 'NOT VERIFIED')} legacy questions / {next_counts.get('image_download_failures', 'NOT VERIFIED')} download failures; structure NOT VERIFIED.`
- current operation: `Begin source-local technical verification and reconstruction for {next_id}; do not inherit prior-source boundaries.`
- next source: `Resolve only after {next_id} finalization from live MASTER.`
- blockers: `none known for reconstruction; production PostgreSQL mutation remains gated and NOT EXECUTED.`
"""
    LOG_PATH.write_text(history + "\n\n" + run + "\n" + active, encoding="utf-8")

    print(
        json.dumps(
            {
                "already": already,
                "next_source_id": next_id,
                "next_source_name": next_name,
                "progress": progress,
                "question_invariant": question_total,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
