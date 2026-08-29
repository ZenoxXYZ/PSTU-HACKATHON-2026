# Execution Tracker

## Markers

- [ ] Pending
- [~] In progress
- [x] Completed and verified
- [!] Blocked by a known issue or bug
- [?] Requires clarification or an engineering/design decision

## Current Status

[x] WS-01 Authoritative Account Foundation completed and verified.
[x] WS-02 Direct Transfer Vertical Slice completed and verified.
[x] WS-03 Money Request + Fulfillment Vertical Slice completed and verified.
[x] WS-04 Golden-Path Integration + Hardening completed and verified.
[x] WS-05 Release + Demo Readiness completed and verified.

`problem.md` contains the approved Money Movement Application problem definition. `plan.md` contains the approved Master System Design and capability-oriented workstream map. All five workstreams are complete. Full Golden Path E2E verified through real PostgreSQL backend. Final test suite: 56 passed, 0 failed, 0 skipped. Migration head: `0003_money_requests`. Local web application serves the full dashboard at `http://127.0.0.1:8000/`.

## Repository Reality At Initialization

- [x] Generic starter foundation exists.
- [x] Generic starter tests exist.
- [x] Approved `problem.md` exists.
- [x] Approved `plan.md` exists.
- [x] Product-specific implementation started with WS-01.
- [x] Product-specific WS-01 verification completed against PostgreSQL.

## Workstream Status Summary

| Workstream | Capability | Status | Golden Path | Blocker | Next |
| ---------- | ---------- | ------ | ----------- | ------- | ---- |
| WS-01 | Authoritative Account Foundation | COMPLETED AND VERIFIED | Supports Alice/Bob setup | None | Complete |
| WS-02 | Direct Transfer Vertical Slice | COMPLETED AND VERIFIED | Alice sends BDT 2,500 to Bob | None | Complete |
| WS-03 | Money Request + Fulfillment Vertical Slice | COMPLETED AND VERIFIED | Bob requests BDT 1,200 from Alice; Alice fulfills | None | Complete |
| WS-04 | Golden-Path Integration + Hardening | COMPLETED AND VERIFIED | Full Alice/Bob journey through real frontend/API/backend/PostgreSQL | None | Complete |
| WS-05 | Release + Demo Readiness | COMPLETED AND VERIFIED | Local demo ready | None | Complete |

## WS-01 - Authoritative Account Foundation

Objective / capability:
Establish PostgreSQL persistence, accounts, lightweight token identity, registration, current balance, and user discovery.

Golden-Path relationship:
Supports Alice/Bob setup.

Dependencies:
Approved `problem.md`, approved `plan.md`, and safe app/test PostgreSQL configuration.

Relevant contracts:
Account entity, registration, current-user, and user-search contracts.

### Backend

- [x] Add account registration use case.
- [x] Add bearer-token generation, storage hash/secure representation, and authentication dependency.
- [x] Add current-user resolution.
- [x] Add user discovery/search behavior.

### Frontend

- [ ] N/A until the account contracts are stable enough for the approved same-origin dashboard scope.

### Persistence

- [x] Add account persistence mapping and constraints.
- [x] Add explicit Alembic migration.
- [x] Ensure registration provisions BDT 100,000 exactly once.

### Integration

- [x] Registration endpoint returns token, user summary, and balance.
- [x] Current-user endpoint returns authenticated user and authoritative balance.
- [x] User search endpoint returns selectable public user summaries.

### Infrastructure

- [x] Confirm safe app/test PostgreSQL URLs before running migrations or database tests.

### Verification

- [x] Safe app/test DB configuration verified.
- [x] Migration applies.
- [x] Registration provisions BDT 100,000 exactly once.
- [x] Duplicate handles rejected.
- [x] Bearer token resolves current actor.
- [x] Current balance returned correctly.
- [x] User lookup works.
- [x] `git diff --check`.
- [x] `git status`.

Status:
COMPLETED AND VERIFIED.

Evidence:
- `backend/models/account.py` defines the WS-01 Account persistence mapping.
- `migrations/versions/0001_accounts.py` is present and `python -m alembic heads` reports `0001_accounts (head)`.
- `backend/routes/auth.py` and `backend/routes/users.py` expose the approved WS-01 API surface.
- Environment safety check verified ignored `.env` loading without exposing credentials: application DB `pstu_money`, test DB `pstu_money_test`, PostgreSQL psycopg URLs, different targets, and `_test` guard.
- Connectivity to both `pstu_money` and `pstu_money_test` passed.
- Test DB Alembic upgrade/current/head passed at `0001_accounts (head)`.
- PostgreSQL schema check verified `accounts` table, UUID id, bigint balance, token hash, required columns, unique handle/token indexes, and non-negative balance constraint.
- Focused PostgreSQL-backed WS-01 tests passed: 14 passed, 0 skipped.
- Full test suite passed: 18 passed, 0 skipped.
- Application DB Alembic upgrade/current/head passed at `0001_accounts (head)`.
- PostgreSQL-backed API smoke passed: Alice and Bob registration returned `201` with `"100000.00"`, Alice `/api/auth/me` returned persisted identity/balance, authenticated user search found Bob and exposed only public fields, duplicate normalized registration returned `409 HANDLE_ALREADY_EXISTS`, and no extra account/starting balance was created.
- Reopened PostgreSQL session read back Alice account state with `10_000_000` paisa balance.
- `git diff --check` passed.

