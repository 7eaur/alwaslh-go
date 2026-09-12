#!/usr/bin/env python3
"""Extract immutable educational source records from the legacy Supabase project.

The extractor never writes to Supabase. It stores source rows as JSON, downloads the
referenced public lesson images without modifying them, and records SHA-256 provenance.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlencode, urlparse
from urllib.request import Request, urlopen

PAGE_SIZE = 1000
MAX_IMAGE_BYTES = 80 * 1024 * 1024
SUPPORTED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def atomic_write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
        handle.write(data)
        temp_name = handle.name
    os.replace(temp_name, path)


def write_json(path: Path, value: Any) -> str:
    data = (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    atomic_write_bytes(path, data)
    return sha256_bytes(data)


class LegacySupabaseReader:
    def __init__(self, base_url: str, publishable_key: str) -> None:
        parsed = urlparse(base_url)
        if parsed.scheme != "https" or not parsed.hostname or not parsed.hostname.endswith(".supabase.co"):
            raise ValueError("LEGACY_SUPABASE_URL must be an https://*.supabase.co URL")
        self.base_url = base_url.rstrip("/")
        self.hostname = parsed.hostname
        self.key = publishable_key.strip()
        if not self.key:
            raise ValueError("LEGACY_SUPABASE_PUBLISHABLE_KEY is empty")

    def _request_json(self, url: str) -> list[dict[str, Any]]:
        request = Request(
            url,
            headers={
                "apikey": self.key,
                "Authorization": f"Bearer {self.key}",
                "Accept": "application/json",
                "User-Agent": "alwaslh-content-reconstruction/1.0",
            },
            method="GET",
        )
        with urlopen(request, timeout=60) as response:  # noqa: S310 - validated HTTPS host
            payload = response.read()
        value = json.loads(payload)
        if not isinstance(value, list):
            raise RuntimeError(f"Unexpected PostgREST response from {url}")
        return value

    def table(
        self,
        table: str,
        *,
        filters: list[tuple[str, str]] | None = None,
        order: str = "id.asc",
    ) -> list[dict[str, Any]]:
        if table not in {"classes", "subjects", "subject_extra_classes", "lessons", "quizzes", "saved_questions"}:
            raise ValueError(f"Unsupported source table: {table}")
        output: list[dict[str, Any]] = []
        offset = 0
        while True:
            params: list[tuple[str, str]] = [("select", "*"), ("order", order), ("limit", str(PAGE_SIZE)), ("offset", str(offset))]
            if filters:
                params.extend(filters)
            url = f"{self.base_url}/rest/v1/{quote(table)}?{urlencode(params)}"
            rows = self._request_json(url)
            output.extend(rows)
            if len(rows) < PAGE_SIZE:
                return output
            offset += len(rows)

    def image(self, source_url: str) -> tuple[bytes, str]:
        parsed = urlparse(source_url)
        if parsed.scheme != "https" or parsed.hostname != self.hostname:
            raise ValueError(f"Image URL is outside the legacy Supabase host: {source_url}")
        expected_prefix = "/storage/v1/object/public/lesson_content/"
        if not parsed.path.startswith(expected_prefix):
            raise ValueError(f"Image URL is outside lesson_content public bucket: {source_url}")
        request = Request(source_url, headers={"User-Agent": "alwaslh-content-reconstruction/1.0"}, method="GET")
        with urlopen(request, timeout=120) as response:  # noqa: S310 - validated HTTPS host
            content_type = response.headers.get_content_type().lower()
            data = response.read(MAX_IMAGE_BYTES + 1)
        if len(data) > MAX_IMAGE_BYTES:
            raise ValueError(f"Image exceeds {MAX_IMAGE_BYTES} bytes: {source_url}")
        if content_type not in SUPPORTED_IMAGE_TYPES:
            raise ValueError(f"Unsupported image content type {content_type}: {source_url}")
        return data, content_type


def page_sort_key(row: dict[str, Any]) -> tuple[int, str, str]:
    number = row.get("page_number")
    return (
        int(number) if isinstance(number, int) else 2**31 - 1,
        str(row.get("created_at") or ""),
        str(row.get("id") or ""),
    )


def image_filename(page: dict[str, Any], content_type: str) -> str:
    page_number = page.get("page_number")
    prefix = f"{page_number:05d}" if isinstance(page_number, int) else "unknown"
    page_id = str(page.get("id"))
    return f"{prefix}-{page_id}{SUPPORTED_IMAGE_TYPES[content_type]}"


def question_rows(pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for page in pages:
        questions = page.get("ai_questions")
        if not isinstance(questions, list):
            continue
        for ordinal, question in enumerate(questions):
            output.append(
                {
                    "legacy_page_id": page.get("id"),
                    "legacy_subject_id": page.get("subject_id"),
                    "page_number": page.get("page_number"),
                    "ordinal": ordinal,
                    "raw": question,
                }
            )
    return output


def extract_subject(
    client: LegacySupabaseReader,
    output_root: Path,
    subject: dict[str, Any],
    *,
    download_images: bool,
) -> dict[str, Any]:
    subject_id = str(subject["id"])
    subject_root = output_root / "subjects" / subject_id
    pages = client.table(
        "lessons",
        filters=[("subject_id", f"eq.{subject_id}")],
        order="page_number.asc.nullslast,created_at.asc,id.asc",
    )
    pages.sort(key=page_sort_key)
    questions = question_rows(pages)

    files: dict[str, str] = {}
    files["subject.json"] = write_json(subject_root / "subject.json", subject)
    files["pages.json"] = write_json(subject_root / "pages.json", pages)
    files["questions.json"] = write_json(subject_root / "questions.json", questions)

    image_manifest: list[dict[str, Any]] = []
    image_anomalies: list[dict[str, Any]] = []
    if download_images:
        for page in pages:
            urls = page.get("image_urls")
            if not isinstance(urls, list) or len(urls) != 1 or not isinstance(urls[0], str):
                image_anomalies.append(
                    {
                        "legacy_page_id": page.get("id"),
                        "page_number": page.get("page_number"),
                        "reason": "expected_exactly_one_image_url",
                        "observed": urls,
                    }
                )
                continue
            source_url = urls[0]
            data, content_type = client.image(source_url)
            filename = image_filename(page, content_type)
            relative = Path("subjects") / subject_id / "images" / filename
            path = output_root / relative
            atomic_write_bytes(path, data)
            image_manifest.append(
                {
                    "legacy_page_id": page.get("id"),
                    "page_number": page.get("page_number"),
                    "source_url": source_url,
                    "content_type": content_type,
                    "byte_size": len(data),
                    "sha256": sha256_bytes(data),
                    "raw_path": relative.as_posix(),
                }
            )

    files["image-manifest.json"] = write_json(subject_root / "image-manifest.json", image_manifest)
    files["image-anomalies.json"] = write_json(subject_root / "image-anomalies.json", image_anomalies)

    return {
        "legacy_subject_id": subject_id,
        "legacy_subject_name": subject.get("name"),
        "page_count": len(pages),
        "question_count": len(questions),
        "downloaded_image_count": len(image_manifest),
        "image_anomaly_count": len(image_anomalies),
        "files": files,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="staging/raw/legacy-supabase")
    parser.add_argument("--subject-id", action="append", dest="subject_ids", help="Repeat to export selected subjects. Omit to export all subjects.")
    parser.add_argument("--download-images", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    url = os.environ.get("LEGACY_SUPABASE_URL", "").strip()
    key = os.environ.get("LEGACY_SUPABASE_PUBLISHABLE_KEY", "").strip()
    if not url or not key:
        print("LEGACY_SUPABASE_URL and LEGACY_SUPABASE_PUBLISHABLE_KEY are required", file=sys.stderr)
        return 2

    output_root = Path(args.output).resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    client = LegacySupabaseReader(url, key)

    classes = client.table("classes", order="name.asc,id.asc")
    subjects = client.table("subjects", order="class_id.asc,name.asc,id.asc")
    subject_extra_classes = client.table("subject_extra_classes", order="subject_id.asc,class_id.asc")
    quizzes = client.table("quizzes", order="subject_id.asc,id.asc")
    saved_questions = client.table("saved_questions", order="lesson_id.asc,id.asc")

    global_files = {
        "classes.json": write_json(output_root / "classes.json", classes),
        "subjects.json": write_json(output_root / "subjects.json", subjects),
        "subject_extra_classes.json": write_json(output_root / "subject_extra_classes.json", subject_extra_classes),
        "quizzes.json": write_json(output_root / "quizzes.json", quizzes),
        "saved_questions.json": write_json(output_root / "saved_questions.json", saved_questions),
    }

    selected = set(args.subject_ids or [])
    unknown = selected - {str(subject.get("id")) for subject in subjects}
    if unknown:
        raise RuntimeError(f"Unknown legacy subject ids: {sorted(unknown)}")
    subject_rows = [subject for subject in subjects if not selected or str(subject.get("id")) in selected]

    subject_exports = [
        extract_subject(client, output_root, subject, download_images=args.download_images)
        for subject in subject_rows
    ]
    manifest = {
        "schema_version": 1,
        "source": {
            "kind": "legacy_supabase",
            "project_ref": urlparse(url).hostname.split(".")[0] if urlparse(url).hostname else None,
            "base_url": url,
        },
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "scope": "all_subjects" if not selected else "selected_subjects",
        "download_images": bool(args.download_images),
        "counts": {
            "classes": len(classes),
            "subjects": len(subjects),
            "subject_extra_classes": len(subject_extra_classes),
            "quizzes": len(quizzes),
            "saved_questions": len(saved_questions),
            "exported_subjects": len(subject_exports),
            "pages": sum(row["page_count"] for row in subject_exports),
            "questions": sum(row["question_count"] for row in subject_exports),
            "images": sum(row["downloaded_image_count"] for row in subject_exports),
        },
        "global_files": global_files,
        "subjects": subject_exports,
    }
    digest = sha256_bytes(canonical_json(manifest))
    manifest["manifest_sha256"] = digest
    write_json(output_root / "export-manifest.json", manifest)
    print(json.dumps({"manifest_sha256": digest, **manifest["counts"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
