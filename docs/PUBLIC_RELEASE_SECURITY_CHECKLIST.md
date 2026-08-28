# Public Release Security Checklist

Use this checklist immediately before and after changing this examples repository from Private to Public.

## Before changing visibility

1. Run the local guard from the repository root:

   ```bash
   python tools/pre_public_security_check.py
   ```

   The check should exit successfully and report `Pre-public security check PASSED.`

2. Review `git status` and `git diff` locally. Do not publish untracked or newly staged files without reviewing them.
3. Confirm that no real invoices, receipts, screenshots containing credentials, `.env` files, private keys, certificate files, or other customer documents are tracked.
4. Confirm all code calls the documented RapidAPI marketplace hostname rather than a provider-only backend hostname.
5. Confirm examples read the consumer key from `RAPIDAPI_KEY`; no live key should appear in source, docs, screenshots, examples, commit messages, issues, or pull requests.
6. Confirm the production implementation remains in its separate Private repository.
7. Review repository history for accidental credentials or confidential documents. If a live credential was ever committed, rotate/revoke it before publication even if the file was later deleted.
8. Review `SECURITY.md` and make sure the reporting instructions are still correct.
9. Review dependency versions. The Python example dependency is intentionally pinned; Dependabot is configured to propose updates.

## Immediately after changing visibility to Public

In GitHub repository **Settings → Advanced Security** (wording can vary):

1. Confirm **Secret scanning** is enabled. GitHub provides secret scanning for public repositories.
2. Enable **Push protection** so supported secrets can be blocked before they are pushed.
3. Enable **Dependabot alerts** and keep the dependency graph enabled.
4. Enable **Private vulnerability reporting** so researchers can report security issues without opening a public issue.
5. Review the **Security** / **Security and quality** tab for any newly generated alerts after GitHub scans the now-public history.

## Main branch controls

Protect `main` from accidental destructive changes:

- prohibit force pushes;
- prohibit branch deletion;
- require changes to go through a pull request when practical;
- do not require an approval count that a one-person repository cannot satisfy;
- add required status checks only after the repository has a reliable CI job to require.

The examples repository previously encountered a GitHub Actions job that failed before useful validation steps ran, so do not make that broken workflow a required status check.

## Public-content rule

Only consumer-facing material belongs here. Do not publish:

- provider secrets or secret names that are unnecessary for consumers;
- direct provider/backend origins;
- internal Cloudflare configuration or account identifiers;
- production source code;
- real customer documents;
- raw production logs;
- credentials, tokens, cookies, session material, or recovery codes.

## If something sensitive is found

1. Treat exposed credentials as compromised and rotate/revoke them immediately.
2. Remove the sensitive material from the current repository state.
3. Clean repository history when appropriate, while assuming any already-public secret may have been copied.
4. Review access/session logs for suspicious use.
5. Document the incident privately and update the guardrails if a new failure mode was discovered.
