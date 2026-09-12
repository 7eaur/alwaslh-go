#!/usr/bin/env python3
"""Download original public Supabase lesson images from a committed raw pages snapshot.

No API key is needed because only URLs already present in the raw snapshot are fetched.
The source images are stored unchanged and hashed with SHA-256.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from urllib.request import Request, urlopen

MAX_IMAGE_BYTES = 80 * 1024 * 1024
SUPPORTED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
        handle.write(data)
        temp_name = handle.name
    os.replace(temp_name, path)


def fetch_public_image(url: str, expected_project_ref: str) -> tuple[bytes, str]:
    parsed = urlparse(url)
    expected_host = f"{expected_project_ref}.supabase.co"
    if parsed.scheme != "https" or parsed.hostname != expected_host:
        raise RuntimeError(f"Unexpected image host: {url}")
    expected_prefix = "/storage/v1/object/public/lesson_content/"
    if not parsed.path.startswith(expected_prefix):
        raise RuntimeError(f"Unexpected storage path: {url}")

    request = Request(url, headers={"User-Agent": "alwaslh-content-reconstruction/1.0"}, method="GET")
    with urlopen(request, timeout=120) as response:  # noqa: S310 - exact HTTPS host validated above
        content_type = response.headers.get_content_type().lower()
        data = response.read(MAX_IMAGE_BYTES + 1)
    if len(data) > MAX_IMAGE_BYTES:
        raise RuntimeError(f"Image exceeds maximum allowed size: {url}")
    if content_type not in SUPPORTED_IMAGE_TYPES:
        raise RuntimeError(f"Unsupported image content type {content_type}: {url}")
    return data, content_type


def filename_for(page_number: int, page_id: str, content_type: str) -> str:
    return f"{page_number:05d}-{page_id}{SUPPORTED_IMAGE_TYPES[content_type]}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mapping", default="staging/config/legacy-subject-map.json")
    parser.add_argument("--key", required=True)
    parser.add_argument("--raw-root", default="staging/raw/legacy-supabase")
    parser.add_argument("--repo-root", default=".")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    config = read_json(repo_root / args.mapping)
    mapping = config["mappings"].get(args.key)
    if not mapping:
        raise RuntimeError(f"Unknown mapping key: {args.key}")

    subject_id = str(mapping["legacySubjectId"])
    project_ref = str(mapping["legacyProjectRef"])
    raw_root = repo_root / args.raw_root
    subject_root = raw_root / "subjects" / subject_id
    pages = read_json(subject_root / "pages.json")
    if len(pages) != int(mapping["expectedPages"]):
        raise RuntimeError("pages.json does not match mapping expectedPages")

    manifest: list[dict[str, Any]] = []
    anomalies: list[dict[str, Any]] = []
    seen_sha: dict[str, list[str]] = {}

    for page in pages:
        page_id = str(page["id"])
        page_number = page.get("page_number")
        urls = page.get("image_urls")
        if not isinstance(page_number, int) or page_number <= 0:
            anomalies.append({"legacy_page_id": page_id, "reason": "invalid_page_number"})
            continue
        if not isinstance(urls, list) or len(urls) != 1 or not isinstance(urls[0], str):
            anomalies.append(
                {
                    "legacy_page_id": page_id,
                    "page_number": page_number,
                    "reason": "expected_exactly_one_image_url",
                    "observed": urls,
                }
            )
            continue

        data, content_type = fetch_public_image(urls[0], project_ref)
        filename = filename_for(page_number, page_id, content_type)
        relative = Path("subjects") / subject_id / "images" / filename
        destination = raw_root / relative
        checksum = sha256_bytes(data)
        if destination.exists():
            existing = destination.read_bytes()
            if sha256_bytes(existing) != checksum:
                raise RuntimeError(f"Existing raw image differs from source: {destination}")
        else:
            atomic_write(destination, data)
        seen_sha.setdefault(checksum, []).append(page_id)
        manifest.append(
            {
                "legacy_page_id": page_id,
                "page_number": page_number,
                "source_url": urls[0],
                "content_type": content_type,
                "byte_size": len(data),
                "sha256": checksum,
                "raw_path": relative.as_posix(),
            }
        )

    manifest.sort(key=lambda row: (int(row["page_number"]), str(row["legacy_page_id"])))
    write_json(subject_root / "image-manifest.json", manifest)
    write_json(subject_root / "image-anomalies.json", anomalies)
    exact_duplicate_groups = [ids for ids in seen_sha.values() if len(ids) > 1]
    result = {
        "images": len(manifest),
        "anomalies": len(anomalies),
        "unique_sha256": len(seen_sha),
        "exact_duplicate_groups": len(exact_duplicate_groups),
        "exact_duplicate_extra_records": sum(len(ids) - 1 for ids in exact_duplicate_groups),
    }
    if anomalies:
        raise RuntimeError(f"Raw image materialization has {len(anomalies)} anomalies: {json.dumps(result)}")
    if len(manifest) != int(mapping["expectedPages"]):
        raise RuntimeError(f"Image count mismatch: {len(manifest)} != {mapping['expectedPages']}")
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
