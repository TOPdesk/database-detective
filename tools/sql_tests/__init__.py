"""Shared helpers for the workshop's sql-test tooling.

- `extractor` pulls `<!-- sql-test: ... -->` markers and their ```sql blocks
  out of material/*.md.
- `db` is a small database abstraction layer (SQLite / MSSQL) used to
  actually run that SQL.
- `config` resolves database connection settings from env vars / a .env
  file.

Used by tools/extract_sql_tests.py (dumps extracted cases as JSON) and
tools/run_sql_tests.py (executes them against a live database via pytest).
"""
