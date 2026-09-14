#!/usr/bin/env python3
"""Read-only technical scanner for legacy content source images.

The scanner never mutates RAW media. It validates each manifest image reference,
computes the real SHA-256, inspects the decoded image with Pillow, records
format/MIME/dimensions/bytes, and reports sequence/identity/duplicate anomalies.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from PIL import Image, UnidentifiedImageError


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_records(manifest_path: Path) -> list[dict[str, Any]]:
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("images", "pages", "records", "items"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    raise ValueError("Unsupported manifest shape: expected list or dict with images/pages/records/items")


def detect_repo_root(manifest_path: Path) -> Path:
    current = manifest_path.resolve().parent
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    raise RuntimeError("Could not locate repository root")


def resolve_image_path(repo_root: Path, image_ref: str) -> Path:
    raw = Path(image_ref)
    candidates = [repo_root / raw]
    if raw.parts and raw.parts[0] == "raw":
        candidates.insert(0, repo_root / "content-staging" / raw)
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return candidates[0]


def normalise_content_type(value: Any) -> str | None:
    if not value:
        return None
    return str(value).split(";", 1)[0].strip().lower() or None


def first_present(row: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in row and row[key] is not None:
            return row[key]
    return None


def scan_record(repo_root: Path, row: dict[str, Any], ordinal: int) -> dict[str, Any]:
    image_ref = first_present(row, "image_file", "image_path", "raw_path", "path")
    manifest_bytes = first_present(row, "image_size", "byte_size")
    manifest_sha = first_present(row, "image_sha256", "sha256")
    manifest_mime = normalise_content_type(first_present(row, "image_content_type", "mime_type"))
    page_number = row.get("page_number")
    result: dict[str, Any] = {
        "ordinal": ordinal,
        "page_number": page_number,
        "page_label": row.get("page_label"),
        "legacy_page_id": row.get("legacy_page_id"),
        "subject_id": row.get("subject_id"),
        "subject_name": row.get("subject_name"),
        "source_url": row.get("source_url"),
        "image_file": image_ref,
        "manifest_bytes": manifest_bytes,
        "manifest_sha256": manifest_sha,
        "manifest_content_type": manifest_mime,
        "exists": False,
        "readable": False,
        "extension": None,
        "extension_mime_guess": None,
        "detected_format": None,
        "detected_mime": None,
        "width": None,
        "height": None,
        "mode": None,
        "actual_bytes": None,
        "actual_sha256": None,
        "bytes_match_manifest": None,
        "sha256_match_manifest": None,
        "mime_match_manifest": None,
        "error": None,
    }

    if not image_ref:
        result["error"] = "missing image reference"
        return result

    image_path = resolve_image_path(repo_root, str(image_ref))
    result["extension"] = image_path.suffix.lower()
    result["extension_mime_guess"] = mimetypes.guess_type(image_path.name)[0]
    result["exists"] = image_path.is_file()
    if not result["exists"]:
        result["error"] = f"referenced image does not exist: {image_ref}"
        return result

    try:
        actual_bytes = image_path.stat().st_size
        actual_sha = sha256_file(image_path)
        result["actual_bytes"] = actual_bytes
        result["actual_sha256"] = actual_sha

        if manifest_bytes is not None:
            result["bytes_match_manifest"] = actual_bytes == int(manifest_bytes)
        if manifest_sha:
            result["sha256_match_manifest"] = actual_sha.lower() == str(manifest_sha).lower()

        with Image.open(image_path) as image:
            detected_format = image.format
            image.verify()
        with Image.open(image_path) as image:
            image.load()
            result["width"], result["height"] = image.size
            result["mode"] = image.mode
            detected_format = image.format or detected_format

        result["detected_format"] = detected_format
        result["detected_mime"] = Image.MIME.get(detected_format) if detected_format else None
        if manifest_mime and result["detected_mime"]:
            result["mime_match_manifest"] = manifest_mime == result["detected_mime"].lower()
        result["readable"] = True
    except (OSError, ValueError, UnidentifiedImageError) as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"

    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--expected-count", type=int)
    args = parser.parse_args()

    manifest_path = args.manifest.resolve()
    repo_root = detect_repo_root(manifest_path)
    records = load_records(manifest_path)
    scanned = [scan_record(repo_root, row, index) for index, row in enumerate(records, start=1)]

    page_numbers = [row["page_number"] for row in scanned if isinstance(row.get("page_number"), int)]
    duplicate_page_numbers = sorted(number for number, count in Counter(page_numbers).items() if count > 1)
    sequence_contiguous = False
    missing_page_numbers: list[int] = []
    if page_numbers:
        ordered_unique = sorted(set(page_numbers))
        expected = list(range(ordered_unique[0], ordered_unique[-1] + 1))
        missing_page_numbers = sorted(set(expected) - set(ordered_unique))
        sequence_contiguous = page_numbers == expected

    sha_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in scanned:
        if row.get("actual_sha256"):
            sha_groups[row["actual_sha256"]].append(
                {"ordinal": row["ordinal"], "page_number": row.get("page_number"), "image_file": row.get("image_file")}
            )
    duplicate_sha_groups = [
        {"sha256": sha, "occurrences": occurrences}
        for sha, occurrences in sorted(sha_groups.items())
        if len(occurrences) > 1
    ]

    subject_ids = sorted({str(row["subject_id"]) for row in scanned if row.get("subject_id")})
    subject_names = sorted({str(row["subject_name"]) for row in scanned if row.get("subject_name")})

    summary = {
        "manifest": str(args.manifest),
        "records": len(scanned),
        "expected_count": args.expected_count,
        "expected_count_match": args.expected_count is None or len(scanned) == args.expected_count,
        "page_number_min": min(page_numbers) if page_numbers else None,
        "page_number_max": max(page_numbers) if page_numbers else None,
        "sequence_contiguous_in_manifest_order": sequence_contiguous,
        "missing_page_numbers": missing_page_numbers,
        "duplicate_page_numbers": duplicate_page_numbers,
        "subject_ids": subject_ids,
        "subject_names": subject_names,
        "subject_identity_consistent": len(subject_ids) <= 1 and len(subject_names) <= 1,
        "exists": sum(bool(row["exists"]) for row in scanned),
        "readable": sum(bool(row["readable"]) for row in scanned),
        "bytes_match_manifest": sum(row["bytes_match_manifest"] is True for row in scanned),
        "sha256_match_manifest": sum(row["sha256_match_manifest"] is True for row in scanned),
        "mime_match_manifest": sum(row["mime_match_manifest"] is True for row in scanned),
        "errors": sum(bool(row["error"]) for row in scanned),
        "duplicate_sha_groups": len(duplicate_sha_groups),
        "formats": dict(sorted(Counter(row["detected_format"] or "UNKNOWN" for row in scanned).items())),
        "extensions": dict(sorted(Counter(row["extension"] or "UNKNOWN" for row in scanned).items())),
    }

    report = {
        "scanner": "corpus_media_scan.py",
        "mode": "read_only",
        "summary": summary,
        "duplicate_sha_groups": duplicate_sha_groups,
        "records": scanned,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    hard_fail = any(
        [
            not summary["expected_count_match"],
            summary["errors"] > 0,
            summary["exists"] != len(scanned),
            summary["readable"] != len(scanned),
            summary["bytes_match_manifest"] != len(scanned),
            summary["sha256_match_manifest"] != len(scanned),
            not summary["subject_identity_consistent"],
            not summary["sequence_contiguous_in_manifest_order"],
            bool(summary["missing_page_numbers"]),
            bool(summary["duplicate_page_numbers"]),
        ]
    )
    return 1 if hard_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
