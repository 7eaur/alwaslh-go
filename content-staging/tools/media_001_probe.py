from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from PIL import Image, ImageChops, ImageStat, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "content-staging" / "runtime" / "media-001"
OUT.mkdir(parents=True, exist_ok=True)

PAGES = [
    {
        "book_page": 5,
        "source_page": 9,
        "legacy_page_id": "706771c2-2145-4682-9bdd-4e7df5c69bf9",
        "expected_sha256": "fc9e15f23d3f5c9a7928aecc70888e30be2c454ab16883e1a3c82290fd581fdb",
        "expected_bytes": 93793,
        "path": "content-staging/raw/legacy-supabase/subjects/1794eea5-4772-4c94-bd2b-b08e5815e733/images/page-00005-706771c2-2145-4682-9bdd-4e7df5c69bf9-image-00.jpg",
    },
    {
        "book_page": 6,
        "source_page": 10,
        "legacy_page_id": "71ba9a99-e009-401f-b65f-8a956218a633",
        "expected_sha256": "fd99f85698dd4870bf8fccf85aa53f47bf484d19b2052473155540627f6aa420",
        "expected_bytes": 116886,
        "path": "content-staging/raw/legacy-supabase/subjects/1794eea5-4772-4c94-bd2b-b08e5815e733/images/page-00006-71ba9a99-e009-401f-b65f-8a956218a633-image-00.jpg",
    },
    {
        "book_page": 7,
        "source_page": 11,
        "legacy_page_id": "710cb3d4-e2c1-4d05-a1ef-2c0a1bbede2b",
        "expected_sha256": "3b7415622af90557ad09585eef776b5ce3fe2c68776a1963b4a2cbf677f5ba61",
        "expected_bytes": 140264,
        "path": "content-staging/raw/legacy-supabase/subjects/1794eea5-4772-4c94-bd2b-b08e5815e733/images/page-00007-710cb3d4-e2c1-4d05-a1ef-2c0a1bbede2b-image-00.jpg",
    },
    {
        "book_page": 8,
        "source_page": 12,
        "legacy_page_id": "4b6090c2-744e-4fc6-8908-87c211a8713b",
        "expected_sha256": "3678974564e2a219840da4fc175d62d9811bd80666d01c81d4f9b49f2328e258",
        "expected_bytes": 106804,
        "path": "content-staging/raw/legacy-supabase/subjects/1794eea5-4772-4c94-bd2b-b08e5815e733/images/page-00008-4b6090c2-744e-4fc6-8908-87c211a8713b-image-00.jpg",
    },
]

PROFILES = [
    {"name": "webp-q82-m6", "quality": 82, "method": 6},
    {"name": "webp-q76-m6", "quality": 76, "method": 6},
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def psnr(a: Image.Image, b: Image.Image) -> float:
    a = a.convert("RGB")
    b = b.convert("RGB")
    diff = ImageChops.difference(a, b)
    stat = ImageStat.Stat(diff)
    mse = sum(v * v for v in stat.rms) / 3.0
    if mse == 0:
        return 99.0
    return 20.0 * math.log10(255.0 / math.sqrt(mse))


def make_contact(raw: Image.Image, candidate: Image.Image, out: Path, label: str) -> None:
    raw = raw.convert("RGB")
    candidate = candidate.convert("RGB")
    # Preserve enough detail to visually inspect text/lines while keeping the artifact manageable.
    max_w = 950
    scale = min(1.0, max_w / raw.width)
    size = (max(1, round(raw.width * scale)), max(1, round(raw.height * scale)))
    r = raw.resize(size, Image.Resampling.LANCZOS)
    c = candidate.resize(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (size[0] * 2, size[1] + 42), "white")
    canvas.paste(r, (0, 42))
    canvas.paste(c, (size[0], 42))
    d = ImageDraw.Draw(canvas)
    d.text((8, 12), "RAW JPEG", fill="black")
    d.text((size[0] + 8, 12), label, fill="black")
    canvas.save(out, "PNG", optimize=True)


def main() -> None:
    report = {
        "task_id": "MEDIA-001",
        "scope": "Grade 9 English / Pupil Book 3 / CURATION-001 pages 5..8",
        "raw_immutable": True,
        "profiles": PROFILES,
        "acceptance_rule": {
            "dimensions_must_match": True,
            "minimum_psnr_db": 32.0,
            "minimum_byte_reduction_percent": 20.0,
            "manual_contact_sheet_review_required": True,
        },
        "pages": [],
    }

    for page in PAGES:
        src = ROOT / page["path"]
        if not src.exists():
            raise SystemExit(f"missing RAW: {src}")
        observed_sha = sha256(src)
        observed_bytes = src.stat().st_size
        if observed_sha != page["expected_sha256"] or observed_bytes != page["expected_bytes"]:
            raise SystemExit(
                f"RAW drift page {page['book_page']}: sha={observed_sha} bytes={observed_bytes}"
            )

        raw = Image.open(src).convert("RGB")
        page_result = {
            **{k: v for k, v in page.items() if k != "path"},
            "raw_path": page["path"],
            "raw_width": raw.width,
            "raw_height": raw.height,
            "candidates": [],
        }

        for profile in PROFILES:
            out_name = f"page-{page['book_page']:02d}-{profile['name']}.webp"
            out = OUT / out_name
            raw.save(out, "WEBP", quality=profile["quality"], method=profile["method"])
            decoded = Image.open(out).convert("RGB")
            size = out.stat().st_size
            reduction = (1.0 - size / observed_bytes) * 100.0
            p = psnr(raw, decoded)
            dimensions_match = decoded.size == raw.size
            objective_pass = dimensions_match and p >= 32.0 and reduction >= 20.0
            contact = OUT / f"page-{page['book_page']:02d}-{profile['name']}-contact.png"
            make_contact(raw, decoded, contact, profile["name"])
            page_result["candidates"].append(
                {
                    "profile": profile["name"],
                    "path": str(out.relative_to(ROOT)),
                    "sha256": sha256(out),
                    "byte_size": size,
                    "byte_reduction_percent": round(reduction, 2),
                    "width": decoded.width,
                    "height": decoded.height,
                    "psnr_db": round(p, 2),
                    "dimensions_match": dimensions_match,
                    "objective_gate_pass": objective_pass,
                    "contact_sheet": str(contact.relative_to(ROOT)),
                }
            )
        report["pages"].append(page_result)

    (OUT / "media-001-probe.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
