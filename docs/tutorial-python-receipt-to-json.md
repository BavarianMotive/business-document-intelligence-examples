# Receipt OCR API: Convert Receipt Images to Structured JSON with Python

Receipt OCR is only useful when your application can turn the result into predictable fields. **Business Document Intelligence** goes beyond raw text by returning normalized receipt JSON with merchant details, transaction data, line items, totals, payment information, and deterministic validation signals.

In this tutorial, you will send a receipt image or PDF through the **Business Document Intelligence API** on RapidAPI and receive structured JSON that is ready for downstream application logic.

This is useful for expense tracking, bookkeeping automation, contractor/job-costing software, accounting workflows, SaaS products, and internal business tools that need receipt data without maintaining OCR parsing glue.

## What you will build

By the end of the tutorial, you will have a Python script that:

1. reads a receipt from disk;
2. sends the original PDF or image bytes through RapidAPI;
3. checks the response;
4. prints normalized receipt JSON;
5. captures `X-Request-ID` for troubleshooting;
6. uses validation signals to decide whether the result is ready for automation.

## Prerequisites

- Python 3.9 or newer.
- A RapidAPI account.
- A subscription to **Business Document Intelligence**. The BASIC plan can be used for evaluation.
- A PDF, JPEG, PNG, or WebP receipt no larger than **5 MiB**.

RapidAPI listing:

<https://rapidapi.com/bavarianmotive-bavarianmotive-default/api/business-document-intelligence>

Use a synthetic or redacted receipt while learning the API. Do not commit live API keys or sensitive customer documents to source control.

## 1. Install `requests`

```bash
python -m pip install requests
```

## 2. Store your RapidAPI key securely

macOS / Linux:

```bash
export RAPIDAPI_KEY="your-rapidapi-key"
```

Windows PowerShell:

```powershell
$env:RAPIDAPI_KEY = "your-rapidapi-key"
```

## 3. Create the receipt parser

Save this as `extract_receipt.py`:

```python
import json
import os
import sys
import uuid
from pathlib import Path

import requests

HOST = "business-document-intelligence.p.rapidapi.com"
ENDPOINT = "/v1/receipts/extract"
MAX_BYTES = 5 * 1024 * 1024

api_key = os.environ.get("RAPIDAPI_KEY", "").strip()
if not api_key:
    raise SystemExit("RAPIDAPI_KEY is not set")

if len(sys.argv) != 2:
    raise SystemExit("Usage: python extract_receipt.py <receipt.pdf|jpg|png|webp>")

path = Path(sys.argv[1]).expanduser().resolve()
if not path.is_file():
    raise SystemExit(f"File not found: {path}")

size = path.stat().st_size
if size == 0:
    raise SystemExit("The document is empty")
if size > MAX_BYTES:
    raise SystemExit("The document exceeds the 5 MiB API limit")

request_id = f"receipt-tutorial.{uuid.uuid4().hex}"

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
python extract_receipt.py ./receipt.png
```

The receipt is sent as the original binary request body using:

```text
Content-Type: application/octet-stream
```

Do not JSON-wrap or base64-encode the document. The API accepts PDF, JPEG, PNG, and WebP files and verifies the document signature before processing.

## 5. Understand the receipt JSON

Successful receipt extraction contains three top-level objects:

- `data` — normalized receipt fields;
- `validation` — deterministic completeness and arithmetic checks;
- `meta` — schema/API version metadata.

A representative response looks like this:

