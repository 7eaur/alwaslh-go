#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SID = "0a76f44b-0a4f-4e36-9ea9-badecf78bf23"
NEXT = "7f02b242-5164-46d1-a82d-7f1023cfa8c9"
RECON = ROOT / "content-staging/reconstruction/educational" / f"{SID}.json"
MASTER = ROOT / "content-staging/manifests/MASTER_CONTENT_MANIFEST.json"
START = "<!-- HISTORY_SOURCE_LOCAL_CHECKPOINT_START -->"
END = "<!-- HISTORY_SOURCE_LOCAL_CHECKPOINT_END -->"


def replace_block(path: Path, body: str) -> None:
    text = path.read_text(encoding="utf-8")
    block = f"{START}\n{body.rstrip()}\n{END}"
    if START in text and END in text:
        before = text.split(START, 1)[0].rstrip()
        after = text.split(END, 1)[1].lstrip()
        text = before + "\n\n" + block + ("\n\n" + after if after else "\n")
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    path.write_text(text, encoding="utf-8")


def main() -> None:
    r = json.loads(RECON.read_text(encoding="utf-8"))
    assert r["status"] == "reconstructed_verified_source_local"
    assert r["reconstructed_book"]["unit_count"] == 0
    assert r["reconstructed_book"]["section_count"] == 1
    assert r["reconstructed_book"]["lesson_count"] == 9
    assert r["reconstructed_book"]["lesson_page_count"] == 47
    assert r["reconstructed_book"]["lesson_review_page_count"] == 12
    assert r["reconstructed_book"]["classified_page_count"] == 61
    assert r["questions"]["legacy_questions"] == 138
    assert r["questions"]["structurally_lesson_linked_questions"] == 138
    assert r["questions"]["review_required_questions"] == 0

    p = json.loads(MASTER.read_text(encoding="utf-8"))
    progress = p["reconstruction_progress"]
    expected = {
        "sources_completed": 12,
        "educational_sources_completed": 3,
        "verified_books": 3,
        "verified_units": 25,
        "verified_lessons": 110,
        "verified_lesson_pages": 413,
        "exam_source_groups_completed": 9,
        "individual_exam_models": 135,
        "exam_pages_completed": 455,
        "source_images_technically_verified": 1011,
        "lesson_linked_structural": 2236,
        "exam_linked_to_individual_model": 967,
        "review_required": 351,
        "unclassified": 22201,
        "raw_mutations": 0,
        "unrelated_mutations": 0,
        "new_imports": 0,
        "new_publications": 0,
    }
    for key, value in expected.items():
        if progress.get(key) != value:
            raise SystemExit(f"baseline drift for {key}: expected {value}, got {progress.get(key)}")

    s = next(x for x in p["sources"] if x["id"] == SID)
    s["classification"] = "educational_book_source"
    s["classification_evidence"] = "61/61 technical verification + complete source-local visual review of stored pages 8..68; page 8 explicit TOC; page 9 first-semester cover; nine explicit lesson starts and lesson-local review boundaries. Current master History references are not equivalent and were not used for semantic mapping."
    s["review_status"] = "reconstructed_verified_source_local"
    s["technical_verification"] = {
        "status": "verified",
        "report_path": f"content-staging/reconstruction/technical/{SID}.json",
        "images_verified": 61,
        "readable": 61,
        "sha256_match_manifest": 61,
        "mime_match_manifest": 61,
        "duplicate_sha_groups_within_source": 0,
    }
    s["reconstruction"] = {
        "status": "verified_source_local",
        "path": f"content-staging/reconstruction/educational/{SID}.json",
        "source_label": "التاريخ الكتاب المدرسي",
        "book_title": "NOT VERIFIED",
        "stored_page_range": [8, 68],
        "retained_pages": 61,
        "explicit_units": 0,
        "sections": 1,
        "lessons": 9,
        "lesson_pages": 47,
        "lesson_review_pages": 12,
        "toc_pages": 1,
        "section_cover_pages": 1,
        "legacy_questions": 138,
        "structurally_lesson_linked_questions": 138,
        "review_required_questions": 0,
        "semantic_question_review": "NOT VERIFIED",
        "master_reference_equivalence": "NOT VERIFIED",
        "raw_mutations": 0,
    }

    p["status"] = "RECONSTRUCTION_IN_PROGRESS_NOT_IMPORT_READY"
    new_progress = dict(progress)
    new_progress.update({
        "sources_completed": 13,
        "educational_sources_completed": 4,
        "verified_books": 4,
        "verified_units": 25,
        "verified_lessons": 119,
        "verified_lesson_pages": 460,
        "source_images_technically_verified": 1011,
        "lesson_linked_structural": 2374,
        "exam_linked_to_individual_model": 967,
        "review_required": 351,
        "unclassified": 22063,
        "raw_mutations": 0,
        "unrelated_mutations": 0,
        "new_imports": 0,
        "new_publications": 0,
    })
    assert new_progress["lesson_linked_structural"] + new_progress["exam_linked_to_individual_model"] + new_progress["review_required"] + new_progress["unclassified"] == 25755
    p["reconstruction_progress"] = new_progress
    MASTER.write_text(json.dumps(p, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    status = """## Reconstruction checkpoint — Grade 9 History source-local semester 1

- Phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`.
- Sources processed: **13/58**; Educational: **4/26**; Exam Source Groups: **9/32**.
- Books / explicit Units / Lessons / Lesson pages: **4 / 25 / 119 / 460**.
- History source: **61/61** technically verified images, stored pages **8..68**, complete source-local visual review.
- Master equivalence: **NOT VERIFIED**; current master History references were explicitly rejected as semantic authority for this RAW.
- Source-local structure: page **8** explicit TOC; page **9** `الفصل الدراسي الأول` cover; **9 lessons**, **47 lesson-content pages**, **12 lesson-review pages**; all **61 pages classified exactly once**.
- Questions: **138/138** structurally lesson-linked by verified source page membership; semantic correctness remains `NOT VERIFIED`; source review-required questions **0**.
- Global questions: Lesson-linked **2,374**; Exam-linked **967**; Review-required **351**; Unclassified **22,063** = **25,755**.
- Individual Exam Models **135**; Exam Pages **455/2,286**; Verified Answer Keys **0**.
- Source images technical **1,011/5,273**; WebP **0/0/0**; Duplicate groups **0/99**.
- RAW / unrelated / imports / publications: **0/0/0/0**.
- Last completed: `0a76f44b-0a4f-4e36-9ea9-badecf78bf23 — التاريخ الكتاب المدرسي`.
- Next: `7f02b242-5164-46d1-a82d-7f1023cfa8c9 — التربية الوطنية`.
"""
    replace_block(ROOT / "content-staging/CONTENT_REBUILD_EXECUTION_STATUS.md", status)
    replace_block(ROOT / "content-staging/CONTENT_REBUILD_HANDOFF.md", """## Active reconstruction handoff — History source-local reconstruction complete

- Last completed: `0a76f44b-0a4f-4e36-9ea9-badecf78bf23 — التاريخ الكتاب المدرسي`.
- Verified: **61/61** technical + complete source-local visual review; **1 explicit semester section / 9 lessons / 47 lesson-content pages / 12 lesson-review pages**.
- Master equivalence remains `NOT VERIFIED`; no master title/boundary was copied.
- Questions: **138/138 structurally lesson-linked; semantic correctness NOT VERIFIED; 0 source review-required**.
- Current/next: `7f02b242-5164-46d1-a82d-7f1023cfa8c9 — التربية الوطنية`.
- Exact next operation: fetch the live National Education manifest/pages; technical verification first; establish source identity only from its own evidence; reconstruct explicit book/section/unit/lesson/review boundaries without inheriting History patterns; map questions only where page membership is proven; assert global invariant; checkpoint.
- RAW/unrelated/import/publication mutations remain **0/0/0/0**.
""")
    replace_block(ROOT / "content-staging/CONTENT_INVENTORY.md", """## Verified reconstruction checkpoint — Grade 9 History source-local slice

- Legacy source `0a76f44b-0a4f-4e36-9ea9-badecf78bf23` has **61/61** technically verified immutable RAW pages, stored **8..68**.
- Complete source-local visual evidence proves page **8** is a TOC for both semesters and page **9** is the first-semester cover; the retained slice contains the complete explicit first-semester lesson sequence from stored pages **10..68**.
- Reconstructed source-local structure: **9 lessons, 47 lesson-content pages, 12 lesson-review pages, 1 TOC page, 1 semester-cover page**; no explicit Unit construct was invented.
- **138/138** source questions are structurally linked to the lesson whose verified page range contains the legacy page; semantic correctness remains `NOT VERIFIED`.
- Current `master` History parts are not content-equivalent to this RAW and remain reference-only for this source.
""")
    replace_block(ROOT / "content-staging/CONTENT_VALIDATION_REPORT.md", """## Grade 9 History source-local reconstruction validation

- Technical verification: **61/61** files exist, readable, size/SHA/MIME match; no within-source SHA duplicates.
- Source-local visual evidence: complete stored-page coverage **8..68**; explicit TOC and semester cover visually verified; all nine lesson start pages and twelve lesson-review pages visually checked.
- Structure: **1 semester section / 9 lessons / 47 lesson-content pages / 12 lesson-review pages**; every one of the **61** retained pages is classified exactly once.
- Questions: **138/138** structurally accounted for by verified page membership; semantic correctness `NOT VERIFIED`.
- Master-equivalence status: `NOT VERIFIED`; 0/61 exact SHA and 0 strong global visual matches against the currently indexed 211 master History pages.
- RAW mutations: **0**.
""")
    replace_block(ROOT / "content-staging/CONTENT_IMPORT_REPORT.md", """## History reconstruction checkpoint — no import performed

The History source-local reconstruction is verified, but the corpus remains `RECONSTRUCTION_IN_PROGRESS_NOT_IMPORT_READY`.

- New imports: **0**; new publications: **0**; production mutations: **0**; RAW mutations: **0**.
- Import readiness remains deferred until corpus reconstruction/boundary discovery is complete.
""")
    cont = ROOT / "content-staging/CONTENT_REBUILD_CONTINUATION_2026-09-14.md"
    if cont.exists():
        replace_block(cont, """## Continuation checkpoint — History source-local reconstruction complete

Continue with `7f02b242-5164-46d1-a82d-7f1023cfa8c9 — التربية الوطنية`; do not rerun History absent fresh drift evidence. Current verified global progress: **13/58 sources; 4/26 educational; 9/32 exam groups; 1,011/5,273 technical images; 2,374 lesson-linked; 967 exam-linked; 351 review-required; 22,063 unclassified**. History master equivalence remains `NOT VERIFIED`, but source-local structure is independently verified from immutable RAW evidence.
""")

    print(json.dumps({
        "checkpoint": "HISTORY_SOURCE_LOCAL",
        "sources": 13,
        "educational": 4,
        "books": 4,
        "units": 25,
        "lessons": 119,
        "lesson_pages": 460,
        "images_verified": 1011,
        "lesson_linked": 2374,
        "unclassified": 22063,
        "invariant": 25755,
        "next_source": NEXT,
        "raw_mutations": 0,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
