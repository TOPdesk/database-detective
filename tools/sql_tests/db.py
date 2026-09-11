"""A small database abstraction layer so the same extracted sql-test cases
can be run against either SQLite or MSSQL.

Both backends implement `Database.run(sql) -> list[dict] | None`: it executes
every statement in `sql` in order (see `split_statements` for how a fenced
block is broken into statements) and returns the *last* statement's result
set as a list of `{column: value}` dicts — or `None` if that last statement
didn't produce a result set at all (e.g. a bare CREATE TABLE/UPDATE/DELETE).
This matches the convention documented in `extractor`: for a multi-statement
block, `rows`/column assertions apply to the block's final SELECT.
"""
import abc
import re
from typing import Optional

from . import config as cfg

_BLANK_LINE_RE = re.compile(r"\n[ \t]*\n")
# Fallback splitter for the one shape in this corpus that has neither a
# blank line nor a ';' between two statements (consecutive `DROP TABLE ...`
# lines): split right before a line that starts a new CREATE/DROP/ALTER
# statement.
_DDL_LINE_RE = re.compile(r"(?im)^(?=\s*(?:CREATE|DROP|ALTER)\b)")


def split_statements(sql: str) -> list[str]:
    """Best-effort split of a fenced sql-test block into individual
    statements, in order.

    This is deliberately not a general SQL parser — it doesn't understand
    semicolons or keywords appearing inside string literals/comments. That's
    fine for this workshop's corpus (checked against every currently marked
    block), but keep it in mind before feeding it arbitrary SQL.
    """
    statements = []
    for paragraph in _BLANK_LINE_RE.split(sql.strip()):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        if ";" in paragraph:
            statements.extend(p.strip() for p in paragraph.split(";") if p.strip())
        else:
            pieces = [p.strip() for p in _DDL_LINE_RE.split(paragraph) if p.strip()]
            statements.extend(pieces or [paragraph])
    return statements


class Database(abc.ABC):
    """A DB-API-ish connection that can run one or more statements and
    report the final statement's result set. Subclasses only need to
    provide `connect`, `close`, and a DB-API cursor via `_cursor`."""

    def __enter__(self) -> "Database":
        self.connect()
        return self

    def __exit__(self, *exc_info) -> None:
        self.close()

    @abc.abstractmethod
    def connect(self) -> None: ...

    @abc.abstractmethod
    def close(self) -> None: ...

    @abc.abstractmethod
    def _cursor(self): ...

    def run(self, sql: str) -> Optional[list[dict]]:
        cursor = self._cursor()
        last_rows: Optional[list[dict]] = None
        try:
            for statement in split_statements(sql):
                cursor.execute(statement)
                if cursor.description is not None:
                    columns = [d[0] for d in cursor.description]
                    last_rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
                else:
                    last_rows = None
            return last_rows
        finally:
            cursor.close()


class SqliteDatabase(Database):
    def __init__(self, path: str):
        self.path = path
        self.connection = None

    def connect(self) -> None:
        import sqlite3
        self.connection = sqlite3.connect(self.path)

    def _cursor(self):
        return self.connection.cursor()

    def close(self) -> None:
        if self.connection is not None:
            self.connection.close()
            self.connection = None


class MssqlDatabase(Database):
    """Connects via python-tds (import name `pytds`), a pure-Python TDS
    client — unlike pyodbc/pymssql it needs no ODBC driver or FreeTDS
    installed on the machine running the tests. Install it with:

        uv sync --extra mssql
    """

    def __init__(self, host: str, port: int, database: str, user: str, password: str):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self) -> None:
        try:
            import pytds
        except ImportError as exc:
            raise ImportError(
                "the mssql backend needs the 'python-tds' package; "
                "install it with `uv sync --extra mssql`"
            ) from exc
        self.connection = pytds.connect(
            server=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password,
        )

    def _cursor(self):
        return self.connection.cursor()

    def close(self) -> None:
        if self.connection is not None:
            self.connection.close()
            self.connection = None


def get_database(config: cfg.Config) -> Database:
    if config.backend == "sqlite":
        assert config.sqlite is not None
        return SqliteDatabase(config.sqlite.path)
    if config.backend == "mssql":
        assert config.mssql is not None
        m = config.mssql
        return MssqlDatabase(
            host=m.host, port=m.port, database=m.database, user=m.user, password=m.password,
        )
    raise ValueError(f"unknown backend {config.backend!r}")
