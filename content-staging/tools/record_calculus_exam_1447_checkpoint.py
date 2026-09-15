#!/usr/bin/env python3
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SID = "dcc316bc-b7b8-4a9f-9022-ecc1e7762a9e"
NAME = "التفاضل والتكامل نماذج وزاريه 1447"
RECON = ROOT / "content-staging/reconstruction/exams/source-groups" / f"{SID}.json"
MASTER = ROOT / "content-staging/manifests/MASTER_CONTENT_MANIFEST.json"
LOG = ROOT / "content-staging/CONTENT_RECONSTRUCTION_AUTOMATION_LOG.md"
START, END = "<!-- CALCULUS_EXAM_1447_CHECKPOINT_START -->", "<!-- CALCULUS_EXAM_1447_CHECKPOINT_END -->"


def replace_block(path, body):
    text = path.read_text(encoding="utf-8")
    block = f"{START}\n{body.rstrip()}\n{END}"
    if START in text and END in text:
        before, after = text.split(START, 1)[0].rstrip(), text.split(END, 1)[1].lstrip()
        text = before + "\n\n" + block + ("\n\n" + after if after else "\n")
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    path.write_text(text, encoding="utf-8")


def processed(source):
    status = str(source.get("review_status") or "")
    return status.startswith("processed_") or status == "reconstructed_verified" or (source.get("reconstruction") or {}).get("status") == "verified"


