#!/usr/bin/env python3
"""Reject common secret-bearing filenames from the Git tracked path set."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import PurePosixPath


BLOCKED_NAMES = {
    ".npmrc",
    ".pypirc",
    "credentials.json",
    "id_ed25519",
    "id_rsa",
    "service-account.json",
}
BLOCKED_SUFFIXES = {".key", ".p12", ".pem", ".pfx"}


def find_sensitive_paths(paths: list[str]) -> list[str]:
    blocked: list[str] = []
    for raw_path in paths:
        normalized = raw_path.replace("\\", "/").strip("/")
        if not normalized:
            continue
        path = PurePosixPath(normalized)
        lowered_parts = tuple(part.casefold() for part in path.parts)
        name = path.name.casefold()
        suffix = path.suffix.casefold()
        is_environment = name == ".env" or name.startswith(".env.")
        is_ssh_material = ".ssh" in lowered_parts
        is_aws_credentials = len(lowered_parts) >= 2 and lowered_parts[-2:] == (".aws", "credentials")
        if (
            name in BLOCKED_NAMES
            or suffix in BLOCKED_SUFFIXES
            or is_environment
            or is_ssh_material
            or is_aws_credentials
        ):
            blocked.append(normalized)
    return sorted(set(blocked), key=str.casefold)


def tracked_paths() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"git ls-files failed with exit {result.returncode}: {detail}")
    return [item.decode("utf-8", errors="strict") for item in result.stdout.split(b"\0") if item]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tracked", action="store_true")
    parser.add_argument("paths", nargs="*")
    args = parser.parse_args()
    if args.tracked == bool(args.paths):
        parser.error("choose exactly one of --tracked or explicit paths")
    try:
        paths = tracked_paths() if args.tracked else args.paths
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    blocked = find_sensitive_paths(paths)
    if blocked:
        print("Sensitive tracked paths are forbidden:", file=sys.stderr)
        for path in blocked:
            print(f"- {path}", file=sys.stderr)
        return 1
    print(f"Sensitive-path check passed for {len(paths)} path(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
