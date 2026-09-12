#!/usr/bin/env python3
"""Compatibility entrypoint for the raw legacy extractor.

Supabase publishable keys (sb_publishable_...) are opaque API keys, not JWTs.
They must be sent on the apikey header without being treated as a Bearer JWT.
Legacy anon JWT keys keep the historical Authorization header behavior.

This shim intentionally delegates all extraction logic to
extract_legacy_supabase.py so the raw export contract stays unchanged.
"""

from __future__ import annotations

import importlib.util
import json
import pathlib
import sys
import urllib.error
import urllib.request
from typing import Any

TOOLS = pathlib.Path(__file__).resolve().parent
SOURCE = TOOLS / "extract_legacy_supabase.py"

spec = importlib.util.spec_from_file_location("legacy_raw_extractor", SOURCE)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load extractor: {SOURCE}")
legacy = importlib.util.module_from_spec(spec)
sys.modules["legacy_raw_extractor"] = legacy
spec.loader.exec_module(legacy)


def request_headers(api_key: str) -> dict[str, str]:
    headers = {
        "apikey": api_key,
        "Accept": "application/json",
        "User-Agent": "alwaslh-content-staging/1.0",
    }
    if not api_key.startswith("sb_"):
        headers["Authorization"] = f"Bearer {api_key}"
    return headers


def request_json(self: Any, url: str) -> Any:
    request = urllib.request.Request(url, headers=request_headers(self.api_key), method="GET")
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as exc:
        raise legacy.ExtractionError(f"legacy request failed: {url}: {exc}") from exc


legacy.LegacyClient._request_json = request_json


if __name__ == "__main__":
    raise SystemExit(legacy.main())
