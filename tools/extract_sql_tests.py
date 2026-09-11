#!/usr/bin/env python3
"""Extract `<!-- sql-test: ... -->` markers and their associated ```sql
blocks from workshop markdown files, and dump them as JSON.

This is the read-only, no-database counterpart to run_sql_tests.py. See
tools/sql_tests/extractor.py for the marker syntax and extraction rules —
both scripts share that logic.

Usage
-----
    python3 tools/extract_sql_tests.py [FILE ...]

With no arguments, scans every .md file under material/.
"""
import argparse
import json
import sys

from sql_tests import extractor


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "files", nargs="*",
        default=extractor.default_files(),
        help="markdown file(s) to scan (default: every .md file under material/)",
    )
    args = parser.parse_args()

    all_tests = extractor.extract_all(args.files)
    print(json.dumps(all_tests, indent=2))
    print(f"\n{len(all_tests)} sql-test marker(s) found.", file=sys.stderr)


if __name__ == "__main__":
    main()
