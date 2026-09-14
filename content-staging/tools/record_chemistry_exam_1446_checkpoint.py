#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_ID = "c09ce569-ea42-4f0b-997f-95b029a7e6ea"
NEXT_SOURCE_ID = "e7c8291c-e904-4e8c-9cd8-2753818cedf3"
RECON = ROOT / "content-staging/reconstruction/exams/source-groups" / f"{SOURCE_ID}.json"
MASTER = ROOT / "content-staging/manifests/MASTER_CONTENT_MANIFEST.json"
START = "<!-- CHEMISTRY_EXAM_1446_CHECKPOINT_START -->"
END = "<!-- CHEMISTRY_EXAM_1446_CHECKPOINT_END -->"


def replace_block(path, body):
    text = path.read_text(encoding="utf-8")
    block = f"{START}\n{body.rstrip()}\n{END}"
    if START in text and END in text:
        text = text.split(START, 1)[0].rstrip() + "\n\n" + block + "\n\n" + text.split(END, 1)[1].lstrip()
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    path.write_text(text, encoding="utf-8")


def main():
    recon = json.loads(RECON.read_text(encoding="utf-8"))
    assert recon["source_occurrence_count"] == 15
    assert recon["individual_exam_model_count"] == 14
    assert recon["exam_page_count"] == 60
    assert recon["verified_answer_key_count"] == 0
    assert recon["duplicate_resolution"]["classification"] == "legitimate_repeated_exam_model_occurrence"

    master = json.loads(MASTER.read_text(encoding="utf-8"))
    src = next(x for x in master["sources"] if x["id"] == SOURCE_ID)
    src.update({
        "classification": "exam_source_group",
        "classification_evidence": "legacy label + 60-page technical verification + full visual review + visible model codes + explicit repeated-P.41 resolution",
        "review_status": "processed_boundary_verified_repeat_classified_answer_keys_not_verified",
        "exam_models": 14,
        "answer_keys": "NOT VERIFIED",
        "technical_verification": {
            "status": "verified",
            "report_path": f"content-staging/reconstruction/technical/{SOURCE_ID}.json",
            "images_verified": 60, "readable": 60, "sha256_match_manifest": 60,
            "mime_match_manifest": 60, "duplicate_sha_groups_within_source": 3
        },
        "exam_reconstruction": {
            "status": recon["status"],
            "path": f"content-staging/reconstruction/exams/source-groups/{SOURCE_ID}.json",
            "source_occurrences": 15,
            "individual_exam_models": 14,
            "exam_pages": 60,
            "canonical_model_pages": 56,
            "pages_per_source_occurrence": 4,
            "question_pages_per_occurrence": 3,
            "correction_sheet_candidates": 15,
            "verified_answer_keys": 0,
            "answer_key_status": "NOT VERIFIED",
            "repeated_model_code": "P.41",
            "repeat_classification": "legitimate_repeated_exam_model_occurrence",
            "exact_sha_duplicate_page_pairs": [[29, 41], [30, 42], [31, 43]],
            "associated_legacy_questions": 0,
            "raw_mutations": 0
        }
    })
    master.setdefault("reconstruction_progress", {}).update({
        "sources_completed": 3, "sources_total": 58,
        "educational_sources_completed": 1, "educational_sources_total": 26,
        "verified_books": 1, "verified_units": 9, "verified_lessons": 57, "verified_lesson_pages": 149,
        "exam_source_groups_completed": 2, "exam_source_groups_total": 32,
        "individual_exam_models": 34, "exam_pages_completed": 120, "exam_pages_total": 2286,
        "verified_answer_keys": 0, "correction_sheet_candidates": 35,
        "source_images_technically_verified": 298, "source_images_total": 5273,
        "webp_derivatives_generated": 0, "webp_derivatives_accepted": 0, "webp_derivatives_rejected": 0,
        "legacy_questions_total": 25755, "lesson_linked_structural": 2225,
        "exam_linked_to_individual_model": 0, "review_required": 351, "unclassified": 23179,
        "duplicate_fingerprint_groups_classified": 0, "duplicate_fingerprint_groups_total": 99,
        "raw_mutations": 0, "unrelated_mutations": 0, "new_imports": 0, "new_publications": 0
    })
    master["status"] = "RECONSTRUCTION_IN_PROGRESS_NOT_IMPORT_READY"
    MASTER.write_text(json.dumps(master, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    status = """## Reconstruction checkpoint — Chemistry Ministry Exams 1446

- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Sources processed: **3/58**; Educational: **1/26**; Exam Source Groups: **2/32**.
- Books / Units / Lessons / Lesson pages: **1 / 9 / 57 / 149**.
- Verified Individual Exam Models: **34** total; finalized Exam Pages: **120/2,286**; Verified Answer Keys: **0**.
- 1446: **15** four-page source occurrences = 3 question pages + 1 candidate-specific electronic correction report; **14 unique models**.
- Visible unique model codes: `P.87, P.45, P.52, P.9, P.3, P.27, P.5, P.41, P.72, P.107, P.25, P.40, P.34, P.89`.
- Pages **29..31 == 41..43** by exact SHA and both are `P.41`; correction pages **32** and **44** are distinct candidate records. Classification: `legitimate_repeated_exam_model_occurrence`; all pages preserved.
- Correction-report candidates total: **35** (20 + 15); standalone official Answer Key status remains `NOT VERIFIED`.
- Source images technically verified: **298/5,273**; WebP generated/accepted/rejected: **0/0/0**.
- Legacy Questions: **25,755**; Lesson-linked **2,225**; Exam-linked **0**; Review-required **351**; Unclassified **23,179**.
- Global duplicate fingerprint groups classified: **0/99**; local 1446 pairs are not counted globally without proven mapping.
- RAW / unrelated / import / publication mutations: **0 / 0 / 0 / 0**.
- Last completed: `c09ce569-ea42-4f0b-997f-95b029a7e6ea`; Next: `e7c8291c-e904-4e8c-9cd8-2753818cedf3` — Chemistry 1447.
"""
    replace_block(ROOT / "content-staging/CONTENT_REBUILD_EXECUTION_STATUS.md", status)

    inventory = """## Verified exam-source reconstruction — Chemistry 1446

- Source Group `c09ce569-ea42-4f0b-997f-95b029a7e6ea`: **60 JPEG pages**, 1..60 contiguous, 60/60 technical checks green.
- Full visual review establishes **15 contiguous four-page source occurrences**; each contains Q1-30, Q31-49, Q50, then candidate-specific `نموذج التصحيح الإلكتروني`.
- **14 unique Individual Exam Models** are verified from visible codes: `P.87, P.45, P.52, P.9, P.3, P.27, P.5, P.41, P.72, P.107, P.25, P.40, P.34, P.89`.
- `P.41` occurs twice: 29..31 and 41..43 are exact-SHA-identical question pages; 32 and 44 are distinct candidate correction reports. Classified `legitimate_repeated_exam_model_occurrence`; all 60 source pages preserved.
- Academic year **1446 / 2024-2025** visually verified; term `NOT VERIFIED`.
- 15 correction reports are linked to their occurrences, but standalone official Answer Key status is `NOT VERIFIED`; verified Answer Keys: **0**.
- Legacy questions: **0**; RAW/import/publication mutations: **0/0/0**.
"""
    replace_block(ROOT / "content-staging/CONTENT_INVENTORY.md", inventory)

    validation = """## Chemistry 1446 exam boundary validation

- **60/60** images passed existence/readability/size/SHA/MIME checks; sequence **1..60** contiguous; failures **0**.
- All 60 pages were visually reviewed via contact sheets 001–012, 013–024, 025–036, 037–048, 049–060.
- 1446 evidence independently establishes **15 × 4-page occurrences** (3 question pages + correction report), not the 1445 three-page pattern.
- Visible model codes resolve to **14 unique models** because `P.41` repeats.
- Explicit duplicate resolution: 29==41, 30==42, 31==43 by SHA; both blocks show `P.41`; correction reports 32/44 differ by candidate record. Classification `legitimate_repeated_exam_model_occurrence`.
- Correction relation is visually verified; standalone official Answer Key status remains `NOT VERIFIED`; verified Answer Keys **0**.
- RAW mutations: **0**.
"""
    replace_block(ROOT / "content-staging/CONTENT_VALIDATION_REPORT.md", validation)

    import_report = """## Chemistry 1446 exam checkpoint — no import performed

- Final artifact: `content-staging/reconstruction/exams/source-groups/c09ce569-ea42-4f0b-997f-95b029a7e6ea.json`.
- Finalized: **60 pages / 15 source occurrences / 14 unique Individual Exam Models / 15 correction reports / 0 verified standalone Answer Keys**.
- Repeated `P.41` occurrence remains preserved with provenance; no automatic deletion or merge.
- New imports / publications / production / RAW mutations: **0 / 0 / 0 / 0**. Import Readiness remains gated on remaining reconstruction.
"""
    replace_block(ROOT / "content-staging/CONTENT_IMPORT_REPORT.md", import_report)

    handoff = """## Active reconstruction handoff — Chemistry Exams 1446 complete

- Repository/branch: `7eaur/alwaslh-go@content/corpus-inventory-20260914`.
- Last completed: `c09ce569-ea42-4f0b-997f-95b029a7e6ea` — Chemistry Ministry Exams 1446.
- Result: **60 technically verified/classified pages; 15 source occurrences; 14 unique Individual Exam Models; 15 correction-report candidates; 0 verified standalone Answer Keys**.
- `P.41` repeats at 29..32 and 41..44; question pages are exact SHA duplicates, correction reports are distinct candidate records. Classification `legitimate_repeated_exam_model_occurrence`; all pages preserved.
- Progress: Sources **3/58**; Educational **1/26**; Exam Groups **2/32**; Individual Exam Models **34**; Exam Pages **120/2,286**; images verified **298/5,273**.
- Next: `e7c8291c-e904-4e8c-9cd8-2753818cedf3` — Chemistry 1447. Verify locally from its own evidence; do not assume prior-year page patterns.
- RAW/unrelated/import/publication mutations: **0/0/0/0**.
"""
    replace_block(ROOT / "content-staging/CONTENT_REBUILD_HANDOFF.md", handoff)

    continuation = """## Superseding exact continuation — Chemistry 1446 finalized

The earlier 1446 IN PROGRESS section is superseded by this evidence-backed checkpoint.

- Chemistry 1446 is **COMPLETE** for current Reconstruction/Boundary scope: **60/60** technical checks green and all **60** pages visually reviewed.
- Final: **15** four-page source occurrences, **14** unique Individual Exam Models, **60** finalized source pages, **15** correction-report candidates, **0** verified standalone Answer Keys.
- Repeated `P.41`: pages 29..31 == 41..43 by exact SHA; pages 32/44 are distinct candidate correction reports. Classification `legitimate_repeated_exam_model_occurrence`; preserve all pages.
- Progress: Sources **3/58**; Educational **1/26**; Books/Units/Lessons/Lesson Pages **1/9/57/149**; Exam Source Groups **2/32**; Individual Exam Models **34**; Exam Pages **120/2,286**; images verified **298/5,273**.
- Questions: **25,755** total; lesson-linked **2,225**; exam-linked **0**; review-required **351**; unclassified **23,179**; duplicate fingerprint groups classified **0/99**.
- RAW/unrelated/import/publication mutations **0/0/0/0**.
- Next source: `e7c8291c-e904-4e8c-9cd8-2753818cedf3` — `الكيمياء نماذج وزاريه 1447`; start technical verification + source-local visual boundary discovery. Do not assume 3 or 4 pages/model.
"""
    replace_block(ROOT / "content-staging/CONTENT_REBUILD_CONTINUATION_2026-09-14.md", continuation)

    print(json.dumps({"sources_processed": 3, "exam_groups_processed": 2, "individual_exam_models": 34,
                      "exam_pages": 120, "verified_answer_keys": 0, "images_verified": 298,
                      "next_source": NEXT_SOURCE_ID, "raw_mutations": 0}, ensure_ascii=False))


if __name__ == "__main__":
    main()
