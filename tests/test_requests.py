from __future__ import annotations

import uuid
from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from backend import database
from backend.errors import AppError
from backend.logic.money import INITIAL_BALANCE_PAISA
from backend.main import app
from backend.models import Account, MoneyRequest, Transfer
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


def request_headers(token: str, idem_key: str | None = None) -> dict[str, str]:
    headers = auth_header(token)
    headers["Idempotency-Key"] = idem_key or str(uuid.uuid4())
    return headers


# ---------------------------------------------------------------------------
# Request Creation Tests
# ---------------------------------------------------------------------------

class TestRequestCreation:
    def test_request_creation_moves_no_money(self, db_session: Session) -> None:
        """Creating a request must not change any balances."""
        with TestClient(app) as client:
            alice = register(client, "alice", "Alice")
            bob = register(client, "bob", "Bob")

        # Verify initial balances
        from backend.database import SessionLocal
        pre_db = SessionLocal()
        try:
            alice_pre = pre_db.scalar(select(Account).where(Account.handle == "alice")).balance_paisa
            bob_pre = pre_db.scalar(select(Account).where(Account.handle == "bob")).balance_paisa
        finally:
            pre_db.close()

        with TestClient(app) as client:
            headers = request_headers(bob["access_token"])
            resp = client.post(
                "/api/requests",
                json={"payer_handle": "alice", "amount": "1200.00"},
                headers=headers,
            )

        assert resp.status_code == 201
        body = resp.json()
        assert body["request"]["state"] == "PENDING"
        assert body["request"]["amount"] == "1200.00"
        assert body["request"]["requester"]["handle"] == "bob"
        assert body["request"]["payer"]["handle"] == "alice"

        # Verify balances unchanged
        post_db = SessionLocal()
        try:
            alice_post = post_db.scalar(select(Account).where(Account.handle == "alice")).balance_paisa
            bob_post = post_db.scalar(select(Account).where(Account.handle == "bob")).balance_paisa
            assert alice_post == alice_pre
            assert bob_post == bob_pre
        finally:
            post_db.close()

    def test_request_appears_to_designated_payer(self, db_session: Session) -> None:
        """The pending request must appear in the payer's incoming list."""
        with TestClient(app) as client:
            alice = register(client, "alice", "Alice")
            bob = register(client, "bob", "Bob")

        with TestClient(app) as client:
            # Bob creates request
            headers = request_headers(bob["access_token"])
            client.post(
                "/api/requests",
                json={"payer_handle": "alice", "amount": "500.00"},
                headers=headers,
            )

            # Alice sees incoming requests
            resp = client.get(
                "/api/requests/incoming?status=pending",
                headers=auth_header(alice["access_token"]),
            )

        assert resp.status_code == 200
        data = resp.json()
        assert len(data["requests"]) == 1
        assert data["requests"][0]["requester"]["handle"] == "bob"
        assert data["requests"][0]["payer"]["handle"] == "alice"
        assert data["requests"][0]["amount"] == "500.00"
        assert data["requests"][0]["state"] == "PENDING"

    def test_only_payer_may_fulfill(self, db_session: Session) -> None:
        """Only the designated payer may fulfill a request."""
        with TestClient(app) as client:
            alice = register(client, "alice", "Alice")
            bob = register(client, "bob", "Bob")
            charlie = register(client, "charlie", "Charlie")

        with TestClient(app) as client:
            # Bob requests from Alice
            headers = request_headers(bob["access_token"])
            resp = client.post(
                "/api/requests",
                json={"payer_handle": "alice", "amount": "100.00"},
                headers=headers,
            )
            request_id = resp.json()["request"]["id"]

            # Charlie tries to fulfill (should fail)
            fulfill_headers = request_headers(charlie["access_token"])
            resp = client.post(
                f"/api/requests/{request_id}/fulfill",
                headers=fulfill_headers,
            )

        assert resp.status_code == 403
        assert resp.json()["code"] == "NOT_DESIGNATED_PAYER"

    def test_fulfillment_moves_money_once(self, db_session: Session) -> None:
        """Fulfilling a request must move money exactly once."""
        with TestClient(app) as client:
            alice = register(client, "alice", "Alice")
            bob = register(client, "bob", "Bob")

        with TestClient(app) as client:
            # Bob requests from Alice
            req_headers = request_headers(bob["access_token"])
            resp = client.post(
                "/api/requests",
                json={"payer_handle": "alice", "amount": "2500.00"},
                headers=req_headers,
            )
            request_id = resp.json()["request"]["id"]

            # Alice fulfills
            fulfill_headers = request_headers(alice["access_token"])
            resp = client.post(
                f"/api/requests/{request_id}/fulfill",
                headers=fulfill_headers,
            )

        assert resp.status_code == 201
        body = resp.json()
        assert body["request"]["state"] == "COMPLETED"
        assert body["transfer"]["kind"] == "REQUEST_FULFILLMENT"
        assert body["transfer"]["amount"] == "2500.00"

        # Verify balances
        from backend.database import SessionLocal
        verify_db = SessionLocal()
        try:
            alice_acc = verify_db.scalar(select(Account).where(Account.handle == "alice"))
            bob_acc = verify_db.scalar(select(Account).where(Account.handle == "bob"))
            assert alice_acc.balance_paisa == INITIAL_BALANCE_PAISA - 250_000
            assert bob_acc.balance_paisa == INITIAL_BALANCE_PAISA + 250_000

            # Verify one transfer exists
            transfers = list(verify_db.scalars(select(Transfer)))
            assert len(transfers) == 1
            assert transfers[0].kind == "REQUEST_FULFILLMENT"
            assert transfers[0].linked_request_id is not None

            # Verify request is completed
            mr = verify_db.scalar(select(MoneyRequest))
            assert mr.state == "COMPLETED"
            assert mr.completed_at is not None
        finally:
            verify_db.close()

    def test_request_creation_idempotency_replay(self, db_session: Session) -> None:
        """Same key + same operation returns 200 replay without extra request."""
        with TestClient(app) as client:
            alice = register(client, "alice", "Alice")
            bob = register(client, "bob", "Bob")

        with TestClient(app) as client:
            idem_key = str(uuid.uuid4())
            headers = request_headers(bob["access_token"], idem_key)

            resp1 = client.post(
                "/api/requests",
                json={"payer_handle": "alice", "amount": "100.00"},
                headers=headers,
            )
            assert resp1.status_code == 201

            # Replay with same key and same payload
            resp2 = client.post(
                "/api/requests",
                json={"payer_handle": "alice", "amount": "100.00"},
                headers=headers,
            )
            assert resp2.status_code == 200
            assert resp1.json()["request"]["id"] == resp2.json()["request"]["id"]

        # Verify only one request exists
        from backend.database import SessionLocal
        verify_db = SessionLocal()
        try:
            requests = list(verify_db.scalars(select(MoneyRequest)))
            assert len(requests) == 1
        finally:
            verify_db.close()

    def test_request_creation_incompatible_key_reuse(self, db_session: Session) -> None:
        """Same key + different payload returns 409."""
        with TestClient(app) as client:
            alice = register(client, "alice", "Alice")
            bob = register(client, "bob", "Bob")
            charlie = register(client, "charlie", "Charlie")

        with TestClient(app) as client:
            idem_key = str(uuid.uuid4())
            headers = request_headers(bob["access_token"], idem_key)

            client.post(
                "/api/requests",
                json={"payer_handle": "alice", "amount": "100.00"},
                headers=headers,
            )

            # Same key, different payer
            resp = client.post(
                "/api/requests",
                json={"payer_handle": "charlie", "amount": "100.00"},
                headers=headers,
            )
            assert resp.status_code == 409
            assert resp.json()["code"] == "IDEMPOTENCY_KEY_REUSED"

    def test_self_request_rejected(self, db_session: Session) -> None:
        """Cannot request money from yourself."""
        with TestClient(app) as client:
            alice = register(client, "alice", "Alice")

        with TestClient(app) as client:
            headers = request_headers(alice["access_token"])
            resp = client.post(
                "/api/requests",
                json={"payer_handle": "alice", "amount": "100.00"},
                headers=headers,
            )
        assert resp.status_code == 400
        assert resp.json()["code"] == "SELF_REQUEST"

    def test_unknown_payer_rejected(self, db_session: Session) -> None:
        """Unknown payer handle is rejected."""
        with TestClient(app) as client:
            alice = register(client, "alice", "Alice")

        with TestClient(app) as client:
            headers = request_headers(alice["access_token"])
            resp = client.post(
                "/api/requests",
                json={"payer_handle": "nonexistent", "amount": "100.00"},
                headers=headers,
            )
        assert resp.status_code == 404
        assert resp.json()["code"] == "PAYER_NOT_FOUND"