Blocker:
None for WS-01.

Next step:
Stop for Control Room review and Workstream Reconstruction, then start WS-02 only after approval.

Deferrals:
Passwords, recovery, token revocation, production authentication hardening, and multi-device account security.

## WS-02 - Direct Transfer Vertical Slice

Objective / capability:
Deliver exact, atomic, idempotent, and concurrency-safe direct money transfer through the real frontend/API/backend/database path.

Golden-Path relationship:
Alice sends BDT 2,500 to Bob.

Dependencies:
WS-01 completed and verified.

Relevant contracts:
Transfer entity, `POST /api/transfers`, money representation, and idempotency-key behavior.

### Backend

- [x] Add direct transfer route/schema/service.
- [x] Enforce authenticated sender authority from bearer token.
- [x] Validate recipient, amount, self-transfer, sufficient funds, and idempotency behavior.
- [x] Translate domain errors to stable API errors.

### Frontend

- [x] Add send-money UI using the real endpoint.
- [x] Generate and retain idempotency key for active mutation/retry.
- [x] Refetch authoritative balance after success.
- [x] Render loading, success, and important error states.

### Persistence

- [x] Add transfer persistence mapping and constraints.
- [x] Persist immutable successful transfers.
- [x] Use PostgreSQL row-level `FOR UPDATE` locking through SQLAlchemy.
- [x] Lock multiple account rows in canonical ascending account-ID order.

### Integration

- [x] Real send form calls real API.
- [x] Backend persists one atomic debit/credit/transfer.
- [x] Frontend displays refreshed authoritative balances.

### Infrastructure

- [x] Use isolated PostgreSQL test database for concurrency verification.

### Verification

- [x] Exact money math.
- [x] Atomic debit/credit.
- [x] Insufficient funds changes nothing.
- [x] Same idempotency key does not double-transfer.
- [x] Incompatible key reuse rejected.
- [x] Concurrent BDT 800 + BDT 800 attempts against BDT 1,000 allow at most one success.
- [x] Real send form calls real endpoint.
- [x] Balance refetch/display is correct.
- [x] `git diff --check`.
- [x] `git status`.

Status:
COMPLETED AND VERIFIED.

Evidence:
- `backend/models/transfer.py` defines the WS-02 Transfer persistence mapping.
- `migrations/versions/0002_transfers.py` is present and `python -m alembic heads` reports `0002_transfers (head)`.
- `backend/routes/transfers.py`, `backend/schemas/transfer.py`, and `backend/services/transfers.py` expose the approved WS-02 API surface.
- `backend/logic/money.py` extended with `parse_paisa()` for exact integer paisa conversion without float.
- Application DB Alembic upgrade/current/head passed at `0002_transfers (head)`.
- PostgreSQL schema check verified `transfers` table: UUID id, UUID FK sender/recipient, bigint amount_paisa, UUID idempotency_key, kind varchar, timestamptz created_at, CHECK amount > 0, CHECK no self-transfer, UNIQUE (sender, idempotency_key), FK constraints to accounts.
- 23 WS-02 focused tests passed: 8 money parsing tests, 13 API behavior tests (exact balances, bearer authority, unknown recipient, self-transfer, insufficient funds, money conservation, idempotency replay, incompatible key reuse, missing/invalid idempotency key, unauthenticated, persisted read-back).
- Mandatory PostgreSQL concurrency test passed: 2 independent sessions, concurrent BDT 800 + BDT 800 against BDT 1,000, exactly one succeeds, one fails INSUFFICIENT_FUNDS, Alice ends BDT 200, one transfer persisted, total money conserved.
- Full test suite passed: 41 passed, 0 skipped.
- Golden Path smoke test passed: Alice register → 100000.00, Bob register → 100000.00, Alice sends BDT 2500 to Bob → 201, Alice balance 97500.00, Bob balance 102500.00, same-key replay → 200 no duplicate, persistence verified after fresh TestClient, DB verification: 1 transfer, total conserved.
- `git diff --check` passed.
- `.env` not tracked, no credentials leaked, no MoneyRequest implementation found.

Blocker:
None for WS-02.

Next step:
Stop for Control Room review and Workstream Reconstruction, then start WS-03 only after approval.

