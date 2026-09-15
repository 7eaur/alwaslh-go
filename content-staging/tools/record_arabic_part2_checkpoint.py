#!/usr/bin/env python3
import hashlib
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SID = "7ddec20e-617e-4e55-bba8-2d371aaf16b6"
NAME = "كتاب العربي - الجزء الثاني"
RECON = ROOT / "content-staging/reconstruction/educational" / f"{SID}.json"
TECH = ROOT / "content-staging/reconstruction/technical" / f"{SID}.json"
CONFLICT = (
    ROOT
    / "content-staging/reconstruction/educational"
    / f"{SID}-page177-conflict-resolution.json"
)
RAW = ROOT / "content-staging/raw/legacy-supabase/subjects" / SID
MASTER = ROOT / "content-staging/manifests/MASTER_CONTENT_MANIFEST.json"
LOG = ROOT / "content-staging/CONTENT_RECONSTRUCTION_AUTOMATION_LOG.md"
START = "<!-- ARABIC_PART2_CHECKPOINT_START -->"
END = "<!-- ARABIC_PART2_CHECKPOINT_END -->"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def expand(spec):
    pages = []
    for token in str(spec).split(","):
        bounds = token.strip().split("..")
        pages.extend(range(int(bounds[0]), int(bounds[-1]) + 1))
    return pages


def replace_checkpoint(path, body):
    text = path.read_text(encoding="utf-8")
    block = f"{START}\n{body.rstrip()}\n{END}"
    if START in text and END in text:
        before = text.split(START, 1)[0].rstrip()
        after = text.split(END, 1)[1].lstrip()
        text = before + "\n\n" + block + ("\n\n" + after if after.strip() else "\n")
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    path.write_text(text, encoding="utf-8")


def completed(source):
    review_status = str(source.get("review_status", "")).lower()
    reconstruction = (source.get("reconstruction") or {}).get("status")
    exam_reconstruction = (source.get("exam_reconstruction") or {}).get("status", "")
    return (
        reconstruction == "verified"
        or "verified_empty" in review_status
        or "reconstructed_verified" in review_status
        or str(exam_reconstruction).startswith("processed_")
    )


reconstruction = read_json(RECON)
technical = read_json(TECH)
conflict = read_json(CONFLICT)
manifest = read_json(RAW / "manifest.json")
raw_pages = read_json(RAW / "pages.json")
counts = reconstruction["counts"]

# Fail closed on every source-local invariant before changing shared state.
assert reconstruction["state"] in {
    "EVIDENCE_RECONSTRUCTED_PENDING_MASTER_CHECKPOINT",
    "MASTER_CHECKPOINTED_RECONSTRUCTED_VERIFIED",
}
assert (
    counts["books"],
    counts["units"],
    counts["semantic_instructional_lessons"],
    counts["lesson_membership_edges"],
    counts["unique_lesson_physical_pages"],
    counts["front_matter_pages"],
    counts["unit_cover_or_intro_pages"],
    counts["assessment_pages"],
    counts["tail_pages"],
    counts["review_required_questions"],
) == (1, 12, 60, 111, 99, 8, 48, 20, 3, 11)
assert [unit["unit"] for unit in reconstruction["units"]] == list(range(13, 25))
assert sum(len(unit["lessons"]) for unit in reconstruction["units"]) == 60

front = set(expand(reconstruction["front_matter"]))
tail = set(expand(reconstruction["tail"]))
intro = set()
assessment = set()
lesson_edges = []
unit_ranges = []
for unit in reconstruction["units"]:
    unit_ranges.extend(expand(unit["range"]))
    intro.update(expand(unit["intro"]))
    assessment.update(expand(unit["assessment"]))
    for lesson in unit["lessons"]:
        lesson_edges.extend(expand(lesson))
lesson_pages = set(lesson_edges)
physical_sets = (front, intro, lesson_pages, assessment, tail)
assert tuple(map(len, physical_sets)) == (8, 48, 99, 20, 3)
assert sum(map(len, physical_sets)) == len(set().union(*physical_sets))
assert set().union(*physical_sets) == set(range(178))
assert unit_ranges == list(range(8, 175))
assert len(lesson_edges) == 111
assert set(reconstruction["shared_lesson_pages"]) == {
    page for page in lesson_pages if lesson_edges.count(page) > 1
}

assert manifest["counts"] == {
    "pages": 178,
    "image_references": 178,
    "images_downloaded": 178,
    "image_download_failures": 0,
    "questions": 11,
}
assert len(raw_pages) == 178
assert sorted(page.get("page_number") for page in raw_pages) == list(range(178))
question_pages = [page for page in raw_pages if page.get("ai_questions")]
assert len(question_pages) == 1
assert question_pages[0]["id"] == "d79b9858-a33a-413b-9740-06a40f2e1eba"
assert question_pages[0]["page_number"] == 177
assert len(question_pages[0]["ai_questions"]) == 11

