# Business Document Intelligence Examples

Public, MIT-licensed examples and tutorials for using the **Business Document Intelligence API** through RapidAPI.

Business Document Intelligence turns invoice, receipt, and common business-document PDFs or images into structured, application-ready JSON. These examples show how to upload the original document as raw binary data, extract normalized fields, use validation signals, and classify unknown business documents.

> This repository contains consumer-side examples only. The production API implementation, provider credentials, and infrastructure remain private.

**Try the API on RapidAPI:** <https://rapidapi.com/bavarianmotive-bavarianmotive-default/api/business-document-intelligence>

## What you can build

- Invoice PDF/image to normalized JSON.
- Receipt PDF/image to normalized JSON.
- Business-document classification and routing.
- Accounts-payable and expense-processing workflows.
- SaaS and automation integrations that need predictable structured data instead of raw OCR text.

## API endpoints

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

Upload the original document as raw binary bytes.

- PDF
- JPEG
- PNG
- WebP
- Maximum request body: **5 MiB**

The examples use `Content-Type: application/octet-stream`, which works across the supported document formats. Do not JSON-wrap or base64-encode document uploads.

## Quick start

### 1. Subscribe on RapidAPI

Open the [Business Document Intelligence listing](https://rapidapi.com/bavarianmotive-bavarianmotive-default/api/business-document-intelligence), select a plan, and copy your consumer API key from RapidAPI's generated code examples.

The BASIC plan can be used for evaluation.

Never commit your RapidAPI key to source control.

### 2. Set your API key

macOS / Linux:

```bash
export RAPIDAPI_KEY="your-rapidapi-key"
```

Windows PowerShell:

```powershell
$env:RAPIDAPI_KEY = "your-rapidapi-key"
```

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

cURL and Windows PowerShell 5.1 examples are available in [`curl/README.md`](curl/README.md).

The Python and Node scripts print the API JSON response to stdout and show the returned `X-Request-ID` on stderr when available.

## Examples

### Python

- [`python/extract_invoice.py`](python/extract_invoice.py) — invoice extraction
- [`python/extract_receipt.py`](python/extract_receipt.py) — receipt extraction
- [`python/classify_document.py`](python/classify_document.py) — document classification
- [`python/bdi_client.py`](python/bdi_client.py) — reusable API client

### Node.js

- [`node/extract-invoice.mjs`](node/extract-invoice.mjs) — invoice extraction
- [`node/extract-receipt.mjs`](node/extract-receipt.mjs) — receipt extraction
- [`node/classify-document.mjs`](node/classify-document.mjs) — document classification
- [`node/bdi-client.mjs`](node/bdi-client.mjs) — reusable API client

### cURL / PowerShell

See [`curl/README.md`](curl/README.md) for cURL and Windows PowerShell 5.1 examples.

## Tutorial

Start with:

**[Convert an Invoice PDF to JSON with Python](docs/tutorial-python-invoice-to-json.md)**

A concise version of this quickstart is also published in the **Tutorials** section of the RapidAPI listing.

## What successful responses contain

Extraction responses use stable, normalized JSON rather than returning only raw OCR text.

For invoice and receipt extraction, successful responses include:

- `data` — normalized extracted fields;
- `validation` — deterministic completeness and reconciliation signals;
- `meta` — schema and API version metadata.

Missing or ambiguous source values are intended to remain `null` rather than being invented. Your application should still decide which fields are required for its own workflow.

## Error handling

Common HTTP responses include:

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

Always check the HTTP status before consuming a response as successful output. Keep the returned `X-Request-ID` when it is useful for troubleshooting.

## Security and privacy

Treat invoices and receipts as potentially sensitive business data.

- Do not commit real customer documents, API keys, secrets, or unredacted sensitive samples.
- Use redacted or synthetic documents for demonstrations and bug reports.
- Keep API credentials in environment variables or a secrets manager.
- Do not post credentials or sensitive source documents in public issues.
- The API is designed to return at most payment-card last four for receipt payment data and to reject full PAN-like leakage.

Before material repository updates or releases, run:

```bash
python tools/pre_public_security_check.py
```

This public repository uses protected `main` branch rules plus GitHub security features including secret protection/push protection, CodeQL, Dependabot, and private vulnerability reporting.

See [`SECURITY.md`](SECURITY.md) for vulnerability-reporting guidance and [`docs/PUBLIC_RELEASE_SECURITY_CHECKLIST.md`](docs/PUBLIC_RELEASE_SECURITY_CHECKLIST.md) for the release-security checklist.

## Repository layout

```text
.
├── python/                         # Python examples using requests
├── node/                           # Node.js 18+ examples using built-in fetch
├── curl/                           # cURL + Windows PowerShell examples
├── docs/                           # Tutorials and release documentation
├── tools/
│   └── pre_public_security_check.py
├── samples/                        # Local test documents; files are gitignored
├── SECURITY.md
├── LICENSE                         # MIT license for this examples repository
├── .env.example
└── .gitignore
```

## License

The code and documentation in this examples repository are available under the [MIT License](LICENSE).

The MIT license applies to this public consumer-examples repository only. The production Business Document Intelligence API implementation remains private and proprietary.

## Product

Business Document Intelligence is provided by **BavarianMotive** and distributed through RapidAPI.
