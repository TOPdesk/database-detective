#!/usr/bin/env python3
"""Extract `<!-- sql-test: ... -->` markers and their associated ```sql blocks
from workshop markdown files.

This is a proof of concept for pulling validation cases directly out of the
markdown lessons, instead of maintaining them separately in query-tests.sql.

Marker syntax
-------------
An HTML comment placed on its own line, directly above a ```sql fenced code
block (blank lines in between are allowed). Being an HTML comment, it is
invisible when the markdown is rendered.

    <!-- sql-test -->
        Just assert the query executes without error.

    <!-- sql-test: rows=50 -->
        Assert the query returns exactly 50 rows.

    <!-- sql-test: rows=1; first_name=Neil; last_name=Davis -->
        Assert the query returns exactly 1 row, and that row's first_name/
        last_name columns equal the given values.

Multiple key=value pairs are separated by ';'. The 'rows' key is parsed as an
int and checked against the row count; every other key is checked against a
column of the same name — in the *first* returned row (so it also works
together with `rows` > 1 plus an `ORDER BY`/`TOP 1`, e.g. "15 rows, top one
has contra_IBAN=...").

Some fenced blocks contain more than one statement (e.g. an UPDATE followed
by a SELECT that confirms it). For those, `rows`/column assertions are
understood to apply to the block's *final* SELECT.

A ```sql block with no marker above it is simply not extracted as a test.

Usage
-----
    python3 tools/extract_sql_tests.py [FILE ...]

With no arguments, scans every .md file under material/.
"""
import argparse
import json
import re
import sys
from pathlib import Path

MARKER_RE = re.compile(r"<!--\s*sql-test\s*(?::\s*(?P<meta>.*?))?\s*-->")
FENCE_START_RE = re.compile(r"^```sql\s*$", re.IGNORECASE)
FENCE_END_RE = re.compile(r"^```\s*$")


def parse_meta(meta: str) -> dict:
    """Parse 'rows=1; first_name=Neil; last_name=Davis' into a dict."""
    expected = {}
    if not meta:
        return expected
    for part in meta.split(";"):
        part = part.strip()
        if not part:
            continue
        key, _, value = part.partition("=")
        key, value = key.strip(), value.strip()
        expected[key] = int(value) if key == "rows" else value
    return expected


def extract(path: Path) -> list[dict]:
    lines = path.read_text().splitlines()
    tests = []
    i = 0
    while i < len(lines):
        m = MARKER_RE.search(lines[i])
        if not m:
            i += 1
            continue

        marker_line = i + 1  # 1-indexed, for humans

        # Look ahead (skipping blank lines) for the opening ```sql fence.
        j = i + 1
        while j < len(lines) and lines[j].strip() == "":
            j += 1
        if j >= len(lines) or not FENCE_START_RE.match(lines[j]):
            # Marker wasn't immediately followed by a sql block; skip it.
            i += 1
            continue

        sql_lines = []
        k = j + 1
        while k < len(lines) and not FENCE_END_RE.match(lines[k]):
            sql_lines.append(lines[k])
            k += 1

        tests.append({
            "file": str(path),
            "marker_line": marker_line,
            "sql_line": j + 2,  # first line of the query, 1-indexed
            "sql": "\n".join(sql_lines).strip(),
            "expected": parse_meta(m.group("meta")),
        })
        i = k + 1
    return tests


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "files", nargs="*",
        default=sorted(str(p) for p in Path("material").glob("**/*.md")),
        help="markdown file(s) to scan (default: every .md file under material/)",
    )
    args = parser.parse_args()

    all_tests = [t for f in args.files for t in extract(Path(f))]
    print(json.dumps(all_tests, indent=2))
    print(f"\n{len(all_tests)} sql-test marker(s) found.", file=sys.stderr)


if __name__ == "__main__":
    main()
