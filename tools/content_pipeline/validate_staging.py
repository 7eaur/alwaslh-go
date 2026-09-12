#!/usr/bin/env python3
"""Validate raw/curated content staging contracts before any application import."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from PIL import Image


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


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
    require(mapping is not None, f"Unknown mapping key: {args.key}")

    subject_id = str(mapping["legacySubjectId"])
    raw_subject = repo_root / args.raw_root / "subjects" / subject_id
    pages = read_json(raw_subject / "pages.json")
    image_manifest = read_json(raw_subject / "image-manifest.json")
    questions = read_json(raw_subject / "questions.json")
    require(len(pages) == int(mapping["expectedPages"]), "Raw page count does not match mapping contract")
    require(len(questions) == int(mapping["expectedQuestions"]), "Raw question count does not match mapping contract")
    require(len(image_manifest) == len(pages), "Every pilot page must have exactly one downloaded raw image")

    raw_page_ids = [str(page["id"]) for page in pages]
    require(len(raw_page_ids) == len(set(raw_page_ids)), "Duplicate legacy page IDs in raw export")
    page_numbers = [page.get("page_number") for page in pages]
    require(all(isinstance(number, int) and number > 0 for number in page_numbers), "Invalid raw page_number")
    require(len(page_numbers) == len(set(page_numbers)), "Duplicate page_number in pilot raw export")

    image_by_page: dict[str, dict[str, Any]] = {}
    raw_sha_values: set[str] = set()
    for image in image_manifest:
        page_id = str(image["legacy_page_id"])
        require(page_id not in image_by_page, f"Duplicate raw image mapping for page {page_id}")
        image_by_page[page_id] = image
        path = repo_root / args.raw_root / str(image["raw_path"])
        require(path.is_file(), f"Missing raw image file: {path}")
        require(path.stat().st_size == int(image["byte_size"]), f"Raw image byte size mismatch: {path}")
        actual_sha = sha256_file(path)
        require(actual_sha == image["sha256"], f"Raw image SHA-256 mismatch: {path}")
        raw_sha_values.add(actual_sha)

    target = mapping["target"]
    document_root = repo_root / args.curated_root / target["classSlug"] / target["subjectSlug"] / target["documentSlug"]
    document = read_json(document_root / "document.json")
    sections = read_json(document_root / "sections.json")
    require(document["page_count"] == len(pages), "Curated document page count mismatch")
    require(document["question_count"] == len(questions), "Curated document question count mismatch")
    require(document["section_count"] == len(sections), "Curated section count mismatch")

    seen_pages: dict[str, str] = {}
    curated_question_count = 0
    curated_lesson_count = 0
    optimized_sha_values: set[str] = set()

    for expected_section_position, section in enumerate(sections):
        require(section["position"] == expected_section_position, "Section positions are not contiguous")
        section_root = document_root / "sections" / section["slug"]
        section_detail = read_json(section_root / "section.json")
        require(section_detail == section, f"Section summary/detail mismatch: {section['slug']}")
        lessons = read_json(section_root / "lessons.json")
        require(len(lessons) == section["lesson_count"], f"Section lesson count mismatch: {section['slug']}")

        for expected_lesson_position, lesson in enumerate(lessons):
            require(lesson["position"] == expected_lesson_position, f"Lesson positions are not contiguous: {lesson['slug']}")
            lesson_root = section_root / "lessons" / lesson["slug"]
            lesson_detail = read_json(lesson_root / "lesson.json")
            require(lesson_detail == lesson, f"Lesson summary/detail mismatch: {lesson['slug']}")
            lesson_pages = read_json(lesson_root / "pages.json")
            lesson_questions = read_json(lesson_root / "questions.json")
            require(len(lesson_pages) == lesson["page_count"], f"Lesson page count mismatch: {lesson['slug']}")
            require(len(lesson_questions) == lesson["question_count"], f"Lesson question count mismatch: {lesson['slug']}")

            lesson_page_ids: set[str] = set()
            previous_number: int | None = None
            for expected_page_position, page in enumerate(lesson_pages):
                require(page["position"] == expected_page_position, f"Page positions are not contiguous: {lesson['slug']}")
                page_id = str(page["legacy_page_id"])
                require(page_id in raw_page_ids, f"Curated page is not present in raw export: {page_id}")
                require(page_id not in seen_pages, f"Legacy page assigned to multiple lessons: {page_id}")
                seen_pages[page_id] = lesson["slug"]
                lesson_page_ids.add(page_id)
                page_number = int(page["page_number"])
                if previous_number is not None:
                    require(page_number == previous_number + 1, f"Non-contiguous page sequence in lesson {lesson['slug']}")
                previous_number = page_number

                raw_image = image_by_page[page_id]
                require(page["raw_image_sha256"] == raw_image["sha256"], f"Curated/raw SHA mismatch for page {page_id}")
                optimized_path = repo_root / str(page["optimized_image_path"])
                require(optimized_path.is_file(), f"Missing optimized image: {optimized_path}")
                require(sha256_file(optimized_path) == page.get("optimized_image_sha256"), f"Optimized SHA mismatch: {optimized_path}")
                require(optimized_path.stat().st_size == int(page.get("optimized_image_bytes", -1)), f"Optimized byte size mismatch: {optimized_path}")
                with Image.open(optimized_path) as image:
                    image.load()
                    require(image.format == "WEBP", f"Optimized image is not WebP: {optimized_path}")
                    require(image.size == (int(page["optimized_width"]), int(page["optimized_height"])), f"Optimized dimensions mismatch: {optimized_path}")
                optimized_sha_values.add(str(page["optimized_image_sha256"]))

            for question in lesson_questions:
                source = question["source"]
                require(str(source["legacy_page_id"]) in lesson_page_ids, f"Question is linked to a page outside its lesson: {lesson['slug']}")
                require(question["review_status"] == "source_preserved", "Raw question must remain source_preserved before review")
            curated_question_count += len(lesson_questions)
            curated_lesson_count += 1

    require(set(seen_pages) == set(raw_page_ids), "Not every raw page is represented exactly once in curated content")
    require(curated_question_count == len(questions), "Not every raw question is represented in curated content")
    require(curated_lesson_count == int(document["lesson_count"]), "Curated lesson count mismatch")

    result = {
        "verified": True,
        "mapping_key": args.key,
        "sections": len(sections),
        "lessons": curated_lesson_count,
        "pages": len(seen_pages),
        "questions": curated_question_count,
        "raw_image_files": len(image_manifest),
        "unique_raw_sha256": len(raw_sha_values),
        "optimized_webp_files": len(optimized_sha_values),
    }
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
