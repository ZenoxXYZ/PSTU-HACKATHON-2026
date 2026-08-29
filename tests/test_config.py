import pytest

from backend.config import (
    DEFAULT_DATABASE_URL,
    database_name_from_url,
    get_database_url,
    is_postgresql_psycopg_url,
    validate_database_targets,
    validate_test_database_url,
)


def test_database_url_uses_safe_default_when_unset(monkeypatch) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)

    assert get_database_url() == DEFAULT_DATABASE_URL


def test_database_url_comes_from_environment(monkeypatch) -> None:
    url = "postgresql+psycopg://localhost:5432/app"
    monkeypatch.setenv("DATABASE_URL", url)

    assert get_database_url() == url


def test_database_target_validation_accepts_isolated_postgresql_test_db() -> None:
    validate_database_targets(
        "postgresql+psycopg://localhost:5432/app",
        "postgresql+psycopg://localhost:5432/app_test",
    )


def test_database_target_validation_rejects_equal_urls() -> None:
    url = "postgresql+psycopg://localhost:5432/app_test"

    with pytest.raises(ValueError, match="must not be equal"):
        validate_database_targets(url, url)


def test_database_target_validation_rejects_non_test_database_name() -> None:
    with pytest.raises(ValueError, match="must end with _test"):
        validate_database_targets(
            "postgresql+psycopg://localhost:5432/app",
            "postgresql+psycopg://localhost:5432/app_not_safe",
        )


def test_test_database_validation_accepts_only_test_database_name() -> None:
    validate_test_database_url("postgresql+psycopg://localhost:5432/app_test")

    with pytest.raises(ValueError, match="must end with _test"):
        validate_test_database_url("postgresql+psycopg://localhost:5432/app")


def test_postgresql_psycopg_url_detection() -> None:
    assert is_postgresql_psycopg_url("postgresql+psycopg://localhost:5432/app")
    assert not is_postgresql_psycopg_url("sqlite+pysqlite:///:memory:")


def test_database_name_from_url_ignores_query_string() -> None:
    assert database_name_from_url("postgresql+psycopg://localhost:5432/app_test?sslmode=disable") == "app_test"
