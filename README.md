# Money Movement Application

PSTU National Hackathon 2026

A simulated-money Money Movement Application MVP where registered users can send and request simulated BDT while the backend preserves financial correctness under invalid input, retries, duplicate actions, and concurrent activity.

The MVP uses fake money only. It does not integrate with real banks, cards, payment gateways, deposits, withdrawals, KYC, or real financial systems.

## Implemented Golden Path

The complete Golden Path is verified and passes:

```text
Alice registers (BDT 100,000)
-> Bob registers (BDT 100,000)
-> Alice sends BDT 2,500 to Bob
-> balances: Alice=97,500.00, Bob=102,500.00
-> Bob requests BDT 1,200 from Alice
-> request=PENDING, no money moved
-> Alice fulfills the request
-> balances: Alice=96,300.00, Bob=103,700.00
-> request=COMPLETED, money moved exactly once
-> persistence verified after refresh/reload
-> one invalid operation rejected without corruption
```

## Architecture

```text
responsive same-origin HTML/CSS/JavaScript frontend
-> FastAPI (modular monolith)
-> Pydantic
-> services/business logic
-> SQLAlchemy
-> PostgreSQL
```

FastAPI serves both the static user-facing dashboard at `/` and `/api/...` endpoints.

## Money Representation

- **Internal:** integer paisa (bigint) for exact authoritative arithmetic
- **HTTP boundary:** fixed decimal BDT strings (e.g. `"2500.00"`)
- **Float is never used** for money calculations

## Authentication

Lightweight opaque bearer-token identity for the simulated-money MVP.

- Registration generates a raw bearer token returned to the browser
- Only a SHA-256 hash of the token is stored in the database
- The raw token is never persisted or logged
- All authenticated requests use `Authorization: Bearer <token>`

## Direct Transfer

- Exact atomic debit/credit/transfer in one PostgreSQL transaction
- Sender authority from bearer token, not frontend-supplied IDs
- Insufficient funds rejected without changing state
- `Idempotency-Key` header for retry and duplicate safety
- Same key + same payload = legitimate replay (200), no double movement
- Same key + different payload = 409 conflict

## MoneyRequest Lifecycle

```text
PENDING -> COMPLETED
```

- Request creation moves no money (PENDING state)
- Only the designated payer may fulfill
- Fulfillment debits payer, credits requester, inserts transfer atomically
- Same-key replay after completion returns original result (200)
- Different-key attempt after completion returns 409 REQUEST_ALREADY_COMPLETED

## Shared Transfer Engine

Both direct transfers and request fulfillment use the same underlying money movement service:

- `backend/services/transfers.py` — direct transfer orchestration
- `backend/services/requests.py` — request fulfillment orchestration

Both enforce identical invariants: canonical lock ordering, sufficient funds check post-lock, atomic debit/credit/transfer record.

## PostgreSQL Concurrency

- Row-level `SELECT ... FOR UPDATE` locks for concurrent spending protection
- Canonical ascending account-ID lock ordering to prevent deadlocks
- `populate_existing=True` execution option to refresh ORM instances after lock acquisition (prevents SQLAlchemy identity-map staleness)
- Balance checked after acquiring all locks, not before

## Idempotency Semantics

Every state-changing POST uses a client-generated UUID `Idempotency-Key` header:

| Operation | Same key + same payload | Same key + different payload |
|-----------|------------------------|------------------------------|
| Direct transfer | 200 replay, no duplicate | 409 IDEMPOTENCY_KEY_REUSED |
| Request creation | 200 replay | 409 IDEMPOTENCY_KEY_REUSED |
| Request fulfillment | 200 replay (even after completion) | 409 IDEMPOTENCY_KEY_REUSED |

## Database / Migrations

- PostgreSQL with Alembic for schema evolution
- Migration head: `0003_money_requests`
- Tables: `accounts`, `transfers`, `money_requests`
- Migrations are the authoritative schema management path

### Running Migrations

```bash
# Apply to application database
DATABASE_URL="postgresql://...pstu_money" python -m alembic upgrade head

# Apply to test database
DATABASE_URL="postgresql://...pstu_money_test" python -m alembic upgrade head
```

## Running Locally

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with PostgreSQL URLs

# Apply migrations
python -m alembic upgrade head

# Run the application
python -m uvicorn backend.main:app --reload

# Open browser
# http://127.0.0.1:8000/
```

## Running Tests

```bash
python -m pytest tests/ -v
```

Tests require a PostgreSQL test database (`pstu_money_test`). The `TEST_DATABASE_URL` environment variable must be set.

**Final suite: 56 passed, 0 failed, 0 skipped**

## Known MVP Limitations

- No password login, account recovery, or token revocation
- No request cancellation, rejection, expiry, or partial payment
- No transaction history UI
- No notifications or real-time updates
- No rate limiting or admin tooling
- No deployment (local demo only)
- Bearer tokens are stored in browser localStorage (demo-grade security)

## Project Structure

```text
backend/
  main.py              App composition, static UI, health endpoint
  config.py            Environment-based configuration
  database.py          SQLAlchemy engine/session setup
  errors.py            Application error types
  models/              SQLAlchemy persistence mappings
  routes/              HTTP endpoints
  schemas/             Pydantic request/response contracts
  services/            Application operations and orchestration
  logic/               Pure business logic (money parsing)
frontend/
  index.html           Same-origin responsive dashboard
migrations/
  versions/            Alembic schema migrations
tests/                 Automated verification
```

## Documentation Map

- `problem.md` — approved WHAT (requirements)
- `plan.md` — approved HOW (Master System Design)
- `execute.md` — live implementation status and evidence
- `README.md` — this file (project-facing documentation)
- actual code, tests, and migrations = implemented truth
