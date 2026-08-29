from __future__ import annotations

import hashlib

from fastapi.testclient import TestClient
from sqlalchemy import select

from backend.logic.money import INITIAL_BALANCE_PAISA
from backend.main import app
from backend.models import Account


def auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def register(client: TestClient, handle: str, display_name: str):
    return client.post("/api/auth/register", json={"handle": handle, "display_name": display_name})


def test_registration_creates_account_once_with_initial_balance_and_hashed_token(db_session) -> None:
    with TestClient(app) as client:
        response = register(client, "Alice", "Alice Example")

    assert response.status_code == 201
    payload = response.json()
    assert payload["token_type"] == "bearer"
    assert payload["user"] == {"handle": "alice", "display_name": "Alice Example"}
    assert payload["balance"] == "100000.00"

    accounts = list(db_session.scalars(select(Account)))
    assert len(accounts) == 1
    account = accounts[0]
    assert account.balance_paisa == INITIAL_BALANCE_PAISA
    assert account.token_hash != payload["access_token"]
    assert account.token_hash == hashlib.sha256(payload["access_token"].encode("utf-8")).hexdigest()


def test_duplicate_normalized_handle_returns_409_without_extra_account(db_session) -> None:
    with TestClient(app) as client:
        first = register(client, "Alice", "Alice Example")
        duplicate = register(client, " ALICE ", "Another Alice")

    assert first.status_code == 201
    assert duplicate.status_code == 409
    assert duplicate.json()["code"] == "HANDLE_ALREADY_EXISTS"
    assert db_session.scalar(select(Account).where(Account.handle == "alice")).balance_paisa == INITIAL_BALANCE_PAISA
    assert len(list(db_session.scalars(select(Account)))) == 1


def test_bearer_auth_me_returns_persisted_authoritative_balance(db_session) -> None:
    with TestClient(app) as client:
        registration = register(client, "Alice", "Alice Example")
        token = registration.json()["access_token"]
        response = client.get("/api/auth/me", headers=auth_header(token))

    assert response.status_code == 200
    assert response.json() == {
        "user": {"handle": "alice", "display_name": "Alice Example"},
        "balance": "100000.00",
    }


def test_auth_failures_use_stable_error_shape(db_session) -> None:
    with TestClient(app) as client:
        missing = client.get("/api/auth/me")
        malformed = client.get("/api/auth/me", headers={"Authorization": "Token abc"})
        invalid = client.get("/api/auth/me", headers=auth_header("not-a-real-token"))

    assert missing.status_code == 401
    assert missing.json()["code"] == "AUTHENTICATION_REQUIRED"
    assert malformed.status_code == 401
    assert malformed.json()["code"] == "AUTHENTICATION_REQUIRED"
    assert invalid.status_code == 401
    assert invalid.json()["code"] == "INVALID_ACCESS_TOKEN"


def test_user_search_allows_short_prefixes_excludes_self_and_leaks_only_public_fields(db_session) -> None:
    with TestClient(app) as client:
        alice = register(client, "Alice", "Alice Example").json()
        register(client, "Alina", "Alina Example")
        register(client, "Bob", "Bob Example")

        response = client.get("/api/users?query=a", headers=auth_header(alice["access_token"]))

    assert response.status_code == 200
    assert response.json() == {"users": [{"handle": "alina", "display_name": "Alina Example"}]}
    assert set(response.json()["users"][0]) == {"handle", "display_name"}


def test_persistence_survives_request_reopening(db_session) -> None:
    with TestClient(app) as client:
        registration = register(client, "Bob", "Bob Example")
        token = registration.json()["access_token"]

    with TestClient(app) as client:
        response = client.get("/api/auth/me", headers=auth_header(token))

    assert response.status_code == 200
    assert response.json()["user"]["handle"] == "bob"
