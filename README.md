# Money Movement Application

A concurrency-safe, idempotent simulated BDT transfer and request system built with FastAPI and PostgreSQL.

## Overview

Money Movement Application is a closed-ecosystem MVP for moving fake BDT between demo users. Users can register accounts, receive an initial simulated balance, send money, request money, view incoming requests, fulfill requests, and refresh persisted financial state.

The technical focus is backend correctness: exact money arithmetic, server-derived authority, atomic state changes, retry safety, and PostgreSQL row-level concurrency control. The frontend is intentionally lightweight: one same-origin HTML/CSS/vanilla JavaScript dashboard served by FastAPI.

This is not a production banking system. It does not connect to real banks, cards, payment gateways, deposits, withdrawals, KYC, or real-money infrastructure.

## Key Features

- Demo account registration with opaque bearer-token identity
- Initial simulated balance of BDT `100000.00` per new account
- Direct money transfers between valid application users
- Request Money workflow with incoming pending request view
- Request fulfillment by the designated payer
- Persistent PostgreSQL account, transfer, and request state
- Retry-safe idempotency for direct sends, request creation, and fulfillment
- PostgreSQL row locks for concurrent spending protection
- Exact integer-paisa financial arithmetic with no float math

## Golden Path

```text
Zihan starts:   100000.00
Ashfika starts: 100000.00

Zihan sends Ashfika 2500.00
Zihan:    97500.00
Ashfika: 102500.00

Ashfika requests 1200.00 from Zihan
Request: PENDING
Balances unchanged

Zihan fulfills the request
Zihan:    96300.00
Ashfika: 103700.00
Request: COMPLETED

Total conserved after account creation: 200000.00
```

## Architecture

```text
Browser
  |
  v
FastAPI routes
  |
  +--> Pydantic schemas
  +--> Bearer-token authentication
  |
  v
Service layer
  |
  v
SQLAlchemy
  |
  v
PostgreSQL
```

The project uses a modular monolith because the MVP is bounded, local-demo friendly, quick to explain, and does not need distributed infrastructure. FastAPI serves the dashboard at `/` and the JSON API under `/api/...`. Alembic owns schema migrations, and pytest verifies the backend and database behavior.

## Backend Correctness Model

### Exact Money

HTTP uses decimal BDT strings such as `"2500.00"`. Internally, money is parsed into integer paisa, so `"2500.00"` becomes `250000`. PostgreSQL stores balances and amounts as integer `BIGINT` values. Authoritative money calculations never use floating-point arithmetic.

### Atomic Transfers

A direct transfer debits the sender, credits the recipient, and inserts the transfer record in one transaction. Request fulfillment debits the payer, credits the requester, inserts a `REQUEST_FULFILLMENT` transfer, and marks the request `COMPLETED` in one transaction.

### Concurrency Control

Transfers use PostgreSQL `SELECT ... FOR UPDATE` through SQLAlchemy. Both affected account rows are locked in canonical UUID order, then the balance is checked after the locks are held. `populate_existing=True` refreshes SQLAlchemy identity-mapped rows after lock waits so stale in-memory balances are not reused.

Verified concurrency scenario:

```text
Zihan has BDT 1000.00
Two concurrent outgoing transfers attempt BDT 800.00 each
Exactly one succeeds
The other receives insufficient funds
Zihan ends at BDT 200.00
```

### Idempotency

State-changing POST requests use a client-generated UUID in the `Idempotency-Key` header. A retry with the same logical operation returns the original result instead of moving money again. Reusing the same key for an incompatible operation is rejected with `409 IDEMPOTENCY_KEY_REUSED`.

The frontend preserves the same key across ambiguous retries for direct send, request creation, and request fulfillment. A new logical operation receives a new key.

### Authentication And Authority

Registration issues an opaque bearer token to the browser. The database stores a SHA-256 token hash, not the raw token. The authenticated bearer identity determines the sender, requester, or payer; the frontend does not choose the authoritative spending account.

For demo account switching, the browser stores account credentials in `localStorage`. This is hackathon/demo authentication, not production auth.

## Money Request Lifecycle

```text
PENDING -> COMPLETED
```

Creating a request moves no money. The authenticated requester chooses a payer, and only that designated payer can fulfill the pending request. Fulfillment uses the same money movement model as direct transfer and serializes competing attempts with a `MoneyRequest` row lock.

