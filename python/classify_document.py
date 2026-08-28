from __future__ import annotations

import argparse

from bdi_client import BdiApiError, post_document, print_json


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Classify a business document with Business Document Intelligence."
    )
    parser.add_argument("document", help="Path to a PDF, JPEG, PNG, or WebP document")
    args = parser.parse_args()

    try:
        payload = post_document("/v1/documents/classify", args.document)
    except (BdiApiError, FileNotFoundError, RuntimeError, ValueError) as exc:
        parser.exit(1, f"error: {exc}\n")

    print_json(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