Deferrals:
Transaction-history UI unless later needed; distributed locks; queues; serializable isolation unless separately replanned.

## WS-03 - Money Request + Fulfillment Vertical Slice

Objective / capability:
Allow requester to create a pending request and designated payer to fulfill it through the shared money-transfer operation.

Golden-Path relationship:
Bob requests BDT 1,200 from Alice; Alice fulfills it.

Dependencies:
WS-01 completed and verified, and WS-02 shared transfer operation available.

Relevant contracts:
MoneyRequest entity, `POST /api/requests`, `GET /api/requests/incoming?status=pending`, `POST /api/requests/{request_id}/fulfill`, request state model, and fulfillment idempotency.

### Backend

- [x] Add money-request creation route/schema/service.
- [x] Add incoming pending-request route/schema/service.
- [x] Add fulfillment route/schema/service.
- [x] Enforce only designated payer may fulfill.
- [x] Preserve approved same-key fulfillment replay after request completion.
- [x] Reject different-key second settlement as `409 REQUEST_ALREADY_COMPLETED`.

### Frontend

- [x] Add request-money UI using the real endpoint.
- [x] Add incoming pending-request list.
- [x] Add fulfill/pay action.
- [x] Generate and retain idempotency key for active request and fulfillment mutations.
- [x] Refetch authoritative balance and pending requests after success.
- [x] Render loading, empty, success, and important error states.

### Persistence

- [x] Add money-request persistence mapping and constraints.
- [x] Ensure creation starts `PENDING` and moves no money.
- [x] Ensure successful fulfillment transfer and `COMPLETED` state update occur atomically.
- [x] Ensure exactly one successful transfer may be linked to a request.

### Integration

- [x] Request appears to designated payer.
- [x] Fulfillment uses the shared transfer operation.
- [x] UI reflects pending and completed states correctly after refetch/read-back.

### Infrastructure

- [x] Use isolated PostgreSQL test database for request fulfillment and replay verification.

### Verification

- [x] Request creation moves no money.
- [x] Request appears to designated payer.
- [x] Only payer may fulfill.
- [x] Successful fulfillment moves money once.
- [x] Request becomes `COMPLETED` atomically with successful transfer.
- [x] Legitimate same-key replay returns original result.
- [x] Different-key second settlement is rejected.
- [x] Refresh/read-back preserves state.
- [x] `git diff --check`.
- [x] `git status`.

Status:
COMPLETED AND VERIFIED.

Evidence:
- `backend/models/request.py` defines the WS-03 MoneyRequest persistence mapping.
- `migrations/versions/0003_money_requests.py` is present and `python -m alembic heads` reports `0003_money_requests (head)`.
- `backend/routes/requests.py`, `backend/schemas/request.py`, and `backend/services/requests.py` expose the approved WS-03 API surface.
- Application DB Alembic upgrade/current/head passed at `0003_money_requests (head)`.
- PostgreSQL schema check verified `money_requests` table: UUID id, UUID FK requester/payer, bigint amount_paisa, varchar state, UUID creation_idempotency_key, timestamptz created_at, nullable timestamptz completed_at, CHECK amount > 0, CHECK no self-request, UNIQUE (requester, creation_idempotency_key), FK constraints to accounts.
- PostgreSQL schema check verified `transfers.linked_request_id`: nullable UUID FK to money_requests, indexed.
- 15 WS-03 focused tests passed: 8 request creation tests (no money movement, appears to payer, only payer may fulfill, fulfillment moves money once, idempotency replay, incompatible key reuse, self-request rejected, unknown payer rejected), 5 fulfillment tests (replay returns 200, different key on completed returns 409, insufficient funds, unknown request, persisted read-back).
- Mandatory PostgreSQL concurrency test passed: 2 independent sessions, concurrent fulfillment of same request, exactly one succeeds, one fails REQUEST_ALREADY_COMPLETED, total money conserved.
- Full Golden Path smoke test passed: Alice register, Bob register, Alice sends BDT 2500, Bob requests BDT 1200, Alice fulfills, balances correct (96300.00 / 103700.00), same-key replay returns 200, different key on completed returns 409, persistence verified after fresh TestClient.
- Full test suite: 56 passed, 0 failed, 0 skipped (concurrency timing bug fixed with populate_existing=True).
- `git diff --check` passed (only CRLF warnings).

Blocker:
None for WS-03.

Next step:
Stop for Control Room review and Workstream Reconstruction, then start WS-04 only after approval.

Deferrals:
Request cancellation, rejection, expiry, editing, and partial payment.

## WS-04 - Golden-Path Integration + Hardening

Objective / capability:
Assemble and harden the complete Alice/Bob journey.

Golden-Path relationship:
Full approved Golden Path.

Dependencies:
WS-01, WS-02, and WS-03 completed and verified.

