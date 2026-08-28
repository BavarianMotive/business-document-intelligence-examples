# cURL Examples

These commands send the original document as raw binary bytes through RapidAPI.

Set your RapidAPI key first.

macOS / Linux:

```bash
export RAPIDAPI_KEY="your-rapidapi-key"
```

Windows PowerShell:

```powershell
$env:RAPIDAPI_KEY = "your-rapidapi-key"
```

## Extract an invoice

macOS / Linux:

```bash
curl --request POST \
  --url https://business-document-intelligence.p.rapidapi.com/v1/invoices/extract \
  --header "Content-Type: application/octet-stream" \
  --header "X-RapidAPI-Host: business-document-intelligence.p.rapidapi.com" \
  --header "X-RapidAPI-Key: $RAPIDAPI_KEY" \
  --data-binary @./invoice.pdf
```

Windows PowerShell 5.1 using `curl.exe`:

```powershell
curl.exe --request POST `
  --url "https://business-document-intelligence.p.rapidapi.com/v1/invoices/extract" `
  --header "Content-Type: application/octet-stream" `
  --header "X-RapidAPI-Host: business-document-intelligence.p.rapidapi.com" `
  --header "X-RapidAPI-Key: $env:RAPIDAPI_KEY" `
  --data-binary "@invoice.pdf"
```

## Extract a receipt

```bash
curl --request POST \
  --url https://business-document-intelligence.p.rapidapi.com/v1/receipts/extract \
  --header "Content-Type: application/octet-stream" \
  --header "X-RapidAPI-Host: business-document-intelligence.p.rapidapi.com" \
  --header "X-RapidAPI-Key: $RAPIDAPI_KEY" \
  --data-binary @./receipt.png
```

## Classify a document

```bash
curl --request POST \
  --url https://business-document-intelligence.p.rapidapi.com/v1/documents/classify \
  --header "Content-Type: application/octet-stream" \
  --header "X-RapidAPI-Host: business-document-intelligence.p.rapidapi.com" \
  --header "X-RapidAPI-Key: $RAPIDAPI_KEY" \
  --data-binary @./document.pdf
```

Supported uploads are PDF, JPEG, PNG, and WebP with a maximum request body of 5 MiB. Do not JSON-wrap or base64-encode the file.
