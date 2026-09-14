#!/usr/bin/env python3
import argparse
import json
import re
from collections import Counter
from pathlib import Path

from PIL import Image, ImageOps, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
RAW_ROOT = ROOT / "content-staging" / "raw" / "legacy-supabase" / "subjects"
OUT_ROOT = ROOT / "content-staging" / "reconstruction" / "exams" / "source-groups"


def lesson_identity(item):
    path = item.get("storage_object_path") or ""
    match = re.search(r"/lesson/([^/]+)/", path)
    return match.group(1) if match else None


def load_pages(subject_dir):
    payload = json.loads((subject_dir / "pages.json").read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("pages", "records", "items", "data"):
            if isinstance(payload.get(key), list):
                return payload[key]
    return []


def page_meta(page):
    if not isinstance(page, dict):
        return {}
    questions = page.get("ai_questions") or []
    return {
        "id": page.get("id"),
        "page_number": page.get("page_number"),
        "title": page.get("title"),
        "content_type": page.get("content_type"),
        "question_count": len(questions) if isinstance(questions, list) else 0,
    }


def raw_file(item):
    rel = Path(item["raw_path"])
    return ROOT / "content-staging" / rel if rel.parts and rel.parts[0] == "raw" else ROOT / rel


def build_contact_sheet(items, output):
    cards = []
    for item in items:
        path = raw_file(item)
        with Image.open(path) as image:
            image = ImageOps.exif_transpose(image).convert("RGB")
            image.thumbnail((420, 560))
            card = Image.new("RGB", (440, 610), "white")
            card.paste(image, ((440 - image.width) // 2, 10))
            draw = ImageDraw.Draw(card)
            draw.text((10, 580), f"page {item['page_number']} | {lesson_identity(item) or 'no-lesson-id'}", fill="black")
            cards.append(card)
    cols = 4
    rows = (len(cards) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 440, max(1, rows) * 610), "white")
    for index, card in enumerate(cards):
        sheet.paste(card, ((index % cols) * 440, (index // cols) * 610))
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, format="JPEG", quality=88)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject-id", required=True)
    parser.add_argument("--visual-dir")
    args = parser.parse_args()

    subject_dir = RAW_ROOT / args.subject_id
    manifest = json.loads((subject_dir / "manifest.json").read_text(encoding="utf-8"))
    pages = load_pages(subject_dir)
    images = sorted(manifest.get("images") or [], key=lambda x: (x.get("page_number") is None, x.get("page_number")))
    metadata = {m.get("page_number"): m for m in map(page_meta, pages) if m.get("page_number") is not None}

    runs = []
    for item in images:
        identity = lesson_identity(item)
        if not runs or runs[-1]["storage_lesson_id"] != identity:
            runs.append({"storage_lesson_id": identity, "items": [item]})
        else:
            runs[-1]["items"].append(item)

    candidates = []
    selected = []
    for ordinal, run in enumerate(runs, 1):
        nums = [item["page_number"] for item in run["items"]]
        mids = [run["items"][0], run["items"][len(run["items"]) // 2], run["items"][-1]]
        for item in mids:
            if item not in selected:
                selected.append(item)
        candidates.append({
            "candidate_ordinal": ordinal,
            "storage_lesson_id": run["storage_lesson_id"],
            "first_page": nums[0],
            "last_page": nums[-1],
            "page_count": len(nums),
            "page_numbers": nums,
            "metadata_first": metadata.get(nums[0]),
            "metadata_middle": metadata.get(nums[len(nums)//2]),
            "metadata_last": metadata.get(nums[-1]),
            "status": "boundary_candidate_not_yet_individual_exam_model",
        })

    all_numbers = [item["page_number"] for item in images if isinstance(item.get("page_number"), int)]
    title_counts = Counter((m.get("title") or "").strip() for m in metadata.values() if (m.get("title") or "").strip())
    report = {
        "schema_version": 1,
        "source_group_id": args.subject_id,
        "source_group_name": manifest.get("legacy_subject", {}).get("name"),
        "classification": "exam_source_group",
        "counts": manifest.get("counts", {}),
        "page_sequence": {
            "first": min(all_numbers) if all_numbers else None,
            "last": max(all_numbers) if all_numbers else None,
            "count": len(all_numbers),
            "contiguous": all_numbers == list(range(min(all_numbers), max(all_numbers)+1)) if all_numbers else False,
        },
        "storage_lesson_identity_runs": len(runs),
        "boundary_candidates": candidates,
        "page_metadata_records": len(metadata),
        "distinct_page_titles": len(title_counts),
        "page_title_counts": dict(title_counts),
        "individual_exam_models": "NOT VERIFIED",
        "answer_keys": "NOT VERIFIED",
        "raw_mutations": 0,
    }
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    output = OUT_ROOT / f"{args.subject_id}-discovery.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if args.visual_dir:
        visual = ROOT / args.visual_dir
        build_contact_sheet(selected, visual / f"{args.subject_id}-boundary-candidates.jpg")
        (visual / f"{args.subject_id}-boundary-candidates.json").write_text(
            json.dumps(candidates, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    print(json.dumps({
        "source_group_id": args.subject_id,
        "pages": len(images),
        "storage_lesson_identity_runs": len(runs),
        "candidate_ranges": [[c["first_page"], c["last_page"]] for c in candidates],
        "individual_exam_models": "NOT VERIFIED",
        "answer_keys": "NOT VERIFIED",
        "raw_mutations": 0,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