assert technical["technical_verified_images"] == 178
assert technical["technical_failures"] == []
assert technical["duplicate_sha_groups"] == []
assert technical["numbered_page_sequence"] == {
    "first": 1,
    "last": 177,
    "count": 177,
    "missing": [],
}
assert len(technical["nonpositive_or_unknown_page_records"]) == 1
assert technical["nonpositive_or_unknown_page_records"][0]["page_number"] == 0
assert technical["nonpositive_or_unknown_page_records"][0]["ok"] is True

disposition = conflict["question_disposition"]
assert disposition["count"] == 11
assert disposition["classification"] == "review_required"
assert disposition["lesson_linked"] == 0
assert disposition["assessment_linked"] == 0
image_evidence = conflict["immutable_image_chain"]
image_path = ROOT / "content-staging" / image_evidence["raw_path"]
assert image_path.exists()
assert image_path.stat().st_size == image_evidence["byte_size"]
assert hashlib.sha256(image_path.read_bytes()).hexdigest() == image_evidence["sha256"]

master = read_json(MASTER)
source = next(item for item in master["sources"] if item["id"] == SID)
progress = master["reconstruction_progress"]
already = source.get("review_status") == "reconstructed_verified"

if not already:
    # These exact prior counters are the concurrency/drift gate for this checkpoint.
    assert (
        progress["sources_completed"],
        progress["educational_sources_completed"],
        progress["verified_books"],
        progress["verified_units"],
        progress["verified_lessons"],
        progress["verified_lesson_pages"],
        progress["source_images_technically_verified"],
        progress["lesson_linked_structural"],
        progress["exam_linked_to_individual_model"],
        progress["review_required"],
        progress["unclassified"],
    ) == (37, 17, 15, 69, 388, 1641, 3190, 13135, 1920, 1229, 9471)
    progress["sources_completed"] += 1
    progress["educational_sources_completed"] += 1
    progress["verified_books"] += 1
    progress["verified_units"] += 12
    progress["verified_lessons"] += 60
    progress["verified_lesson_pages"] += 99
    progress["source_images_technically_verified"] += 178
    progress["review_required"] += 11
    progress["unclassified"] -= 11

source["classification"] = "educational_book_source"
source["classification_evidence"] = (
    "178/178 immutable RAW technical verification + complete visual review + exact "
    "lesson-header evidence + page-177 provenance conflict resolution + shared "
    "physical lesson-page policy"
)
source["review_status"] = "reconstructed_verified"
source["technical_verification"] = {
    "status": "verified",
    "report_path": f"content-staging/reconstruction/technical/{SID}.json",
    "images_verified": 178,
    "readable": 178,
    "sha256_match_manifest": 178,
    "mime_match_manifest": 178,
    "duplicate_sha_groups_within_source": 0,
    "page_sequence": "page 0 preserved plus contiguous 1..177",
}
source["reconstruction"] = {
    "status": "verified",
    "path": f"content-staging/reconstruction/educational/{SID}.json",
    "book_title": NAME,
    "retained_page_range": [0, 177],
    "retained_pages": 178,
    "units": 12,
    "lessons": 60,
    "lesson_pages": 99,
    "lesson_membership_edges": 111,
    "front_matter_pages": 8,
    "unit_cover_or_intro_pages": 48,
    "assessment_pages": 20,
    "tail_pages": 3,
    "shared_physical_lesson_pages": reconstruction["shared_lesson_pages"],
    "legacy_questions": 11,
    "structurally_lesson_linked_questions": 0,
    "structurally_assessment_linked_questions": 0,
    "review_required_questions": 11,
    "question_conflict_evidence": (
        f"content-staging/reconstruction/educational/{SID}-page177-conflict-resolution.json"
    ),
    "semantic_question_review": "NOT VERIFIED",
    "raw_mutations": 0,
}
master["status"] = "RECONSTRUCTION_IN_PROGRESS_NOT_IMPORT_READY"

assert (
    progress["sources_completed"],
    progress["educational_sources_completed"],
    progress["verified_books"],
    progress["verified_units"],
    progress["verified_lessons"],
    progress["verified_lesson_pages"],
    progress["source_images_technically_verified"],
    progress["lesson_linked_structural"],
    progress["exam_linked_to_individual_model"],
    progress["review_required"],
    progress["unclassified"],
) == (38, 18, 16, 81, 448, 1740, 3368, 13135, 1920, 1240, 9460)
assert (
    progress["lesson_linked_structural"]
    + progress["exam_linked_to_individual_model"]
    + progress["review_required"]
    + progress["unclassified"]
    == progress["legacy_questions_total"]
    == 25755
)
assert all(
    progress[key] == 0
    for key in ("raw_mutations", "unrelated_mutations", "new_imports", "new_publications")
)

