#!/usr/bin/env python3
import json
from pathlib import Path

SUBJECT_ID = "14ef15e0-5524-473a-bbdb-996df35ba535"
ROOT = Path("content-staging/raw/legacy-supabase/subjects") / SUBJECT_ID
OUT = Path("content-staging/reconstruction/exams/source-groups") / f"{SUBJECT_ID}-anomaly-evidence.json"

pages = json.loads((ROOT / "pages.json").read_text(encoding="utf-8"))
manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))

records = []
for source_index, page in enumerate(pages):
    page_number = page.get("page_number")
    if page_number not in {34, 35, 36, 37}:
        continue
    images = page.get("images") or []
    records.append({
        "source_index": source_index,
        "legacy_page_id": page.get("id"),
        "page_number": page_number,
        "title": page.get("title"),
        "content_type": page.get("content_type"),
        "question_count": len(page.get("ai_questions") or []),
        "image_count": len(images),
        "image_refs": [
            {
                "url": image.get("url") if isinstance(image, dict) else image,
                "path": image.get("path") if isinstance(image, dict) else None,
            }
            for image in images
        ],
    })

manifest_images = []
for source_index, image in enumerate(manifest.get("images", [])):
    if image.get("page_number") in {34, 35, 36, 37}:
        manifest_images.append({
            "manifest_image_index": source_index,
            "legacy_page_id": image.get("legacy_page_id"),
            "page_number": image.get("page_number"),
            "raw_path": image.get("raw_path"),
            "sha256": image.get("sha256"),
            "byte_size": image.get("byte_size"),
            "source_url": image.get("source_url"),
        })

payload = {
    "schema_version": 1,
    "source_group_id": SUBJECT_ID,
    "operation": "source_local_duplicate_page_number_evidence",
    "raw_mutations": 0,
    "manifest_anomaly": {
        "duplicate_page_numbers": manifest.get("anomalies", {}).get("duplicate_page_numbers", []),
        "missing_expected_page_number_from_sequence": 35,
    },
    "page_records_34_37_in_source_order": records,
    "manifest_image_records_34_37_in_manifest_order": manifest_images,
    "interpretation": "NOT VERIFIED — this artifact records identities/order only; model-boundary resolution requires visual evidence plus metadata reconciliation.",
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(payload, ensure_ascii=False, indent=2))
