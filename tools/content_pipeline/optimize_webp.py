#!/usr/bin/env python3
"""Create web-ready WebP copies for curated pages without modifying raw source images."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import tempfile
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops, ImageOps, ImageStat

QUALITY_CANDIDATES = (90, 88, 85, 82)
MIN_PSNR_DB = 36.0


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def normalized_rgb(image: Image.Image) -> Image.Image:
    image = ImageOps.exif_transpose(image)
    if image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGB")
    if image.mode == "RGBA":
        background = Image.new("RGB", image.size, "white")
        background.paste(image, mask=image.getchannel("A"))
        return background
    return image.convert("RGB")


def psnr(reference: Image.Image, candidate: Image.Image) -> float:
    if reference.size != candidate.size:
        return 0.0
    diff = ImageChops.difference(reference, candidate)
    stats = ImageStat.Stat(diff)
    rms = stats.rms
    mse = sum(value * value for value in rms) / max(len(rms), 1)
    if mse == 0:
        return float("inf")
    return 20.0 * math.log10(255.0 / math.sqrt(mse))


def encode_candidate(reference: Image.Image, quality: int) -> tuple[bytes, float]:
    with tempfile.NamedTemporaryFile(suffix=".webp", delete=True) as temp:
        reference.save(temp.name, format="WEBP", quality=quality, method=6, optimize=True)
        data = Path(temp.name).read_bytes()
        with Image.open(temp.name) as decoded:
            decoded.load()
            decoded_rgb = normalized_rgb(decoded)
            score = psnr(reference, decoded_rgb)
    return data, score


def choose_webp(reference: Image.Image, original_bytes: int) -> tuple[bytes, int, float]:
    accepted: list[tuple[bytes, int, float]] = []
    for quality in QUALITY_CANDIDATES:
        data, score = encode_candidate(reference, quality)
        if score >= MIN_PSNR_DB:
            accepted.append((data, quality, score))
    if not accepted:
        data, score = encode_candidate(reference, 92)
        return data, 92, score

    meaningful = [candidate for candidate in accepted if len(candidate[0]) <= original_bytes * 0.95]
    pool = meaningful or accepted
    return min(pool, key=lambda item: len(item[0]))


def iter_pages_files(document_root: Path) -> list[Path]:
    return sorted(document_root.glob("sections/*/lessons/*/pages.json"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, help="Curated document root")
    parser.add_argument("--raw-root", default="staging/raw/legacy-supabase")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--report", default="staging/reports/image-optimization.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    document_root = (repo_root / args.root).resolve()
    raw_root = (repo_root / args.raw_root).resolve()
    pages_files = iter_pages_files(document_root)
    if not pages_files:
        raise RuntimeError(f"No curated pages.json files below {document_root}")

    report_rows: list[dict[str, Any]] = []
    original_total = 0
    optimized_total = 0

    for pages_file in pages_files:
        pages = read_json(pages_file)
        changed = False
        for page in pages:
            raw_path = raw_root / str(page["raw_image_path"])
            if not raw_path.is_file():
                raise RuntimeError(f"Missing raw image: {raw_path}")
            actual_raw_sha = sha256_file(raw_path)
            if actual_raw_sha != page["raw_image_sha256"]:
                raise RuntimeError(f"Raw SHA-256 mismatch: {raw_path}")

            output_path = repo_root / str(page["optimized_image_path"])
            output_path.parent.mkdir(parents=True, exist_ok=True)
            original_size = raw_path.stat().st_size
            with Image.open(raw_path) as source:
                source.load()
                reference = normalized_rgb(source)
                width, height = reference.size
                data, quality, score = choose_webp(reference, original_size)

            output_path.write_bytes(data)
            with Image.open(output_path) as check:
                check.load()
                if check.format != "WEBP":
                    raise RuntimeError(f"Optimizer did not produce WebP: {output_path}")
                if check.size != (width, height):
                    raise RuntimeError(f"Optimized dimensions changed: {output_path}")

            optimized_sha = sha256_file(output_path)
            page["optimized_image_sha256"] = optimized_sha
            page["optimized_image_bytes"] = len(data)
            page["optimized_image_content_type"] = "image/webp"
            page["optimized_width"] = width
            page["optimized_height"] = height
            page["optimized_quality"] = quality
            page["optimized_psnr_db"] = None if math.isinf(score) else round(score, 3)
            changed = True

            original_total += original_size
            optimized_total += len(data)
            report_rows.append(
                {
                    "legacy_page_id": page["legacy_page_id"],
                    "page_number": page["page_number"],
                    "raw_path": page["raw_image_path"],
                    "raw_sha256": actual_raw_sha,
                    "raw_bytes": original_size,
                    "optimized_path": page["optimized_image_path"],
                    "optimized_sha256": optimized_sha,
                    "optimized_bytes": len(data),
                    "quality": quality,
                    "psnr_db": None if math.isinf(score) else round(score, 3),
                    "width": width,
                    "height": height,
                    "savings_percent": round((1 - len(data) / original_size) * 100, 2) if original_size else 0,
                }
            )
        if changed:
            write_json(pages_file, pages)

    report = {
        "schema_version": 1,
        "document_root": args.root,
        "image_count": len(report_rows),
        "raw_total_bytes": original_total,
        "optimized_total_bytes": optimized_total,
        "savings_bytes": original_total - optimized_total,
        "savings_percent": round((1 - optimized_total / original_total) * 100, 2) if original_total else 0,
        "minimum_psnr_db": MIN_PSNR_DB,
        "images": report_rows,
    }
    write_json(repo_root / args.report, report)
    print(json.dumps({key: report[key] for key in ("image_count", "raw_total_bytes", "optimized_total_bytes", "savings_percent")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
