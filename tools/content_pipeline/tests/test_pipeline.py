from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools" / "content_pipeline"))

import extract_legacy_supabase as extract  # noqa: E402
import reconstruct_content as reconstruct  # noqa: E402


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ContentPipelineUnitTests(unittest.TestCase):
    def test_group_lessons_respects_section_and_contiguous_title(self) -> None:
        pages = [
            {"legacy_page_id": "p1", "page_number": 1, "canonical_title": "Same"},
            {"legacy_page_id": "p2", "page_number": 2, "canonical_title": "Same"},
            {"legacy_page_id": "p3", "page_number": 4, "canonical_title": "Same"},
        ]
        lessons = reconstruct.group_lessons(pages, "subject")
        self.assertEqual(len(lessons), 2)
        self.assertEqual([p["page_number"] for p in lessons[0]["pages"]], [1, 2])
        self.assertEqual([p["page_number"] for p in lessons[1]["pages"]], [4])

    def test_image_filename_is_deterministic(self) -> None:
        page = {"id": "11111111-1111-1111-1111-111111111111", "page_number": 7}
        self.assertEqual(
            extract.image_filename(page, "image/jpeg"),
            "00007-11111111-1111-1111-1111-111111111111.jpg",
        )


class ContentPipelineIntegrationTests(unittest.TestCase):
    def test_reconstruct_optimize_validate_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            repo = Path(temp_name)
            subject_id = "1794eea5-4772-4c94-bd2b-b08e5815e733"
            config = {
                "version": 1,
                "mappings": {
                    "fixture": {
                        "legacyProjectRef": "fixture-project",
                        "legacyClassId": "class-id",
                        "legacyClassName": "Fixture Class",
                        "legacySubjectId": subject_id,
                        "legacySubjectName": "Fixture Subject",
                        "expectedPages": 3,
                        "expectedQuestions": 2,
                        "target": {
                            "classSlug": "grade-9",
                            "subjectSlug": "english",
                            "documentSlug": "pupil-book",
                            "documentKind": "textbook",
                        },
                        "structure": {
                            "strategy": "manifest_book_page",
                            "manifestPath": "source/manifest.json",
                            "sourcePageField": "page_number",
                            "manifestPageField": "book_page",
                            "sectionField": "section",
                            "titleField": "title",
                        },
                    }
                },
            }
            write_json(repo / "staging/config/legacy-subject-map.json", config)
            write_json(
                repo / "source/manifest.json",
                [
                    {"book_page": 1, "section": "Unit 1", "title": "Lesson A"},
                    {"book_page": 2, "section": "Unit 1", "title": "Lesson A"},
                    {"book_page": 3, "section": "Unit 2", "title": "Lesson B"},
                ],
            )

            raw_subject = repo / "staging/raw/legacy-supabase/subjects" / subject_id
            pages = []
            image_manifest = []
            for number, (title, question_count) in enumerate(
                [("Lesson A", 1), ("Lesson A", 0), ("Lesson B", 1)], start=1
            ):
                page_id = f"00000000-0000-0000-0000-{number:012d}"
                questions = []
                if question_count:
                    questions.append(
                        {
                            "type": "mcq",
                            "question": f"Question {number}",
                            "options": ["A", "B", "C", "D"],
                            "correct_option_index": 0,
                            "difficulty": "medium",
                            "explanation": "fixture",
                        }
                    )
                pages.append(
                    {
                        "id": page_id,
                        "subject_id": subject_id,
                        "title": title,
                        "page_number": number,
                        "created_at": f"2026-01-01T00:00:0{number}Z",
                        "content_type": "lesson",
                        "image_urls": [f"https://fixture.invalid/{number}.jpg"],
                        "ai_questions": questions,
                    }
                )
                raw_image_rel = Path("subjects") / subject_id / "images" / f"{number:05d}-{page_id}.jpg"
                raw_image = repo / "staging/raw/legacy-supabase" / raw_image_rel
                raw_image.parent.mkdir(parents=True, exist_ok=True)
                Image.new("RGB", (128, 160), (245 - number, 245, 245)).save(raw_image, "JPEG", quality=95)
                image_manifest.append(
                    {
                        "legacy_page_id": page_id,
                        "page_number": number,
                        "source_url": f"https://fixture.invalid/{number}.jpg",
                        "content_type": "image/jpeg",
                        "byte_size": raw_image.stat().st_size,
                        "sha256": sha256(raw_image),
                        "raw_path": raw_image_rel.as_posix(),
                    }
                )

            write_json(raw_subject / "subject.json", {"id": subject_id, "name": "Fixture Subject"})
            write_json(raw_subject / "pages.json", pages)
            write_json(
                raw_subject / "questions.json",
                [
                    {
                        "legacy_page_id": page["id"],
                        "legacy_subject_id": subject_id,
                        "page_number": page["page_number"],
                        "ordinal": ordinal,
                        "raw": question,
                    }
                    for page in pages
                    for ordinal, question in enumerate(page["ai_questions"])
                ],
            )
            write_json(raw_subject / "image-manifest.json", image_manifest)
            write_json(raw_subject / "image-anomalies.json", [])

            commands = [
                [
                    sys.executable,
                    str(ROOT / "tools/content_pipeline/reconstruct_content.py"),
                    "--repo-root",
                    str(repo),
                    "--mapping",
                    "staging/config/legacy-subject-map.json",
                    "--key",
                    "fixture",
                ],
                [
                    sys.executable,
                    str(ROOT / "tools/content_pipeline/optimize_webp.py"),
                    "--repo-root",
                    str(repo),
                    "--root",
                    "staging/curated/grade-9/english/pupil-book",
                ],
                [
                    sys.executable,
                    str(ROOT / "tools/content_pipeline/validate_staging.py"),
                    "--repo-root",
                    str(repo),
                    "--mapping",
                    "staging/config/legacy-subject-map.json",
                    "--key",
                    "fixture",
                ],
            ]
            outputs = []
            for command in commands:
                completed = subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
                outputs.append(completed.stdout.strip())

            reconstructed = json.loads(outputs[0])
            verified = json.loads(outputs[2])
            self.assertEqual(reconstructed["sections"], 2)
            self.assertEqual(reconstructed["lessons"], 2)
            self.assertEqual(reconstructed["pages"], 3)
            self.assertEqual(reconstructed["questions"], 2)
            self.assertTrue(verified["verified"])
            self.assertEqual(verified["optimized_webp_files"], 3)


if __name__ == "__main__":
    unittest.main()