reconstruction["state"] = "MASTER_CHECKPOINTED_RECONSTRUCTED_VERIFIED"
reconstruction["checkpoint"] = {
    "status": "verified",
    "start_head": os.environ.get("START_HEAD", "NOT VERIFIED"),
    "canonical_progress": {
        "sources": "38/58",
        "educational": "18/26",
        "books": 16,
        "units": 81,
        "lessons": 448,
        "lesson_pages": 1740,
        "source_images": "3368/5273",
        "review_required": 1240,
        "unclassified": 9460,
    },
    "production_database_mutation": 0,
}
write_json(RECON, reconstruction)
write_json(MASTER, master)

sources = master["sources"]
source_index = next(index for index, item in enumerate(sources) if item["id"] == SID)
next_source = next(
    (item for item in sources[source_index + 1 :] + sources[:source_index] if not completed(item)),
    None,
)
next_id = next_source["id"] if next_source else "NONE"
next_name = (
    (next_source.get("legacy_source") or {}).get("name")
    or next_source.get("name")
    or "UNKNOWN"
    if next_source
    else "NONE"
)
next_counts = next_source.get("counts", {}) if next_source else {}

body = f"""## Reconstruction checkpoint — Arabic book part 2

- Sources processed: **{progress['sources_completed']}/{progress['sources_total']}**; Educational: **{progress['educational_sources_completed']}/{progress['educational_sources_total']}**; Exam groups: **{progress['exam_source_groups_completed']}/{progress['exam_source_groups_total']}**.
- Books / Units / Lessons / unique physical Lesson pages: **{progress['verified_books']} / {progress['verified_units']} / {progress['verified_lessons']} / {progress['verified_lesson_pages']}**.
- Arabic Part 2: **178/178** technical; page **0** preserved plus contiguous **1..177**; **12 Units (13..24) / 60 semantic Lessons / 111 membership edges / 99 unique physical lesson pages / 48 intro-cover / 20 assessment / 8 front matter / 3 tail**.
- Physical invariant: **8 + 48 + 99 + 20 + 3 = 178**.
- Page 177 conflict: immutable image association is verified as the back cover; its **11** stale/misattached legacy questions remain **review_required**, with **0 lesson-linked** and **0 assessment-linked**; semantic correctness is **NOT VERIFIED**.
- Questions: **{progress['lesson_linked_structural']} + {progress['exam_linked_to_individual_model']} + {progress['review_required']} + {progress['unclassified']} = 25,755**.
- Technical images: **{progress['source_images_technically_verified']}/{progress['source_images_total']}**. RAW/unrelated/import/publication mutations **0/0/0/0**.
- Production PostgreSQL cleanup/import: **NOT EXECUTED**; reconstruction remains not import-ready corpus-wide.
- Last completed: `{SID} — {NAME}`. Next: `{next_id} — {next_name}`.
"""

for filename in (
    "CONTENT_REBUILD_EXECUTION_STATUS.md",
    "CONTENT_REBUILD_HANDOFF.md",
    "CONTENT_INVENTORY.md",
    "CONTENT_VALIDATION_REPORT.md",
    "CONTENT_IMPORT_REPORT.md",
    "CONTENT_REBUILD_CONTINUATION_2026-09-14.md",
):
    path = ROOT / "content-staging" / filename
    if path.exists():
        replace_checkpoint(path, body)

