from __future__ import annotations

import hashlib
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from backend import database
from backend.errors import AppError
from backend.logic.money import INITIAL_BALANCE_PAISA, format_paisa, parse_paisa
from backend.main import app
from backend.models import Account, Transfer
from backend.services.accounts import token_hash


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def register(client: TestClient, handle: str, display_name: str) -> dict:
    resp = client.post(
        "/api/auth/register",
        json={"handle": handle, "display_name": display_name},
    )
    return resp.json()


def transfer_headers(token: str, idem_key: str | None = None) -> dict[str, str]:
    headers = auth_header(token)
    headers["Idempotency-Key"] = idem_key or str(uuid.uuid4())
    return headers


# ---------------------------------------------------------------------------
# 1-5. Money parsing tests
# ---------------------------------------------------------------------------

class TestMoneyParsing:
    def test_valid_amount_parses_exact_paisa(self) -> None:
        assert parse_paisa("2500.00") == 250_000
        assert parse_paisa("0.01") == 1
        assert parse_paisa("100000.00") == 10_000_000
        assert parse_paisa("1.99") == 199

    def test_zero_rejected(self) -> None:
        with pytest.raises(ValueError, match="greater than zero"):
            parse_paisa("0.00")

    def test_negative_rejected(self) -> None:
        with pytest.raises(ValueError):
            parse_paisa("-100.00")

    def test_malformed_rejected(self) -> None:
        for bad in ["abc", "12.1", "12.123", "12.", ".12", "", "  ", "12,00.00"]:
            with pytest.raises(ValueError):
                parse_paisa(bad)

    def test_excess_precision_rejected(self) -> None:
        with pytest.raises(ValueError):
            parse_paisa("100.001")

    def test_non_string_rejected(self) -> None:
        with pytest.raises(ValueError, match="must be a string"):
            parse_paisa(100)  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="must be a string"):
            parse_paisa(None)  # type: ignore[arg-type]

    def test_scientific_notation_rejected(self) -> None:
        with pytest.raises(ValueError):
            parse_paisa("1e5.00")

    def test_whitespace_only_rejected(self) -> None:
        with pytest.raises(ValueError):
            parse_paisa("   ")


# ---------------------------------------------------------------------------
# 6-17. Transfer API tests
# ---------------------------------------------------------------------------

