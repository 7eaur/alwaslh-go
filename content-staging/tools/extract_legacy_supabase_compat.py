#!/usr/bin/env python3
"""Compatibility entrypoint for the raw legacy extractor.

Supabase publishable keys (sb_publishable_...) are opaque API keys, not JWTs.
They must be sent on the apikey header without being treated as a Bearer JWT.
Legacy anon JWT keys keep the historical Authorization header behavior.

This shim intentionally delegates all extraction logic to
extract_legacy_supabase.py so the raw export contract stays unchanged.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
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


def normalize_api_key(api_key: str) -> str:
    value = api_key.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1].strip()
    return value


def request_headers(api_key: str) -> dict[str, str]:
    normalized = normalize_api_key(api_key)
    headers = {
        "apikey": normalized,
        "Accept": "application/json",
        "User-Agent": "alwaslh-content-staging/1.0",
    }
    if not normalized.startswith("sb_"):
        headers["Authorization"] = f"Bearer {normalized}"
    return headers


def request_json(self: Any, url: str) -> Any:
    request = urllib.request.Request(url, headers=request_headers(self.api_key), method="GET")
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read(512).decode("utf-8", errors="replace")
        raise legacy.ExtractionError(
            f"legacy request failed: {url}: HTTP {exc.code}: {body}"
        ) from exc
    except (urllib.error.URLError, json.JSONDecodeError) as exc:
        raise legacy.ExtractionError(f"legacy request failed: {url}: {exc}") from exc


legacy.LegacyClient._request_json = request_json


if __name__ == "__main__":
    configured = normalize_api_key(os.getenv("LEGACY_SUPABASE_PUBLISHABLE_KEY", ""))
    kind = (
        "publishable"
        if configured.startswith("sb_publishable_")
        else "legacy_jwt"
        if configured.startswith("eyJ")
        else "other"
    )
    fingerprint = hashlib.sha256(configured.encode("utf-8")).hexdigest()[:16] if configured else "missing"
    print(
        f"legacy_key_diagnostic kind={kind} length={len(configured)} sha256_prefix={fingerprint}",
        file=sys.stderr,
    )
    raise SystemExit(legacy.main())
