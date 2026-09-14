#!/usr/bin/env python3
import argparse
import hashlib
import json
import mimetypes
from collections import Counter, defaultdict
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
RAW_ROOT = ROOT / "content-staging" / "raw" / "legacy-supabase" / "subjects"
OUT_ROOT = ROOT / "content-staging" / "reconstruction" / "technical"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_raw_path(raw_path: str) -> Path:
    path = Path(raw_path)
    if path.parts and path.parts[0] == "raw":
        return ROOT / "content-staging" / path
    if path.parts and path.parts[0] == "content-staging":
        return ROOT / path
    return ROOT / "content-staging" / path


def load_pages(subject_dir: Path):
    path = subject_dir / "pages.json"
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("pages", "data", "records", "items"):
            value = data.get(key)
            if isinstance(value, list):
                return value
    return []


def candidate_title(page):
    if not isinstance(page, dict):
        return None
    for key in ("title", "lesson_title", "name", "page_title"):
        value = page.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    lesson = page.get("lesson")
    if isinstance(lesson, dict):
        for key in ("title", "name"):
            value = lesson.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    return None


def candidate_page_number(page):
    if not isinstance(page, dict):
        return None
    for key in ("page_number", "number", "page"):
        value = page.get(key)
        if isinstance(value, int):
            return value
        if isinstance(value, str) and value.isdigit():
            return int(value)
    return None


def verify_subject(subject_id: str) -> dict:
    subject_dir = RAW_ROOT / subject_id
    manifest_path = subject_dir / "manifest.json"
    if not manifest_path.exists():
        raise SystemExit(f"missing manifest: {manifest_path}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    images = manifest.get("images") or []
    records = []
    page_numbers = []
    actual_sha_groups = defaultdict(list)
    failures = []

    for index, item in enumerate(images):
        raw_path = item.get("raw_path")
        page_number = item.get("page_number")
        path = resolve_raw_path(raw_path or "")
        record = {
            "index": index,
            "page_number": page_number,
            "legacy_page_id": item.get("legacy_page_id"),
            "raw_path": raw_path,
            "manifest_byte_size": item.get("byte_size"),
            "manifest_sha256": item.get("sha256"),
            "manifest_mime_type": item.get("mime_type"),
            "exists": path.is_file(),
        }
        if isinstance(page_number, int):
            page_numbers.append(page_number)
        if not path.is_file():
            record.update({"readable": False, "error": "missing_file"})
            failures.append(record)
            records.append(record)
            continue

        actual_size = path.stat().st_size
        actual_sha = sha256_file(path)
        guessed_mime = mimetypes.guess_type(path.name)[0]
        actual_sha_groups[actual_sha].append(raw_path)
        record.update({
            "actual_byte_size": actual_size,
            "byte_size_match": actual_size == item.get("byte_size"),
            "actual_sha256": actual_sha,
            "sha256_match": actual_sha == item.get("sha256"),
            "extension": path.suffix.lower(),
            "guessed_mime_type": guessed_mime,
        })
        try:
            with Image.open(path) as image:
                image.verify()
            with Image.open(path) as image:
                width, height = image.size
                image_format = image.format
                pil_mime = Image.MIME.get(image_format)
            record.update({
                "readable": True,
                "width": width,
                "height": height,
                "image_format": image_format,
                "pil_mime_type": pil_mime,
                "mime_matches_manifest": pil_mime == item.get("mime_type"),
            })
        except Exception as exc:
            record.update({"readable": False, "error": f"{type(exc).__name__}: {exc}"})
            failures.append(record)
        records.append(record)

    page_counter = Counter(page_numbers)
    unique_pages = sorted(page_counter)
    missing_sequence = []
    if unique_pages:
        missing_sequence = sorted(set(range(unique_pages[0], unique_pages[-1] + 1)) - set(unique_pages))
    duplicate_page_numbers = sorted(number for number, count in page_counter.items() if count > 1)

    duplicate_sha_groups = [
        {"sha256": sha, "count": len(paths), "raw_paths": paths}
        for sha, paths in sorted(actual_sha_groups.items()) if len(paths) > 1
    ]

    pages = load_pages(subject_dir)
    title_candidates = []
    previous = object()
    for page in pages:
        title = candidate_title(page)
        if title and title != previous:
            title_candidates.append({"page_number": candidate_page_number(page), "title": title})
        if title:
            previous = title

    checks = {
        "manifest_image_count": len(images),
        "existing_files": sum(1 for record in records if record["exists"]),
        "readable_images": sum(1 for record in records if record.get("readable")),
        "sha256_matches": sum(1 for record in records if record.get("sha256_match")),
        "byte_size_matches": sum(1 for record in records if record.get("byte_size_match")),
        "mime_matches": sum(1 for record in records if record.get("mime_matches_manifest")),
        "failures": len(failures),
    }
    all_verified = bool(images) and all(
        record.get("exists")
        and record.get("readable")
        and record.get("sha256_match")
        and record.get("byte_size_match")
        and record.get("mime_matches_manifest")
        for record in records
    )

    sample_indexes = sorted(set(i for i in (0, len(records) // 2, len(records) - 1) if 0 <= i < len(records)))
    report = {
        "schema_version": 1,
        "operation": "non_destructive_media_verification",
        "subject_id": subject_id,
        "manifest_path": str(manifest_path.relative_to(ROOT)).replace("\\", "/"),
        "manifest_sha256": sha256_file(manifest_path),
        "source_counts": manifest.get("counts", {}),
        "checks": checks,
        "all_images_technically_verified": all_verified,
        "page_sequence": {
            "first_page_number": unique_pages[0] if unique_pages else None,
            "last_page_number": unique_pages[-1] if unique_pages else None,
            "unique_page_numbers": len(unique_pages),
            "missing_page_numbers": missing_sequence,
            "duplicate_page_numbers": duplicate_page_numbers,
        },
        "duplicate_sha256_groups_within_subject": duplicate_sha_groups,
        "metadata_boundary_candidates": title_candidates,
        "samples": [records[i] for i in sample_indexes],
        "failures": failures,
        "records": records,
        "raw_mutations": 0,
    }
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject-id", required=True)
    args = parser.parse_args()
    report = verify_subject(args.subject_id)
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    output = OUT_ROOT / f"{args.subject_id}.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "subject_id": args.subject_id,
        "output": str(output.relative_to(ROOT)),
        "checks": report["checks"],
        "page_sequence": report["page_sequence"],
        "all_images_technically_verified": report["all_images_technically_verified"],
        "boundary_candidate_count": len(report["metadata_boundary_candidates"]),
        "duplicate_sha_groups": len(report["duplicate_sha256_groups_within_subject"]),
    }, ensure_ascii=False))
    if not report["all_images_technically_verified"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
