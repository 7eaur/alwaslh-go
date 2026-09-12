#!/usr/bin/env python3
"""Assemble a reviewable raw subject snapshot from small committed page chunks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def page_sort_key(row: dict[str, Any]) -> tuple[int, str, str]:
    number = row.get("page_number")
    return (
        int(number) if isinstance(number, int) else 2**31 - 1,
        str(row.get("created_at") or ""),
        str(row.get("id") or ""),
    )


def assemble(subject_root: Path, subject_id: str, expected_pages: int, expected_questions: int) -> dict[str, int]:
    chunk_files = sorted((subject_root / "page-chunks").glob("*.json"))
    if not chunk_files:
        raise RuntimeError(f"No page chunks found below {subject_root / 'page-chunks'}")

    pages: list[dict[str, Any]] = []
    for chunk_file in chunk_files:
        chunk = read_json(chunk_file)
        if not isinstance(chunk, list):
            raise RuntimeError(f"Page chunk must be an array: {chunk_file}")
        pages.extend(chunk)

    pages.sort(key=page_sort_key)
    if len(pages) != expected_pages:
        raise RuntimeError(f"Raw page count mismatch: {len(pages)} != {expected_pages}")

    ids: set[str] = set()
    numbers: set[int] = set()
    questions: list[dict[str, Any]] = []
    for page in pages:
        page_id = str(page.get("id") or "")
        if not page_id or page_id in ids:
            raise RuntimeError(f"Missing/duplicate page id: {page_id}")
        ids.add(page_id)
        if str(page.get("subject_id")) != subject_id:
            raise RuntimeError(f"Page belongs to another subject: {page_id}")
        page_number = page.get("page_number")
        if not isinstance(page_number, int) or page_number <= 0 or page_number in numbers:
            raise RuntimeError(f"Missing/duplicate/invalid page number: {page_number}")
        numbers.add(page_number)
        raw_questions = page.get("ai_questions")
        if raw_questions is None:
            raw_questions = []
        if not isinstance(raw_questions, list):
            raise RuntimeError(f"ai_questions must be an array: {page_id}")
        for ordinal, question in enumerate(raw_questions):
            questions.append(
                {
                    "legacy_page_id": page_id,
                    "legacy_subject_id": subject_id,
                    "page_number": page_number,
                    "ordinal": ordinal,
                    "raw": question,
                }
            )

    if len(questions) != expected_questions:
        raise RuntimeError(f"Raw question count mismatch: {len(questions)} != {expected_questions}")

    write_json(subject_root / "pages.json", pages)
    write_json(subject_root / "questions.json", questions)
    return {"pages": len(pages), "questions": len(questions), "chunks": len(chunk_files)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject-id", required=True)
    parser.add_argument("--expected-pages", required=True, type=int)
    parser.add_argument("--expected-questions", required=True, type=int)
    parser.add_argument("--raw-root", default="staging/raw/legacy-supabase")
    parser.add_argument("--repo-root", default=".")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    subject_root = repo_root / args.raw_root / "subjects" / args.subject_id
    result = assemble(subject_root, args.subject_id, args.expected_pages, args.expected_questions)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