# ---------------------------------------------------------------------------
# Fulfillment Tests
# ---------------------------------------------------------------------------

class TestFulfillment:
    def test_fulfillment_replay_returns_200(self, db_session: Session) -> None:
        """Same key + same request + same payer returns 200 without second transfer."""
        with TestClient(app) as client:
            alice = register(client, "alice", "Alice")
            bob = register(client, "bob", "Bob")

        with TestClient(app) as client:
            # Bob requests
            req_headers = request_headers(bob["access_token"])
            resp = client.post(
                "/api/requests",
                json={"payer_handle": "alice", "amount": "100.00"},
                headers=req_headers,
            )
            request_id = resp.json()["request"]["id"]

            # Alice fulfills
            fulfill_key = str(uuid.uuid4())
            fulfill_headers = request_headers(alice["access_token"], fulfill_key)
            resp1 = client.post(
                f"/api/requests/{request_id}/fulfill",
                headers=fulfill_headers,
            )
            assert resp1.status_code == 201

            # Replay with same key
            resp2 = client.post(
                f"/api/requests/{request_id}/fulfill",
                headers=fulfill_headers,
            )
            assert resp2.status_code == 200
            assert resp1.json()["transfer"]["id"] == resp2.json()["transfer"]["id"]

        # Verify only one transfer
        from backend.database import SessionLocal
        verify_db = SessionLocal()
        try:
            transfers = list(verify_db.scalars(select(Transfer)))
            assert len(transfers) == 1
        finally:
            verify_db.close()

    def test_different_key_on_completed_request_rejected(self, db_session: Session) -> None:
        """Completed request + different key returns 409 REQUEST_ALREADY_COMPLETED."""
        with TestClient(app) as client:
            alice = register(client, "alice", "Alice")
            bob = register(client, "bob", "Bob")

        with TestClient(app) as client:
            # Bob requests
            req_headers = request_headers(bob["access_token"])
            resp = client.post(
                "/api/requests",
                json={"payer_handle": "alice", "amount": "100.00"},
                headers=req_headers,
            )
            request_id = resp.json()["request"]["id"]

            # Alice fulfills with key1
            key1 = str(uuid.uuid4())
            fulfill_headers1 = request_headers(alice["access_token"], key1)
            client.post(
                f"/api/requests/{request_id}/fulfill",
                headers=fulfill_headers1,
            )

            # Alice tries again with key2
            key2 = str(uuid.uuid4())
            fulfill_headers2 = request_headers(alice["access_token"], key2)
            resp = client.post(
                f"/api/requests/{request_id}/fulfill",
                headers=fulfill_headers2,
            )

        assert resp.status_code == 409
        assert resp.json()["code"] == "REQUEST_ALREADY_COMPLETED"

    def test_fulfillment_insufficient_funds(self, db_session: Session) -> None:
        """Fulfillment rejected when payer has insufficient funds."""
        with TestClient(app) as client:
            alice = register(client, "alice", "Alice")
            bob = register(client, "bob", "Bob")

        # Set Alice balance to BDT 100
        db_session.execute(
            text("UPDATE accounts SET balance_paisa = 10000 WHERE handle = 'alice'")
        )
        db_session.commit()

        with TestClient(app) as client:
            # Bob requests BDT 200
            req_headers = request_headers(bob["access_token"])
            resp = client.post(
                "/api/requests",
                json={"payer_handle": "alice", "amount": "200.00"},
                headers=req_headers,
            )
            request_id = resp.json()["request"]["id"]

            # Alice tries to fulfill
            fulfill_headers = request_headers(alice["access_token"])
            resp = client.post(
                f"/api/requests/{request_id}/fulfill",
                headers=fulfill_headers,
            )

        assert resp.status_code == 409
        assert resp.json()["code"] == "INSUFFICIENT_FUNDS"

        # Verify no state change
        from backend.database import SessionLocal
        verify_db = SessionLocal()
        try:
            alice_acc = verify_db.scalar(select(Account).where(Account.handle == "alice"))
            assert alice_acc.balance_paisa == 10_000  # unchanged
            mr = verify_db.scalar(select(MoneyRequest))
            assert mr.state == "PENDING"  # still pending
            transfers = list(verify_db.scalars(select(Transfer)))
            assert len(transfers) == 0  # no transfer
        finally:
            verify_db.close()

    def test_unknown_request_rejected(self, db_session: Session) -> None:
        """Unknown request ID is rejected."""
        with TestClient(app) as client:
            alice = register(client, "alice", "Alice")

        fake_id = str(uuid.uuid4())
        with TestClient(app) as client:
            headers = request_headers(alice["access_token"])
            resp = client.post(
                f"/api/requests/{fake_id}/fulfill",
                headers=headers,
            )
        assert resp.status_code == 404
        assert resp.json()["code"] == "REQUEST_NOT_FOUND"

    def test_fulfillment_persisted_read_back(self, db_session: Session) -> None:
        """Fulfillment persists correctly and is readable from a fresh session."""
        with TestClient(app) as client:
            alice = register(client, "alice", "Alice")
            bob = register(client, "bob", "Bob")

        with TestClient(app) as client:
            # Bob requests
            req_headers = request_headers(bob["access_token"])
            resp = client.post(
                "/api/requests",
                json={"payer_handle": "alice", "amount": "3000.00"},
                headers=req_headers,
            )
            request_id = resp.json()["request"]["id"]

            # Alice fulfills
            fulfill_headers = request_headers(alice["access_token"])
            client.post(
                f"/api/requests/{request_id}/fulfill",
                headers=fulfill_headers,
            )

        # Fresh session read-back
        from backend.database import SessionLocal
        verify_db = SessionLocal()
        try:
            mr = verify_db.scalar(select(MoneyRequest))
            assert mr is not None
            assert mr.state == "COMPLETED"
            assert mr.completed_at is not None

            transfer = verify_db.scalar(
                select(Transfer).where(Transfer.linked_request_id == mr.id)
            )
            assert transfer is not None
            assert transfer.kind == "REQUEST_FULFILLMENT"
            assert transfer.amount_paisa == 300_000

            alice_acc = verify_db.scalar(select(Account).where(Account.handle == "alice"))
            bob_acc = verify_db.scalar(select(Account).where(Account.handle == "bob"))
            assert alice_acc.balance_paisa == INITIAL_BALANCE_PAISA - 300_000
            assert bob_acc.balance_paisa == INITIAL_BALANCE_PAISA + 300_000
        finally:
            verify_db.close()