class TestTransferAPI:
    def test_valid_transfer_produces_exact_balances(self, db_session: Session) -> None:
        with TestClient(app) as client:
            alice = register(client, "alice", "Alice")
            bob = register(client, "bob", "Bob")
            headers = transfer_headers(alice["access_token"])
            resp = client.post(
                "/api/transfers",
                json={"recipient_handle": "bob", "amount": "2500.00"},
                headers=headers,
            )
        assert resp.status_code == 201
        body = resp.json()
        assert body["transfer"]["amount"] == "2500.00"
        assert body["transfer"]["kind"] == "DIRECT"
        assert body["transfer"]["recipient"]["handle"] == "bob"

        # Verify balances via new session
        from backend.database import SessionLocal
        new_db = SessionLocal()
        try:
            alice_acc = new_db.scalar(select(Account).where(Account.handle == "alice"))
            bob_acc = new_db.scalar(select(Account).where(Account.handle == "bob"))
            assert alice_acc.balance_paisa == INITIAL_BALANCE_PAISA - 250_000
            assert bob_acc.balance_paisa == INITIAL_BALANCE_PAISA + 250_000
        finally:
            new_db.close()

    def test_sender_authority_from_bearer_token(self, db_session: Session) -> None:
        """The transfer must use the authenticated sender, not a body field."""
        with TestClient(app) as client:
            alice = register(client, "alice", "Alice")
            bob = register(client, "bob", "Bob")
            # Alice's token sends money
            headers = transfer_headers(alice["access_token"])
            resp = client.post(
                "/api/transfers",
                json={"recipient_handle": "bob", "amount": "100.00"},
                headers=headers,
            )
        assert resp.status_code == 201

    def test_unknown_recipient_rejected(self, db_session: Session) -> None:
        with TestClient(app) as client:
            alice = register(client, "alice", "Alice")
            headers = transfer_headers(alice["access_token"])
            resp = client.post(
                "/api/transfers",
                json={"recipient_handle": "nonexistent", "amount": "100.00"},
                headers=headers,
            )
        assert resp.status_code == 404
        assert resp.json()["code"] == "RECIPIENT_NOT_FOUND"

    def test_self_transfer_rejected(self, db_session: Session) -> None:
        with TestClient(app) as client:
            alice = register(client, "alice", "Alice")
            headers = transfer_headers(alice["access_token"])
            resp = client.post(
                "/api/transfers",
                json={"recipient_handle": "alice", "amount": "100.00"},
                headers=headers,
            )
        assert resp.status_code == 400
        assert resp.json()["code"] == "SELF_TRANSFER"

    def test_insufficient_funds_no_state_change(self, db_session: Session) -> None:
        with TestClient(app) as client:
            alice = register(client, "alice", "Alice")
            bob = register(client, "bob", "Bob")
            headers = transfer_headers(alice["access_token"])
            resp = client.post(
                "/api/transfers",
                json={"recipient_handle": "bob", "amount": "999999.00"},
                headers=headers,
            )
        assert resp.status_code == 409
        assert resp.json()["code"] == "INSUFFICIENT_FUNDS"
        # Verify no state change
        from backend.database import SessionLocal
        new_db = SessionLocal()
        try:
            alice_acc = new_db.scalar(select(Account).where(Account.handle == "alice"))
            bob_acc = new_db.scalar(select(Account).where(Account.handle == "bob"))
            assert alice_acc.balance_paisa == INITIAL_BALANCE_PAISA
            assert bob_acc.balance_paisa == INITIAL_BALANCE_PAISA
            assert new_db.scalar(select(Transfer)) is None
        finally:
            new_db.close()

    def test_one_transfer_persisted_and_money_conserved(self, db_session: Session) -> None:
        with TestClient(app) as client:
            alice = register(client, "alice", "Alice")
            bob = register(client, "bob", "Bob")
            headers = transfer_headers(alice["access_token"])
            client.post(
                "/api/transfers",
                json={"recipient_handle": "bob", "amount": "5000.00"},
                headers=headers,
            )
        from backend.database import SessionLocal
        new_db = SessionLocal()
        try:
            transfers = list(new_db.scalars(select(Transfer)))
            assert len(transfers) == 1
            t = transfers[0]
            assert t.amount_paisa == 500_000
            assert t.kind == "DIRECT"
            alice_acc = new_db.scalar(select(Account).where(Account.handle == "alice"))
            bob_acc = new_db.scalar(select(Account).where(Account.handle == "bob"))
            total = alice_acc.balance_paisa + bob_acc.balance_paisa
            assert total == INITIAL_BALANCE_PAISA * 2
        finally:
            new_db.close()

    def test_same_key_replay_no_second_movement(self, db_session: Session) -> None:
        with TestClient(app) as client:
            alice = register(client, "alice", "Alice")
            bob = register(client, "bob", "Bob")
            idem_key = str(uuid.uuid4())
            headers = transfer_headers(alice["access_token"], idem_key)
            resp1 = client.post(
                "/api/transfers",
                json={"recipient_handle": "bob", "amount": "1000.00"},
                headers=headers,
            )
            assert resp1.status_code == 201
            # Replay with same key
            resp2 = client.post(
                "/api/transfers",
                json={"recipient_handle": "bob", "amount": "1000.00"},
                headers=headers,
            )
            assert resp2.status_code == 200
            assert resp1.json()["transfer"]["id"] == resp2.json()["transfer"]["id"]
        # Verify only one transfer, balances unchanged from first
        from backend.database import SessionLocal
        new_db = SessionLocal()
        try:
            transfers = list(new_db.scalars(select(Transfer)))
            assert len(transfers) == 1
            alice_acc = new_db.scalar(select(Account).where(Account.handle == "alice"))
            bob_acc = new_db.scalar(select(Account).where(Account.handle == "bob"))
            assert alice_acc.balance_paisa == INITIAL_BALANCE_PAISA - 100_000
            assert bob_acc.balance_paisa == INITIAL_BALANCE_PAISA + 100_000
        finally:
            new_db.close()

    def test_incompatible_key_reuse_returns_409(self, db_session: Session) -> None:
        with TestClient(app) as client:
            alice = register(client, "alice", "Alice")
            bob = register(client, "bob", "Bob")
            idem_key = str(uuid.uuid4())
            headers = transfer_headers(alice["access_token"], idem_key)
            client.post(
                "/api/transfers",
                json={"recipient_handle": "bob", "amount": "1000.00"},
                headers=headers,
            )
            # Same key, different amount
            resp = client.post(
                "/api/transfers",
                json={"recipient_handle": "bob", "amount": "2000.00"},
                headers=headers,
            )
            assert resp.status_code == 409
            assert resp.json()["code"] == "IDEMPOTENCY_KEY_REUSED"

    def test_sender_idempotency_uniqueness_exists(self, db_session: Session) -> None:
        """DB enforces UNIQUE(sender_account_id, idempotency_key)."""
        with TestClient(app) as client:
            alice = register(client, "alice", "Alice")
            bob = register(client, "bob", "Bob")
            idem_key = uuid.uuid4()
            # Insert directly into DB to test constraint
            db_session.execute(
                text(
                    "INSERT INTO transfers (id, sender_account_id, recipient_account_id, "
                    "amount_paisa, idempotency_key, kind) "
                    "VALUES (:id, :sid, :rid, :amt, :ik, :kind)"
                ),
                {
                    "id": str(uuid.uuid4()),
                    "sid": str(db_session.scalar(select(Account).where(Account.handle == "alice")).id),
                    "rid": str(db_session.scalar(select(Account).where(Account.handle == "bob")).id),
                    "amt": 10000,
                    "ik": str(idem_key),
                    "kind": "DIRECT",
                },
            )
            db_session.commit()

    def test_invalid_amount_rejected(self, db_session: Session) -> None:
        with TestClient(app) as client:
            alice = register(client, "alice", "Alice")
            bob = register(client, "bob", "Bob")
            headers = transfer_headers(alice["access_token"])
            resp = client.post(
                "/api/transfers",
                json={"recipient_handle": "bob", "amount": "abc"},
                headers=headers,
            )
        assert resp.status_code == 422

    def test_missing_idempotency_key_rejected(self, db_session: Session) -> None:
        with TestClient(app) as client:
            alice = register(client, "alice", "Alice")
            bob = register(client, "bob", "Bob")
            resp = client.post(
                "/api/transfers",
                json={"recipient_handle": "bob", "amount": "100.00"},
                headers=auth_header(alice["access_token"]),
            )
        assert resp.status_code == 422
        assert resp.json()["code"] == "IDEMPOTENCY_KEY_REQUIRED"

    def test_invalid_idempotency_key_rejected(self, db_session: Session) -> None:
        with TestClient(app) as client:
            alice = register(client, "alice", "Alice")
            bob = register(client, "bob", "Bob")
            headers = auth_header(alice["access_token"])
            headers["Idempotency-Key"] = "not-a-uuid"
            resp = client.post(
                "/api/transfers",
                json={"recipient_handle": "bob", "amount": "100.00"},
                headers=headers,
            )
        assert resp.status_code == 422
        assert resp.json()["code"] == "INVALID_IDEMPOTENCY_KEY"

    def test_unauthenticated_transfer_rejected(self, db_session: Session) -> None:
        with TestClient(app) as client:
            resp = client.post(
                "/api/transfers",
                json={"recipient_handle": "bob", "amount": "100.00"},
                headers={"Idempotency-Key": str(uuid.uuid4())},
            )
        assert resp.status_code == 401

    def test_persisted_read_back_new_session(self, db_session: Session) -> None:
        """Transfer persists and is readable from a completely fresh DB session."""
        with TestClient(app) as client:
            alice = register(client, "alice", "Alice")
            bob = register(client, "bob", "Bob")
            headers = transfer_headers(alice["access_token"])
            client.post(
                "/api/transfers",
                json={"recipient_handle": "bob", "amount": "7500.00"},
                headers=headers,
            )
        # Fresh session read-back
        from backend.database import SessionLocal
        new_db = SessionLocal()
        try:
            transfer = new_db.scalar(select(Transfer))
            assert transfer is not None
            assert transfer.amount_paisa == 750_000
            assert transfer.kind == "DIRECT"
            alice_acc = new_db.scalar(select(Account).where(Account.handle == "alice"))
            bob_acc = new_db.scalar(select(Account).where(Account.handle == "bob"))
            assert alice_acc.balance_paisa == INITIAL_BALANCE_PAISA - 750_000
            assert bob_acc.balance_paisa == INITIAL_BALANCE_PAISA + 750_000
        finally:
            new_db.close()


