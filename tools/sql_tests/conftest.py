import json
import os

import pytest

from . import config as cfg
from . import db as dbmod
from . import extractor


def _cases() -> list[dict]:
    files_env = os.environ.get("SQLTEST_MD_FILES")
    files = json.loads(files_env) if files_env else extractor.default_files()
    return extractor.extract_all(files)


def pytest_generate_tests(metafunc):
    if "sql_test_case" in metafunc.fixturenames:
        cases = _cases()
        ids = [f"{c['file']}:{c['sql_line']}" for c in cases]
        metafunc.parametrize("sql_test_case", cases, ids=ids)


@pytest.fixture(scope="session")
def database():
    """A single live connection, reused across every test in the run.

    Deliberately session-scoped rather than reset per test: several of the
    workshop's own solutions are UPDATE/INSERT/DELETE statements whose
    effect the *next* exercise's solution depends on (see data-modification
    .md's Klein->Kleiner rename, or the Otto/Kathie insert-then-delete). The
    tests need to run in file/marker order against shared, mutating state,
    exactly like a person working through the lessons top to bottom would —
    not each in its own isolated transaction.

    That also means this suite is not safely re-runnable against the same
    persistent database without restoring it first, same as the workshop's
    own "back up before, restore after" guidance in data-modification.md.
    """
    config = cfg.load_config()
    database = dbmod.get_database(config)
    database.connect()
    try:
        yield database
    finally:
        database.close()
