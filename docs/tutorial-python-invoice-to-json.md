# How to Extract Invoice Data from a PDF to JSON with Python

If your application receives invoices as PDFs or images, the useful output usually is not raw OCR text. You need predictable fields that your software can validate, store, and route.

This tutorial uses the **Business Document Intelligence API** on RapidAPI to upload an invoice as raw binary data and return normalized JSON with invoice data plus deterministic validation signals.

## What you will build

By the end of this tutorial you will have a Python script that:

1. reads an invoice from disk;
2. sends the original file through RapidAPI;
3. checks the HTTP response;
4. prints the normalized JSON;
5. captures `X-Request-ID` for troubleshooting.

## Prerequisites

- Python 3.9 or newer.
- A RapidAPI account.
- A subscription to Business Document Intelligence. The BASIC plan can be used for evaluation.
- A PDF, JPEG, PNG, or WebP invoice no larger than **5 MiB**.

RapidAPI listing:

<https://rapidapi.com/bavarianmotive-bavarianmotive-default/api/business-document-intelligence>

Use a redacted or synthetic document while learning the API. Do not commit real customer invoices or credentials to source control.

## 1. Install `requests`

Create a project directory and install the HTTP client:

```bash
python -m pip install requests
```

## 2. Put your RapidAPI key in an environment variable

Do not paste a real API key into source code.

macOS / Linux:

```bash
export RAPIDAPI_KEY="your-rapidapi-key"
```

Windows PowerShell:

```powershell
$env:RAPIDAPI_KEY = "your-rapidapi-key"
```

## 3. Create the extraction script

Save this as `extract_invoice.py`:

```python
import json
import os
import sys
import uuid
from pathlib import Path

import requests

HOST = "business-document-intelligence.p.rapidapi.com"
ENDPOINT = "/v1/invoices/extract"
MAX_BYTES = 5 * 1024 * 1024

api_key = os.environ.get("RAPIDAPI_KEY", "").strip()
if not api_key:
    raise SystemExit("RAPIDAPI_KEY is not set")

if len(sys.argv) != 2:
    raise SystemExit("Usage: python extract_invoice.py <invoice.pdf|jpg|png|webp>")

path = Path(sys.argv[1]).expanduser().resolve()
if not path.is_file():
    raise SystemExit(f"File not found: {path}")

size = path.stat().st_size
if size == 0:
    raise SystemExit("The document is empty")
if size > MAX_BYTES:
    raise SystemExit("The document exceeds the 5 MiB API limit")

request_id = f"tutorial.{uuid.uuid4().hex}"

response = requests.post(
    f"https://{HOST}{ENDPOINT}",
    headers={
        "Content-Type": "application/octet-stream",
        "X-RapidAPI-Host": HOST,
        "X-RapidAPI-Key": api_key,
        "X-Request-ID": request_id,
    },
    data=path.read_bytes(),
    timeout=90,
)

returned_request_id = response.headers.get("X-Request-ID")
if returned_request_id:
    print(f"X-Request-ID: {returned_request_id}", file=sys.stderr)

try:
    payload = response.json()
except ValueError:
    raise SystemExit(
        f"HTTP {response.status_code}: API returned a non-JSON response"
    )

if not response.ok:
    raise SystemExit(
        f"HTTP {response.status_code}:\n{json.dumps(payload, indent=2)}"
    )

print(json.dumps(payload, indent=2))
```

## 4. Run it

```bash
python extract_invoice.py ./invoice.pdf
```

The document is sent as the original binary request body. It is **not** wrapped in JSON and it is **not** base64 encoded.

The same request format works for supported PDFs, JPEGs, PNGs, and WebP files. The backend verifies the actual file signature rather than trusting only a filename extension.

## 5. Understand the response

A successful invoice extraction returns three top-level objects:

- `data` — normalized invoice fields such as vendor/customer information, invoice and PO identifiers, dates, currency, payment terms, totals, line items, and notes;
- `validation` — deterministic signals for core-field completeness and arithmetic reconciliation;
- `meta` — response schema/API metadata.

The validation object includes signals such as:

```text
core_fields_complete
missing_core_fields
totals_reconciled
line_items_reconciled
warnings
```

Missing or ambiguous source values are intended to remain `null` rather than being invented. Your application should still decide which fields are required for its own workflow.

## Why `X-Request-ID` matters

The example generates an `X-Request-ID` for every call. The API returns a request ID in the response so you can correlate a specific request when debugging an integration or reporting a reproducible processing issue.

A request ID is for correlation only. It does not make a request idempotent and it should never contain secrets or customer data.

## Common errors

| HTTP status | What to check |
| --- | --- |
| `400` | Request body is empty or invalid. |
| `413` | The document is larger than 5 MiB. |
| `415` | File format is unsupported or the declared type does not match the file signature. |
| `422` | The converted document exceeds the synchronous complexity limit. |
| `429` | Your current rate limit has been exceeded. |
| `502` | Processing failed safely or the processing result was rejected. |
| `503` | Processing or a required security control is temporarily unavailable. |
| `504` | Processing timed out after bounded retry attempts. |

When handling errors in production, inspect the JSON `error` object and retain the returned `X-Request-ID` in your application logs.

## Try the repository version

This repository also includes a reusable client and ready-to-run examples:

```bash
cd python
python -m pip install -r requirements.txt
python extract_invoice.py /path/to/invoice.pdf
```

The same client powers the receipt and classification examples:

```bash
python extract_receipt.py /path/to/receipt.png
python classify_document.py /path/to/document.pdf
```

## Next steps

Once invoice extraction is working, a common workflow is:

1. call `/v1/documents/classify` when the document type is unknown;
2. inspect `routing.supported_extraction` and `routing.recommended_endpoint`;
3. route invoices to `/v1/invoices/extract`;
4. route receipts to `/v1/receipts/extract`;
5. use the returned validation signals before writing extracted data into downstream systems.

Business Document Intelligence is designed for applications that need structured document data rather than raw OCR text.