# ---------------------------------------------------------------------------
# Mandatory PostgreSQL concurrency test for fulfillment
# ---------------------------------------------------------------------------

class TestFulfillmentConcurrency:
    def test_two_concurrent_fulfillments_only_one_succeeds(self, db_session: Session) -> None:
        """Two concurrent fulfillments of the same request must allow at most one."""
        with TestClient(app) as client:
            alice = register(client, "alice", "Alice")
            bob = register(client, "bob", "Bob")

        # Set Alice balance to BDT 1000
        db_session.execute(
            text("UPDATE accounts SET balance_paisa = 100000 WHERE handle = 'alice'")
        )
        db_session.commit()

        # Bob creates a request for BDT 800
        with TestClient(app) as client:
            req_headers = request_headers(bob["access_token"])
            resp = client.post(
                "/api/requests",
                json={"payer_handle": "alice", "amount": "800.00"},
                headers=req_headers,
            )
            request_id = uuid.UUID(resp.json()["request"]["id"])

        # Record pre-fulfillment total
        from backend.database import SessionLocal as SL
        pre_db = SL()
        try:
            alice_pre = pre_db.scalar(select(Account).where(Account.handle == "alice")).balance_paisa
            bob_pre = pre_db.scalar(select(Account).where(Account.handle == "bob")).balance_paisa
            total_before = alice_pre + bob_pre
        finally:
            pre_db.close()

        alice_token = alice["access_token"]

        # Create two independent sessions simulating concurrent transactions
        session1 = SL()
        session2 = SL()
        try:
            def do_fulfill(session: Session, token: str, req_id: uuid.UUID, key: str) -> tuple[int, str]:
                from backend.services.accounts import find_account_by_raw_token
                from backend.services.requests import fulfill_money_request
                payer = find_account_by_raw_token(session, token)
                if payer is None:
                    return (-1, "payer_not_found")
                try:
                    mr, transfer, is_new = fulfill_money_request(
                        session, payer, req_id, uuid.UUID(key)
                    )
                    session.commit()
                    return (201 if is_new else 200, "ok")
                except AppError as exc:
                    session.rollback()
                    return (exc.status_code, exc.code)
                except Exception as exc:
                    session.rollback()
                    return (500, f"{type(exc).__name__}: {exc}")

            key1 = str(uuid.uuid4())
            key2 = str(uuid.uuid4())

            with ThreadPoolExecutor(max_workers=2) as pool:
                f1 = pool.submit(do_fulfill, session1, alice_token, request_id, key1)
                f2 = pool.submit(do_fulfill, session2, alice_token, request_id, key2)
                r1 = f1.result()
                r2 = f2.result()

            # Exactly one should succeed
            success_count = sum(1 for code, _ in [r1, r2] if code == 201)
            assert success_count == 1, f"Expected exactly one success, got {success_count} (results={[r1, r2]})"
            fail_count = sum(1 for code, _ in [r1, r2] if code == 409)
            assert fail_count == 1, f"Expected exactly one failure, got {fail_count} (results={[r1, r2]})"

            # Verify Alice's final balance is BDT 200 (20000 paisa)
            verify_db = SL()
            try:
                alice_acc = verify_db.scalar(select(Account).where(Account.handle == "alice"))
                assert alice_acc.balance_paisa == 20000, f"Expected 20000 paisa, got {alice_acc.balance_paisa}"
            finally:
                verify_db.close()

            # Verify exactly one transfer exists
            verify_db2 = SL()
            try:
                transfers = list(verify_db2.scalars(select(Transfer)))
                assert len(transfers) == 1, f"Expected 1 transfer, got {len(transfers)}"
                assert transfers[0].amount_paisa == 80000
                assert transfers[0].kind == "REQUEST_FULFILLMENT"
            finally:
                verify_db2.close()

            # Verify total money conserved
            verify_db3 = SL()
            try:
                alice_acc = verify_db3.scalar(select(Account).where(Account.handle == "alice"))
                bob_acc = verify_db3.scalar(select(Account).where(Account.handle == "bob"))
                total_after = alice_acc.balance_paisa + bob_acc.balance_paisa
                assert total_after == total_before, f"Money not conserved: before={total_before} after={total_after}"
            finally:
                verify_db3.close()
        finally:
            session1.close()
            session2.close()


