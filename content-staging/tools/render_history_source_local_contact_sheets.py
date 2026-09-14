from __future__ import annotations

import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SID = "0a76f44b-0a4f-4e36-9ea9-badecf78bf23"
ROOT = Path("content-staging/raw/legacy-supabase/subjects") / SID
MANIFEST = ROOT / "manifest.json"
OUT = Path("_artifacts/history-source-local")
INDEX = Path("content-staging/reconstruction/educational") / f"{SID}-visual-index.json"


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    images = sorted(manifest["images"], key=lambda x: (x["page_number"], x["legacy_page_id"], x.get("image_index", 0)))
    assert len(images) == 61
    assert [x["page_number"] for x in images] == list(range(8, 69))

    OUT.mkdir(parents=True, exist_ok=True)
    thumb_w, thumb_h = 424, 600
    label_h = 52
    cols, rows = 4, 3
    sheet_w, sheet_h = cols * thumb_w, rows * (thumb_h + label_h)
    font = ImageFont.load_default()
    sheets = []

    for batch_index in range(0, len(images), cols * rows):
        batch = images[batch_index:batch_index + cols * rows]
        canvas = Image.new("RGB", (sheet_w, sheet_h), "white")
        draw = ImageDraw.Draw(canvas)
        page_numbers = []
        for i, rec in enumerate(batch):
            p = Path("content-staging") / rec["raw_path"]
            with Image.open(p) as im:
                im = im.convert("RGB")
                im.thumbnail((thumb_w, thumb_h))
                x = (i % cols) * thumb_w + (thumb_w - im.width) // 2
                y0 = (i // cols) * (thumb_h + label_h)
                y = y0 + (thumb_h - im.height) // 2
                canvas.paste(im, (x, y))
            page_numbers.append(rec["page_number"])
            label = f"stored {rec['page_number']} | {rec['legacy_page_id'][:8]} | q={sum(1 for q in manifest.get('questions', []) if q.get('legacy_page_id') == rec['legacy_page_id'])}"
            draw.text(((i % cols) * thumb_w + 8, y0 + thumb_h + 8), label, fill="black", font=font)

        lo, hi = page_numbers[0], page_numbers[-1]
        name = f"history-source-pages-{lo:03d}-{hi:03d}.jpg"
        path = OUT / name
        canvas.save(path, "JPEG", quality=88, optimize=True)
        sheets.append({"file": name, "stored_pages": page_numbers})

    index = {
        "schema_version": 1,
        "operation": "source_local_visual_evidence_render",
        "subject_id": SID,
        "authority": "immutable RAW pages only",
        "raw_image_count": 61,
        "stored_page_range": [8, 68],
        "contact_sheet_count": len(sheets),
        "sheets": sheets,
        "raw_mutations": 0,
        "semantic_boundaries": "NOT VERIFIED",
        "note": "Rendering only. This file does not infer book/unit/lesson/review boundaries. Human visual inspection is required before semantic reconstruction."
    }
    INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(index, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
