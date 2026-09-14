#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_ID = "e7c8291c-e904-4e8c-9cd8-2753818cedf3"
RECON_PATH = ROOT / "content-staging/reconstruction/exams/source-groups" / f"{SOURCE_ID}.json"
MASTER_PATH = ROOT / "content-staging/manifests/MASTER_CONTENT_MANIFEST.json"
START = "<!-- CHEMISTRY_EXAM_1447_CHECKPOINT_START -->"
END = "<!-- CHEMISTRY_EXAM_1447_CHECKPOINT_END -->"


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
    if recon.get("individual_exam_model_count") != 28:
        raise SystemExit("1447 unique model count is not finalized")
    if recon.get("finalized_exam_page_count") != 116 or recon.get("review_required_page_count") != 8:
        raise SystemExit("1447 finalized/review page counts are not finalized")
    if recon.get("review_required_block_count") != 2 or recon.get("verified_source_occurrence_count") != 29:
        raise SystemExit("1447 occurrence boundary counts are not finalized")
    qmap = recon.get("question_mapping") or {}
    linked = int(qmap.get("exam_linked_structural", -1))
    review_q = int(qmap.get("review_required", -1))
    if linked < 0 or review_q < 0 or linked + review_q != 226:
        raise SystemExit("1447 question mapping is not complete")

    master = json.loads(MASTER_PATH.read_text(encoding="utf-8"))
    sources = master.get("sources") or []
    current_index = next((i for i, s in enumerate(sources) if s.get("id") == SOURCE_ID), None)
    if current_index is None:
        raise SystemExit("1447 source missing from master manifest")
    source = sources[current_index]
    old_processed = is_processed(source)
    old_exam = source.get("exam_reconstruction") if isinstance(source.get("exam_reconstruction"), dict) else {}
    old_tech = source.get("technical_verification") if isinstance(source.get("technical_verification"), dict) else {}

    old_models = int(old_exam.get("individual_exam_models") or 0)
    old_pages = int(old_exam.get("finalized_exam_pages") or old_exam.get("exam_pages") or 0)
    old_corrections = int(old_exam.get("correction_sheet_candidates") or 0)
    old_linked = int(old_exam.get("exam_linked_questions") or 0)
    old_review_q = int(old_exam.get("review_required_questions") or 0)
    old_images = int(old_tech.get("images_verified") or 0)

    source.update({
        "classification": "exam_source_group",
        "classification_evidence": "legacy label + 124-page full technical scan + full 124-page visual review + visible question/correction model-code matching + explicit mismatch isolation",
        "review_status": "processed_boundary_verified_with_review_required_mismatches_answer_keys_not_verified",
        "exam_models": 28,
        "answer_keys": "NOT VERIFIED",
        "technical_verification": {
            "status": "verified",
            "report_path": f"content-staging/reconstruction/technical/{SOURCE_ID}.json",
            "images_verified": 124,
            "readable": 124,
            "sha256_match_manifest": 124,
            "mime_match_manifest": 124,
            "duplicate_sha_groups_within_source": 9,
        },
        "exam_reconstruction": {
            "status": recon["status"],
            "path": f"content-staging/reconstruction/exams/source-groups/{SOURCE_ID}.json",
            "source_blocks_reviewed": 31,
            "verified_source_occurrences": 29,
            "review_required_blocks": 2,
            "individual_exam_models": 28,
            "source_pages": 124,
            "finalized_exam_pages": 116,
            "review_required_pages": 8,
            "pages_per_source_block": 4,
            "question_pages_per_verified_occurrence": 3,
            "correction_sheet_candidates": 31,
            "model_matched_correction_reports": 29,
            "verified_answer_keys": 0,
            "answer_key_status": "NOT VERIFIED",
            "exam_linked_questions": linked,
            "review_required_questions": review_q,
            "associated_legacy_questions": 226,
            "semantic_question_correctness": "NOT VERIFIED",
            "raw_mutations": 0,
        }
    })

    progress = master.setdefault("reconstruction_progress", {})
    progress["sources_completed"] = int(progress.get("sources_completed") or 0) + (0 if old_processed else 1)
    progress["exam_source_groups_completed"] = int(progress.get("exam_source_groups_completed") or 0) + (0 if old_processed else 1)
    progress["individual_exam_models"] = int(progress.get("individual_exam_models") or 0) + (28 - old_models)
    progress["exam_pages_completed"] = int(progress.get("exam_pages_completed") or 0) + (116 - old_pages)
    progress["correction_sheet_candidates"] = int(progress.get("correction_sheet_candidates") or 0) + (31 - old_corrections)
    progress["source_images_technically_verified"] = int(progress.get("source_images_technically_verified") or 0) + (124 - old_images)
    progress["exam_linked_to_individual_model"] = int(progress.get("exam_linked_to_individual_model") or 0) + (linked - old_linked)
    progress["review_required"] = int(progress.get("review_required") or 0) + (review_q - old_review_q)
    newly_classified_questions = (linked + review_q) - (old_linked + old_review_q)
    progress["unclassified"] = int(progress.get("unclassified") or 0) - newly_classified_questions
    for key, value in {
        "sources_total": 58,
        "educational_sources_total": 26,
        "exam_source_groups_total": 32,
        "exam_pages_total": 2286,
        "source_images_total": 5273,
        "legacy_questions_total": 25755,
        "duplicate_fingerprint_groups_total": 99,
        "verified_answer_keys": 0,
        "raw_mutations": 0,
        "unrelated_mutations": 0,
        "new_imports": 0,
        "new_publications": 0,
    }.items():
        progress[key] = value

    invariant = (
        int(progress.get("lesson_linked_structural") or 0)
        + int(progress.get("exam_linked_to_individual_model") or 0)
        + int(progress.get("review_required") or 0)
        + int(progress.get("unclassified") or 0)
    )
    if invariant != 25755:
        raise SystemExit(f"Global question-classification invariant failed: {invariant}")
    if progress["unclassified"] < 0:
        raise SystemExit("Global unclassified count became negative")

    master["status"] = "RECONSTRUCTION_IN_PROGRESS_NOT_IMPORT_READY"
    next_source = next_unprocessed_source(master, current_index)
    next_id = next_source.get("id") if next_source else "NONE"
    next_name = (next_source.get("legacy_source") or {}).get("name") if next_source else "NONE"
    MASTER_PATH.write_text(json.dumps(master, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    p = progress
    status = f"""## Reconstruction checkpoint — Chemistry Ministry Exams 1447

- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Sources processed: **{p['sources_completed']}/58**; Educational: **{p.get('educational_sources_completed', 0)}/26**; Exam Source Groups: **{p['exam_source_groups_completed']}/32**.
- Books / Units / Lessons / Lesson pages: **{p.get('verified_books', 0)} / {p.get('verified_units', 0)} / {p.get('verified_lessons', 0)} / {p.get('verified_lesson_pages', 0)}**.
- Verified Individual Exam Models: **{p['individual_exam_models']}**; finalized Exam Pages: **{p['exam_pages_completed']}/2,286**; Verified Answer Keys: **0**.
- Chemistry 1447: **124/124** technical checks green; all **124** pages visually reviewed; **31** four-page source blocks; **29** verified model-matched occurrences; **28** unique models; **116** finalized model pages; **8** pages isolated as `review_required`.
- Mismatch blocks: pages **37..40** (`P.61` questions / `P.31` correction) and **45..48** (`P.28` questions / `P.88` correction). No missing question pages were fabricated.
- `P.8` at **49..52** and **57..60** is a legitimate repeated model occurrence; exact duplicate question pages are preserved with distinct candidate correction reports.
- Correction/electronic-answer sheet candidates total: **{p['correction_sheet_candidates']}**; official standalone Answer Keys remain `NOT VERIFIED`.
- Source images technically verified: **{p['source_images_technically_verified']}/5,273**; WebP generated/accepted/rejected: **{p.get('webp_derivatives_generated', 0)}/{p.get('webp_derivatives_accepted', 0)}/{p.get('webp_derivatives_rejected', 0)}**.
- Legacy Questions: **25,755**; Lesson-linked **{p.get('lesson_linked_structural', 0)}**; Exam-linked **{p['exam_linked_to_individual_model']}**; Review-required **{p['review_required']}**; Unclassified **{p['unclassified']}**.
- 1447 question mapping: **{linked}** structurally exam-linked + **{review_q}** review-required = **226/226** accounted for; semantic correctness `NOT VERIFIED`.
- Global duplicate fingerprint groups classified: **{p.get('duplicate_fingerprint_groups_classified', 0)}/99**; local 1447 exact-SHA groups are recorded separately and do not alter the global fingerprint baseline without proven mapping.
- RAW / unrelated / import / publication mutations: **0 / 0 / 0 / 0**.
- Last completed: `{SOURCE_ID}` — `الكيمياء نماذج وزاريه 1447`.
- Next source: `{next_id}` — `{next_name}`.
"""
    replace_block(ROOT / "content-staging/CONTENT_REBUILD_EXECUTION_STATUS.md", status)

    inventory = f"""## Verified exam-source reconstruction — Chemistry 1447

- Source Group `{SOURCE_ID}`: **124 JPEG pages**, sequence **1..124**, **124/124** technical checks green, **9** within-source duplicate SHA groups, RAW mutations **0**.
- Full visual review: **31** four-page blocks. **29** have matching visible question/correction model codes and resolve to **28 unique Individual Exam Models**; `P.8` legitimately occurs twice.
- Finalized model pages: **116**. Review-required pages: **8** in two isolated mismatches: `37..40` = `P.61` questions / `P.31` correction; `45..48` = `P.28` questions / `P.88` correction.
- Exact duplicate question blocks: `1..3 == 45..47` (`P.28`), `37..39 == 65..67` (`P.61`), `49..51 == 57..59` (`P.8`). Only the `P.8` repeat is fully model-matched in both occurrences; the other duplicate occurrences remain isolated for review.
- Academic year **1447 / 2025-2026** visually verified; term `NOT VERIFIED`.
- Correction report candidates: **31**; model-matched correction relations: **29**; verified standalone Answer Keys: **0**.
- Legacy questions: **226** = **{linked}** structurally linked to verified models + **{review_q}** review-required; semantic correctness `NOT VERIFIED`.
- No RAW deletion/merge, import, publication, or production mutation occurred.
"""
    replace_block(ROOT / "content-staging/CONTENT_INVENTORY.md", inventory)

    validation = f"""## Chemistry 1447 exam boundary validation

- **124/124** images passed existence/readability/byte-size/SHA/MIME verification; sequence **1..124** contiguous; failures **0**.
- Every page was visually inspected through eleven contact sheets, including final sheet 121–124.
- Source-local structure: **31** four-page blocks; **29** model-code-matched occurrences; **28** unique verified Individual Exam Models; **116** finalized pages.
- Two mismatched blocks are deliberately not finalized: `37..40` (`P.61` / `P.31`) and `45..48` (`P.28` / `P.88`). They remain `review_required`; no synthetic pages or inferred model relations were created.
- Nine exact-SHA duplicate page pairs reduce to three repeated three-page question blocks. `P.8` is classified `legitimate_repeated_exam_model_occurrence`; the `P.28` and `P.61` mismatched duplicate blocks remain `review_required` / duplicate-source-import candidates rather than being auto-deleted.
- **226/226** legacy questions are structurally accounted for: **{linked}** exam-linked and **{review_q}** review-required. Semantic correctness remains `NOT VERIFIED`.
- Standalone official Answer Keys: **0 / NOT VERIFIED**. RAW mutations: **0**.
"""
    replace_block(ROOT / "content-staging/CONTENT_VALIDATION_REPORT.md", validation)

    import_report = f"""## Chemistry 1447 exam checkpoint — no import performed

- Final artifact: `content-staging/reconstruction/exams/source-groups/{SOURCE_ID}.json`.
- Finalized: **28 unique Individual Exam Models / 116 model pages** from **29** verified occurrences; **8** source pages isolated in two `review_required` blocks.
- Questions: **{linked}** structurally exam-linked; **{review_q}** review-required; semantic correctness `NOT VERIFIED`.
- Correction-report candidates: **31**; verified standalone Answer Keys: **0**.
- New imports / publications / production / RAW mutations: **0 / 0 / 0 / 0**. Import Readiness remains gated on remaining reconstruction.
"""
    replace_block(ROOT / "content-staging/CONTENT_IMPORT_REPORT.md", import_report)

    handoff = f"""## Active reconstruction handoff — Chemistry Exams 1447 complete

- Repository/branch: `7eaur/alwaslh-go@content/corpus-inventory-20260914`.
- Last completed: `{SOURCE_ID}` — Chemistry Ministry Exams 1447.
- Result: **124/124** technically verified and visually reviewed pages; **29** verified occurrences; **28** unique models; **116** finalized model pages; **8** pages isolated as review-required; **31** correction-report candidates; **0** verified standalone Answer Keys.
- Review-required blocks: `37..40` (`P.61` questions / `P.31` correction) and `45..48` (`P.28` questions / `P.88` correction). Keep all provenance; do not fabricate or silently repair.
- Questions: **{linked}** exam-linked + **{review_q}** review-required = **226/226** source questions accounted for.
- Progress: Sources **{p['sources_completed']}/58**; Educational **{p.get('educational_sources_completed', 0)}/26**; Exam Groups **{p['exam_source_groups_completed']}/32**; Individual Exam Models **{p['individual_exam_models']}**; Exam Pages **{p['exam_pages_completed']}/2,286**; images verified **{p['source_images_technically_verified']}/5,273**.
- Next: `{next_id}` — `{next_name}`. Start from its own technical/visual evidence; do not reuse chemistry-year boundary assumptions.
- RAW/unrelated/import/publication mutations: **0/0/0/0**.
"""
    replace_block(ROOT / "content-staging/CONTENT_REBUILD_HANDOFF.md", handoff)

    continuation = f"""## Superseding continuation — Chemistry 1447 finalized

- Chemistry 1447 is closed for the current Reconstruction/Boundary scope with isolated review-required anomalies rather than guessed repairs.
- **124/124** technical verification; full visual review of **124** pages; **31** source blocks; **29** verified model-matched occurrences; **28** unique models; **116** finalized exam pages; **8** review-required pages; **31** correction-report candidates; **0** verified standalone Answer Keys.
- Mismatches retained: `37..40` = `P.61` questions / `P.31` correction; `45..48` = `P.28` questions / `P.88` correction. `P.8` repeat is legitimate and preserved.
- Source questions: **226/226** structurally accounted for (**{linked}** exam-linked, **{review_q}** review-required); semantic correctness `NOT VERIFIED`.
- Global progress: Sources **{p['sources_completed']}/58**; Educational **{p.get('educational_sources_completed', 0)}/26**; Books/Units/Lessons/Lesson Pages **{p.get('verified_books', 0)}/{p.get('verified_units', 0)}/{p.get('verified_lessons', 0)}/{p.get('verified_lesson_pages', 0)}**; Exam Groups **{p['exam_source_groups_completed']}/32**; Models **{p['individual_exam_models']}**; Exam Pages **{p['exam_pages_completed']}/2,286**; images **{p['source_images_technically_verified']}/5,273**.
- Legacy Questions **25,755**; Lesson-linked **{p.get('lesson_linked_structural', 0)}**; Exam-linked **{p['exam_linked_to_individual_model']}**; Review-required **{p['review_required']}**; Unclassified **{p['unclassified']}**; duplicate fingerprint groups classified **{p.get('duplicate_fingerprint_groups_classified', 0)}/99**.
- RAW/unrelated/import/publication mutations **0/0/0/0**.
- Next source: `{next_id}` — `{next_name}`. Continue source-local technical verification → visual boundary discovery → reconstruction.
"""
    replace_block(ROOT / "content-staging/CONTENT_REBUILD_CONTINUATION_2026-09-14.md", continuation)

    print(json.dumps({
        "sources_processed": p["sources_completed"],
        "exam_groups_processed": p["exam_source_groups_completed"],
        "individual_exam_models": p["individual_exam_models"],
        "exam_pages_processed": p["exam_pages_completed"],
        "verified_answer_keys": 0,
        "source_images_technically_verified": p["source_images_technically_verified"],
        "exam_linked_questions": p["exam_linked_to_individual_model"],
        "review_required_questions": p["review_required"],
        "unclassified_questions": p["unclassified"],
        "next_source": next_id,
        "next_source_name": next_name,
        "raw_mutations": 0,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
