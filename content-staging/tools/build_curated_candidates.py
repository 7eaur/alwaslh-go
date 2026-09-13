#!/usr/bin/env python3
"""Build reviewable curriculum candidates from raw legacy pages + document manifest.

This does NOT create final production lessons. It reconstructs Document/Section
membership and emits page-level lesson/activity candidates with explicit review
status while preserving immutable raw provenance.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
from collections import defaultdict
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[2]
STAGING = ROOT / "content-staging"
RAW = STAGING / "raw" / "legacy-supabase"
CURATED = STAGING / "curated"
FULL_REPORT = RAW / "FULL_EXTRACTION_REPORT.json"


def read_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: pathlib.Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stable_id(seed: str) -> str:
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()[:20]


def normalize_title(value: str) -> str:
    return " ".join(value.strip().split())


def unique_page_map(rows: list[dict[str, Any]], *, field: str, label: str) -> dict[int, dict[str, Any]]:
    result: dict[int, dict[str, Any]] = {}
    duplicates: list[int] = []
    for row in rows:
        value = row.get(field)
        if not isinstance(value, int):
            continue
        if value in result:
            duplicates.append(value)
        result[value] = row
    if duplicates:
        raise SystemExit(f"duplicate {label} page numbers require manual resolution: {sorted(set(duplicates))}")
    return result


def index_raw_images(raw_manifest: dict[str, Any], pages: dict[int, dict[str, Any]]) -> dict[int, dict[str, Any]]:
    images = raw_manifest.get("images")
    if not isinstance(images, list):
        raise SystemExit("raw subject manifest images must be an array")

    by_page = unique_page_map(images, field="page_number", label="raw image")
    missing = sorted(set(pages) - set(by_page))
    extra = sorted(set(by_page) - set(pages))
    if missing or extra:
        raise SystemExit(f"raw image/page coverage mismatch: missing={missing} extra={extra}")

    for page_number, page in pages.items():
        image = by_page[page_number]
        if image.get("legacy_page_id") != page.get("id"):
            raise SystemExit(f"raw image provenance mismatch at page {page_number}")
        if not image.get("raw_path") or not image.get("sha256"):
            raise SystemExit(f"raw image provenance incomplete at page {page_number}")
        if int(image.get("byte_size", 0)) <= 0:
            raise SystemExit(f"raw image byte size invalid at page {page_number}")
    return by_page


def full_report_subject(full_report: dict[str, Any], subject_id: str) -> dict[str, Any]:
    rows = full_report.get("subjects")
    if not isinstance(rows, list):
        raise SystemExit("full extraction report subjects must be an array")
    matches = [row for row in rows if row.get("subject_id") == subject_id]
    if len(matches) != 1:
        raise SystemExit(f"full extraction report subject entry must be unique: {subject_id}")
    return matches[0]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject-id", required=True)
    parser.add_argument("--source-manifest", required=True, help="Path to reviewed document manifest.json")
    parser.add_argument("--class-slug", required=True)
    parser.add_argument("--subject-slug", required=True)
    parser.add_argument("--document-slug", required=True)
    parser.add_argument("--document-type", default="unknown")
    parser.add_argument("--document-year", default=None)
    args = parser.parse_args()

    raw_dir = RAW / "subjects" / args.subject_id
    pages_path = raw_dir / "pages.json"
    raw_manifest_path = raw_dir / "manifest.json"
    source_manifest_path = ROOT / args.source_manifest

    for required in (pages_path, raw_manifest_path, FULL_REPORT, source_manifest_path):
        if not required.exists():
            raise SystemExit(f"missing required curation input: {required}")

    pages = read_json(pages_path)
    raw_manifest = read_json(raw_manifest_path)
    full_report = read_json(FULL_REPORT)
    source_manifest = read_json(source_manifest_path)
    if not isinstance(pages, list) or not isinstance(source_manifest, list):
        raise SystemExit("pages and source manifest must be arrays")

    raw_counts = raw_manifest.get("counts", {})
    if raw_counts.get("image_download_failures") != 0:
        raise SystemExit("raw subject contains image download failures")
    if raw_counts.get("images_downloaded") != raw_counts.get("image_references"):
        raise SystemExit("raw subject image download count is incomplete")

    page_by_number = unique_page_map(pages, field="page_number", label="raw")
    if len(page_by_number) != len(pages):
        raise SystemExit("raw pages with missing/invalid page_number require manual resolution")

    raw_images_by_page = index_raw_images(raw_manifest, page_by_number)

    report_subject = full_report_subject(full_report, args.subject_id)
    raw_manifest_sha = raw_manifest.get("manifest_sha256")
    if not raw_manifest_sha or report_subject.get("manifest_sha256") != raw_manifest_sha:
        raise SystemExit("raw subject manifest does not match the verified full-extraction snapshot")

    structural = [entry for entry in source_manifest if isinstance(entry.get("book_page"), int)]
    structural_by_book_page = unique_page_map(structural, field="book_page", label="source manifest")
    missing_structure = sorted(set(page_by_number) - set(structural_by_book_page))
    extra_structure = sorted(set(structural_by_book_page) - set(page_by_number))
    if missing_structure or extra_structure:
        raise SystemExit(
            f"source manifest/raw page coverage mismatch: missing={missing_structure} extra={extra_structure}"
        )

    sections: dict[str, list[dict[str, Any]]] = defaultdict(list)
    page_candidates: list[dict[str, Any]] = []
    total_questions = 0
    for page_number in sorted(page_by_number):
        page = page_by_number[page_number]
        entry = structural_by_book_page[page_number]
        image = raw_images_by_page[page_number]
        section_title = normalize_title(str(entry["section"]))
        source_title = normalize_title(str(page["title"]))
        manifest_title = normalize_title(str(entry["title"]))
        question_count = len(page.get("ai_questions", [])) if isinstance(page.get("ai_questions"), list) else 0
        total_questions += question_count
        candidate_seed = f"{args.subject_id}:{page['id']}"
        candidate = {
            "candidate_id": f"page-candidate-{stable_id(candidate_seed)}",
            "legacy_page_id": page["id"],
            "book_page": page_number,
            "source_page": entry.get("source_page"),
            "section": section_title,
            "legacy_title": source_title,
            "manifest_title": manifest_title,
            "title_match": source_title == manifest_title,
            "question_count": question_count,
            "raw_image": {
                "raw_path": image["raw_path"],
                "sha256": image["sha256"],
                "byte_size": int(image["byte_size"]),
                "mime_type": image.get("mime_type"),
                "storage_bucket": image.get("storage_bucket"),
                "storage_object_path": image.get("storage_object_path"),
            },
            "status": "review_required",
            "review_reason": "page title is an activity/lesson candidate; final lesson boundary not automatically asserted",
        }
        sections[section_title].append(candidate)
        page_candidates.append(candidate)

    section_rows = []
    for position, (title, candidates) in enumerate(sections.items(), start=1):
        section_seed = f"{args.subject_id}:{title}"
        section_rows.append(
            {
                "section_id": f"section-{stable_id(section_seed)}",
                "title": title,
                "position": position,
                "first_book_page": candidates[0]["book_page"],
                "last_book_page": candidates[-1]["book_page"],
                "page_count": len(candidates),
                "candidate_ids": [candidate["candidate_id"] for candidate in candidates],
                "status": "structure_recovered",
            }
        )

    title_mismatches = [candidate for candidate in page_candidates if not candidate["title_match"]]
    result = {
        "schema_version": 2,
        "target": {
            "class_slug": args.class_slug,
            "subject_slug": args.subject_slug,
            "document_slug": args.document_slug,
            "document_type": args.document_type,
            "document_year": args.document_year,
        },
        "legacy_subject_id": args.subject_id,
        "provenance": {
            "full_extraction_snapshot_sha256": full_report.get("snapshot_sha256"),
            "source_inventory_sha256": full_report.get("source_inventory_sha256"),
            "raw_subject_manifest_sha256": raw_manifest_sha,
            "raw_pages_sha256": raw_manifest.get("pages_sha256"),
            "source_manifest_path": args.source_manifest,
            "source_manifest_sha256": sha256_file(source_manifest_path),
        },
        "counts": {
            "raw_pages": len(pages),
            "raw_images": len(raw_images_by_page),
            "sections": len(section_rows),
            "page_candidates": len(page_candidates),
            "questions": total_questions,
            "title_mismatches": len(title_mismatches),
        },
        "sections": section_rows,
        "page_candidates": page_candidates,
        "unresolved": {
            "title_mismatches": title_mismatches,
            "lesson_boundaries": "all page candidates require reviewed grouping before production import",
        },
        "publication_status": "not_importable",
    }

    out = CURATED / args.class_slug / args.subject_slug / args.document_slug / "reconstruction-candidates.json"
    write_json(out, result)
    print(json.dumps({"output": str(out.relative_to(ROOT)), "counts": result["counts"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