Relevant contracts:
All approved MVP API/data/frontend contracts.

### Backend

- [x] Routes, schemas, services, errors, and persistence behavior reconciled across the full journey.

### Frontend

- [x] Registration, account switching, balance, send, request, incoming request, fulfillment, and refetch behavior verified.
- [x] Loading, empty, success, and error states verified.

### Persistence

- [x] Persisted state after refresh/read-back verified across the complete journey.

### Integration

- [x] Complete Alice/Bob Golden Path through real frontend/API/backend/PostgreSQL.
- [x] One important invalid operation (different-key fulfillment on completed request) rejected without corrupting state.
- [x] Contract consistency verified.

### Infrastructure

- [x] Local runtime startup path documented and reliable.

### Verification

- [x] Registration (201, BDT 100,000 initial balance).
- [x] Account switching via localStorage credentials.
- [x] Direct transfer (201, exact balances).
- [x] Request creation (201, PENDING, no money moved).
- [x] Request fulfillment (201, COMPLETED, money moved).
- [x] Loading/error/success states in frontend.
- [x] Persistence after fresh TestClient/reload.
- [x] Important invalid/duplicate operation (409 REQUEST_ALREADY_COMPLETED).
- [x] Contract consistency.
- [x] `git diff --check`.
- [x] `git status`.

Status:
COMPLETED AND VERIFIED.

Evidence:
- Full Golden Path E2E verified: Alice register (100000.00) -> Bob register (100000.00) -> Alice sends 2500 (Alice=97500.00, Bob=102500.00) -> Bob requests 1200 (PENDING, no money moved) -> Alice fulfills (Alice=96300.00, Bob=103700.00, COMPLETED).
- Persistence verified after fresh TestClient.
- Different-key fulfillment on completed request returns 409.
- DB: 2 transfers (DIRECT + REQUEST_FULFILLMENT), linked correctly.
- Frontend dashboard serves all views: register, switch, balance, send, request, incoming, fulfill.
- `/api/health` returns `{"status": "ok"}`.
- `git diff --check` passed.

Blocker:
None.

Next step:
WS-05 Release + Demo Readiness.

Deferrals:
Optional polish and non-Golden-Path features.

## WS-05 - Release + Demo Readiness

Objective / capability:
Stop feature growth, verify chosen runtime, reconcile project docs, perform final review/readiness, and protect demo state.

Golden-Path relationship:
Final demo readiness.

Dependencies:
WS-04 passing.

Relevant contracts:
Selected release path, runtime instructions, final documentation, and demo evidence.

### Backend

- [x] Startup verified on local release path.
- [x] `/api/health` returns `{"status": "ok"}`.

### Frontend

- [x] User-facing application loads at `http://127.0.0.1:8000/`.
- [x] Frontend calls same-origin `/api/...` endpoints.

### Persistence

- [x] Database connectivity verified.
- [x] Migrations applied (head: `0003_money_requests`).
- [x] Persisted Golden-Path state verified.

### Integration

- [x] Local Golden-Path E2E passes.
- [x] Chosen-path (local) final E2E passes.
- [x] Demo path rehearsed.

### Infrastructure

- [x] Release decision: protected local demo.
- [x] No deployment complexity.
- [x] Source/Git state safe.

### Verification

- [x] Local Golden-Path E2E passes.
- [x] Release decision made: local demo.
- [x] Local final E2E passes.
- [x] README final reconciliation completed.
- [x] Known limitations/deferrals documented in README.
- [x] Source/Git state safe: no secrets, .env ignored, CRLF warnings only.
- [x] Demo rehearsed.
- [x] `git diff --check` passed.
- [x] `git status` clean.

Status:
COMPLETED AND VERIFIED.

Evidence:
- Local application starts at `http://127.0.0.1:8000/`.
- `/api/health` returns `{"status": "ok"}`.
- Dashboard loads with register, switch, balance, send, request, incoming, fulfill views.
- Full Golden Path verified through real PostgreSQL.
- Final suite: 56 passed, 0 failed, 0 skipped.
- Migration head: `0003_money_requests`.
- README reconciled to verified implementation.
- execute.md reconciled.
- No secrets in tracked files.
- `.env` not tracked.

Blocker:
None.

Next step:
Release freeze. No more feature development.

Deferrals:
Deployment provider selection remains deferred (local demo selected).

## Explicit Global Deferrals

- Real bank/card/payment gateway integration.
- Passwords, account recovery, token revocation, production authentication hardening, and KYC.
- Request cancel/reject/expiry/editing and partial payment.
- Transaction-history UI unless later needed.
- Notifications and real-time updates.
- Rate limiting and admin tooling.
- Advanced fraud/ML.
- Multiple currencies.
- Queues, caches, microservices, distributed locks, and containerization unless separately approved.
- Deployment provider selection until release decision.
