from __future__ import annotations

import json
import os
import sys
import uuid
from pathlib import Path
from typing import Any

import requests

DEFAULT_HOST = "business-document-intelligence.p.rapidapi.com"
MAX_DOCUMENT_BYTES = 5 * 1024 * 1024
DEFAULT_TIMEOUT_SECONDS = 90


class BdiApiError(RuntimeError):
    """Raised when the API returns a non-success response."""


def _rapidapi_key() -> str:
    key = os.getenv("RAPIDAPI_KEY", "").strip()
    if not key:
        raise RuntimeError(
            "RAPIDAPI_KEY is not set. Set it in your environment before running this example."
        )
    return key


def _host() -> str:
    return os.getenv("RAPIDAPI_HOST", DEFAULT_HOST).strip() or DEFAULT_HOST


def _read_document(path_value: str) -> tuple[Path, bytes]:
    path = Path(path_value).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Document not found: {path}")

    size = path.stat().st_size
    if size == 0:
        raise ValueError("Document is empty.")
    if size > MAX_DOCUMENT_BYTES:
        raise ValueError(
            f"Document is {size} bytes; the API maximum is {MAX_DOCUMENT_BYTES} bytes (5 MiB)."
        )

    return path, path.read_bytes()


def post_document(endpoint: str, document_path: str) -> dict[str, Any]:
    path, body = _read_document(document_path)
    host = _host()
    request_id = f"example.{uuid.uuid4().hex}"

    response = requests.post(
        f"https://{host}{endpoint}",
        headers={
            "Content-Type": "application/octet-stream",
            "X-RapidAPI-Host": host,
            "X-RapidAPI-Key": _rapidapi_key(),
            "X-Request-ID": request_id,
        },
        data=body,
        timeout=DEFAULT_TIMEOUT_SECONDS,
    )

    returned_request_id = response.headers.get("X-Request-ID")
    if returned_request_id:
        print(f"X-Request-ID: {returned_request_id}", file=sys.stderr)

    try:
        payload = response.json()
    except ValueError:
        payload = {"raw_response": response.text}

    if not response.ok:
        detail = json.dumps(payload, indent=2, sort_keys=True)
        raise BdiApiError(
            f"API request failed for {path.name} with HTTP {response.status_code}:\n{detail}"
        )

    if not isinstance(payload, dict):
        raise BdiApiError("API returned a successful response that was not a JSON object.")

    return payload


def print_json(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))
