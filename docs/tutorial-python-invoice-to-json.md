# Convert an Invoice PDF to JSON with Python

If your application receives invoices as PDFs or images, raw OCR text is usually only the first step. Production workflows need predictable fields that software can validate, store, and route.

In this tutorial, you will use the **Business Document Intelligence API** on RapidAPI as an invoice parser: upload an invoice as raw binary data and receive normalized JSON containing vendor/customer details, invoice identifiers, dates, totals, line items, and deterministic validation signals.

This is useful for accounts-payable automation, expense workflows, SaaS products, internal business tools, and any application that needs to turn invoice PDFs into structured JSON.

## What you will build

By the end of the tutorial, you will have a Python script that:

1. reads an invoice from disk;
2. sends the original file through RapidAPI;
3. checks the HTTP response;
4. prints normalized invoice JSON;
5. captures `X-Request-ID` for troubleshooting.

## Prerequisites

- Python 3.9 or newer.
- A RapidAPI account.
- A subscription to **Business Document Intelligence**. The BASIC plan can be used for evaluation.
- A PDF, JPEG, PNG, or WebP invoice no larger than **5 MiB**.

RapidAPI listing:

<https://rapidapi.com/bavarianmotive-bavarianmotive-default/api/business-document-intelligence>

Use a redacted or synthetic invoice while learning the API. Do not commit real customer documents or API credentials to source control.

## 1. Install the Python HTTP client

Install `requests`:

```bash
python -m pip install requests
```

## 2. Store your RapidAPI key in an environment variable

Do not hard-code a real API key into your script.

macOS / Linux:

```bash
export RAPIDAPI_KEY="your-rapidapi-key"
```

Windows PowerShell:

```powershell
$env:RAPIDAPI_KEY = "your-rapidapi-key"
```

## 3. Create the invoice extraction script

Save the following as `extract_invoice.py`:

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

## 4. Run the parser

```bash
python extract_invoice.py ./invoice.pdf
```

The document is sent as the original binary request body. It is **not** JSON-wrapped and it is **not** base64 encoded.

The same request format works with supported PDFs, JPEGs, PNGs, and WebP images. The backend verifies the actual file signature instead of trusting only the filename extension.

## 5. Understand the JSON response

A successful invoice extraction contains three top-level objects:

- `data` — normalized invoice fields;
- `validation` — deterministic completeness and arithmetic checks;
- `meta` — schema/API version metadata.

A representative response looks like this. The values below are illustrative; your output depends on the source document.

```json
{
  "data": {
    "document_type": "invoice",
    "vendor": {
      "name": "Northwind Office Supply",
      "address": "100 Market Street, Boston, MA 02110",
      "tax_id": null,
      "email": "billing@example.com",
      "phone": null
    },
    "customer": {
      "name": "Example Company",
      "address": null,
      "tax_id": null,
      "email": null,
      "phone": null
    },
    "invoice_number": "INV-1042",
    "purchase_order_number": "PO-818",
    "invoice_date": "2026-08-15",
    "due_date": "2026-09-14",
    "currency": "USD",
    "payment_terms": "Net 30",
    "subtotal": 100.0,
    "tax": 6.25,
    "shipping": 0.0,
    "discount": 0.0,
    "total": 106.25,
    "amount_due": 106.25,
    "line_items": [
      {
        "description": "Office supplies",
        "sku": "SUP-100",
        "quantity": 2,
        "unit_price": 50.0,
        "amount": 100.0,
        "tax_amount": null
      }
    ],
    "notes": null
  },
  "validation": {
    "core_fields_complete": true,
    "missing_core_fields": [],
    "totals_reconciled": true,
    "line_items_reconciled": true,
    "warnings": []
  },
  "meta": {
    "schema_version": "invoice.v1",
    "api_version": "0.6.0"
  }
}
```

Invoice data can include vendor/customer information, invoice and purchase-order identifiers, dates, currency, payment terms, totals, line items, and notes.

Missing or ambiguous source values are intended to remain `null` rather than being invented. Your application should still decide which fields are required for its own workflow.

## 6. Use the validation signals

The API does more than return extracted text. The `validation` object contains signals that can help your application decide whether a document should continue automatically or be reviewed.

Important fields include:

```text
core_fields_complete
missing_core_fields
totals_reconciled
line_items_reconciled
warnings
```

For example, you might automatically accept an invoice only when the fields you require are present and the relevant totals reconcile. Treat these signals as application inputs, not as a guarantee that every source document is correct.

## Why `X-Request-ID` matters

The example generates an `X-Request-ID` for every call. The API returns a request ID in the response so you can correlate a specific request while debugging an integration or reporting a reproducible processing issue.

A request ID is for correlation only. It does not make a request idempotent, and it should never contain secrets or customer data.

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

For production integrations, inspect the JSON `error` object and retain the returned `X-Request-ID` in your application logs.

## Unknown document type? Classify first

If your application receives a mixed stream of business documents, call:

```text
POST /v1/documents/classify
```

The classifier recognizes invoices, receipts, purchase orders, quotes, bills, statements, and other documents. When extraction is supported, the response includes a routing hint such as:

```json
{
  "routing": {
    "supported_extraction": true,
    "recommended_endpoint": "/v1/invoices/extract"
  }
}
```

A common workflow is therefore:

1. classify an unknown document;
2. inspect `routing.supported_extraction`;
3. send invoices to `/v1/invoices/extract`;
4. send receipts to `/v1/receipts/extract`;
5. use the validation signals before writing data into downstream systems.

## Next step

You now have a working **invoice PDF to JSON** flow in Python through RapidAPI.

Try the same approach with a synthetic receipt using `/v1/receipts/extract`, or use `/v1/documents/classify` when the incoming document type is unknown.

Business Document Intelligence is designed for developers who need structured, application-ready business document data rather than raw OCR text.
