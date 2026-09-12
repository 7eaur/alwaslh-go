#!/usr/bin/env python3
"""Read-only extractor for Alwaslh legacy Supabase educational content.

The extractor never mutates Supabase. It exports database records and referenced
public lesson images into content-staging/raw/legacy-supabase with SHA-256
provenance. Raw outputs are immutable source evidence: structural anomalies are
recorded, not silently repaired and not used to discard source rows.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import mimetypes
import os
import pathlib
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from dataclasses import dataclass
from typing import Any, Iterable

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW_ROOT = ROOT / "raw" / "legacy-supabase"
PAGE_SIZE = 500
MAX_IMAGE_BYTES = 60 * 1024 * 1024
IMAGE_WORKERS = 6


class ExtractionError(RuntimeError):
    pass


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_json(value: Any) -> str:
    return sha256_bytes(canonical_json(value).encode("utf-8"))


def write_json(path: pathlib.Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(payload, encoding="utf-8")
    tmp.replace(path)


def require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ExtractionError(f"missing environment variable: {name}")
    return value


@dataclass(frozen=True)
class LegacyClient:
    base_url: str
    api_key: str

    @classmethod
    def from_env(cls) -> "LegacyClient":
        base_url = require_env("LEGACY_SUPABASE_URL").rstrip("/")
        parsed = urllib.parse.urlparse(base_url)
        if parsed.scheme != "https" or not parsed.hostname or not parsed.hostname.endswith(".supabase.co"):
            raise ExtractionError("LEGACY_SUPABASE_URL must be an https://*.supabase.co URL")
        return cls(base_url=base_url, api_key=require_env("LEGACY_SUPABASE_PUBLISHABLE_KEY"))

    def _request_json(self, url: str) -> Any:
        request = urllib.request.Request(
            url,
            headers={
                "apikey": self.api_key,
                "Authorization": f"Bearer {self.api_key}",
                "Accept": "application/json",
                "User-Agent": "alwaslh-content-staging/1.0",
            },
            method="GET",
        )
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                return json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as exc:
            raise ExtractionError(f"legacy request failed: {url}: {exc}") from exc

    def table_rows(
        self,
        table: str,
        select: str,
        filters: dict[str, str] | None = None,
        order: str | None = None,
    ) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        offset = 0
        while True:
            query: dict[str, str] = {
                "select": select,
                "limit": str(PAGE_SIZE),
                "offset": str(offset),
            }
            if filters:
                query.update(filters)
            if order:
                query["order"] = order
            url = f"{self.base_url}/rest/v1/{urllib.parse.quote(table)}?{urllib.parse.urlencode(query, safe='(),.*:')}"
            batch = self._request_json(url)
            if not isinstance(batch, list):
                raise ExtractionError(f"unexpected PostgREST response for {table}")
            rows.extend(batch)
            if len(batch) < PAGE_SIZE:
                return rows
            offset += len(batch)

    def download_public_storage(self, source_url: str) -> tuple[bytes, str]:
        parsed = urllib.parse.urlparse(source_url)
        base = urllib.parse.urlparse(self.base_url)
        if parsed.scheme != "https" or parsed.hostname != base.hostname:
            raise ExtractionError(f"image URL is outside legacy Supabase host: {source_url}")
        marker = "/storage/v1/object/public/lesson_content/"
        if marker not in parsed.path:
            raise ExtractionError(f"image URL is outside lesson_content public bucket: {source_url}")
        request = urllib.request.Request(
            source_url,
            headers={"User-Agent": "alwaslh-content-staging/1.0"},
            method="GET",
        )
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                data = response.read(MAX_IMAGE_BYTES + 1)
                mime = response.headers.get_content_type()
        except (urllib.error.URLError, urllib.error.HTTPError) as exc:
            raise ExtractionError(f"image download failed: {source_url}: {exc}") from exc
        if not data or len(data) > MAX_IMAGE_BYTES:
            raise ExtractionError(f"invalid image size for {source_url}: {len(data)}")
        if mime not in {"image/jpeg", "image/png", "image/webp"}:
            guessed, _ = mimetypes.guess_type(parsed.path)
            mime = guessed or mime
        if mime not in {"image/jpeg", "image/png", "image/webp"}:
            raise ExtractionError(f"unsupported image mime {mime}: {source_url}")
        return data, mime


def image_extension(mime: str) -> str:
    return {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}[mime]


def image_object_path(source_url: str) -> str:
    parsed = urllib.parse.urlparse(source_url)
    marker = "/storage/v1/object/public/lesson_content/"
    return urllib.parse.unquote(parsed.path.split(marker, 1)[1])


def page_anomalies(pages: list[dict[str, Any]], subject_id: str) -> dict[str, Any]:
    null_page_numbers: list[str] = []
    invalid_subject_ids: list[str] = []
    missing_images: list[str] = []
    multiple_images: list[str] = []
    malformed_image_urls: list[str] = []
    malformed_questions: list[str] = []
    numeric_positions: list[int] = []

    for row in pages:
        row_id = str(row.get("id"))
        if row.get("subject_id") != subject_id:
            invalid_subject_ids.append(row_id)
        page_number = row.get("page_number")
        if isinstance(page_number, int) and page_number > 0:
            numeric_positions.append(page_number)
        else:
            null_page_numbers.append(row_id)
        urls = row.get("image_urls")
        if not isinstance(urls, list):
            malformed_image_urls.append(row_id)
        else:
            valid_urls = [url for url in urls if isinstance(url, str) and url.strip()]
            if len(valid_urls) == 0:
                missing_images.append(row_id)
            if len(valid_urls) > 1:
                multiple_images.append(row_id)
            if len(valid_urls) != len(urls):
                malformed_image_urls.append(row_id)
        if not isinstance(row.get("ai_questions"), list):
            malformed_questions.append(row_id)

    counts = Counter(numeric_positions)
    duplicate_page_numbers = sorted(number for number, count in counts.items() if count > 1)
    return {
        "null_or_invalid_page_numbers": null_page_numbers,
        "duplicate_page_numbers": duplicate_page_numbers,
        "invalid_subject_ids": invalid_subject_ids,
        "missing_images": missing_images,
        "multiple_images": multiple_images,
        "malformed_image_urls": malformed_image_urls,
        "malformed_ai_questions": malformed_questions,
    }


def extract_inventory(client: LegacyClient) -> dict[str, Any]:
    classes = client.table_rows("classes", "id,name,created_at", order="name.asc,id.asc")
    subjects = client.table_rows("subjects", "id,name,class_id,created_at", order="class_id.asc,name.asc,id.asc")
    links = client.table_rows("subject_extra_classes", "subject_id,class_id", order="subject_id.asc,class_id.asc")
    inventory = {
        "source": client.base_url,
        "classes": classes,
        "subjects": subjects,
        "subject_extra_classes": links,
        "counts": {
            "classes": len(classes),
            "subjects": len(subjects),
            "subject_extra_classes": len(links),
        },
    }
    inventory["sha256"] = sha256_json(inventory)
    write_json(RAW_ROOT / "inventory" / "inventory.json", inventory)
    return inventory


def _save_image(
    page: dict[str, Any], image_index: int, source_url: str, subject_dir: pathlib.Path, client: LegacyClient
) -> dict[str, Any]:
    data, mime = client.download_public_storage(source_url)
    digest = sha256_bytes(data)
    ext = image_extension(mime)
    page_number = page.get("page_number")
    page_label = f"{page_number:05d}" if isinstance(page_number, int) and page_number > 0 else "unknown"
    filename = f"page-{page_label}-{page['id']}-image-{image_index:02d}{ext}"
    image_path = subject_dir / "images" / filename
    image_path.parent.mkdir(parents=True, exist_ok=True)

    if image_path.exists():
        existing = image_path.read_bytes()
        if sha256_bytes(existing) != digest:
            raise ExtractionError(f"existing raw image checksum mismatch: {image_path}")
    else:
        with tempfile.NamedTemporaryFile(dir=image_path.parent, delete=False) as temp:
            temp.write(data)
            temp_path = pathlib.Path(temp.name)
        temp_path.replace(image_path)

    return {
        "legacy_page_id": page["id"],
        "page_number": page_number,
        "image_index": image_index,
        "source_url": source_url,
        "storage_bucket": "lesson_content",
        "storage_object_path": image_object_path(source_url),
        "raw_path": str(image_path.relative_to(ROOT)).replace("\\", "/"),
        "mime_type": mime,
        "byte_size": len(data),
        "sha256": digest,
    }


def extract_subject(client: LegacyClient, subject_id: str) -> dict[str, Any]:
    subjects = client.table_rows(
        "subjects",
        "id,name,class_id,created_at",
        filters={"id": f"eq.{subject_id}"},
    )
    if len(subjects) != 1:
        raise ExtractionError(f"legacy subject not found or ambiguous: {subject_id}")
    subject = subjects[0]
    classes = client.table_rows(
        "classes",
        "id,name,created_at",
        filters={"id": f"eq.{subject['class_id']}"},
    )
    if len(classes) != 1:
        raise ExtractionError(f"legacy class not found for subject: {subject_id}")
    legacy_class = classes[0]

    pages = client.table_rows(
        "lessons",
        "id,subject_id,title,image_urls,summary,ai_questions,page_number,created_at,extracted_text,audio_url,ai_thumbnails,content_type",
        filters={"subject_id": f"eq.{subject_id}"},
        order="page_number.asc,created_at.asc,id.asc",
    )

    subject_dir = RAW_ROOT / "subjects" / subject_id
    write_json(subject_dir / "subject.json", {"class": legacy_class, "subject": subject})
    write_json(subject_dir / "pages.json", pages)

    anomalies = page_anomalies(pages, subject_id)
    image_tasks: list[tuple[dict[str, Any], int, str]] = []
    for page in pages:
        urls = page.get("image_urls")
        if not isinstance(urls, list):
            continue
        for image_index, source_url in enumerate(urls):
            if isinstance(source_url, str) and source_url.strip():
                image_tasks.append((page, image_index, source_url))

    images: list[dict[str, Any]] = []
    image_failures: list[dict[str, Any]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=IMAGE_WORKERS) as pool:
        future_map = {
            pool.submit(_save_image, page, image_index, source_url, subject_dir, client): (
                str(page.get("id")), image_index, source_url
            )
            for page, image_index, source_url in image_tasks
        }
        for future in concurrent.futures.as_completed(future_map):
            page_id, image_index, source_url = future_map[future]
            try:
                images.append(future.result())
            except Exception as exc:  # preserve raw DB rows and report binary retrieval failures separately
                image_failures.append(
                    {
                        "legacy_page_id": page_id,
                        "image_index": image_index,
                        "source_url": source_url,
                        "error": str(exc),
                    }
                )
    images.sort(
        key=lambda row: (
            row["page_number"] if isinstance(row["page_number"], int) else 2**31 - 1,
            row["legacy_page_id"],
            row["image_index"],
        )
    )

    question_count = sum(
        len(page["ai_questions"]) for page in pages if isinstance(page.get("ai_questions"), list)
    )
    manifest = {
        "source": {
            "project_url": client.base_url,
            "table": "public.lessons",
            "storage_bucket": "lesson_content",
        },
        "legacy_class": legacy_class,
        "legacy_subject": subject,
        "status": "empty" if not pages else "extracted",
        "counts": {
            "pages": len(pages),
            "image_references": len(image_tasks),
            "images_downloaded": len(images),
            "image_download_failures": len(image_failures),
            "questions": question_count,
        },
        "anomalies": anomalies,
        "image_download_failures": image_failures,
        "pages_sha256": sha256_json(pages),
        "images": images,
    }
    manifest["manifest_sha256"] = sha256_json(manifest)
    write_json(subject_dir / "manifest.json", manifest)
    return manifest


def subject_ids_from_inventory(inventory: dict[str, Any]) -> Iterable[str]:
    for subject in inventory["subjects"]:
        value = subject.get("id")
        if isinstance(value, str) and value:
            yield value


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract legacy Alwaslh content without mutating the source")
    parser.add_argument("--subject-id", help="Extract exactly one legacy subject UUID")
    parser.add_argument("--all", action="store_true", help="Extract every legacy subject, including empty subjects")
    parser.add_argument("--inventory-only", action="store_true", help="Export classes/subjects inventory only")
    args = parser.parse_args()
    if sum(bool(value) for value in (args.subject_id, args.all, args.inventory_only)) != 1:
        parser.error("choose exactly one of --subject-id, --all, or --inventory-only")

    client = LegacyClient.from_env()
    inventory = extract_inventory(client)
    if args.inventory_only:
        print(json.dumps(inventory["counts"], ensure_ascii=False))
        return 0

    subject_ids = [args.subject_id] if args.subject_id else list(subject_ids_from_inventory(inventory))
    failures: list[dict[str, str]] = []
    completed: list[dict[str, Any]] = []
    for subject_id in subject_ids:
        assert subject_id is not None
        try:
            manifest = extract_subject(client, subject_id)
            completed.append(
                {
                    "subject_id": subject_id,
                    "status": manifest["status"],
                    "counts": manifest["counts"],
                    "anomalies": manifest["anomalies"],
                    "manifest_sha256": manifest["manifest_sha256"],
                }
            )
            print(f"extracted {subject_id}: {manifest['counts']}")
        except ExtractionError as exc:
            failures.append({"subject_id": subject_id, "error": str(exc)})
            print(f"blocked {subject_id}: {exc}", file=sys.stderr)
            if args.subject_id:
                raise

    write_json(RAW_ROOT / "extraction-summary.json", {"completed": completed, "blocked": failures})
    if failures:
        print(f"completed={len(completed)} blocked={len(failures)}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
