# Business Document Intelligence Examples

Examples for the **Business Document Intelligence API** on RapidAPI.

The API classifies common business documents and extracts normalized JSON from invoices and receipts. This repository contains Python, Node.js, cURL, and PowerShell examples for calling it with real PDF or image files.

**Try the API:** <https://rapidapi.com/bavarianmotive-bavarianmotive-default/api/business-document-intelligence>

> This repository contains consumer examples only. The production API implementation remains private.

## What it does

- Extract invoice fields, totals, line items, vendor/customer details, and validation signals.
- Extract normalized receipt data.
- Classify invoices, receipts, purchase orders, quotes, bills, statements, and other business documents.
- Return `X-Request-ID` values that can be kept for troubleshooting.

## Quick start

### 1. Subscribe on RapidAPI

Open the [Business Document Intelligence listing](https://rapidapi.com/bavarianmotive-bavarianmotive-default/api/business-document-intelligence) and select a plan. The BASIC plan is available for evaluation.

### 2. Set your API key

macOS / Linux:

```bash
export RAPIDAPI_KEY="your-rapidapi-key"
```

Windows PowerShell:

```powershell
$env:RAPIDAPI_KEY = "your-rapidapi-key"
```

Do not commit a live RapidAPI key to source control.

### 3. Run an example

Python invoice extraction:

```bash
cd python
python -m pip install -r requirements.txt
python extract_invoice.py /path/to/invoice.pdf
```

Node.js 18+ invoice extraction:

```bash
cd node
node extract-invoice.mjs /path/to/invoice.pdf
```

The scripts print the JSON response to stdout and the returned request ID to stderr when available.

## Concrete example

A simple synthetic invoice such as:

```text
Northwind Office Supply
Invoice INV-1042
2 x Office supplies @ $50.00
Subtotal: $100.00
Tax: $6.25
Total: $106.25
```

maps into fields such as `vendor`, `invoice_number`, `line_items`, `subtotal`, `tax`, and `total`, together with validation and schema metadata.

See **[the full synthetic input/output example](docs/example-invoice.md)** for the corresponding JSON shape.

## Endpoints

| Purpose | Method | Endpoint |
| --- | --- | --- |
| Health check | `GET` | `/health` |
| Classify a document | `POST` | `/v1/documents/classify` |
| Extract an invoice | `POST` | `/v1/invoices/extract` |
| Extract a receipt | `POST` | `/v1/receipts/extract` |

RapidAPI host:

```text
business-document-intelligence.p.rapidapi.com
```

## Supported files

Send the original file as raw binary data with `Content-Type: application/octet-stream`.

- PDF
- JPEG
- PNG
- WebP
- Maximum request body: **5 MiB**

Do not JSON-wrap or base64-encode document uploads.

## Examples

### Python

- [`python/extract_invoice.py`](python/extract_invoice.py) — invoice extraction
- [`python/extract_receipt.py`](python/extract_receipt.py) — receipt extraction
- [`python/classify_document.py`](python/classify_document.py) — document classification
- [`python/bdi_client.py`](python/bdi_client.py) — reusable client

### Node.js

- [`node/extract-invoice.mjs`](node/extract-invoice.mjs) — invoice extraction
- [`node/extract-receipt.mjs`](node/extract-receipt.mjs) — receipt extraction
- [`node/classify-document.mjs`](node/classify-document.mjs) — document classification
- [`node/bdi-client.mjs`](node/bdi-client.mjs) — reusable client

### cURL and PowerShell

See [`curl/README.md`](curl/README.md).

## Tutorial

The longer walkthrough is **[Convert an Invoice PDF to JSON with Python](docs/tutorial-python-invoice-to-json.md)**. A shorter version is also published in the Tutorials section of the RapidAPI listing.

## Response structure

Successful invoice and receipt extractions contain three top-level sections:

- `data` — extracted fields;
- `validation` — completeness and reconciliation checks;
- `meta` — schema and API version metadata.

Missing or ambiguous source values may be returned as `null`. Applications should decide which fields are required for their own workflows.

## Common errors

| Status | Meaning |
| --- | --- |
| `400` | Invalid or empty request |
| `413` | Document exceeds 5 MiB |
| `415` | Unsupported file or signature mismatch |
| `422` | Document is too complex for synchronous processing |
| `429` | Rate limit exceeded |
| `502` | Processing failed safely |
| `503` | Processing temporarily unavailable |
| `504` | Processing timed out after bounded retries |

Always check the HTTP status before treating a response as successful.

## Security

Use synthetic or redacted documents in examples and bug reports. Keep credentials in environment variables or a secrets manager, and never post API keys or sensitive source documents in public issues.

Before material updates, run:

```bash
python tools/release_security_check.py
```

See [`SECURITY.md`](SECURITY.md) for vulnerability-reporting guidance.

## License

The examples and documentation in this repository are available under the [MIT License](LICENSE). The production Business Document Intelligence API implementation is separate and proprietary.

Business Document Intelligence is provided by **BavarianMotive** and distributed through RapidAPI.
