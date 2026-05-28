#!/usr/bin/env python3
"""Handcraft pre-flight detection.

Single-shot scan of the current project + host. Prints JSON to stdout.
Writes no state — the model consumes the output live each turn it needs it.

The model renders the user-facing banner from the JSON. This script makes no
UI decisions — it only reports facts.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

# (kind, scope-glob, language hint)
LSP_CANDIDATES = [
    ("pyright", "**/*.py", "python"),
    ("mypy", "**/*.py", "python"),
    ("tsserver", "**/*.{ts,tsx,js,jsx}", "ts/js"),
    ("deno", "**/*.{ts,tsx,js,jsx}", "ts/js"),
    ("rust-analyzer", "**/*.rs", "rust"),
    ("gopls", "**/*.go", "go"),
]

FORMATTER_CANDIDATES = [
    ("ruff", "**/*.py"),
    ("black", "**/*.py"),
    ("prettier", "**/*.{ts,tsx,js,jsx,json,md,css}"),
    ("eslint", "**/*.{ts,tsx,js,jsx}"),
    ("rustfmt", "**/*.rs"),
    ("gofmt", "**/*.go"),
]

TEST_RUNNER_CANDIDATES = [
    ("pytest", "**/*.py"),
    ("jest", "**/*.{ts,tsx,js,jsx}"),
    ("vitest", "**/*.{ts,tsx,js,jsx}"),
    ("cargo", "**/*.rs"),   # cargo test
    ("go", "**/*.go"),      # go test
]

CONVENTION_FILES = [
    "CLAUDE.md",
    "AGENTS.md",
    ".cursorrules",
    ".aider.conf.yml",
    "GEMINI.md",
]

LINTER_CONFIG_FILES = [
    "ruff.toml",
    ".eslintrc",
    ".eslintrc.js",
    ".eslintrc.json",
    ".eslintrc.yml",
    ".prettierrc",
    ".prettierrc.json",
    "pyproject.toml",   # only count if it has [tool.*]
]


def detect_coding_guidelines(cwd: Path) -> list[dict]:
    out: list[dict] = []
    for name in CONVENTION_FILES:
        p = cwd / name
        if p.is_file():
            out.append({
                "kind": "convention",
                "path": str(p),
                "rule_count": sum(1 for line in p.read_text(errors="ignore").splitlines() if line.strip()),
                "mtime": datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc).isoformat(),
            })
    for name in LINTER_CONFIG_FILES:
        p = cwd / name
        if not p.is_file():
            continue
        if name == "pyproject.toml":
            text = p.read_text(errors="ignore")
            if "[tool." not in text:
                continue
        out.append({
            "kind": "linter_config",
            "path": str(p),
            "rule_count": 0,
            "mtime": datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc).isoformat(),
        })
    return out


def detect_lsps() -> list[dict]:
    return [
        {"kind": kind, "scope": scope, "language": lang, "ok": True}
        for kind, scope, lang in LSP_CANDIDATES
        if shutil.which(kind)
    ]


def detect_formatters() -> list[dict]:
    return [
        {"kind": kind, "scope": scope, "ok": True}
        for kind, scope in FORMATTER_CANDIDATES
        if shutil.which(kind)
    ]


def detect_test_runners() -> list[dict]:
    return [
        {"kind": kind, "scope": scope, "ok": True}
        for kind, scope in TEST_RUNNER_CANDIDATES
        if shutil.which(kind)
    ]


def detect_docs_access() -> list[dict]:
    """Conservative — only reports what this script can verify.

    MCP servers can't be enumerated from here; the model knows its own MCP
    list and should augment this. Web fetch is assumed if the host exposes
    it (also model's job to confirm).
    """
    out: list[dict] = []
    if (Path.home() / ".claude").is_dir():
        out.append({"kind": "host_hint", "name": "claude_code_dir_present", "ok": True})
    return out


def scan(cwd: Path) -> dict:
    return {
        "scanned_at": datetime.now(tz=timezone.utc).isoformat(),
        "cwd": str(cwd.resolve()),
        "coding_guidelines": detect_coding_guidelines(cwd),
        "lsps": detect_lsps(),
        "docs_access": detect_docs_access(),
        "test_runners": detect_test_runners(),
        "formatters": detect_formatters(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cwd", default=os.getcwd(), help="Project root (default: cwd)")
    args = parser.parse_args()
    print(json.dumps(scan(Path(args.cwd)), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
