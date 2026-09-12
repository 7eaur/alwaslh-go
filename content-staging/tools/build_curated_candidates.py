#!/usr/bin/env python3
"""Build reviewable curriculum candidates from raw legacy pages + document manifest.

This does NOT create final production lessons. It reconstructs Document/Section
membership and emits lesson/activity candidates with explicit review status.
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


def read_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: pathlib.Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def stable_id(seed: str) -> str:
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()[:20]


def normalize_title(value: str) -> str:
    return " ".join(value.strip().split())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject-id", required=True)
    parser.add_argument("--source-manifest", required=True, help="Path to existing document manifest.json")
    parser.add_argument("--class-slug", required=True)
    parser.add_argument("--subject-slug", required=True)
    parser.add_argument("--document-slug", required=True)
    args = parser.parse_args()

    raw_dir = RAW / "subjects" / args.subject_id
    pages_path = raw_dir / "pages.json"
    if not pages_path.exists():
        raise SystemExit(f"missing raw pages: {pages_path}")
    pages = read_json(pages_path)
    manifest = read_json(ROOT / args.source_manifest)
    if not isinstance(pages, list) or not isinstance(manifest, list):
        raise SystemExit("pages and source manifest must be arrays")

    page_by_number = {int(page["page_number"]): page for page in pages}
    if len(page_by_number) != len(pages):
        raise SystemExit("duplicate raw page_number values require manual resolution")

    structural = [entry for entry in manifest if isinstance(entry.get("book_page"), int)]
    structural_by_book_page = {int(entry["book_page"]): entry for entry in structural}
    missing_structure = sorted(set(page_by_number) - set(structural_by_book_page))
    if missing_structure:
        raise SystemExit(f"manifest lacks book pages: {missing_structure}")

    sections: dict[str, list[dict[str, Any]]] = defaultdict(list)
    page_candidates: list[dict[str, Any]] = []
    for page_number in sorted(page_by_number):
        page = page_by_number[page_number]
        entry = structural_by_book_page[page_number]
        section_title = normalize_title(str(entry["section"]))
        source_title = normalize_title(str(page["title"]))
        manifest_title = normalize_title(str(entry["title"]))
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
            "question_count": int(page.get("question_count", len(page.get("ai_questions", [])))),
            "status": "review_required",
            "review_reason": "page title is an activity/lesson candidate; final lesson boundary not automatically asserted",
        }
        sections[section_title].append(candidate)
        page_candidates.append(candidate)

    section_rows = []
    for position, (title, candidates) in enumerate(sections.items()):
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
        "schema_version": 1,
        "target": {
            "class_slug": args.class_slug,
            "subject_slug": args.subject_slug,
            "document_slug": args.document_slug,
        },
        "legacy_subject_id": args.subject_id,
        "source_manifest": args.source_manifest,
        "counts": {
            "raw_pages": len(pages),
            "sections": len(section_rows),
            "page_candidates": len(page_candidates),
            "title_mismatches": len(title_mismatches),
        },
        "sections": section_rows,
        "page_candidates": page_candidates,
        "unresolved": {
            "title_mismatches": title_mismatches,
            "lesson_boundaries": "all page candidates require reviewed grouping before production import",
        },
    }

    out = CURATED / args.class_slug / args.subject_slug / args.document_slug / "reconstruction-candidates.json"
    write_json(out, result)
    print(json.dumps(result["counts"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
