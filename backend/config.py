from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import unquote

DEFAULT_DATABASE_URL = "sqlite+pysqlite:///:memory:"
ENV_FILE = Path(__file__).resolve().parents[1] / ".env"
POSTGRESQL_PSYCOPG_PREFIXES = ("postgresql+psycopg://", "postgresql+psycopg2://")

_ENV_LOADED = False


def load_local_env() -> None:
    """Load simple KEY=VALUE pairs from the local ignored .env file."""
    global _ENV_LOADED
    if _ENV_LOADED:
        return

    _ENV_LOADED = True
    if not ENV_FILE.exists():
        return

    for raw_line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key:
            continue
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def get_database_url() -> str:
    """Return the configured database URL without requiring a live connection."""
    load_local_env()
    return os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)


def get_test_database_url() -> str | None:
    load_local_env()
    return os.getenv("TEST_DATABASE_URL")


def is_postgresql_psycopg_url(database_url: str) -> bool:
    return database_url.startswith(POSTGRESQL_PSYCOPG_PREFIXES)


def database_name_from_url(database_url: str) -> str:
    path = database_url.split("?", 1)[0].rsplit("/", 1)[-1]
    return unquote(path)


def validate_database_targets(app_url: str, test_url: str) -> None:
    if app_url == test_url:
        raise ValueError("DATABASE_URL and TEST_DATABASE_URL must not be equal.")
    if not is_postgresql_psycopg_url(app_url):
        raise ValueError("DATABASE_URL must use PostgreSQL with psycopg.")
    validate_test_database_url(test_url)


def validate_test_database_url(test_url: str) -> None:
    if not is_postgresql_psycopg_url(test_url):
        raise ValueError("TEST_DATABASE_URL must use PostgreSQL with psycopg.")
    if not database_name_from_url(test_url).endswith("_test"):
        raise ValueError("TEST_DATABASE_URL database name must end with _test.")