def main():
    recon = json.loads(RECON.read_text(encoding="utf-8"))
    assert (recon["individual_exam_model_count"], recon["finalized_exam_page_count"], recon["correction_sheet_candidate_count"], recon["verified_answer_key_count"], recon["duplicate_sha256_groups_within_source"]) == (31, 124, 31, 0, 9)
    models, qmap = recon["models"], recon["question_mapping"]
    assert len(models) == 31 and [page for model in models for page in model["ordered_page_numbers"]] == list(range(1, 125))
    assert [model["associated_legacy_questions"] for model in models[:10]] == [80, 54] + [40] * 8
    assert not any(model["associated_legacy_questions"] for model in models[10:])
    assert (qmap["exam_linked_structural"], qmap["review_required"], qmap["unassigned_within_source"], len(qmap["records"])) == (454, 0, 0, 454)

    master = json.loads(MASTER.read_text(encoding="utf-8"))
    sources, p = master["sources"], master["reconstruction_progress"]
    index = next(i for i, source in enumerate(sources) if source["id"] == SID)
    source = sources[index]
    already = source.get("review_status") == "processed_boundary_verified_questions_structurally_linked_answer_keys_not_verified"
    if not already:
        expected = {"sources_completed": 40, "exam_source_groups_completed": 22, "individual_exam_models": 415, "exam_pages_completed": 1454, "correction_sheet_candidates": 421, "source_images_technically_verified": 3548, "lesson_linked_structural": 13135, "exam_linked_to_individual_model": 1960, "review_required": 1240, "unclassified": 9420}
        actual = {key: p.get(key) for key in expected}
        if actual != expected:
            raise SystemExit(f"concurrency/drift gate failed: {actual}")
        for key, amount in {"sources_completed": 1, "exam_source_groups_completed": 1, "individual_exam_models": 31, "exam_pages_completed": 124, "correction_sheet_candidates": 31, "source_images_technically_verified": 124, "exam_linked_to_individual_model": 454, "unclassified": -454}.items():
            p[key] += amount

    source.update({
        "classification": "exam_source_group",
        "classification_evidence": "legacy exam label + 124/124 immutable RAW technical verification + complete 124-page source-local visual review resolving thirty-one four-page question/question/question/correction occurrences",
        "review_status": "processed_boundary_verified_questions_structurally_linked_answer_keys_not_verified",
        "exam_models": 31,
        "answer_keys": "NOT VERIFIED",
        "technical_verification": {"status": "verified", "report_path": f"content-staging/reconstruction/technical/{SID}.json", "images_verified": 124, "readable": 124, "sha256_match_manifest": 124, "mime_match_manifest": 124, "duplicate_sha_groups_within_source": 9, "duplicate_disposition": "preserved_as_distinct_source_occurrences_no_merge_no_raw_mutation", "page_sequence": "contiguous 1..124"},
        "exam_reconstruction": {"status": recon["status"], "path": f"content-staging/reconstruction/exams/source-groups/{SID}.json", "source_blocks_reviewed": 31, "verified_source_occurrences": 31, "review_required_blocks": 0, "individual_exam_models": 31, "source_pages": 124, "finalized_exam_pages": 124, "review_required_pages": 0, "pages_per_source_block": 4, "question_pages_per_verified_occurrence": 3, "correction_sheet_candidates": 31, "verified_answer_keys": 0, "answer_key_status": "NOT VERIFIED", "exam_linked_questions": 454, "review_required_questions": 0, "associated_legacy_questions": 454, "semantic_question_correctness": "NOT VERIFIED", "duplicate_sha_groups_within_source": 9, "raw_mutations": 0},
    })
    final = {"sources_completed": 41, "exam_source_groups_completed": 23, "individual_exam_models": 446, "exam_pages_completed": 1578, "correction_sheet_candidates": 452, "source_images_technically_verified": 3672, "lesson_linked_structural": 13135, "exam_linked_to_individual_model": 2414, "review_required": 1240, "unclassified": 8966}
    actual = {key: p.get(key) for key in final}
    if actual != final:
        raise SystemExit(f"final counter invariant failed: {actual}")
    invariant = sum(p[key] for key in ("lesson_linked_structural", "exam_linked_to_individual_model", "review_required", "unclassified"))
    assert invariant == p["legacy_questions_total"] == 25755
    assert all(p[key] == 0 for key in ("raw_mutations", "unrelated_mutations", "new_imports", "new_publications"))
    master["status"] = "RECONSTRUCTION_IN_PROGRESS_NOT_IMPORT_READY"
    next_source = next(item for item in sources[index + 1:] + sources[:index] if not processed(item))
    next_id, next_name, next_counts = next_source["id"], next_source["legacy_source"]["name"], next_source.get("counts", {})
    MASTER.write_text(json.dumps(master, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    body = f"""## Reconstruction checkpoint — Calculus Ministry Exams 1447

- Source `{SID}` — `{NAME}` completed from source-local evidence: **124/124** technical images, contiguous **1..124**, and complete visual review.
- Resolved **31** Individual Exam Models / **124** Exam Pages; each occurrence has three question pages plus one correction/result candidate.
- Duplicate SHA groups: **9**, preserved as distinct source occurrences without merge or RAW mutation.
- Legacy questions: **454/454** structurally linked by preserved page membership to the first ten models; semantic correctness **NOT VERIFIED**.
- Correction candidates **31**; verified standalone Answer Keys **0 / NOT VERIFIED**.
- Progress: Sources **{p['sources_completed']}/58**; Educational **{p['educational_sources_completed']}/26**; Exam Groups **{p['exam_source_groups_completed']}/32**; Models **{p['individual_exam_models']}**; Exam Pages **{p['exam_pages_completed']}/2,286**; technical images **{p['source_images_technically_verified']}/5,273**.
- Questions: **{p['lesson_linked_structural']} + {p['exam_linked_to_individual_model']} + {p['review_required']} + {p['unclassified']} = 25,755**. RAW/unrelated/import/publication mutations **0/0/0/0**.
- Production PostgreSQL cleanup/import: **NOT EXECUTED**; reconstruction remains corpus-wide in progress.
- Next source: `{next_id}` — `{next_name}`.
"""
    for filename in ("CONTENT_REBUILD_EXECUTION_STATUS.md", "CONTENT_REBUILD_HANDOFF.md", "CONTENT_INVENTORY.md", "CONTENT_VALIDATION_REPORT.md", "CONTENT_IMPORT_REPORT.md", "CONTENT_REBUILD_CONTINUATION_2026-09-14.md"):
        path = ROOT / "content-staging" / filename
        if path.exists():
            replace_block(path, body)

    log = LOG.read_text(encoding="utf-8")
    marker = "\n## ACTIVE CHECKPOINT\n"
    history = log.rsplit(marker, 1)[0].rstrip() if marker in log else log.rstrip()
    now = datetime.now(timezone(timedelta(hours=3))).isoformat(timespec="seconds")
    run = f"""## RUN {now} — Worker A

- state: COMPLETE_SOURCE_HANDOFF
- start HEAD: `{os.environ.get('START_HEAD', 'NOT VERIFIED')}`
- end HEAD before handoff-log commit: `WORKTREE_PENDING_COMMIT`
- source at start: `{SID} — {NAME}`
- completed: verified 124/124 RAW images; reviewed all 124 pages; resolved 31 four-page exam occurrences; structurally linked 454 questions from the first ten occurrences; preserved nine duplicate-SHA groups; updated MASTER/status.
- ambiguity: semantic correctness and standalone official Answer Keys remain `NOT VERIFIED`; no guessed promotion.
- invariant: PASS (`{p['lesson_linked_structural']} + {p['exam_linked_to_individual_model']} + {p['review_required']} + {p['unclassified']} = 25,755`).
- progress: Sources {p['sources_completed']}/58; Exam Groups {p['exam_source_groups_completed']}/32; Models {p['individual_exam_models']}; Exam Pages {p['exam_pages_completed']}/2286; technical images {p['source_images_technically_verified']}/5273.
- current source: `{next_id} — {next_name}`
- exact next operation: `Re-fetch live HEAD; technically verify its {next_counts.get('pages', 'NOT VERIFIED')} RAW pages; reconstruct only from source-local evidence; map {next_counts.get('questions', 'NOT VERIFIED')} questions only where proven; checkpoint.`
- production PostgreSQL: `NOT EXECUTED; gated until import-ready batch/schema dry-run.`
"""
    active = f"""## ACTIVE CHECKPOINT

- state: `COMPLETE_SOURCE_HANDOFF`
- branch: `content/corpus-inventory-20260914`
- latest validated source: `{SID} — {NAME}`
- progress: `{p['sources_completed']}/58 sources; {p['educational_sources_completed']}/26 educational; {p['exam_source_groups_completed']}/32 exam groups; {p['individual_exam_models']} models; {p['exam_pages_completed']}/2286 exam pages; {p['source_images_technically_verified']}/5273 technical images.`
- invariant: `{p['lesson_linked_structural']} + {p['exam_linked_to_individual_model']} + {p['review_required']} + {p['unclassified']} = 25,755`; mutations/import/publication `0/0/0/0`.
- current source: `{next_id} — {next_name}`
- baseline: `{next_counts.get('pages', 'NOT VERIFIED')} pages / {next_counts.get('image_references', 'NOT VERIFIED')} images / {next_counts.get('questions', 'NOT VERIFIED')} questions / {next_counts.get('image_download_failures', 'NOT VERIFIED')} failures; structure NOT VERIFIED.`
- current operation: `Begin source-local technical verification and reconstruction; do not inherit prior boundaries.`
- blockers: `none known for reconstruction; production PostgreSQL mutation remains gated and NOT EXECUTED.`
"""
    LOG.write_text(history + "\n\n" + run + "\n" + active, encoding="utf-8")
    print(json.dumps({"already": already, "next_source_id": next_id, "next_source_name": next_name, "progress": p, "question_invariant": invariant}, ensure_ascii=False))


if __name__ == "__main__":
    main()
