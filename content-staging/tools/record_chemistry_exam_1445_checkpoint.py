#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_ID = "e101d097-7a14-44e5-b242-cdeb9a312b77"
RECON_PATH = ROOT / "content-staging" / "reconstruction" / "exams" / "source-groups" / f"{SOURCE_ID}.json"
MANIFEST_PATH = ROOT / "content-staging" / "manifests" / "MASTER_CONTENT_MANIFEST.json"
START = "<!-- CHEMISTRY_EXAM_1445_CHECKPOINT_START -->"
END = "<!-- CHEMISTRY_EXAM_1445_CHECKPOINT_END -->"


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


def patch_master(recon):
    payload = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    source = next((item for item in payload["sources"] if item["id"] == SOURCE_ID), None)
    if not source:
        raise SystemExit("Exam 1445 source missing from master manifest")
    source["classification"] = "exam_source_group"
    source["classification_evidence"] = "legacy label + 60-page full technical scan + full-page visual boundary review"
    source["review_status"] = "processed_boundary_verified_answer_keys_not_verified"
    source["technical_verification"] = {
        "status": "verified",
        "report_path": f"content-staging/reconstruction/technical/{SOURCE_ID}.json",
        "images_verified": 60,
        "readable": 60,
        "sha256_match_manifest": 60,
        "mime_match_manifest": 60,
        "duplicate_sha_groups_within_source": 0,
    }
    source["exam_reconstruction"] = {
        "status": recon["status"],
        "path": f"content-staging/reconstruction/exams/source-groups/{SOURCE_ID}.json",
        "individual_exam_models": 20,
        "exam_pages": 60,
        "pages_per_model": 3,
        "question_pages_per_model": 2,
        "correction_sheet_candidates": 20,
        "verified_answer_keys": 0,
        "answer_key_status": "NOT VERIFIED",
        "associated_legacy_questions": 0,
        "raw_mutations": 0,
    }
    source["exam_models"] = 20
    source["answer_keys"] = "NOT VERIFIED"

    progress = payload.setdefault("reconstruction_progress", {})
    progress.update({
        "sources_completed": 2,
        "sources_total": 58,
        "educational_sources_completed": 1,
        "educational_sources_total": 26,
        "verified_books": 1,
        "verified_units": 9,
        "verified_lessons": 57,
        "verified_lesson_pages": 149,
        "exam_source_groups_completed": 1,
        "exam_source_groups_total": 32,
        "individual_exam_models": 20,
        "exam_pages_completed": 60,
        "exam_pages_total": 2286,
        "verified_answer_keys": 0,
        "correction_sheet_candidates": 20,
        "source_images_technically_verified": 238,
        "source_images_total": 5273,
        "webp_derivatives_generated": 0,
        "webp_derivatives_accepted": 0,
        "webp_derivatives_rejected": 0,
        "legacy_questions_total": 25755,
        "lesson_linked_structural": 2225,
        "exam_linked_to_individual_model": 0,
        "review_required": 351,
        "unclassified": 23179,
        "duplicate_fingerprint_groups_classified": 0,
        "duplicate_fingerprint_groups_total": 99,
        "raw_mutations": 0,
        "unrelated_mutations": 0,
        "new_imports": 0,
        "new_publications": 0,
    })
    payload["status"] = "RECONSTRUCTION_IN_PROGRESS_NOT_IMPORT_READY"
    MANIFEST_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    recon = json.loads(RECON_PATH.read_text(encoding="utf-8"))
    if recon.get("individual_exam_model_count") != 20 or recon.get("exam_page_count") != 60:
        raise SystemExit("Exam 1445 reconstruction not complete")
    patch_master(recon)

    status = """## Reconstruction checkpoint — Chemistry Ministry Exams 1445

- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Sources processed: **2/58**
- Educational sources processed: **1/26**
- Verified Books / Units / Lessons / Lesson pages: **1 / 9 / 57 / 149**
- Exam Source Groups processed: **1/32**
- Individual Exam Models: **20**
- Exam pages processed: **60/2,286**
- Verified Answer Keys: **0**
- Correction/electronic-answer sheet candidates: **20**; official Answer Key status remains `NOT VERIFIED`.
- Source images technically verified: **238/5,273** (178 Chemistry textbook + 60 Chemistry exams 1445).
- Chemistry 1445 source technical result: **60/60** exist, readable, byte-size match, SHA-256 match, MIME match; page sequence 1..60 contiguous; within-source duplicate SHA groups **0**.
- WebP derivatives generated / accepted / rejected: **0 / 0 / 0**.
- Legacy questions baseline: **25,755**.
- Structurally lesson-linked: **2,225**; review-required: **351**; exam-linked to Individual Exam Models: **0**; remaining unclassified: **23,179**.
- Duplicate fingerprint groups classified: **0/99**.
- RAW mutations / unrelated mutations / new imports / new publications: **0 / 0 / 0 / 0**.
- Last completed source: `e101d097-7a14-44e5-b242-cdeb9a312b77` — `الكيمياء نماذج وزاريه 1445`.
- Next source: `c09ce569-ea42-4f0b-997f-95b029a7e6ea` — `الكيمياء نماذج وزاريه 1446`.
"""
    replace_block(ROOT / "content-staging" / "CONTENT_REBUILD_EXECUTION_STATUS.md", status)

    inventory = """## Verified exam-source reconstruction — Chemistry 1445

- Exam Source Group: `e101d097-7a14-44e5-b242-cdeb9a312b77` (`الكيمياء نماذج وزاريه 1445`).
- RAW: **60 JPEG pages**, sequence **1..60**, no missing/duplicate page numbers.
- Technical verification: **60/60** exist, readable, byte-size matched, SHA-256 matched, MIME matched; **0** within-source duplicate SHA groups.
- Storage metadata alone exposes one `/lesson/` identity for all 60 pages and was therefore rejected as a final exam boundary signal.
- Full visual review of all 60 pages establishes **20 Individual Exam Models**. Each model is a contiguous 3-page block: **2 question pages + 1 correction/electronic-answer sheet candidate**.
- Verified exam pages: **60**.
- Verified official Answer Keys: **0**. The 20 third pages are associated correction-sheet candidates, but `Answer Key = NOT VERIFIED` until explicit evidence proves official-key status.
- Official model codes/titles and term: `NOT VERIFIED` rather than inferred from source order.
- Associated legacy questions: **0**.
- RAW mutations/imports/publications: **0/0/0**.
"""
    replace_block(ROOT / "content-staging" / "CONTENT_INVENTORY.md", inventory)

    validation = """## Chemistry 1445 exam boundary validation

`e101d097-7a14-44e5-b242-cdeb9a312b77` passed technical and boundary-discovery gates:

- **60/60** images technically verified (exist/readable/size/SHA/MIME), **0 errors**, **0 within-source duplicate SHA groups**.
- Exact contiguous page sequence **1..60**.
- Every page was visually inspected through five complete contact sheets: 001–012, 013–024, 025–036, 037–048, 049–060.
- A consistent repeated structure was verified across the entire source: two exam-question pages followed by a correction/electronic-answer sheet, yielding **20 non-overlapping three-page Individual Exam Models**.
- The single storage `/lesson/` identity is explicitly not used as the model boundary.
- The third page of each model is not promoted to official `Answer Key`; all **20** remain correction-sheet candidates and Answer Key status is `NOT VERIFIED`.
- RAW mutations: **0**.
"""
    replace_block(ROOT / "content-staging" / "CONTENT_VALIDATION_REPORT.md", validation)

    import_report = """## Chemistry 1445 exam checkpoint — no import performed

- Reconstruction artifact: `content-staging/reconstruction/exams/source-groups/e101d097-7a14-44e5-b242-cdeb9a312b77.json`.
- Technical artifact: `content-staging/reconstruction/technical/e101d097-7a14-44e5-b242-cdeb9a312b77.json`.
- Discovered: **20 Individual Exam Models / 60 exam pages / 20 correction-sheet candidates / 0 verified Answer Keys**.
- New imports / publications / production mutations / RAW mutations: **0 / 0 / 0 / 0**.
- Import Readiness is still gated on completion of corpus reconstruction and remaining Exam Source Groups.
"""
    replace_block(ROOT / "content-staging" / "CONTENT_IMPORT_REPORT.md", import_report)

    handoff = """## Active reconstruction handoff — Chemistry Exams 1445 complete

- Repository: `7eaur/alwaslh-go`
- Branch: `content/corpus-inventory-20260914`
- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Last completed source: `e101d097-7a14-44e5-b242-cdeb9a312b77` — Chemistry Ministry Exams 1445.
- Result: **60 technically verified pages; 20 Individual Exam Models; 3 pages/model; 20 correction-sheet candidates; 0 verified Answer Keys**.
- Full source-group visual review completed; model boundaries are verified. Official model codes/titles/term and official Answer Key status remain `NOT VERIFIED` where evidence is insufficient.
- Completed corpus so far: **2/58 sources**, including **1/26 educational sources** and **1/32 Exam Source Groups**.
- Current/next source: `c09ce569-ea42-4f0b-997f-95b029a7e6ea` — `الكيمياء نماذج وزاريه 1446`.
- Exact next operation: technical scan all 60 pages, detect storage/metadata candidates, export full visual contact sheets, resolve Individual Exam Model boundaries and correction/answer-key relations, then checkpoint and continue.
- RAW mutations / unrelated mutations / imports / publications: **0 / 0 / 0 / 0**.
"""
    replace_block(ROOT / "content-staging" / "CONTENT_REBUILD_HANDOFF.md", handoff)

    print(json.dumps({
        "sources_processed": 2,
        "exam_groups_processed": 1,
        "individual_exam_models": 20,
        "exam_pages_processed": 60,
        "verified_answer_keys": 0,
        "correction_sheet_candidates": 20,
        "source_images_technically_verified": 238,
        "next_source": "c09ce569-ea42-4f0b-997f-95b029a7e6ea",
        "raw_mutations": 0,
    }))


if __name__ == "__main__":
    main()