# ---------------------------------------------------------------------------
# Mandatory PostgreSQL concurrency test
# ---------------------------------------------------------------------------

class TestConcurrency:
    def test_two_concurrent_transfers_only_one_succeeds(self, db_session: Session) -> None:
        """Two concurrent BDT 800 transfers from Alice (BDT 1000) must allow at most one."""
        # Register accounts using API to get tokens
        with TestClient(app) as client:
            alice = register(client, "alice", "Alice")
            bob = register(client, "bob", "Bob")
            charlie = register(client, "charlie", "Charlie")

        # Set Alice balance to BDT 1000 (100000 paisa)
        db_session.execute(
            text("UPDATE accounts SET balance_paisa = 100000 WHERE handle = 'alice'")
        )
        db_session.commit()

        # Record pre-transfer total for conservation check
        from backend.database import SessionLocal as SL
        pre_db = SL()
        try:
            alice_pre = pre_db.scalar(select(Account).where(Account.handle == "alice")).balance_paisa
            bob_pre = pre_db.scalar(select(Account).where(Account.handle == "bob")).balance_paisa
            charlie_pre = pre_db.scalar(select(Account).where(Account.handle == "charlie")).balance_paisa
            total_before = alice_pre + bob_pre + charlie_pre
        finally:
            pre_db.close()

        alice_token = alice["access_token"]

        # Create two independent sessions simulating concurrent transactions
        from backend.database import SessionLocal
        session1 = SessionLocal()
        session2 = SessionLocal()
        try:
            results: list[tuple[int, str]] = []

            def do_transfer(session: Session, token: str, recipient: str, key: str) -> tuple[int, str]:
                """Simulate a transfer through the service in an isolated session."""
                from backend.services.accounts import find_account_by_raw_token
                from backend.services.transfers import execute_direct_transfer
                from backend.schemas.transfer import TransferRequest
                sender = find_account_by_raw_token(session, token)
                if sender is None:
                    return (-1, "sender_not_found")
                req = TransferRequest(recipient_handle=recipient, amount="800.00")
                try:
                    transfer, is_new = execute_direct_transfer(
                        session, sender, req, uuid.UUID(key)
                    )
                    session.commit()
                    return (201 if is_new else 200, "ok")
                except AppError as exc:
                    session.rollback()
                    return (409, exc.code)
                except Exception as exc:
                    session.rollback()
                    return (500, f"{type(exc).__name__}: {exc}")

            key1 = str(uuid.uuid4())
            key2 = str(uuid.uuid4())

            with ThreadPoolExecutor(max_workers=2) as pool:
                f1 = pool.submit(do_transfer, session1, alice_token, "bob", key1)
                f2 = pool.submit(do_transfer, session2, alice_token, "charlie", key2)
                r1 = f1.result()
                r2 = f2.result()
                results = [r1, r2]

            # Exactly one should succeed (201), the other fail (409)
            success_count = sum(1 for code, _ in results if code == 201)
            assert success_count == 1, f"Expected exactly one success, got {success_count} (results={results})"
            fail_count = sum(1 for code, _ in results if code == 409)
            assert fail_count == 1, f"Expected exactly one failure, got {fail_count} (results={results})"

            # Verify Alice's final balance is BDT 200 (20000 paisa)
            verify_db = SL()
            try:
                alice_acc = verify_db.scalar(select(Account).where(Account.handle == "alice"))
                assert alice_acc.balance_paisa == 20000, f"Expected 20000 paisa, got {alice_acc.balance_paisa}"
                assert alice_acc.balance_paisa >= 0, "Balance must never be negative"
            finally:
                verify_db.close()

            # Verify exactly one Transfer exists
            verify_db2 = SL()
            try:
                transfers = list(verify_db2.scalars(select(Transfer)))
                assert len(transfers) == 1, f"Expected 1 transfer, got {len(transfers)}"
                assert transfers[0].amount_paisa == 80000
            finally:
                verify_db2.close()

            # Verify total money conserved
            verify_db3 = SL()
            try:
                alice_acc = verify_db3.scalar(select(Account).where(Account.handle == "alice"))
                bob_acc = verify_db3.scalar(select(Account).where(Account.handle == "bob"))
                charlie_acc = verify_db3.scalar(select(Account).where(Account.handle == "charlie"))
                total_after = alice_acc.balance_paisa + bob_acc.balance_paisa + charlie_acc.balance_paisa
                assert total_after == total_before, f"Money not conserved: before={total_before} after={total_after}"
            finally:
                verify_db3.close()
        finally:
            session1.close()
            session2.close()
