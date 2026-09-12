#!/usr/bin/env python3
"""Reconstruct curriculum hierarchy from immutable raw source + reviewed structure hints.

This script does not infer units from page titles. A mapping must explicitly name a
structure strategy. The initial English pilot uses the repository's book manifest and
joins legacy page_number to manifest.book_page.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import unicodedata
from pathlib import Path
from typing import Any


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def normalize_text(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value).split()).strip()


def slug_piece(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii").lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")
    return normalized[:48] or "section"


def short_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:10]


def group_lessons(section_pages: list[dict[str, Any]], legacy_subject_id: str) -> list[dict[str, Any]]:
    """Group only contiguous pages with the same manifest title inside one section."""
    lessons: list[dict[str, Any]] = []
    current: list[dict[str, Any]] = []
    current_title = ""

    def flush() -> None:
        nonlocal current
        if not current:
            return
        first = current[0]
        source_key = f"{legacy_subject_id}:{first['legacy_page_id']}"
        first_page = int(first["page_number"])
        lessons.append(
            {
                "source_key": source_key,
                "slug": f"lesson-{first_page:03d}-{short_hash(source_key)}",
                "title": current_title,
                "first_page_number": first_page,
                "last_page_number": int(current[-1]["page_number"]),
                "pages": list(current),
            }
        )
        current = []

    for page in section_pages:
        title = normalize_text(str(page["canonical_title"]))
        previous = current[-1] if current else None
        contiguous = previous is not None and int(page["page_number"]) == int(previous["page_number"]) + 1
        if current and (title != current_title or not contiguous):
            flush()
        if not current:
            current_title = title
        current.append(page)
    flush()
    return lessons


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mapping", default="staging/config/legacy-subject-map.json")
    parser.add_argument("--key", required=True)
    parser.add_argument("--raw-root", default="staging/raw/legacy-supabase")
    parser.add_argument("--curated-root", default="staging/curated")
    parser.add_argument("--repo-root", default=".")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    config = read_json(repo_root / args.mapping)
    mapping = config["mappings"].get(args.key)
    if not mapping:
        raise RuntimeError(f"Unknown mapping key: {args.key}")
    if mapping["structure"]["strategy"] != "manifest_book_page":
        raise RuntimeError(f"Unsupported structure strategy: {mapping['structure']['strategy']}")

    legacy_subject_id = str(mapping["legacySubjectId"])
    raw_subject_root = repo_root / args.raw_root / "subjects" / legacy_subject_id
    pages = read_json(raw_subject_root / "pages.json")
    image_manifest = read_json(raw_subject_root / "image-manifest.json")
    if len(pages) != int(mapping["expectedPages"]):
        raise RuntimeError(f"Source page count mismatch: {len(pages)} != {mapping['expectedPages']}")

    source_question_count = sum(len(page.get("ai_questions") or []) for page in pages)
    if source_question_count != int(mapping["expectedQuestions"]):
        raise RuntimeError(
            f"Source question count mismatch: {source_question_count} != {mapping['expectedQuestions']}"
        )

    structure_path = repo_root / mapping["structure"]["manifestPath"]
    structure_manifest = read_json(structure_path)
    by_book_page: dict[int, dict[str, Any]] = {}
    for row in structure_manifest:
        book_page = row.get(mapping["structure"]["manifestPageField"])
        if not isinstance(book_page, int):
            continue
        if book_page in by_book_page:
            raise RuntimeError(f"Duplicate structure book_page: {book_page}")
        by_book_page[book_page] = row

    image_by_page = {str(row["legacy_page_id"]): row for row in image_manifest}
    if len(image_by_page) != len(pages):
        raise RuntimeError("Raw image manifest must contain exactly one downloaded image per pilot page")

    joined_pages: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    for page in pages:
        page_number = page.get(mapping["structure"]["sourcePageField"])
        if not isinstance(page_number, int):
            raise RuntimeError(f"Missing source page number: {page.get('id')}")
        structure = by_book_page.get(page_number)
        if not structure:
            raise RuntimeError(f"No structure manifest row for book page {page_number}")
        image = image_by_page.get(str(page["id"]))
        if not image:
            raise RuntimeError(f"No raw image for legacy page {page['id']}")
        canonical_title = normalize_text(str(structure[mapping["structure"]["titleField"]]))
        legacy_title = normalize_text(str(page.get("title") or ""))
        if canonical_title != legacy_title:
            warnings.append(
                {
                    "type": "title_mismatch",
                    "legacy_page_id": page["id"],
                    "page_number": page_number,
                    "legacy_title": legacy_title,
                    "manifest_title": canonical_title,
                }
            )
        joined_pages.append(
            {
                "legacy_page_id": page["id"],
                "legacy_subject_id": legacy_subject_id,
                "page_number": page_number,
                "legacy_title": legacy_title,
                "canonical_title": canonical_title,
                "section_title": normalize_text(str(structure[mapping["structure"]["sectionField"]])),
                "content_type": page.get("content_type"),
                "raw_image_path": image["raw_path"],
                "raw_image_sha256": image["sha256"],
                "raw_image_bytes": image["byte_size"],
                "raw_image_content_type": image["content_type"],
                "source_image_url": image["source_url"],
                "questions": page.get("ai_questions") or [],
            }
        )

    target = mapping["target"]
    document_root = repo_root / args.curated_root / target["classSlug"] / target["subjectSlug"] / target["documentSlug"]
    if document_root.exists():
        shutil.rmtree(document_root)
    document_root.mkdir(parents=True, exist_ok=True)

    ordered_sections: list[str] = []
    by_section: dict[str, list[dict[str, Any]]] = {}
    for page in joined_pages:
        title = page["section_title"]
        if title not in by_section:
            ordered_sections.append(title)
            by_section[title] = []
        by_section[title].append(page)

    section_summaries: list[dict[str, Any]] = []
    total_lessons = 0
    total_questions = 0
    for section_position, section_title in enumerate(ordered_sections):
        section_slug = f"section-{section_position + 1:02d}-{slug_piece(section_title)}"
        section_root = document_root / "sections" / section_slug
        section_pages = by_section[section_title]
        lessons = group_lessons(section_pages, legacy_subject_id)
        lesson_summaries: list[dict[str, Any]] = []

        for lesson_position, lesson in enumerate(lessons):
            lesson_root = section_root / "lessons" / lesson["slug"]
            curated_pages: list[dict[str, Any]] = []
            questions: list[dict[str, Any]] = []
            for page_position, page in enumerate(lesson["pages"]):
                optimized_rel = (
                    Path("staging/curated")
                    / target["classSlug"]
                    / target["subjectSlug"]
                    / target["documentSlug"]
                    / "sections"
                    / section_slug
                    / "lessons"
                    / lesson["slug"]
                    / "media"
                    / f"page-{int(page['page_number']):05d}.webp"
                ).as_posix()
                curated_pages.append(
                    {
                        "position": page_position,
                        "legacy_page_id": page["legacy_page_id"],
                        "page_number": page["page_number"],
                        "legacy_title": page["legacy_title"],
                        "canonical_title": page["canonical_title"],
                        "raw_image_path": page["raw_image_path"],
                        "raw_image_sha256": page["raw_image_sha256"],
                        "raw_image_bytes": page["raw_image_bytes"],
                        "raw_image_content_type": page["raw_image_content_type"],
                        "optimized_image_path": optimized_rel,
                    }
                )
                for ordinal, raw_question in enumerate(page["questions"]):
                    questions.append(
                        {
                            "source": {
                                "legacy_page_id": page["legacy_page_id"],
                                "page_number": page["page_number"],
                                "ordinal": ordinal,
                                "raw_image_sha256": page["raw_image_sha256"],
                            },
                            "raw": raw_question,
                            "review_status": "source_preserved",
                        }
                    )

            lesson_doc = {
                "schema_version": 1,
                "slug": lesson["slug"],
                "title": lesson["title"],
                "position": lesson_position,
                "section_slug": section_slug,
                "legacy_subject_id": legacy_subject_id,
                "source_key": lesson["source_key"],
                "first_page_number": lesson["first_page_number"],
                "last_page_number": lesson["last_page_number"],
                "page_count": len(curated_pages),
                "question_count": len(questions),
                "review_status": "needs_review",
            }
            write_json(lesson_root / "lesson.json", lesson_doc)
            write_json(lesson_root / "pages.json", curated_pages)
            write_json(lesson_root / "questions.json", questions)
            lesson_summaries.append(lesson_doc)
            total_lessons += 1
            total_questions += len(questions)

        section_doc = {
            "schema_version": 1,
            "slug": section_slug,
            "title": section_title,
            "position": section_position,
            "page_count": len(section_pages),
            "lesson_count": len(lessons),
            "review_status": "derived_from_manifest",
        }
        write_json(section_root / "section.json", section_doc)
        write_json(section_root / "lessons.json", lesson_summaries)
        section_summaries.append(section_doc)

    document_doc = {
        "schema_version": 1,
        "class_slug": target["classSlug"],
        "subject_slug": target["subjectSlug"],
        "document_slug": target["documentSlug"],
        "document_kind": target["documentKind"],
        "legacy_project_ref": mapping["legacyProjectRef"],
        "legacy_class_id": mapping["legacyClassId"],
        "legacy_class_name": mapping["legacyClassName"],
        "legacy_subject_id": legacy_subject_id,
        "legacy_subject_name": mapping["legacySubjectName"],
        "structure_strategy": mapping["structure"]["strategy"],
        "structure_manifest_path": mapping["structure"]["manifestPath"],
        "section_count": len(section_summaries),
        "lesson_count": total_lessons,
        "page_count": len(joined_pages),
        "question_count": total_questions,
        "review_status": "needs_review",
    }
    write_json(document_root / "document.json", document_doc)
    write_json(document_root / "sections.json", section_summaries)
    write_json(document_root / "reconstruction-warnings.json", warnings)

    print(
        json.dumps(
            {
                "document": f"{target['classSlug']}/{target['subjectSlug']}/{target['documentSlug']}",
                "sections": len(section_summaries),
                "lessons": total_lessons,
                "pages": len(joined_pages),
                "questions": total_questions,
                "warnings": len(warnings),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