```json
{
  "data": {
    "document_type": "receipt",
    "merchant": {
      "name": "EXAMPLE MARKET",
      "address": "100 Main Street, Boston, MA 02110",
      "tax_id": null,
      "phone": null
    },
    "receipt_number": "R-1042",
    "transaction_date": "2026-08-28",
    "transaction_time": "14:35",
    "currency": "USD",
    "payment_method": "Visa",
    "payment_card_last4": "4242",
    "subtotal": 20.0,
    "tax": 1.6,
    "tip": 2.0,
    "discount": 1.0,
    "total": 22.6,
    "line_items": [
      {
        "description": "Sparkling Water",
        "sku": null,
        "quantity": 2,
        "unit_price": 3.0,
        "amount": 6.0
      },
      {
        "description": "Sandwich",
        "sku": null,
        "quantity": 1,
        "unit_price": 12.0,
        "amount": 12.0
      },
      {
        "description": "Fruit",
        "sku": null,
        "quantity": 1,
        "unit_price": 2.0,
        "amount": 2.0
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
    "schema_version": "receipt.v1",
    "api_version": "0.6.0"
  }
}
```

See **[the full synthetic receipt example](example-receipt.md)**.

## 6. Important receipt fields

The receipt schema can include:

- merchant name, address, tax ID, and phone;
- receipt or transaction identifier;
- transaction date and time;
- currency;
- payment method or card brand;
- payment-card last four;
- subtotal, tax, tip, discount, and total;
- line-item descriptions, quantities, prices, and amounts;
- short material notes.

Missing or ambiguous source values may be returned as `null` instead of being guessed.

## 7. Use validation before automation

The API returns deterministic validation information such as:

```text
core_fields_complete
missing_core_fields
totals_reconciled
line_items_reconciled
warnings
```

For example, if the receipt has a subtotal, tax, tip, discount, and total, the API can report whether those values reconcile arithmetically. If line-item amounts and a subtotal are available, it can also report whether the item amounts reconcile to the subtotal.

Your application can use those signals to decide whether to continue automatically or route the receipt for review.

## 8. Payment-card privacy

Receipt extraction is intentionally conservative around payment-card data.

The API exposes at most:

```text
payment_card_last4
```

When the final four digits are visible, they can be returned as a four-digit string such as `"4242"`. Full payment-card numbers are not part of the receipt response contract.

## 9. Why `X-Request-ID` matters

Every request can include an `X-Request-ID`, and the API returns a request ID in the response. Keep it with your application logs when troubleshooting a specific extraction.

Request IDs are for correlation only. They do not provide idempotent replay or duplicate suppression, and they should not contain secrets or customer information.

## Common errors

| HTTP status | What to check |
| --- | --- |
| `400` | Request body is empty or invalid. |
| `413` | The document exceeds the 5 MiB limit. |
| `415` | The file format is unsupported or the bytes do not match the declared/supported type. |
| `422` | The converted document is too complex for synchronous processing. |
| `429` | The current rate limit has been exceeded. |
| `502` | Processing failed safely or the result could not be validated. |
| `503` | Processing is temporarily unavailable. |
| `504` | Processing timed out after bounded retry attempts. |

For `429`, `503`, and `504`, check `Retry-After` when present. Do not automatically retry `400`, `413`, `415`, or most `422` responses without changing the input.

## Unknown document type? Classify first

If your application receives mixed documents, call:

```text
POST /v1/documents/classify
```

The classifier recognizes invoices, receipts, purchase orders, quotes, bills, statements, and other documents. For supported extraction types, it returns a routing hint such as:

```json
{
  "routing": {
    "supported_extraction": true,
    "recommended_endpoint": "/v1/receipts/extract"
  }
}
```

A useful workflow is:

```text
Upload document
    ↓
POST /v1/documents/classify
    ↓
Read recommended_endpoint
    ↓
POST /v1/receipts/extract
    ↓
Use normalized + validated JSON
```

Not every classified document type currently has a corresponding extraction endpoint.

## Next step

You now have a working **receipt image to JSON** flow in Python through RapidAPI.

Try the same API with different synthetic or redacted receipt layouts, then use the returned validation signals and `X-Request-ID` in your own workflow.

If your application also processes invoices, see **[Convert an Invoice PDF to JSON with Python](tutorial-python-invoice-to-json.md)**.
