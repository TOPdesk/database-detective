"""Database connection configuration for the sql-test runner.

Resolved from, highest precedence first:

1. Real process environment variables (`SQLTEST_*`).
2. A `.env` file (loaded via python-dotenv; never overrides a real env var
   that's already set).
3. Built-in defaults.

`tools/run_sql_tests.py`'s command-line flags are folded into the process
environment before `load_config()` is called, so in practice the full
precedence order is: CLI args > env vars > .env file > defaults. This module
only ever looks at the environment — it doesn't know about argparse — so it
works the same way whether you go through run_sql_tests.py or invoke pytest
directly against tools/sql_tests/test_queries.py with the environment (or a
.env file in the current directory) set up yourself.
"""
import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

_dotenv_loaded_from: Optional[str] = None


class ConfigError(Exception):
    """Raised when the environment doesn't describe a usable database."""


def load_dotenv_file(path: str = ".env") -> None:
    """Load `path` into the process environment (no-op if it doesn't exist).
    Never overrides a variable that's already set in the real environment.
    """
    global _dotenv_loaded_from
    load_dotenv(dotenv_path=path, override=False)
    _dotenv_loaded_from = path


@dataclass
class SqliteConfig:
    path: str


@dataclass
class MssqlConfig:
    host: str
    port: int
    database: str
    user: str
    password: str


@dataclass
class Config:
    backend: str
    sqlite: Optional[SqliteConfig] = None
    mssql: Optional[MssqlConfig] = None


def load_config() -> Config:
    """Read SQLTEST_* env vars (loading a .env file first, unless one has
    already been loaded) and return a validated Config, or raise
    ConfigError with a message describing what's missing.
    """
    if _dotenv_loaded_from is None:
        load_dotenv_file(".env")

    backend = os.environ.get("SQLTEST_BACKEND", "sqlite").lower()

    if backend == "sqlite":
        path = os.environ.get("SQLTEST_SQLITE_PATH")
        if not path:
            raise ConfigError(
                "sqlite backend needs a database file: set SQLTEST_SQLITE_PATH "
                "(env var, .env file, or --sqlite-path)"
            )
        return Config(backend="sqlite", sqlite=SqliteConfig(path=path))

    if backend == "mssql":
        required = {
            "database": "SQLTEST_MSSQL_DATABASE",
            "user": "SQLTEST_MSSQL_USER",
            "password": "SQLTEST_MSSQL_PASSWORD",
        }
        missing = [env for env in required.values() if not os.environ.get(env)]
        if missing:
            raise ConfigError(
                f"mssql backend needs {', '.join(missing)} "
                "(env vars, .env file, or the matching --mssql-* flags)"
            )
        return Config(
            backend="mssql",
            mssql=MssqlConfig(
                host=os.environ.get("SQLTEST_MSSQL_HOST", "localhost"),
                port=int(os.environ.get("SQLTEST_MSSQL_PORT", "1433")),
                database=os.environ["SQLTEST_MSSQL_DATABASE"],
                user=os.environ["SQLTEST_MSSQL_USER"],
                password=os.environ["SQLTEST_MSSQL_PASSWORD"],
            ),
        )

    raise ConfigError(f"unknown SQLTEST_BACKEND {backend!r}; expected 'sqlite' or 'mssql'")
