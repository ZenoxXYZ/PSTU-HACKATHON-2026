from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest
from sqlalchemy import text

from backend import database
from backend.config import get_database_url, get_test_database_url, validate_database_targets, validate_test_database_url

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def postgresql_test_url() -> str:
    test_url = get_test_database_url()
    if not test_url:
        pytest.skip("TEST_DATABASE_URL is required for PostgreSQL-backed WS-01 tests.")

    app_url = get_database_url()
    validate_database_targets(app_url, test_url)
    return test_url


@pytest.fixture(scope="session")
def configure_postgresql_test_database(postgresql_test_url: str) -> None:
    os.environ["DATABASE_URL"] = postgresql_test_url
    database.configure_database(postgresql_test_url)
    result = subprocess.run(
        [str(ROOT / ".venv" / "Scripts" / "python.exe"), "-m", "alembic", "upgrade", "head"],
        cwd=ROOT,
        env={**os.environ, "DATABASE_URL": postgresql_test_url},
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        pytest.fail("Alembic migration failed for TEST_DATABASE_URL.")


@pytest.fixture()
def clean_accounts(postgresql_test_url: str, configure_postgresql_test_database: None) -> None:
    validate_test_database_url(postgresql_test_url)
    with database.engine.begin() as connection:
        connection.execute(text("DELETE FROM transfers"))
        connection.execute(text("DELETE FROM money_requests"))
        connection.execute(text("DELETE FROM accounts"))


@pytest.fixture()
def db_session(clean_accounts: None):
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
