The workshop materials are built using mkdocs, a python markdown-based static site generator.
Dependencies are managed with [uv](https://docs.astral.sh/uv/) and declared in `pyproject.toml`.

## Development

If you want develop & preview your changes locally, you can run

```sh
uv sync
# (this creates a .venv with mkdocs installed into it)
uv run mkdocs serve
```

Now point your browser to http://localhost:8000

It's also possible to generate all static files locally to check the directory structure.

```sh
uv run mkdocs build
# static files will be placed in the ./public directory
```

## Testing the workshop's SQL

The exercises' solution queries are annotated in the markdown with invisible
`<!-- sql-test: ... -->` markers (see `tools/sql_tests/extractor.py` for the
marker syntax). Two tools work with these:

```sh
# Just extract the markers + their SQL as JSON (no database needed)
uv run python3 tools/extract_sql_tests.py

# Actually run them against a live database and report pass/fail via pytest
uv run python3 tools/run_sql_tests.py --backend sqlite --sqlite-path detective.db
```

`run_sql_tests.py` needs a database to connect to, configured via CLI flags
(as above), environment variables, or a `.env` file — copy `.env.example` to
`.env` and fill it in. Run with `--help` for the full list of options,
including how to test against MS SQL Server instead of SQLite (needs the
optional `mssql` dependency group: `uv sync --extra mssql`).

Note that some of the workshop's own solutions are `UPDATE`/`INSERT`/`DELETE`
statements that later exercises depend on, so tests run in marker order
against one shared connection rather than each in isolation. This means the
suite isn't safely re-runnable against the same persistent database without
restoring it first — same as the workshop's own backup/restore guidance in
`data-modification.md`.