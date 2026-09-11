#!/usr/bin/env python3
"""Run the workshop's `<!-- sql-test: ... -->` markers against a live
database (SQLite or MSSQL), reporting results via pytest.

Connection configuration is resolved from, in order of precedence:
CLI flags > real environment variables > a .env file > built-in defaults.
See tools/sql_tests/config.py for the exact env var names, or run with
--help. A template is available at .env.example.

Examples
--------
    # SQLite, config from CLI flags
    python3 tools/run_sql_tests.py --backend sqlite --sqlite-path detective.db

    # SQLite, config from a .env file (see .env.example)
    python3 tools/run_sql_tests.py

    # MSSQL (needs `uv sync --extra mssql`)
    python3 tools/run_sql_tests.py --backend mssql --mssql-host localhost \\
        --mssql-database detective --mssql-user sa --mssql-password '...'

    # Only test one file, and pass extra flags through to pytest
    python3 tools/run_sql_tests.py material/sequel-basicland/basic-querying.md -- -k rows

Note: several of the workshop's own solutions are UPDATE/INSERT/DELETE
statements that later exercises depend on (see data-modification.md). This
suite runs tests in marker order against one shared, mutating connection —
same as someone working through the lessons top to bottom — and is *not*
safely re-runnable against the same persistent database without restoring
it first.
"""
import argparse
import json
import os
import sys
from pathlib import Path

from sql_tests import config as cfg

CLI_TO_ENV = {
    "backend": "SQLTEST_BACKEND",
    "sqlite_path": "SQLTEST_SQLITE_PATH",
    "mssql_host": "SQLTEST_MSSQL_HOST",
    "mssql_port": "SQLTEST_MSSQL_PORT",
    "mssql_database": "SQLTEST_MSSQL_DATABASE",
    "mssql_user": "SQLTEST_MSSQL_USER",
    "mssql_password": "SQLTEST_MSSQL_PASSWORD",
}


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "files", nargs="*",
        help="markdown file(s) to test (default: every .md file under material/)",
    )
    parser.add_argument("--env-file", default=".env", help="path to a .env file to load (default: .env)")
    parser.add_argument("--backend", choices=["sqlite", "mssql"], help="database backend")
    parser.add_argument("--sqlite-path", help="path to the sqlite database file")
    parser.add_argument("--mssql-host", help="MSSQL server host (default: localhost)")
    parser.add_argument("--mssql-port", type=int, help="MSSQL server port (default: 1433)")
    parser.add_argument("--mssql-database", help="MSSQL database name")
    parser.add_argument("--mssql-user", help="MSSQL user name")
    parser.add_argument("--mssql-password", help="MSSQL password")
    parser.add_argument(
        "pytest_args", nargs=argparse.REMAINDER,
        help="anything after `--` is passed straight through to pytest",
    )
    args = parser.parse_args(argv)
    if args.pytest_args and args.pytest_args[0] == "--":
        args.pytest_args = args.pytest_args[1:]
    return args


def main(argv=None):
    args = parse_args(argv if argv is not None else sys.argv[1:])

    cfg.load_dotenv_file(args.env_file)

    for attr, env_name in CLI_TO_ENV.items():
        value = getattr(args, attr)
        if value is not None:
            os.environ[env_name] = str(value)

    if args.files:
        os.environ["SQLTEST_MD_FILES"] = json.dumps(args.files)
    else:
        os.environ.pop("SQLTEST_MD_FILES", None)

    try:
        cfg.load_config()
    except cfg.ConfigError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    import pytest

    test_file = str(Path(__file__).resolve().parent / "sql_tests" / "test_queries.py")
    return pytest.main(["-v", test_file, *args.pytest_args])


if __name__ == "__main__":
    raise SystemExit(main())
