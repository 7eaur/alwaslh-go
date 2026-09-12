#!/usr/bin/env python3
"""Derive optimized WebP images from immutable staged raw images.

This tool never overwrites raw source images. It writes WebP derivatives and a
machine-readable optimization report with source/derived SHA-256 checksums.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys
from typing import Any

try:
    from PIL import Image, ImageFile
except ImportError as exc:  # pragma: no cover - environment dependency
    raise SystemExit("Pillow is required: pip install Pillow") from exc

ImageFile.LOAD_TRUNCATED_IMAGES = False
ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW_ROOT = ROOT / "raw" / "legacy-supabase"
DERIVED_ROOT = ROOT / "derived" / "webp"
REPORT_ROOT = ROOT / "reports"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(path: pathlib.Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def optimize_one(raw_path: pathlib.Path, output_path: pathlib.Path, quality: int) -> dict[str, Any]:
    source_bytes = raw_path.read_bytes()
    source_sha = sha256_bytes(source_bytes)
    source_size = len(source_bytes)

    with Image.open(raw_path) as image:
        image.load()
        source_dimensions = image.size
        source_mode = image.mode
        if image.mode not in {"RGB", "RGBA"}:
            if "A" in image.getbands():
                image = image.convert("RGBA")
            else:
                image = image.convert("RGB")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = output_path.with_suffix(".tmp.webp")
        image.save(
            temp_path,
            format="WEBP",
            quality=quality,
            method=6,
            lossless=False,
            exact=True,
        )

    with Image.open(temp_path) as verify:
        verify.load()
        if verify.size != source_dimensions:
            temp_path.unlink(missing_ok=True)
            raise RuntimeError(f"dimension mismatch for {raw_path}")

    optimized_size = temp_path.stat().st_size
    optimized_sha = sha256_file(temp_path)
    temp_path.replace(output_path)
    return {
        "raw_path": str(raw_path.relative_to(ROOT)).replace("\\", "/"),
        "webp_path": str(output_path.relative_to(ROOT)).replace("\\", "/"),
        "source_sha256": source_sha,
        "optimized_sha256": optimized_sha,
        "source_bytes": source_size,
        "optimized_bytes": optimized_size,
        "saved_bytes": source_size - optimized_size,
        "saved_percent": round(((source_size - optimized_size) / source_size) * 100, 2) if source_size else 0,
        "width": source_dimensions[0],
        "height": source_dimensions[1],
        "source_mode": source_mode,
        "quality": quality,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create WebP derivatives without modifying raw staging images")
    parser.add_argument("--subject-id", required=True)
    parser.add_argument("--quality", type=int, default=90)
    parser.add_argument("--min-savings-percent", type=float, default=5.0)
    args = parser.parse_args()
    if not 75 <= args.quality <= 100:
        parser.error("--quality must be between 75 and 100 for textbook readability")

    subject_dir = RAW_ROOT / "subjects" / args.subject_id
    manifest_path = subject_dir / "manifest.json"
    if not manifest_path.exists():
        raise SystemExit(f"missing raw subject manifest: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    images = manifest.get("images")
    if not isinstance(images, list) or not images:
        raise SystemExit("raw manifest contains no images")

    report_rows: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []
    for entry in images:
        raw_rel = entry.get("raw_path")
        page_id = entry.get("legacy_page_id")
        page_number = entry.get("page_number")
        expected_sha = entry.get("sha256")
        if not isinstance(raw_rel, str) or not isinstance(page_id, str) or not isinstance(page_number, int):
            failures.append({"page": str(page_id), "error": "invalid manifest image entry"})
            continue
        raw_path = ROOT / raw_rel
        if not raw_path.exists():
            failures.append({"page": page_id, "error": "raw image missing"})
            continue
        actual_sha = sha256_file(raw_path)
        if actual_sha != expected_sha:
            failures.append({"page": page_id, "error": "raw checksum mismatch"})
            continue

        output_path = DERIVED_ROOT / args.subject_id / f"page-{page_number:05d}-{page_id}.webp"
        try:
            row = optimize_one(raw_path, output_path, args.quality)
            row["legacy_page_id"] = page_id
            row["page_number"] = page_number
            row["accepted"] = row["saved_percent"] >= args.min_savings_percent
            if not row["accepted"]:
                # A larger derivative is not useful; keep the raw source as canonical input.
                output_path.unlink(missing_ok=True)
                row["webp_path"] = None
                row["optimized_sha256"] = None
                row["optimized_bytes"] = None
            report_rows.append(row)
        except Exception as exc:  # noqa: BLE001 - report every image failure
            failures.append({"page": page_id, "error": str(exc)})

    report_rows.sort(key=lambda row: (row["page_number"], row["legacy_page_id"]))
    total_source = sum(int(row["source_bytes"]) for row in report_rows)
    total_optimized = sum(int(row["optimized_bytes"] or row["source_bytes"]) for row in report_rows)
    report = {
        "subject_id": args.subject_id,
        "quality": args.quality,
        "min_savings_percent": args.min_savings_percent,
        "source_images": len(images),
        "processed": len(report_rows),
        "accepted_webp": sum(1 for row in report_rows if row["accepted"]),
        "failures": failures,
        "source_bytes": total_source,
        "effective_bytes": total_optimized,
        "saved_bytes": total_source - total_optimized,
        "saved_percent": round(((total_source - total_optimized) / total_source) * 100, 2) if total_source else 0,
        "images": report_rows,
    }
    write_json(REPORT_ROOT / f"image-optimization-{args.subject_id}.json", report)
    print(json.dumps({key: report[key] for key in ("source_images", "processed", "accepted_webp", "saved_bytes", "saved_percent")}, ensure_ascii=False))
    return 2 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
