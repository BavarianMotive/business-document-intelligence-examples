# Security Policy

## Scope

This repository contains **consumer-side examples and tutorials** for the Business Document Intelligence API. The production API implementation, provider credentials, infrastructure configuration, and internal security controls are intentionally kept outside this repository.

Security issues in the examples repository can still matter, especially if they could cause users to expose API keys, upload documents unsafely, trust invalid responses, or copy insecure integration patterns.

## Reporting a security issue

Please **do not open a public GitHub issue** for a suspected vulnerability, leaked credential, or sensitive document exposure.

Use the private provider/support contact available from the Business Document Intelligence listing on RapidAPI and clearly mark the message as a **security report**. Include only the minimum information needed to reproduce the issue.

Do not send:

- RapidAPI keys or provider secrets;
- passwords or session tokens;
- real customer invoices or receipts;
- full payment-card numbers;
- other unredacted confidential business data.

A request-specific `X-Request-ID` may be included when it helps identify an API call and does not itself contain sensitive information.

## Credential handling

Examples in this repository read the RapidAPI consumer key from the `RAPIDAPI_KEY` environment variable. Never hard-code a live key in source code, examples, screenshots, shell history intended for publication, or committed `.env` files.

If a credential is accidentally committed or published, treat it as compromised: revoke or rotate it immediately before attempting repository-history cleanup.

## Document handling

Use synthetic or thoroughly redacted documents for examples, screenshots, tutorials, tests, and bug reports. Local files placed in `samples/` are intentionally ignored by Git.

## Production boundary

Consumers should call the RapidAPI marketplace hostname documented in this repository. Do not attempt to discover, document, or bypass BavarianMotive's provider-only backend or marketplace authentication controls.

## Supported versions

Security guidance in this repository tracks the currently documented public Business Document Intelligence API. Older example revisions may no longer represent the recommended integration pattern.
