"""
Recompute source_hash for every node in every domain CSV.

Usage:
    python3 scripts/refresh_hashes.py [--domain nemoclaw] [--dry-run]

For each node:
  1. Fetch source_url (10s timeout, 3 retries with backoff)
  2. SHA-256 the raw response bytes
  3. Write 'sha256:<hex>' back to the CSV

Sentinels (written verbatim; not a hash failure — a source state):
  sha256:restricted   → URL returned 4xx / 5xx (page requires auth or is gone)
  sha256:unavailable  → Network error / timeout after retries
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import sys
import time
from pathlib import Path

try:
    import httpx
except ImportError:
    print("httpx not installed — run: pip install httpx", file=sys.stderr)
    sys.exit(1)

DOMAINS_DIR = Path(__file__).parent.parent / "src" / "ckg_nvidia_nemoclaw" / "domains"
TIMEOUT = 10.0
RETRIES = 3
BACKOFF = 1.5


def fetch_hash(url: str) -> str:
    for attempt in range(RETRIES):
        try:
            resp = httpx.get(url, timeout=TIMEOUT, follow_redirects=True,
                             headers={"User-Agent": "ckg-nvidia-nemoclaw/0.5.0 refresh_hashes"})
            if resp.status_code >= 400:
                return "sha256:restricted"
            return "sha256:" + hashlib.sha256(resp.content).hexdigest()
        except Exception:
            if attempt < RETRIES - 1:
                time.sleep(BACKOFF ** attempt)
    return "sha256:unavailable"


def refresh_domain(domain: str, dry_run: bool = False) -> None:
    csv_path = DOMAINS_DIR / f"{domain}.csv"
    if not csv_path.exists():
        print(f"  [skip] {domain}.csv not found", file=sys.stderr)
        return

    with open(csv_path, newline="") as f:
        rows = list(csv.DictReader(f))

    fieldnames = list(rows[0].keys()) if rows else []
    if "SourceHash" not in fieldnames:
        fieldnames.append("SourceHash")

    url_cache: dict[str, str] = {}
    updated = 0

    for row in rows:
        url = row.get("SourceURL", "").strip()
        if not url:
            row["SourceHash"] = "sha256:no-source-url"
            continue
        if url not in url_cache:
            h = fetch_hash(url)
            url_cache[url] = h
            print(f"  {h[:20]}...  {url}")
        row["SourceHash"] = url_cache[url]
        updated += 1

    if dry_run:
        print(f"  [dry-run] {updated} rows would be updated")
        return

    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"  wrote {updated} hashes to {csv_path.name}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Refresh source_hash for CKG domain CSVs")
    parser.add_argument("--domain", help="Single domain to refresh (default: all)")
    parser.add_argument("--dry-run", action="store_true", help="Print hashes without writing")
    args = parser.parse_args()

    domains = [args.domain] if args.domain else [p.stem for p in DOMAINS_DIR.glob("*.csv")]
    for domain in domains:
        print(f"\nDomain: {domain}")
        refresh_domain(domain, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
