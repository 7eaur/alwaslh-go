#!/usr/bin/env python3
"""Fast corpus image verification + selective deep-review queue.

Reads every legacy RAW image, verifies bytes against the pinned manifest,
computes lightweight visual fingerprints, and produces low-resolution source
overviews. It does NOT OCR, mutate RAW, infer curriculum boundaries as facts,
or import/publish anything.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFile, ImageOps

ImageFile.LOAD_TRUNCATED_IMAGES = False

BOUNDARY_RE = re.compile(
    r"(?:^|\s)(الوحدة|الدرس|الفصل|الباب|مراجعة|المراجعة|اختبار|امتحان|نموذج\s+إجابة|نموذج\s+اجابة|الإجابات|الاجابات|الحل|"
    r"unit|lesson|chapter|section|revision|review|exam|test|answer\s+key|answers)(?:\s|$)",
    re.IGNORECASE,
)
PAGE_SUFFIX_RE = re.compile(r"[-–—]?\s*(?:الصفحة|page)\s*0*\d+\s*$", re.IGNORECASE)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def dhash(image: Image.Image) -> int:
    gray = ImageOps.grayscale(image).resize((9, 8), Image.Resampling.LANCZOS)
    px = list(gray.getdata())
    value = 0
    for y in range(8):
        row = y * 9
        for x in range(8):
            value = (value << 1) | int(px[row + x] > px[row + x + 1])
    return value


def hamming(a: int | None, b: int | None) -> int | None:
    if a is None or b is None:
        return None
    return (a ^ b).bit_count()


def percentile(values: list[int], q: float) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    idx = min(len(s) - 1, max(0, round((len(s) - 1) * q)))
    return float(s[idx])


def resolve_image(repo_root: Path, staging_root: Path, raw_path: str) -> Path:
    p = Path(raw_path)
    candidates = [repo_root / p, staging_root / p]
    if raw_path.startswith("content-staging/"):
        candidates.insert(0, repo_root / raw_path)
    for c in candidates:
        if c.exists():
            return c
    return candidates[-1]


def clean_boundary_text(page: dict[str, Any], source_name: str) -> str:
    fields = []
    for key in ("extracted_text", "summary", "title"):
        value = page.get(key)
        if isinstance(value, str) and value.strip():
            text = value.strip()
            if key == "title":
                text = PAGE_SUFFIX_RE.sub("", text)
                if source_name and text.strip() == source_name.strip():
                    continue
                if source_name and text.startswith(source_name):
                    text = text[len(source_name):].strip(" -–—:")
            if text:
                fields.append(text)
    return "\n".join(fields)


def make_overview(rows: list[dict[str, Any]], output: Path, title: str) -> None:
    if not rows:
        return
    cols = 10
    tw, th = 120, 170
    label_h = 20
    gap = 6
    rows_n = (len(rows) + cols - 1) // cols
    canvas = Image.new("RGB", (cols * (tw + gap) + gap, rows_n * (th + label_h + gap) + gap + 28), "white")
    draw = ImageDraw.Draw(canvas)
    draw.text((8, 7), title[:120], fill="black")
    for i, row in enumerate(rows):
        r, c = divmod(i, cols)
        x = gap + c * (tw + gap)
        y = 28 + gap + r * (th + label_h + gap)
        try:
            with Image.open(row["resolved_path"]) as im:
                thumb = ImageOps.contain(im.convert("RGB"), (tw, th), Image.Resampling.LANCZOS)
            ox = x + (tw - thumb.width) // 2
            oy = y + (th - thumb.height) // 2
            canvas.paste(thumb, (ox, oy))
        except Exception:
            draw.rectangle((x, y, x + tw - 1, y + th - 1), outline="black")
            draw.text((x + 4, y + 4), "ERROR", fill="black")
        pnum = row.get("page_number")
        draw.text((x + 3, y + th + 2), f"p{pnum} #{i+1}", fill="black")
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, "JPEG", quality=58, optimize=True, progressive=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--staging-root", default="content-staging")
    ap.add_argument("--master", default="content-staging/manifests/MASTER_CONTENT_MANIFEST.json")
    ap.add_argument("--out", default="content-staging/reports/selective-image-analysis")
    args = ap.parse_args()

    repo_root = Path(args.repo_root).resolve()
    staging_root = (repo_root / args.staging_root).resolve()
    master_path = (repo_root / args.master).resolve()
    out = (repo_root / args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    master = json.loads(master_path.read_text(encoding="utf-8"))
    sources = master.get("sources") or []
    expected_total = int((master.get("counts") or {}).get("raw_image_references") or 0)

    all_rows: list[dict[str, Any]] = []
    source_reports: list[dict[str, Any]] = []
    review_queue: list[dict[str, Any]] = []
    actual_sha_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    hard_errors: list[dict[str, Any]] = []

    for src in sources:
        sid = src["id"]
        src_name = (src.get("legacy_source") or {}).get("name") or sid
        classification = src.get("classification") or "unknown"
        manifest_path = repo_root / src["manifest_path"]
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        subject_dir = manifest_path.parent
        pages_path = subject_dir / "pages.json"
        pages = json.loads(pages_path.read_text(encoding="utf-8")) if pages_path.exists() else []
        page_by_id = {str(p.get("id")): p for p in pages if p.get("id")}

        rows: list[dict[str, Any]] = []
        prev_hash: int | None = None
        prev_dims: tuple[int, int] | None = None
        prev_pnum: Any = None

        for index, img in enumerate(manifest.get("images") or []):
            path = resolve_image(repo_root, staging_root, img["raw_path"])
            page = page_by_id.get(str(img.get("legacy_page_id")), {})
            record: dict[str, Any] = {
                "source_id": sid,
                "source_name": src_name,
                "classification": classification,
                "sequence_index": index + 1,
                "legacy_page_id": img.get("legacy_page_id"),
                "page_number": img.get("page_number"),
                "raw_path": img.get("raw_path"),
                "resolved_path": str(path),
                "manifest_byte_size": img.get("byte_size"),
                "manifest_sha256": img.get("sha256"),
                "exists": path.exists(),
                "readable": False,
                "byte_size_match": False,
                "sha256_match": False,
                "format": None,
                "mode": None,
                "width": None,
                "height": None,
                "dhash": None,
                "prev_dhash_distance": None,
                "reasons": [],
            }
            if not path.exists():
                record["reasons"].append("missing_file")
                hard_errors.append(record.copy())
                rows.append(record)
                all_rows.append(record)
                continue

            actual_size = path.stat().st_size
            actual_sha = sha256_file(path)
            record["actual_byte_size"] = actual_size
            record["actual_sha256"] = actual_sha
            record["byte_size_match"] = actual_size == img.get("byte_size")
            record["sha256_match"] = actual_sha == img.get("sha256")
            if not record["byte_size_match"]:
                record["reasons"].append("byte_size_mismatch")
            if not record["sha256_match"]:
                record["reasons"].append("sha256_mismatch")
            actual_sha_groups[actual_sha].append({"source_id": sid, "page_number": img.get("page_number"), "raw_path": img.get("raw_path")})

            try:
                with Image.open(path) as probe:
                    probe.verify()
                with Image.open(path) as im:
                    im.load()
                    record["readable"] = True
                    record["format"] = im.format
                    record["mode"] = im.mode
                    record["width"], record["height"] = im.size
                    hv = dhash(im)
                    record["dhash"] = f"{hv:016x}"
                    record["prev_dhash_distance"] = hamming(prev_hash, hv)
                    dims = im.size
                    if prev_dims is not None and dims != prev_dims:
                        record["reasons"].append("dimension_change")
                    prev_dims = dims
                    prev_hash = hv
            except Exception as exc:
                record["image_error"] = repr(exc)
                record["reasons"].append("unreadable_image")
                hard_errors.append(record.copy())

            pnum = record["page_number"]
            if index == 0:
                record["reasons"].append("source_first")
            if index == len(manifest.get("images") or []) - 1:
                record["reasons"].append("source_last")
            if prev_pnum is not None and isinstance(prev_pnum, int) and isinstance(pnum, int) and pnum != prev_pnum + 1:
                record["reasons"].append("page_number_discontinuity")
            prev_pnum = pnum

            boundary_text = clean_boundary_text(page, src_name)
            if boundary_text and BOUNDARY_RE.search(boundary_text):
                record["reasons"].append("text_boundary_signal")
                record["boundary_text_excerpt"] = boundary_text[:500]

            rows.append(record)
            all_rows.append(record)

        distances = [int(r["prev_dhash_distance"]) for r in rows if r.get("prev_dhash_distance") is not None]
        p90 = percentile(distances, 0.90)
        jump_threshold = max(18.0, p90)
        exam = classification == "exam_collection_candidate"
        for r in rows:
            dist = r.get("prev_dhash_distance")
            if dist is not None and dist >= jump_threshold:
                r["reasons"].append("visual_jump")
            # Sparse guard samples: deep review stays bounded while every image is technically verified.
            if exam and (r["sequence_index"] - 1) % 10 == 0:
                r["reasons"].append("exam_guard_sample")
            if r["reasons"]:
                review_queue.append({k: v for k, v in r.items() if k != "resolved_path"})

        make_overview(rows, out / "overviews" / f"{sid}.jpg", f"{src_name} | {classification} | {len(rows)} pages")
        source_reports.append({
            "source_id": sid,
            "source_name": src_name,
            "classification": classification,
            "images": len(rows),
            "readable": sum(1 for r in rows if r["readable"]),
            "sha256_matches": sum(1 for r in rows if r["sha256_match"]),
            "size_matches": sum(1 for r in rows if r["byte_size_match"]),
            "visual_jump_threshold": jump_threshold,
            "candidate_pages": sum(1 for r in rows if r["reasons"]),
            "overview": f"overviews/{sid}.jpg",
        })

    duplicate_groups = [v for v in actual_sha_groups.values() if len(v) > 1]
    summary = {
        "status": "TECHNICAL_SCAN_COMPLETE" if not hard_errors else "TECHNICAL_SCAN_FAILED",
        "expected_images": expected_total,
        "scanned_images": len(all_rows),
        "existing_images": sum(1 for r in all_rows if r["exists"]),
        "readable_images": sum(1 for r in all_rows if r["readable"]),
        "byte_size_matches": sum(1 for r in all_rows if r["byte_size_match"]),
        "sha256_matches": sum(1 for r in all_rows if r["sha256_match"]),
        "sources": len(source_reports),
        "exam_sources": sum(1 for s in source_reports if s["classification"] == "exam_collection_candidate"),
        "deep_review_candidates": len(review_queue),
        "actual_sha256_duplicate_groups": len(duplicate_groups),
        "hard_errors": len(hard_errors),
        "raw_mutations": 0,
        "imports": 0,
        "publications": 0,
        "notes": [
            "Every image was opened and byte-verified; semantic deep review is selective.",
            "Candidate flags are review hints, not verified Lesson/Unit/Exam boundaries.",
            "No RAW file is written or recompressed by this pipeline.",
        ],
    }

    report = {
        "summary": summary,
        "sources": source_reports,
        "deep_review_queue": review_queue,
        "actual_duplicate_groups": duplicate_groups,
        "hard_errors": hard_errors,
        "images": [{k: v for k, v in r.items() if k != "resolved_path"} for r in all_rows],
    }
    (out / "TECHNICAL_IMAGE_SCAN.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "DEEP_REVIEW_QUEUE.json").write_text(json.dumps(review_queue, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Selective Image Analysis Report",
        "",
        f"Status: `{summary['status']}`",
        "",
        f"- Images: {summary['scanned_images']}/{summary['expected_images']}",
        f"- Readable: {summary['readable_images']}/{summary['expected_images']}",
        f"- SHA-256 matches: {summary['sha256_matches']}/{summary['expected_images']}",
        f"- Byte-size matches: {summary['byte_size_matches']}/{summary['expected_images']}",
        f"- Sources: {summary['sources']}",
        f"- Exam source groups: {summary['exam_sources']}",
        f"- Selective deep-review candidates: {summary['deep_review_candidates']}",
        f"- Actual SHA-256 duplicate groups: {summary['actual_sha256_duplicate_groups']}",
        f"- Hard errors: {summary['hard_errors']}",
        "- RAW mutations: 0",
        "- Imports/Publications: 0/0",
        "",
        "## Method",
        "All RAW images are technically verified. Deep semantic review is intentionally limited to source edges, metadata boundary signals, sequence anomalies, visual change points, dimension changes, and sparse exam guard samples. Overview sheets provide fast visual inspection without pretending candidate flags are verified curriculum/exam boundaries.",
        "",
        "## Source summary",
        "",
        "| Source | Type | Images | Readable | SHA match | Candidates |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for s in source_reports:
        lines.append(f"| {s['source_name']} | {s['classification']} | {s['images']} | {s['readable']} | {s['sha256_matches']} | {s['candidate_pages']} |")
    (out / "SELECTIVE_IMAGE_ANALYSIS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    if len(all_rows) != expected_total or hard_errors or summary["sha256_matches"] != expected_total:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