Duplicate fulfillment is currently prevented by request row locking, the `PENDING -> COMPLETED` service transition, and fulfillment idempotency/service logic. The schema has a foreign key and index on `transfers.linked_request_id`; a database-level unique linked-request constraint remains a possible defense-in-depth improvement.

## Technology Stack

| Area | Technology |
| --- | --- |
| Backend | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Validation | Pydantic |
| Frontend | HTML, CSS, vanilla JavaScript |
| Testing | pytest |
| Server | Uvicorn |

## Repository Structure

```text
backend/
  models/      SQLAlchemy persistence mappings
  schemas/     Pydantic request/response contracts
  services/    Application operations and transactions
  routes/      FastAPI HTTP endpoints
  logic/       Pure money parsing and validation helpers
frontend/      Same-origin browser dashboard
migrations/    Alembic schema migrations
tests/         PostgreSQL-backed automated verification

problem.md     Approved problem interpretation
plan.md        Approved engineering design
execute.md     Verified implementation tracker
```

## API Overview

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/api/health` | Health check |
| `POST` | `/api/auth/register` | Register account and issue bearer token |
| `GET` | `/api/auth/me` | Read authenticated account and balance |
| `GET` | `/api/users?query=...` | Search valid users |
| `POST` | `/api/transfers` | Create direct transfer |
| `POST` | `/api/requests` | Create money request |
| `GET` | `/api/requests/incoming?status=pending` | List pending requests for current payer |
| `POST` | `/api/requests/{request_id}/fulfill` | Fulfill pending request |

## Local Setup

Use Windows PowerShell from the repository root.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` with private local PostgreSQL credentials:

```env
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/money_movement_app
TEST_DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/money_movement_app_test
```

The app and test databases must be different. The test database name must end with `_test`.

Apply migrations and start the app:

```powershell
python -m alembic upgrade head
python -m uvicorn backend.main:app --reload --port 8000
```

Open:

```text
http://127.0.0.1:8000/
```

If port `8000` is unavailable, use another local port such as `8001`:

```powershell
python -m uvicorn backend.main:app --reload --port 8001
```

## Running Tests

```powershell
python -m pytest tests -q
```

Verified release result:

```text
56 passed
0 failed
0 skipped
```

## Demo Walkthrough

1. Register Zihan.
2. Register Ashfika.
3. Switch to Zihan and send Ashfika `2500.00`.
4. Confirm Zihan shows `97500.00` and Ashfika shows `102500.00`.
5. Switch to Ashfika and request `1200.00` from Zihan.
6. Switch to Zihan and view the incoming pending request.
7. Fulfill the request.
8. Confirm Zihan shows `96300.00`, Ashfika shows `103700.00`, and the request is no longer pending.
9. Refresh to demonstrate persisted state.

## Important Engineering Decisions

- Store money as integer paisa instead of floating-point values.
- Derive financial authority from the authenticated bearer token.
- Use database transactions for each accepted money movement.
- Lock account rows with deterministic ordering for concurrent transfers.
- Refresh ORM instances after lock waits to avoid stale balances.
- Use idempotency keys across retries for all money-moving or state-creating POSTs.
- Keep the frontend lightweight and backend-authoritative.
- Avoid microservices, queues, distributed locks, and deployment complexity for this bounded MVP.

## Verified State

- Workstreams complete: WS-01 account/auth, WS-02 direct transfer, WS-03 request/fulfillment, WS-04 Golden Path integration, WS-05 release readiness
- Alembic head: `0003_money_requests`
- Full backend suite: `56 passed, 0 failed, 0 skipped`
- Golden Path verified against PostgreSQL
- Local browser UI served by FastAPI at `/`
- Current release checkpoint includes the frontend retry-safety fix

## Limitations And Future Work

- No phone, password, OTP, or production login flow
- Browser credentials stored in `localStorage`
- No account recovery or token revocation
- No request cancellation, rejection, expiry, editing, or partial payment
- No transaction-history UI
- No notifications or real-time updates
- No rate limiting or admin tooling
- No public production deployment
- No browser E2E automation
- No real money, bank, card, or payment-gateway integration
- Database-level unique constraint on `transfers.linked_request_id` can be added as defense in depth

## Event Context

Built for PSTU National Hackathon 2026 as a local-demo software MVP. Public deployment is not required by the current repository release decision.
