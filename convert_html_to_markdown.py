#!/usr/bin/env python3
"""
Convert every scraped Snowflake docs HTML page in the html/ folder into a Markdown
file in the markdown/ folder, mirroring the same directory structure.

Only the main article content is converted (nav, header, footer, and sidebar
chrome are dropped), and heading anchor links ("¶") are stripped for clean output.

Usage:
    python convert_html_to_markdown.py [--input-dir html] [--output-dir markdown]
                                        [--workers N] [--force] [--limit N]
"""

from __future__ import annotations

import argparse
import re
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from bs4 import BeautifulSoup
from markdownify import markdownify

# Collapses 3+ blank lines left behind after stripping elements.
BLANK_LINES_RE = re.compile(r"\n{3,}")


def extract_article_html(html: str) -> str | None:
    soup = BeautifulSoup(html, "lxml")
    article = (
        soup.find("article", attrs={"data-testid": "article-content"})
        or soup.find("main")
        or soup.find("body")
    )
    if article is None:
        return None

    for tag in article.find_all(["script", "style"]):
        tag.decompose()
    for tag in article.find_all("a", class_="headerlink"):
        tag.decompose()

    return str(article)


def convert_file(src: Path, dest: Path) -> tuple[Path, str]:
    try:
        html = src.read_text(encoding="utf-8", errors="replace")
        article_html = extract_article_html(html)
        if article_html is None:
            return src, "no content found"

        text = markdownify(article_html, heading_style="ATX", bullets="-")
        text = BLANK_LINES_RE.sub("\n\n", text).strip() + "\n"

        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8")
        return src, "ok"
    except Exception as exc:  # noqa: BLE001 - report and keep going
        return src, f"failed: {exc}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input-dir", default="html", help="Folder containing scraped HTML files (default: html)")
    parser.add_argument("--output-dir", default="markdown", help="Folder to write converted Markdown files into (default: markdown)")
    parser.add_argument("--workers", type=int, default=None, help="Parallel worker processes (default: number of CPUs)")
    parser.add_argument("--force", action="store_true", help="Re-convert files even if the output .md already exists")
    parser.add_argument("--limit", type=int, default=None, help="Only process the first N files (useful for testing)")
    args = parser.parse_args()

    input_dir = Path(args.input_dir).resolve()
    output_dir = Path(args.output_dir).resolve()

    html_files = sorted(input_dir.rglob("*.html"))
    if args.limit:
        html_files = html_files[: args.limit]
    print(f"Found {len(html_files)} HTML files under {input_dir}")

    jobs = []
    for src in html_files:
        rel = src.relative_to(input_dir).with_suffix(".md")
        dest = output_dir / rel
        if dest.exists() and not args.force:
            continue
        jobs.append((src, dest))
    print(f"{len(jobs)} files need conversion ({len(html_files) - len(jobs)} already up to date)")

    ok = 0
    failed: list[tuple[Path, str]] = []
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(convert_file, src, dest): src for src, dest in jobs}
        total = len(futures)
        done = 0
        for future in as_completed(futures):
            src, status = future.result()
            done += 1
            if status == "ok":
                ok += 1
            else:
                failed.append((src, status))
            if done % 200 == 0 or done == total:
                print(f"[{done}/{total}] ok={ok} failed={len(failed)}")

    if failed:
        print(f"\n{len(failed)} files failed to convert:")
        for src, status in failed[:20]:
            print(f"  {src}: {status}")
        if len(failed) > 20:
            print(f"  ... and {len(failed) - 20} more")

    print(f"\nDone. ok={ok} failed={len(failed)} output_dir={output_dir}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