log = LOG.read_text(encoding="utf-8")
active_marker = "\n## ACTIVE CHECKPOINT\n"
history = log.rsplit(active_marker, 1)[0].rstrip() if active_marker in log else log.rstrip()
start_head = os.environ.get("START_HEAD", "NOT VERIFIED")
now = datetime.now(timezone(timedelta(hours=3))).isoformat(timespec="seconds")
run = f"""## RUN {now} — Worker A

- state: COMPLETE_SOURCE_HANDOFF
- start HEAD: `{start_head}`
- end HEAD before handoff-log commit: `WORKTREE_PENDING_COMMIT`
- phase: `CONTENT RECONSTRUCTION + EXAM BOUNDARY DISCOVERY`
- source at start: `{SID} — {NAME}`
- completed in this run: validated and checkpointed the existing evidence-backed Arabic Part 2 reconstruction; finalized 1 Book / 12 Units / 60 semantic Lessons / 99 unique physical Lesson pages; preserved page 0 and shared-page semantics; quarantined all 11 stale page-177 questions as review_required; updated MASTER/status evidence; resolved the next source from live MASTER.
- evidence/artifacts: `{RECON.relative_to(ROOT)}`; `{CONFLICT.relative_to(ROOT)}`; complete visual artifact `10398967254` / run `34975254689`.
- ambiguity/review_required: the 11 page-177 questions have no proven lesson/assessment page and remain review_required; semantic correctness `NOT VERIFIED`; no guessed reassignment.
- invariant result: PASS (`{progress['lesson_linked_structural']} + {progress['exam_linked_to_individual_model']} + {progress['review_required']} + {progress['unclassified']} = 25,755`); physical `8 + 48 + 99 + 20 + 3 = 178`.
- Sources processed: {progress['sources_completed']}/{progress['sources_total']}
- Educational: {progress['educational_sources_completed']}/{progress['educational_sources_total']}
- Books / Units / Lessons / Lesson Pages: {progress['verified_books']} / {progress['verified_units']} / {progress['verified_lessons']} / {progress['verified_lesson_pages']}
- Exam Source Groups: {progress['exam_source_groups_completed']}/{progress['exam_source_groups_total']}
- Individual Exam Models: {progress['individual_exam_models']}
- Exam Pages: {progress['exam_pages_completed']}/{progress['exam_pages_total']}
- Verified Answer Keys: {progress['answer_keys']}
- Source images technical: {progress['source_images_technically_verified']}/{progress['source_images_total']}
- Legacy Questions: {progress['legacy_questions_total']}
- Lesson-linked: {progress['lesson_linked_structural']}
- Exam-linked: {progress['exam_linked_to_individual_model']}
- Review-required: {progress['review_required']}
- Unclassified: {progress['unclassified']}
- Duplicate groups classified: {progress['duplicate_fingerprint_groups_classified']}/{progress['duplicate_fingerprint_groups_total']}
- RAW mutations: 0
- Unrelated mutations: 0
- New imports: 0
- New publications: 0
- last completed source: `{SID} — {NAME}`
- current source: `{next_id} — {next_name}`
- exact next operation: `Re-fetch live HEAD/baton; verify no active workflow for {next_id}; technically verify its {next_counts.get('pages', 'NOT VERIFIED')} immutable RAW page records; discover source-local Individual Exam Model/correction/Answer-Key boundaries without inheriting prior packet patterns; map questions only where proven; quarantine uncertainty; assert invariants; checkpoint.`
- next source: `Resolve only after {next_id} finalization from live MASTER.`
- blockers: `none for reconstruction continuation; production database cleanup/import remains gated until an import-ready batch and modern schema dry-run are verified.`
- handoff note: `Do not rerun Arabic Part 2 absent drift evidence. Its 11 page-177 questions are excluded from clean lesson/assessment import until independently resolved.`
"""
active = f"""## ACTIVE CHECKPOINT

- state: `COMPLETE_SOURCE_HANDOFF`
- branch: `content/corpus-inventory-20260914`
- latest validated source: `{SID} — {NAME}`
- progress: `{progress['sources_completed']}/{progress['sources_total']} sources; {progress['educational_sources_completed']}/{progress['educational_sources_total']} educational; {progress['exam_source_groups_completed']}/{progress['exam_source_groups_total']} exam groups; {progress['verified_books']} books; {progress['verified_units']} units; {progress['verified_lessons']} lessons; {progress['verified_lesson_pages']} unique physical lesson pages; {progress['source_images_technically_verified']}/{progress['source_images_total']} technical images.`
- invariant: `{progress['lesson_linked_structural']} + {progress['exam_linked_to_individual_model']} + {progress['review_required']} + {progress['unclassified']} = 25,755`; RAW/unrelated/import/publication mutations `0/0/0/0`.
- current source: `{next_id} — {next_name}`
- current source baseline: `{next_counts.get('pages', 'NOT VERIFIED')} pages / {next_counts.get('image_references', 'NOT VERIFIED')} images / {next_counts.get('questions', 'NOT VERIFIED')} legacy questions / {next_counts.get('image_download_failures', 'NOT VERIFIED')} download failures; structure NOT VERIFIED.`
- current operation: `Begin source-local technical verification and exam-boundary discovery for {next_id}; do not inherit prior-source boundaries.`
- next source: `Resolve only after {next_id} finalization from live MASTER.`
- blockers: `none known for reconstruction; production PostgreSQL mutation remains gated and NOT EXECUTED.`
"""
LOG.write_text(history + "\n\n" + run + "\n" + active, encoding="utf-8")

print(
    json.dumps(
        {
            "already": already,
            "next_source_id": next_id,
            "next_source_name": next_name,
            "progress": progress,
        },
        ensure_ascii=False,
    )
)
