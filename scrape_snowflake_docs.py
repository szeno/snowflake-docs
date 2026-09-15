#!/usr/bin/env python3
"""
Crawl the Snowflake documentation site (https://docs.snowflake.com/en) and save
raw HTML pages to disk, mirroring the URL path structure.

Page list is sourced from the site's sitemap (https://docs.snowflake.com/en/sitemap.xml)
rather than following links, so the crawl is complete and doesn't need to guess at
navigation structure.

Usage:
    python scrape_snowflake_docs.py [--output-dir DIR] [--workers N] [--delay SECONDS]
                                     [--limit N] [--force] [--retries N]

Examples:
    python scrape_snowflake_docs.py
    python scrape_snowflake_docs.py --output-dir html --workers 8 --delay 0.25
    python scrape_snowflake_docs.py --limit 50   # smoke test on a small subset
"""

from __future__ import annotations

import argparse
import fnmatch
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

SITEMAP_URL = "https://docs.snowflake.com/en/sitemap.xml"
BASE_HOST = "docs.snowflake.com"
USER_AGENT = "snowflake-docs-archiver/1.0 (+local research crawl)"

# Mirrors the Disallow rules in https://docs.snowflake.com/robots.txt for /en/.
ROBOTS_DISALLOW_PATTERNS = [
    "/en/sql-reference/commands-*",
    "/en/INCLUDE/*",
    "/en/DRAFT/*",
    "/en/PREVIEW/*",
]


def is_allowed(path: str) -> bool:
    return not any(fnmatch.fnmatch(path, pattern) for pattern in ROBOTS_DISALLOW_PATTERNS)


def fetch_sitemap_urls(session: requests.Session) -> list[str]:
    resp = session.get(SITEMAP_URL, timeout=30)
    resp.raise_for_status()
    root = ElementTree.fromstring(resp.content)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [loc.text.strip() for loc in root.findall(".//sm:url/sm:loc", ns) if loc.text]
    return urls


def url_to_path(url: str, output_dir: Path) -> Path:
    parsed = urlparse(url)
    rel = parsed.path.strip("/")
    if not rel:
        rel = "index"
    return output_dir / f"{rel}.html"


class RateLimiter:
    """Ensures at least `interval` seconds pass between requests, across all threads."""

    def __init__(self, interval: float):
        self.interval = interval
        self._lock = threading.Lock()
        self._next_allowed = 0.0

    def wait(self) -> None:
        if self.interval <= 0:
            return
        with self._lock:
            now = time.monotonic()
            sleep_for = self._next_allowed - now
            if sleep_for > 0:
                time.sleep(sleep_for)
                now = time.monotonic()
            self._next_allowed = now + self.interval


def build_session(retries: int) -> requests.Session:
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    retry = Retry(
        total=retries,
        backoff_factor=1.0,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def download_one(
    url: str,
    output_dir: Path,
    session: requests.Session,
    limiter: RateLimiter,
    force: bool,
) -> tuple[str, str]:
    dest = url_to_path(url, output_dir)
    if dest.exists() and not force:
        return url, "skipped"

    limiter.wait()
    try:
        resp = session.get(url, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as exc:
        return url, f"failed: {exc}"

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(resp.content)
    return url, "ok"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output-dir", default="html", help="Directory to save HTML pages into (default: html)")
    parser.add_argument("--workers", type=int, default=6, help="Concurrent download workers (default: 6)")
    parser.add_argument("--delay", type=float, default=0.3, help="Minimum seconds between requests, shared across workers (default: 0.3)")
    parser.add_argument("--retries", type=int, default=3, help="Retries per request on transient errors (default: 3)")
    parser.add_argument("--limit", type=int, default=None, help="Only process the first N URLs (useful for testing)")
    parser.add_argument("--force", action="store_true", help="Re-download pages even if the output file already exists")
    args = parser.parse_args()

    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    session = build_session(args.retries)

    print(f"Fetching sitemap: {SITEMAP_URL}")
    urls = fetch_sitemap_urls(session)
    print(f"Sitemap contains {len(urls)} URLs")

    urls = [u for u in urls if urlparse(u).hostname == BASE_HOST and is_allowed(urlparse(u).path)]
    print(f"{len(urls)} URLs allowed after robots.txt filtering")

    if args.limit:
        urls = urls[: args.limit]
        print(f"Limiting to first {len(urls)} URLs")

    limiter = RateLimiter(args.delay)
    failed: list[str] = []
    skipped = 0
    ok = 0

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(download_one, url, output_dir, session, limiter, args.force): url
            for url in urls
        }
        total = len(futures)
        done = 0
        for future in as_completed(futures):
            url, status = future.result()
            done += 1
            if status == "ok":
                ok += 1
            elif status == "skipped":
                skipped += 1
            else:
                failed.append(url)
                print(f"[{done}/{total}] FAILED {url}: {status}", file=sys.stderr)
            if done % 100 == 0 or done == total:
                print(f"[{done}/{total}] ok={ok} skipped={skipped} failed={len(failed)}")

    if failed:
        failures_file = output_dir / "_failed_urls.txt"
        failures_file.write_text("\n".join(failed) + "\n")
        print(f"\n{len(failed)} URLs failed. See {failures_file}")

    print(f"\nDone. ok={ok} skipped={skipped} failed={len(failed)} output_dir={output_dir}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
