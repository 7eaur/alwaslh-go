#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUBJECT_ID = "f0c5228c-7d5b-4ec2-85ed-ce59139ce0a4"
RECON_PATH = ROOT / "content-staging" / "reconstruction" / "educational" / f"{SUBJECT_ID}.json"
MANIFEST_PATH = ROOT / "content-staging" / "manifests" / "MASTER_CONTENT_MANIFEST.json"

START = "<!-- CHEMISTRY_RECONSTRUCTION_CHECKPOINT_START -->"
END = "<!-- CHEMISTRY_RECONSTRUCTION_CHECKPOINT_END -->"


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


def patch_master_manifest(recon):
    payload = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    source = next((item for item in payload["sources"] if item["id"] == SUBJECT_ID), None)
    if not source:
        raise SystemExit("Chemistry source missing from MASTER_CONTENT_MANIFEST")

    book = recon["reconstructed_book"]
    source["classification"] = "educational_book_source"
    source["classification_evidence"] = "verified RAW/master SHA identity + trusted master TOC + page-title continuity + selective visual boundary review"
    source["review_status"] = "reconstructed_verified"
    source["technical_verification"] = {
        "status": "verified",
        "report_path": f"content-staging/reconstruction/technical/{SUBJECT_ID}.json",
        "images_verified": 178,
        "readable": 178,
        "sha256_match_manifest": 178,
        "mime_match_manifest": 178,
        "duplicate_sha_groups_within_source": 0,
    }
    source["reconstruction"] = {
        "status": "verified",
        "path": f"content-staging/reconstruction/educational/{SUBJECT_ID}.json",
        "book_title": book["title"],
        "retained_page_range": book["legacy_retained_page_range"],
        "retained_pages": 178,
        "units": 9,
        "lessons": 57,
        "lesson_pages": 149,
        "unit_cover_pages": 10,
        "unit_review_pages": 14,
        "appendix_pages": 5,
        "legacy_questions": 2576,
        "structurally_lesson_linked_questions": 2225,
        "review_required_questions": 351,
        "semantic_question_review": "NOT VERIFIED",
        "raw_mutations": 0,
    }
    payload["status"] = "RECONSTRUCTION_IN_PROGRESS_NOT_IMPORT_READY"
    payload["reconstruction_progress"] = {
        "sources_completed": 1,
        "sources_total": 58,
        "educational_sources_completed": 1,
        "educational_sources_total": 26,
        "verified_books": 1,
        "verified_units": 9,
        "verified_lessons": 57,
        "verified_lesson_pages": 149,
        "exam_source_groups_completed": 0,
        "exam_source_groups_total": 32,
        "individual_exam_models": 0,
        "exam_pages_completed": 0,
        "exam_pages_total": 2286,
        "answer_keys": 0,
        "source_images_technically_verified": 178,
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
    }
    MANIFEST_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    recon = json.loads(RECON_PATH.read_text(encoding="utf-8"))
    if recon.get("status") != "reconstructed_verified":
        raise SystemExit("Chemistry reconstruction is not verified")
    patch_master_manifest(recon)

    status = """## Reconstruction checkpoint — Third Secondary Chemistry

- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Sources processed: **1/58**
- Educational sources processed: **1/26**
- Verified Books / Units / Lessons / Lesson pages: **1 / 9 / 57 / 149**
- Exam source groups processed: **0/32**
- Individual Exam Models / Exam pages / Answer Keys: **0 / 0 of 2,286 / 0**
- Source images technically verified: **178/5,273**
- Chemistry source verification: 178 exists, 178 readable, 178 byte-size matches, 178 SHA-256 matches, 178 MIME matches; page range **11..188** contiguous; duplicate SHA groups within this source: **0**.
- WebP derivatives generated / accepted / rejected: **0 / 0 / 0**. The verified Chemistry RAW source is already WebP; derivative optimization has not been executed yet.
- Legacy questions baseline: **25,755**.
- Structurally lesson-linked: **2,225** (page-local mapping only; semantic correctness `NOT VERIFIED`).
- Review-required from Chemistry unit covers/reviews: **351**.
- Exam-linked to an Individual Exam Model: **0**.
- Remaining unclassified: **23,179**.
- Duplicate fingerprint groups classified: **0/99**.
- RAW mutations / unrelated mutations / new imports / new publications: **0 / 0 / 0 / 0**.
- Last completed source: `f0c5228c-7d5b-4ec2-85ed-ce59139ce0a4` — `الكيمياء الكتاب المدرسي`.
- Next source: `e101d097-7a14-44e5-b242-cdeb9a312b77` — `الكيمياء نماذج وزاريه 1445`.
"""
    replace_block(ROOT / "content-staging" / "CONTENT_REBUILD_EXECUTION_STATUS.md", status)

    inventory = """## Verified reconstruction checkpoint — Chemistry textbook

The first non-Grade-9 educational source is now structurally reconstructed and technically verified.

- Legacy source: `f0c5228c-7d5b-4ec2-85ed-ce59139ce0a4` (`الكيمياء الكتاب المدرسي`).
- Trusted reference: `master@f81ebb6ef6198818fa091f7a8c1c81b4de7dbd23`, `الكيمياء ثالث ثانوي/كتاب الكيمياء`.
- Legacy retained slice: numbered pages **11..188**, exactly **178** contiguous pages.
- RAW/master shared SHA-256 equality: **178/178**.
- Master-only numbered pages outside the retained slice: **3..10** and **189..193**.
- Reconstructed structure: **1 Book, 9 Units, 57 Lessons, 149 Lesson pages, 10 Unit-cover pages, 14 Unit-review pages, 5 Glossary pages**.
- The glossary is pages **184..188** and is not modeled as Lessons.
- The 2,576 legacy Chemistry questions remain preserved. **2,225** are structurally attached to verified lesson-page groups; **351** are on unit covers/reviews and remain `review_required`. Semantic correctness remains `NOT VERIFIED`.
- This checkpoint does not change the established corpus baseline of 58 legacy sources, 5,273 source images, 25,755 legacy questions, 32 Exam Source Groups, 2,286 exam-source pages, or 99 duplicate fingerprint groups.
"""
    replace_block(ROOT / "content-staging" / "CONTENT_INVENTORY.md", inventory)

    validation = """## Chemistry reconstruction validation

`f0c5228c-7d5b-4ec2-85ed-ce59139ce0a4` passed the first complete source reconstruction gate:

- Technical image scan: **178/178** exist, readable, byte-size matched, SHA-256 matched, MIME matched; **0 errors**; **0 within-source duplicate SHA groups**.
- Sequence: exact contiguous numbered range **11..188**; no missing or duplicate page numbers.
- Trusted-master cross-check: all **178/178** retained RAW pages are byte-identical by SHA-256 to `master@f81ebb6ef6198818fa091f7a8c1c81b4de7dbd23` for the same numbered pages.
- Boundary evidence: trusted table of contents pages 7..10, exact page-title runs, and selective visual review of unit starts, unit reviews, glossary start/end, and master-only front/back pages.
- Verified structure: **9 Units, 57 Lessons, 149 Lesson pages, 10 Unit-cover pages, 14 Unit-review pages, 5 Glossary pages**.
- No page was equated to a Lesson merely because it existed; multi-page title runs were grouped and Unit/Review/Glossary pages were modeled separately.
- RAW mutations: **0**.

Still `NOT VERIFIED`: semantic correctness of the legacy questions, cross-lesson meaning for unit-review questions, WebP derivative optimization, and all unprocessed sources/exam-model boundaries.
"""
    replace_block(ROOT / "content-staging" / "CONTENT_VALIDATION_REPORT.md", validation)

    import_report = """## Reconstruction checkpoint — no import performed

Chemistry textbook reconstruction is verified, but the corpus is **not import-ready yet**.

- Reconstruction artifact: `content-staging/reconstruction/educational/f0c5228c-7d5b-4ec2-85ed-ce59139ce0a4.json`.
- Technical artifact: `content-staging/reconstruction/technical/f0c5228c-7d5b-4ec2-85ed-ce59139ce0a4.json`.
- New imports: **0**.
- New publications: **0**.
- Production mutations: **0**.
- RAW mutations: **0**.
- PostgreSQL import contract review remains deferred until corpus Reconstruction and Exam Boundary Discovery are complete, per the execution gate.
"""
    replace_block(ROOT / "content-staging" / "CONTENT_IMPORT_REPORT.md", import_report)

    handoff = """## Active reconstruction handoff — Chemistry complete

- Repository: `7eaur/alwaslh-go`
- Branch: `content/corpus-inventory-20260914`
- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- Last completed source: `f0c5228c-7d5b-4ec2-85ed-ce59139ce0a4` — Third Secondary Chemistry textbook.
- Completed source result: **178 technically verified pages; 1 Book; 9 Units; 57 Lessons; 149 Lesson pages; 14 review pages; 5 glossary pages**.
- Evidence: exact RAW/master SHA identity for pages 11..188 plus trusted TOC and selective visual boundary inspection.
- Questions: 2,225 structurally lesson-linked; 351 `review_required`; semantic correctness `NOT VERIFIED`.
- Exam Source Groups completed: **0/32**.
- Current/next source: `e101d097-7a14-44e5-b242-cdeb9a312b77` — `الكيمياء نماذج وزاريه 1445`.
- Exact next operation: technical scan the 60-page exam source group, detect Individual Exam Model boundaries, selectively inspect starts/ends/answer-key candidates, then map pages/questions without treating the 60-page group as one exam.
- Unresolved corpus-wide: remaining 25 educational candidates; all 32 Exam Source Groups; Individual Exam Models; Answer Keys; remaining technical image scan; WebP derivative decisions; 99 duplicate fingerprint groups; remaining question classifications.
- RAW mutations / unrelated mutations / imports / publications remain **0 / 0 / 0 / 0**.
"""
    replace_block(ROOT / "content-staging" / "CONTENT_REBUILD_HANDOFF.md", handoff)

    print(json.dumps({
        "master_manifest_patched": True,
        "markdown_reports_updated": 5,
        "sources_processed": 1,
        "technical_images_verified": 178,
        "next_source": "e101d097-7a14-44e5-b242-cdeb9a312b77",
        "raw_mutations": 0,
    }))


if __name__ == "__main__":
    main()
