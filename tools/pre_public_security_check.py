from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_TRACKED_PATHS = {
    ".env",
    "credentials.json",
    "secrets.json",
}

FORBIDDEN_SUFFIXES = {
    ".pem",
    ".key",
    ".p12",
    ".pfx",
    ".jks",
    ".pdf",
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}

SUSPICIOUS_PATTERNS = [
    (
        re.compile(r"RAPIDAPI_KEY\s*=\s*(?!your-rapidapi-key(?:\s|$))([^\s#]+)", re.IGNORECASE),
        "non-placeholder RAPIDAPI_KEY assignment",
    ),
    (
        re.compile(r"(?i)(?:api[_-]?key|token|secret|password)\s*[:=]\s*['\"][A-Za-z0-9_./+=-]{20,}['\"]"),
        "possible hard-coded credential",
    ),
    (
        re.compile(r"(?i)authorization\s*[:=]\s*['\"]bearer\s+[A-Za-z0-9_.-]{20,}['\"]"),
        "possible hard-coded bearer token",
    ),
    (
        re.compile(r"https?://[^\s'\"`]+\.workers\.dev", re.IGNORECASE),
        "direct Workers provider hostname",
    ),
    (
        re.compile(r"rapidapi[_-]?proxy[_-]?secret", re.IGNORECASE),
        "provider-only marketplace secret name",
    ),
]

TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".py",
    ".mjs",
    ".js",
    ".json",
    ".yaml",
    ".yml",
    ".example",
    "",
}


def tracked_files() -> list[Path]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"Unable to list tracked files with git: {exc}")

    entries = [item for item in result.stdout.decode("utf-8").split("\0") if item]
    return [Path(item) for item in entries]


def main() -> int:
    failures: list[str] = []

    for relative_path in tracked_files():
        normalized = relative_path.as_posix()
        lower_name = relative_path.name.lower()
        suffix = relative_path.suffix.lower()

        if normalized in FORBIDDEN_TRACKED_PATHS:
            failures.append(f"forbidden tracked path: {normalized}")

        if suffix in FORBIDDEN_SUFFIXES:
            failures.append(f"review required for tracked binary/sensitive file: {normalized}")

        if lower_name.startswith(".env") and normalized != ".env.example":
            failures.append(f"environment file must not be tracked: {normalized}")

        full_path = ROOT / relative_path
        if not full_path.is_file() or suffix not in TEXT_SUFFIXES:
            continue

        try:
            text = full_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            failures.append(f"non-UTF-8 tracked file requires manual review: {normalized}")
            continue

        for pattern, description in SUSPICIOUS_PATTERNS:
            if pattern.search(text):
                failures.append(f"{description} found in {normalized}")

    if failures:
        print("Pre-public security check FAILED:")
        for failure in sorted(set(failures)):
            print(f"- {failure}")
        return 1

    print("Pre-public security check PASSED.")
    print("No tracked document samples, key material, direct provider hostnames, or obvious hard-coded credentials were detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
