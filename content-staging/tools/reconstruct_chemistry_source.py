#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUBJECT_ID = "f0c5228c-7d5b-4ec2-85ed-ce59139ce0a4"
SUBJECT_DIR = ROOT / "content-staging" / "raw" / "legacy-supabase" / "subjects" / SUBJECT_ID
TECH_PATH = ROOT / "content-staging" / "reconstruction" / "technical" / f"{SUBJECT_ID}.json"
OUT_PATH = ROOT / "content-staging" / "reconstruction" / "educational" / f"{SUBJECT_ID}.json"
MASTER_ROOT = ROOT / "master-reference" / "الكيمياء ثالث ثانوي" / "كتاب الكيمياء" / "الصور"
MASTER_COMMIT = "f81ebb6ef6198818fa091f7a8c1c81b4de7dbd23"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_pages():
    payload = json.loads((SUBJECT_DIR / "pages.json").read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise SystemExit("Chemistry pages.json must be a list")
    return payload


def qcount(page):
    questions = page.get("ai_questions") or []
    return len(questions) if isinstance(questions, list) else 0


def build_runs(pages):
    runs = []
    for page in pages:
        title = (page.get("title") or "").strip()
        number = page.get("page_number")
        if not isinstance(number, int) or not title:
            raise SystemExit(f"Missing page_number/title in page record: {page.get('id')}")
        row = {
            "page_number": number,
            "legacy_page_id": page.get("id"),
            "title": title,
            "legacy_question_count": qcount(page),
        }
        if not runs or runs[-1]["title"] != title:
            runs.append({"title": title, "rows": [row]})
        else:
            runs[-1]["rows"].append(row)
    for run in runs:
        nums = [row["page_number"] for row in run["rows"]]
        run["first_page"] = nums[0]
        run["last_page"] = nums[-1]
        run["page_numbers"] = nums
    return runs


def master_index():
    if not MASTER_ROOT.is_dir():
        raise SystemExit(f"Missing trusted master reference: {MASTER_ROOT}")
    result = {}
    for path in MASTER_ROOT.iterdir():
        match = re.match(r"^ص(\d{3})\b", path.name)
        if match:
            result[int(match.group(1))] = path
    return result


def main():
    subject = json.loads((SUBJECT_DIR / "subject.json").read_text(encoding="utf-8"))
    manifest = json.loads((SUBJECT_DIR / "manifest.json").read_text(encoding="utf-8"))
    pages = load_pages()
    tech = json.loads(TECH_PATH.read_text(encoding="utf-8"))
    if not tech.get("all_images_technically_verified"):
        raise SystemExit("Technical verification is not green")

    numbers = [page["page_number"] for page in pages]
    if numbers != list(range(11, 189)):
        raise SystemExit("Legacy Chemistry pages are not exact contiguous 11..188")
    if len(pages) != 178 or manifest["counts"]["pages"] != 178:
        raise SystemExit("Unexpected Chemistry page count")

    raw_by_page = {item["page_number"]: item for item in manifest["images"]}
    master = master_index()
    if min(master) != 3 or max(master) != 193:
        raise SystemExit(f"Unexpected trusted master numbered range: {min(master)}..{max(master)}")
    shared_mismatches = []
    for number in numbers:
        item = raw_by_page[number]
        raw = ROOT / "content-staging" / item["raw_path"]
        master_path = master.get(number)
        if not master_path or sha256(raw) != sha256(master_path):
            shared_mismatches.append(number)
    if shared_mismatches:
        raise SystemExit(f"RAW/master SHA mismatches: {shared_mismatches}")

    runs = build_runs(pages)
    unit_indexes = [i for i, run in enumerate(runs) if run["title"].startswith("الوحدة ")]
    if len(unit_indexes) != 9:
        raise SystemExit(f"Expected 9 units, got {len(unit_indexes)}")

    units = []
    lesson_total = 0
    for unit_no, start in enumerate(unit_indexes, 1):
        end = unit_indexes[unit_no] if unit_no < len(unit_indexes) else len(runs)
        segment = runs[start:end]
        header = segment[0]
        match = re.match(r"الوحدة\s+([^\-]+)\s*-\s*(.+)", header["title"])
        unit_title = match.group(2).strip() if match else header["title"]
        lessons = []
        review_pages = []
        lesson_no = 0
        for run in segment[1:]:
            if run["title"].startswith("تقويم الوحدة"):
                review_pages.extend(run["page_numbers"])
                continue
            if run["title"] == "المصطلحات العلمية":
                continue
            lesson_no += 1
            lesson_total += 1
            lesson_rows = run["rows"]
            lessons.append({
                "id": f"chemistry-u{unit_no:02d}-l{lesson_no:02d}",
                "ordinal": lesson_no,
                "title": run["title"],
                "first_page": run["first_page"],
                "last_page": run["last_page"],
                "page_count": len(run["page_numbers"]),
                "page_numbers": run["page_numbers"],
                "legacy_page_ids": [row["legacy_page_id"] for row in lesson_rows],
                "legacy_question_count": sum(row["legacy_question_count"] for row in lesson_rows),
                "status": "verified_from_toc_page_titles_and_continuity",
            })
        unit_pages = []
        for run in segment:
            if run["title"] != "المصطلحات العلمية":
                unit_pages.extend(run["page_numbers"])
        units.append({
            "id": f"chemistry-u{unit_no:02d}",
            "ordinal": unit_no,
            "title": unit_title,
            "source_header_title": header["title"],
            "first_page": min(unit_pages),
            "last_page": max(unit_pages),
            "page_count": len(unit_pages),
            "unit_cover_pages": header["page_numbers"],
            "lesson_count": len(lessons),
            "lessons": lessons,
            "review_pages": review_pages,
            "status": "verified",
        })

    glossary_run = next((run for run in runs if run["title"] == "المصطلحات العلمية"), None)
    if not glossary_run or glossary_run["page_numbers"] != [184, 185, 186, 187, 188]:
        raise SystemExit("Glossary boundary is not exact 184..188")
    appendices = [{
        "type": "glossary",
        "title": "المصطلحات العلمية",
        "first_page": 184,
        "last_page": 188,
        "page_count": 5,
        "page_numbers": [184, 185, 186, 187, 188],
        "status": "verified",
    }]

    lesson_page_count = sum(lesson["page_count"] for unit in units for lesson in unit["lessons"])
    cover_page_count = sum(len(unit["unit_cover_pages"]) for unit in units)
    review_page_count = sum(len(unit["review_pages"]) for unit in units)
    if (lesson_total, lesson_page_count, cover_page_count, review_page_count) != (57, 149, 10, 14):
        raise SystemExit("Unexpected reconstructed Chemistry counts")

    question_total = sum(qcount(page) for page in pages)
    lesson_questions = sum(lesson["legacy_question_count"] for unit in units for lesson in unit["lessons"])
    cover_numbers = {p for unit in units for p in unit["unit_cover_pages"]}
    review_numbers = {p for unit in units for p in unit["review_pages"]}
    cover_questions = sum(qcount(page) for page in pages if page["page_number"] in cover_numbers)
    review_questions = sum(qcount(page) for page in pages if page["page_number"] in review_numbers)
    appendix_questions = sum(qcount(page) for page in pages if page["page_number"] >= 184)
    if question_total != 2576:
        raise SystemExit(f"Unexpected question count: {question_total}")

    output = {
        "schema_version": 1,
        "source_id": SUBJECT_ID,
        "source_type": "educational_book_source",
        "legacy_identity": {
            "class_id": subject["class"]["id"],
            "class_name": subject["class"]["name"].strip(),
            "subject_name": subject["subject"]["name"],
        },
        "reconstructed_book": {
            "title": "كتاب الكيمياء",
            "grade_or_level": "ثالث ثانوي",
            "subject": "الكيمياء",
            "legacy_retained_page_range": [11, 188],
            "legacy_retained_page_count": 178,
            "trusted_master_reference": {
                "commit": MASTER_COMMIT,
                "folder": "الكيمياء ثالث ثانوي/كتاب الكيمياء",
                "numbered_page_range": [3, 193],
                "shared_page_range": [11, 188],
                "shared_sha256_equal": 178,
                "shared_sha256_mismatch_or_missing": 0,
                "master_only_numbered_pages_outside_legacy_range": [3,4,5,6,7,8,9,10,189,190,191,192,193],
            },
            "unit_count": 9,
            "lesson_count": 57,
            "lesson_page_count": 149,
            "unit_cover_page_count": 10,
            "review_page_count": 14,
            "appendix_page_count": 5,
            "units": units,
            "appendices": appendices,
        },
        "technical_verification": tech["checks"],
        "question_baseline": {
            "legacy_questions": question_total,
            "lesson_page_questions": lesson_questions,
            "unit_cover_questions": cover_questions,
            "review_questions": review_questions,
            "appendix_questions": appendix_questions,
            "semantic_link_status": "NOT VERIFIED",
        },
        "evidence": {
            "toc_pages": [7, 8, 9, 10],
            "boundary_method": "trusted master table of contents + exact page-title runs + SHA-equal RAW/master mapping + selective visual inspection",
            "raw_mutations": 0,
        },
        "status": "reconstructed_verified",
        "notes": [
            "Legacy is a contiguous retained slice of the same trusted master book: numbered pages 11..188.",
            "Master pages 3..10 are before the retained Legacy slice; pages 189..193 are after it.",
            "Unit covers and unit reviews are modeled separately from lessons; glossary 184..188 is an appendix, not lessons.",
            "Question semantic correctness and final lesson-question linkage remain NOT VERIFIED; page-local structural counts only are recorded.",
            "No RAW file was modified.",
        ],
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUT_PATH.relative_to(ROOT)),
        "units": 9,
        "lessons": 57,
        "lesson_pages": 149,
        "unit_cover_pages": 10,
        "review_pages": 14,
        "appendix_pages": 5,
        "legacy_questions": 2576,
        "raw_master_sha_equal": 178,
        "raw_mutations": 0,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
