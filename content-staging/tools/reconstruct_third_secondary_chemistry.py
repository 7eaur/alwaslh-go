#!/usr/bin/env python3
"""Reconstruct the legacy Third Secondary Chemistry textbook source.

This is a derived, read-only reconstruction over immutable legacy RAW data.
It never edits RAW files. It validates the already-probed media/reference
evidence, groups contiguous source titles, reconstructs Unit -> Lesson -> Page
boundaries, and classifies nested legacy questions structurally.

Important modelling rule:
The source table of contents labels entries as topics, while legacy page records
use content_type="lesson" broadly (including unit starts/reviews). Therefore
only contiguous non-unit/non-review/non-appendix topic-title runs are mapped to
platform Lessons. Unit-start and unit-review questions remain review_required.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SUBJECT_ID = "f0c5228c-7d5b-4ec2-85ed-ce59139ce0a4"
CLASS_ID = "075b135c-8159-4727-a365-f7396690fb3f"
EXPECTED_PAGES = 178
EXPECTED_QUESTIONS = 2576
EXPECTED_UNITS = 9
EXPECTED_LESSONS = 57
EXPECTED_LESSON_PAGES = 149
EXPECTED_UNIT_INTRO_PAGES = 10
EXPECTED_UNIT_REVIEW_PAGES = 14
EXPECTED_APPENDIX_PAGES = 5
EXPECTED_LESSON_QUESTIONS = 2225
EXPECTED_REVIEW_REQUIRED_QUESTIONS = 351
EXPECTED_MASTER_COMMIT = "f81ebb6ef6198818fa091f7a8c1c81b4de7dbd23"
VISUALLY_REVIEWED_PAGES = [
    6, 7, 8, 9, 10, 11, 12, 22, 35, 40, 106, 112, 169, 180, 183, 184, 188, 189, 193
]


@dataclass
class Segment:
    title: str
    start_page: int
    end_page: int
    pages: list[dict[str, Any]]

    @property
    def page_count(self) -> int:
        return len(self.pages)

    @property
    def question_count(self) -> int:
        return sum(len(page.get("ai_questions") or []) for page in self.pages)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def group_title_runs(pages: list[dict[str, Any]]) -> list[Segment]:
    segments: list[Segment] = []
    current: list[dict[str, Any]] = []
    current_title: str | None = None
    for page in pages:
        title = str(page.get("title") or "").strip()
        if current and title != current_title:
            segments.append(
                Segment(
                    title=current_title or "",
                    start_page=int(current[0]["page_number"]),
                    end_page=int(current[-1]["page_number"]),
                    pages=current,
                )
            )
            current = []
        current_title = title
        current.append(page)
    if current:
        segments.append(
            Segment(
                title=current_title or "",
                start_page=int(current[0]["page_number"]),
                end_page=int(current[-1]["page_number"]),
                pages=current,
            )
        )
    return segments


def segment_kind(title: str) -> str:
    if title.startswith("الوحدة "):
        return "unit_intro"
    if title.startswith("تقويم الوحدة"):
        return "unit_review"
    if title == "المصطلحات العلمية":
        return "appendix"
    return "lesson"


def serialise_page(
    page: dict[str, Any],
    image: dict[str, Any],
    *,
    structural_kind: str,
    unit_id: str | None,
    lesson_id: str | None,
) -> dict[str, Any]:
    questions = page.get("ai_questions") or []
    if structural_kind == "lesson":
        question_classification = "lesson_question"
    elif structural_kind in {"unit_intro", "unit_review"}:
        question_classification = "review_required"
    else:
        question_classification = "unclassified"
    return {
        "page_number": int(page["page_number"]),
        "legacy_page_record_id": page.get("id"),
        "legacy_image_page_id": image.get("legacy_page_id"),
        "title": page.get("title"),
        "structural_kind": structural_kind,
        "unit_id": unit_id,
        "lesson_id": lesson_id,
        "raw_image": {
            "path": image.get("raw_path"),
            "sha256": image.get("sha256"),
            "bytes": image.get("byte_size"),
            "mime_type": image.get("mime_type"),
            "source_url": image.get("source_url"),
        },
        "legacy_question_count": len(questions),
        "question_classification": question_classification,
        "question_provenance_rule": "legacy_page_record_id + zero_based_ai_question_index",
    }


def reconstruct(
    raw_manifest: dict[str, Any],
    pages: list[dict[str, Any]],
    technical_scan: dict[str, Any],
    master_cross_reference: dict[str, Any],
    *,
    workflow_run_id: int | None,
) -> dict[str, Any]:
    pages = sorted(pages, key=lambda item: int(item["page_number"]))
    image_by_page = {int(item["page_number"]): item for item in raw_manifest["images"]}

    page_numbers = [int(page["page_number"]) for page in pages]
    if page_numbers != list(range(11, 189)):
        raise ValueError("Chemistry RAW page sequence must be exactly 11..188")
    if len(pages) != EXPECTED_PAGES or len(image_by_page) != EXPECTED_PAGES:
        raise ValueError("Unexpected Chemistry page/image count")
    if sum(len(page.get("ai_questions") or []) for page in pages) != EXPECTED_QUESTIONS:
        raise ValueError("Unexpected Chemistry legacy question count")

    tech = technical_scan["summary"]
    required_tech = {
        "records": EXPECTED_PAGES,
        "exists": EXPECTED_PAGES,
        "readable": EXPECTED_PAGES,
        "bytes_match_manifest": EXPECTED_PAGES,
        "sha256_match_manifest": EXPECTED_PAGES,
        "mime_match_manifest": EXPECTED_PAGES,
        "errors": 0,
        "duplicate_sha_groups": 0,
    }
    for key, expected in required_tech.items():
        if tech.get(key) != expected:
            raise ValueError(f"Technical scan mismatch for {key}: {tech.get(key)!r} != {expected!r}")
    if tech.get("page_number_min") != 11 or tech.get("page_number_max") != 188:
        raise ValueError("Unexpected technical scan page range")
    if tech.get("sequence_contiguous_in_manifest_order") is not True:
        raise ValueError("Technical scan sequence is not contiguous")

    if master_cross_reference.get("master_reference_commit") != EXPECTED_MASTER_COMMIT:
        raise ValueError("Unexpected trusted master reference commit")
    if master_cross_reference.get("shared_sha256_equal") != EXPECTED_PAGES:
        raise ValueError("RAW/master shared-range SHA-256 equality is incomplete")
    if master_cross_reference.get("shared_sha256_mismatch_or_missing") != 0:
        raise ValueError("RAW/master shared-range mismatch exists")

    segments = group_title_runs(pages)
    units: list[dict[str, Any]] = []
    appendix: list[dict[str, Any]] = []
    page_map: list[dict[str, Any]] = []
    current_unit: dict[str, Any] | None = None
    lesson_index = 0

    for segment in segments:
        kind = segment_kind(segment.title)
        if kind == "unit_intro":
            if current_unit is not None and current_unit.get("review") is None:
                raise ValueError(f"Previous unit lacks a review before {segment.title}")
            unit_index = len(units) + 1
            unit_id = f"chemistry-third-secondary-u{unit_index:02d}"
            current_unit = {
                "id": unit_id,
                "index": unit_index,
                "title": segment.title,
                "start_page": segment.start_page,
                "end_page": None,
                "intro": {
                    "start_page": segment.start_page,
                    "end_page": segment.end_page,
                    "page_count": segment.page_count,
                    "legacy_question_count": segment.question_count,
                    "question_classification": "review_required",
                },
                "lessons": [],
                "review": None,
            }
            units.append(current_unit)
            for page in segment.pages:
                page_map.append(
                    serialise_page(
                        page,
                        image_by_page[int(page["page_number"])],
                        structural_kind=kind,
                        unit_id=unit_id,
                        lesson_id=None,
                    )
                )
            continue

        if kind == "appendix":
            for page in segment.pages:
                page_map.append(
                    serialise_page(
                        page,
                        image_by_page[int(page["page_number"])],
                        structural_kind=kind,
                        unit_id=None,
                        lesson_id=None,
                    )
                )
            appendix.append(
                {
                    "title": segment.title,
                    "start_page": segment.start_page,
                    "end_page": segment.end_page,
                    "page_count": segment.page_count,
                    "legacy_question_count": segment.question_count,
                }
            )
            continue

        if current_unit is None:
            raise ValueError(f"Segment occurs before first unit: {segment.title}")

        if kind == "unit_review":
            if current_unit.get("review") is not None:
                raise ValueError(f"Duplicate review for {current_unit['title']}")
            current_unit["review"] = {
                "title": segment.title,
                "start_page": segment.start_page,
                "end_page": segment.end_page,
                "page_count": segment.page_count,
                "legacy_question_count": segment.question_count,
                "question_classification": "review_required",
            }
            current_unit["end_page"] = segment.end_page
            for page in segment.pages:
                page_map.append(
                    serialise_page(
                        page,
                        image_by_page[int(page["page_number"])],
                        structural_kind=kind,
                        unit_id=current_unit["id"],
                        lesson_id=None,
                    )
                )
            continue

        lesson_index += 1
        local_lesson_index = len(current_unit["lessons"]) + 1
        lesson_id = f"{current_unit['id']}-l{local_lesson_index:02d}"
        lesson = {
            "id": lesson_id,
            "global_index": lesson_index,
            "unit_lesson_index": local_lesson_index,
            "title": segment.title,
            "start_page": segment.start_page,
            "end_page": segment.end_page,
            "page_count": segment.page_count,
            "legacy_question_count": segment.question_count,
            "question_classification": "lesson_question",
        }
        current_unit["lessons"].append(lesson)
        for page in segment.pages:
            page_map.append(
                serialise_page(
                    page,
                    image_by_page[int(page["page_number"])],
                    structural_kind=kind,
                    unit_id=current_unit["id"],
                    lesson_id=lesson_id,
                )
            )

    if len(units) != EXPECTED_UNITS:
        raise ValueError(f"Expected {EXPECTED_UNITS} units, got {len(units)}")
    if any(unit.get("review") is None for unit in units):
        raise ValueError("Every reconstructed unit must have a verified review boundary")
    if sum(len(unit["lessons"]) for unit in units) != EXPECTED_LESSONS:
        raise ValueError("Unexpected reconstructed lesson count")

    page_map.sort(key=lambda item: item["page_number"])
    if [item["page_number"] for item in page_map] != list(range(11, 189)):
        raise ValueError("Derived page map is not complete/contiguous")

    counts = {
        "pages": len(page_map),
        "units": len(units),
        "lessons": sum(len(unit["lessons"]) for unit in units),
        "lesson_pages": sum(item["structural_kind"] == "lesson" for item in page_map),
        "unit_intro_pages": sum(item["structural_kind"] == "unit_intro" for item in page_map),
        "unit_review_pages": sum(item["structural_kind"] == "unit_review" for item in page_map),
        "appendix_pages": sum(item["structural_kind"] == "appendix" for item in page_map),
        "legacy_questions": sum(item["legacy_question_count"] for item in page_map),
        "lesson_question": sum(
            item["legacy_question_count"] for item in page_map if item["question_classification"] == "lesson_question"
        ),
        "exam_question": 0,
        "review_required": sum(
            item["legacy_question_count"] for item in page_map if item["question_classification"] == "review_required"
        ),
        "unclassified": sum(
            item["legacy_question_count"] for item in page_map if item["question_classification"] == "unclassified"
        ),
        "technically_verified_images": EXPECTED_PAGES,
    }
    expected_counts = {
        "pages": EXPECTED_PAGES,
        "units": EXPECTED_UNITS,
        "lessons": EXPECTED_LESSONS,
        "lesson_pages": EXPECTED_LESSON_PAGES,
        "unit_intro_pages": EXPECTED_UNIT_INTRO_PAGES,
        "unit_review_pages": EXPECTED_UNIT_REVIEW_PAGES,
        "appendix_pages": EXPECTED_APPENDIX_PAGES,
        "legacy_questions": EXPECTED_QUESTIONS,
        "lesson_question": EXPECTED_LESSON_QUESTIONS,
        "exam_question": 0,
        "review_required": EXPECTED_REVIEW_REQUIRED_QUESTIONS,
        "unclassified": 0,
        "technically_verified_images": EXPECTED_PAGES,
    }
    if counts != expected_counts:
        raise ValueError(f"Derived count mismatch: {counts!r} != {expected_counts!r}")

    return {
        "schema_version": 1,
        "status": "STRUCTURALLY_RECONSTRUCTED_WITH_REVIEW_REQUIRED",
        "source": {
            "legacy_class_id": CLASS_ID,
            "legacy_subject_id": SUBJECT_ID,
            "legacy_class_name": raw_manifest.get("legacy_class", {}).get("name"),
            "legacy_source_name": raw_manifest.get("legacy_subject", {}).get("name"),
            "raw_manifest_path": f"content-staging/raw/legacy-supabase/subjects/{SUBJECT_ID}/manifest.json",
            "raw_pages_path": f"content-staging/raw/legacy-supabase/subjects/{SUBJECT_ID}/pages.json",
            "raw_page_range": [11, 188],
        },
        "book": {
            "title": "الكيمياء الكتاب المدرسي",
            "class": "الكيمياء ثالث ثانوي",
            "capture_kind": "partial_original_book_capture",
            "capture_note": "Legacy RAW contains book pages 11..188 only; missing master-only numbered pages are not synthesized or imported.",
        },
        "mapping_policy": {
            "source_toc_label": "الموضوع",
            "legacy_content_type_observed": "lesson",
            "platform_lesson_rule": "contiguous non-unit/non-review/non-appendix title run",
            "unit_intro_question_rule": "review_required",
            "unit_review_question_rule": "review_required",
            "appendix_question_rule": "unclassified",
            "reason": "Avoids inventing lessons for unit covers/reviews while preserving all source topic boundaries and page provenance.",
        },
        "counts": counts,
        "units": units,
        "appendix": appendix,
        "pages": page_map,
        "evidence": {
            "trusted_master_reference_commit": EXPECTED_MASTER_COMMIT,
            "shared_raw_master_sha256_equal": EXPECTED_PAGES,
            "shared_raw_master_sha256_mismatch_or_missing": 0,
            "master_only_numbered_pages_outside_legacy_range": master_cross_reference.get(
                "master_only_numbered_pages_outside_legacy_range"
            ),
            "technical_scan": {
                "exists": tech.get("exists"),
                "readable": tech.get("readable"),
                "bytes_match_manifest": tech.get("bytes_match_manifest"),
                "sha256_match_manifest": tech.get("sha256_match_manifest"),
                "mime_match_manifest": tech.get("mime_match_manifest"),
                "duplicate_sha_groups": tech.get("duplicate_sha_groups"),
                "formats": tech.get("formats"),
                "extensions": tech.get("extensions"),
            },
            "selective_visual_review_pages": VISUALLY_REVIEWED_PAGES,
            "workflow_run_id": workflow_run_id,
        },
        "unresolved": [
            {
                "type": "question_placement",
                "count": EXPECTED_REVIEW_REQUIRED_QUESTIONS,
                "status": "review_required",
                "reason": "Questions originate on unit-intro or unit-review pages and are not silently attached to an invented Lesson.",
            }
        ],
        "import_status": "NOT VERIFIED",
        "publication_status": "NOT VERIFIED",
        "raw_mutations": 0,
        "unrelated_mutations": 0,
        "new_imports": 0,
        "new_publications": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-manifest", required=True, type=Path)
    parser.add_argument("--pages", required=True, type=Path)
    parser.add_argument("--technical-scan", required=True, type=Path)
    parser.add_argument("--master-cross-reference", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--workflow-run-id", type=int)
    args = parser.parse_args()

    result = reconstruct(
        load_json(args.raw_manifest),
        load_json(args.pages),
        load_json(args.technical_scan),
        load_json(args.master_cross_reference),
        workflow_run_id=args.workflow_run_id,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "counts": result["counts"], "unresolved": result["unresolved"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
