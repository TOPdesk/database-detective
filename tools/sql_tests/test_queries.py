"""Runs every `<!-- sql-test: ... -->` marker extracted from material/
against a live database.

Not meant to be run directly with bare `pytest` — the `database` fixture
needs its connection configured first (see conftest.py and ../config.py).
Use tools/run_sql_tests.py, which resolves the connection config from CLI
flags / env vars / a .env file and then hands off to pytest for collection
and reporting.
"""


def test_sql_query(database, sql_test_case):
    sql = sql_test_case["sql"]
    expected = sql_test_case["expected"]

    rows = database.run(sql)

    if "rows" in expected:
        actual_row_count = len(rows) if rows is not None else 0
        assert actual_row_count == expected["rows"], (
            f"expected {expected['rows']} row(s), got {actual_row_count}\n{sql}"
        )

    column_checks = {k: v for k, v in expected.items() if k != "rows"}
    if column_checks:
        assert rows, f"expected at least 1 row to check column values, got none\n{sql}"
        first_row = {k.lower(): v for k, v in rows[0].items()}
        for column, expected_value in column_checks.items():
            actual_value = first_row.get(column.lower())
            assert str(actual_value) == str(expected_value), (
                f"expected column {column!r} = {expected_value!r} in the first row, "
                f"got {actual_value!r}\n{sql}"
            )
