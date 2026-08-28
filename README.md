# Business Document Intelligence Examples

Practical examples and tutorials for using the **Business Document Intelligence API** through RapidAPI.

Business Document Intelligence turns invoices, receipts, and common business documents into structured, application-ready JSON. The examples in this repository show how to send original PDF or image files as raw binary data and work with normalized API responses.

> This repository contains consumer-side examples only. The production API implementation remains private.

**RapidAPI:** <https://rapidapi.com/bavarianmotive-bavarianmotive-default/api/business-document-intelligence>

## What you can do

- Extract normalized data from invoices.
- Extract normalized data from receipts.
- Classify invoices, receipts, purchase orders, quotes, bills, statements, and other business documents.
- Use `X-Request-ID` to correlate a request with support or application logs.

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

Subscribe to **Business Document Intelligence** on RapidAPI and copy your consumer API key from RapidAPI's generated code examples.

Never commit your RapidAPI key to this repository.

### 2. Set your API key

macOS / Linux:

```bash
export RAPIDAPI_KEY="your-rapidapi-key"
```

Windows PowerShell:

```powershell
$env:RAPIDAPI_KEY = "your-rapidapi-key"
```

### 3. Pick an example

Python:

```bash
cd python
python -m pip install -r requirements.txt
python extract_invoice.py /path/to/invoice.pdf
```

Node.js 18+:

```bash
cd node
node extract-invoice.mjs /path/to/invoice.pdf
```

cURL and Windows PowerShell 5.1 examples are available in [`curl/README.md`](curl/README.md).

The Python and Node scripts print the API's JSON response to stdout and show the returned request ID on stderr when available.

## Repository layout

```text
.
├── python/                         # Python examples using requests
├── node/                           # Node.js 18+ examples using built-in fetch
├── curl/                           # cURL + Windows PowerShell examples
├── docs/
│   ├── tutorial-python-invoice-to-json.md
│   └── spotlight-copy.md
├── samples/                        # Put local test documents here; files are gitignored
├── .env.example
└── .gitignore
```

## Security and privacy

Treat invoices and receipts as potentially sensitive business data.

- Do not commit real customer documents, API keys, secrets, or unredacted sensitive samples.
- Use redacted or synthetic documents for demonstrations.
- Keep API credentials in environment variables or a secrets manager.
- When asking for support, include the `X-Request-ID` when useful, but do not post credentials or sensitive source documents in a public issue.

The API is designed to return at most payment-card last four for receipt payment data and to reject full PAN-like leakage.

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

Always check the HTTP status before consuming a response as successful output.

## Tutorials

Start with:

**[How to extract invoice data from a PDF to JSON with Python](docs/tutorial-python-invoice-to-json.md)**

Additional receipt and classification tutorials can be added as the examples evolve.

## Product

Business Document Intelligence is provided by **BavarianMotive** and distributed through RapidAPI.
