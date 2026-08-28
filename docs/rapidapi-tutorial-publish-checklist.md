# RapidAPI Tutorial Publishing Checklist

This is the release checklist for the first public Business Document Intelligence tutorial.

## Tutorial

**Title**

```text
Convert an Invoice PDF to JSON with Python
```

**Source content**

Use:

```text
docs/tutorial-python-invoice-to-json.md
```

The tutorial is intentionally self-contained so it can be published while this examples repository is still private.

## Before publishing

- Confirm the API listing is Public.
- Confirm the BASIC plan is available for evaluation.
- Confirm the tutorial calls the RapidAPI hostname, not the provider-only Workers hostname.
- Confirm no real RapidAPI key appears in the tutorial.
- Confirm the request body is documented as raw binary `application/octet-stream`.
- Confirm the 5 MiB maximum and supported PDF/JPEG/PNG/WebP formats are still current.
- Confirm `/v1/invoices/extract` remains the invoice extraction route.
- Preview all Markdown and code blocks in RapidAPI before publishing.
- If adding a banner image, use a wide image that communicates invoice-to-JSON clearly and does not contain credentials or customer documents.

## Publish flow in RapidAPI

1. Open the public Business Document Intelligence listing.
2. Open the **Tutorials** tab.
3. Choose **Add Tutorial**.
4. Use the title above.
5. Paste the Markdown body from `docs/tutorial-python-invoice-to-json.md`.
6. Optionally add a wide banner image URL.
7. Save as a Draft first and preview it.
8. Check headings, tables, JSON, Python, Bash, and PowerShell formatting.
9. Publish the tutorial when the preview is clean.

## Spotlight after the tutorial is public

Use the recommended copy from:

```text
docs/spotlight-copy.md
```

Set the Spotlight destination to the **published RapidAPI tutorial URL**, not this private GitHub repository.

Recommended Spotlight title:

```text
Convert Invoice PDFs to JSON with Python
```

Recommended CTA:

```text
Read the tutorial
```

## Public examples repository

Do not make this repository Public solely to publish the first tutorial. The tutorial does not depend on it.

After the tutorial and Spotlight are live, the repository can be reviewed one more time for secrets, samples, links, and presentation before changing its visibility to Public.
