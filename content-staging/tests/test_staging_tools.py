from __future__ import annotations

import importlib.util
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
TOOLS = ROOT / "content-staging" / "tools"


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, TOOLS / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {filename}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


extractor = load_module("legacy_extractor", "extract_legacy_supabase.py")
builder = load_module("curated_builder", "build_curated_candidates.py")


class RawExtractionTests(unittest.TestCase):
    def test_page_anomalies_preserve_duplicates_instead_of_blocking(self):
        subject_id = "subject-1"
        pages = [
            {
                "id": "a",
                "subject_id": subject_id,
                "page_number": 1,
                "image_urls": ["https://example.invalid/a.jpg"],
                "ai_questions": [],
            },
            {
                "id": "b",
                "subject_id": subject_id,
                "page_number": 1,
                "image_urls": [],
                "ai_questions": [],
            },
            {
                "id": "c",
                "subject_id": subject_id,
                "page_number": None,
                "image_urls": ["x", "y"],
                "ai_questions": "malformed",
            },
        ]
        result = extractor.page_anomalies(pages, subject_id)
        self.assertEqual(result["duplicate_page_numbers"], [1])
        self.assertEqual(result["null_or_invalid_page_numbers"], ["c"])
        self.assertEqual(result["missing_images"], ["b"])
        self.assertEqual(result["multiple_images"], ["c"])
        self.assertEqual(result["malformed_ai_questions"], ["c"])

    def test_canonical_json_digest_is_order_independent_for_object_keys(self):
        left = {"b": 2, "a": 1}
        right = {"a": 1, "b": 2}
        self.assertEqual(extractor.sha256_json(left), extractor.sha256_json(right))


class CurationTests(unittest.TestCase):
    def test_stable_id_is_deterministic(self):
        self.assertEqual(builder.stable_id("same"), builder.stable_id("same"))
        self.assertNotEqual(builder.stable_id("same"), builder.stable_id("different"))
        self.assertEqual(len(builder.stable_id("same")), 20)

    def test_title_normalization_only_collapses_whitespace(self):
        self.assertEqual(builder.normalize_title("  Unit   1  -  Revision "), "Unit 1 - Revision")


if __name__ == "__main__":
    unittest.main()