# ---------------------------------------------------------------------------
# Golden Path smoke test (WS-01 + WS-02 + WS-03)
# ---------------------------------------------------------------------------

class TestGoldenPath:
    def test_full_golden_path(self, db_session: Session) -> None:
        """Complete Golden Path: register, send, request, fulfill, verify persistence."""
        with TestClient(app) as client:
            # 1-2. Register Alice and Bob
            alice = register(client, "alice", "Alice")
            bob = register(client, "bob", "Bob")
            assert alice["balance"] == "100000.00"
            assert bob["balance"] == "100000.00"

            # 3. Alice sends BDT 2,500 to Bob
            idem_key1 = str(uuid.uuid4())
            headers1 = request_headers(alice["access_token"], idem_key1)
            resp = client.post(
                "/api/transfers",
                json={"recipient_handle": "bob", "amount": "2500.00"},
                headers=headers1,
            )
            assert resp.status_code == 201

            # 4. Verify balances after send
            me1 = client.get("/api/auth/me", headers=auth_header(alice["access_token"]))
            me2 = client.get("/api/auth/me", headers=auth_header(bob["access_token"]))
            assert me1.json()["balance"] == "97500.00"
            assert me2.json()["balance"] == "102500.00"

            # 5. Bob requests BDT 1,200 from Alice
            req_idem = str(uuid.uuid4())
            req_headers = request_headers(bob["access_token"], req_idem)
            resp = client.post(
                "/api/requests",
                json={"payer_handle": "alice", "amount": "1200.00"},
                headers=req_headers,
            )
            assert resp.status_code == 201
            assert resp.json()["request"]["state"] == "PENDING"
            request_id = resp.json()["request"]["id"]

            # 6. No money moved yet
            me1 = client.get("/api/auth/me", headers=auth_header(alice["access_token"]))
            me2 = client.get("/api/auth/me", headers=auth_header(bob["access_token"]))
            assert me1.json()["balance"] == "97500.00"
            assert me2.json()["balance"] == "102500.00"

            # 7. Alice sees pending request
            resp = client.get(
                "/api/requests/incoming?status=pending",
                headers=auth_header(alice["access_token"]),
            )
            assert resp.status_code == 200
            assert len(resp.json()["requests"]) == 1
            assert resp.json()["requests"][0]["id"] == request_id

            # 8. Alice fulfills the request
            fulfill_key = str(uuid.uuid4())
            fulfill_headers = request_headers(alice["access_token"], fulfill_key)
            resp = client.post(
                f"/api/requests/{request_id}/fulfill",
                headers=fulfill_headers,
            )
            assert resp.status_code == 201
            assert resp.json()["request"]["state"] == "COMPLETED"
            assert resp.json()["transfer"]["kind"] == "REQUEST_FULFILLMENT"

            # 9. Verify final balances
            me1 = client.get("/api/auth/me", headers=auth_header(alice["access_token"]))
            me2 = client.get("/api/auth/me", headers=auth_header(bob["access_token"]))
            # Alice: 100000 - 2500 - 1200 = 96300
            # Bob: 100000 + 2500 + 1200 = 103700
            assert me1.json()["balance"] == "96300.00"
            assert me2.json()["balance"] == "103700.00"

            # 10. Persistence after fresh TestClient
        with TestClient(app) as client:
            me1 = client.get("/api/auth/me", headers=auth_header(alice["access_token"]))
            me2 = client.get("/api/auth/me", headers=auth_header(bob["access_token"]))
            assert me1.json()["balance"] == "96300.00"
            assert me2.json()["balance"] == "103700.00"

            # 11. Important: same-key replay returns 200 (no double-transfer)
            resp = client.post(
                f"/api/requests/{request_id}/fulfill",
                headers=fulfill_headers,
            )
            assert resp.status_code == 200  # legitimate idempotent replay
            assert resp.json()["request"]["state"] == "COMPLETED"

            # 12. Different key on completed request returns 409
            diff_key_headers = request_headers(alice["access_token"], str(uuid.uuid4()))
            resp = client.post(
                f"/api/requests/{request_id}/fulfill",
                headers=diff_key_headers,
            )
            assert resp.status_code == 409
            assert resp.json()["code"] == "REQUEST_ALREADY_COMPLETED"

        # Verify DB state
        from backend.database import SessionLocal
        verify_db = SessionLocal()
        try:
            transfers = list(verify_db.scalars(select(Transfer)))
            assert len(transfers) == 2  # 1 direct + 1 fulfillment

            requests = list(verify_db.scalars(select(MoneyRequest)))
            assert len(requests) == 1
            assert requests[0].state == "COMPLETED"

            total = sum(
                verify_db.scalar(select(Account)).balance_paisa
                for _ in range(1)
            )
            # Verify conservation: total should be 200000
            alice_final = verify_db.scalar(select(Account).where(Account.handle == "alice")).balance_paisa
            bob_final = verify_db.scalar(select(Account).where(Account.handle == "bob")).balance_paisa
            assert alice_final + bob_final == INITIAL_BALANCE_PAISA * 2
        finally:
            verify_db.close()
