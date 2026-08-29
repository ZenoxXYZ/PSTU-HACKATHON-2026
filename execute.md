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

`problem.md` contains the approved Money Movement Application problem definition. `plan.md` contains the approved Master System Design and capability-oriented workstream map. WS-01 account foundation code, migration, routes, services, and tests have been added and verified. WS-02 direct transfer vertical slice including Transfer model, migration, service with atomic transaction/row locking/idempotency, API route, money parsing, comprehensive tests, concurrency test, frontend send flow, and Golden Path smoke test have been verified against PostgreSQL. WS-03 through WS-05 remain not started.

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
| WS-01 | Authoritative Account Foundation | COMPLETED AND VERIFIED | Supports Alice/Bob setup | None | Control Room review and Workstream Reconstruction before WS-02 |
| WS-02 | Direct Transfer Vertical Slice | COMPLETED AND VERIFIED | Alice sends BDT 2,500 to Bob | None | Control Room review before WS-03 |
| WS-03 | Money Request + Fulfillment Vertical Slice | NOT STARTED | Bob requests BDT 1,200 from Alice; Alice fulfills | Depends on WS-01 and WS-02 shared transfer operation | Start after direct transfer slice is verified |
| WS-04 | Golden-Path Integration + Hardening | NOT STARTED | Full approved Alice/Bob journey | Depends on WS-01, WS-02, and WS-03 | Start after request/fulfillment slice is verified |
| WS-05 | Release + Demo Readiness | NOT STARTED | Final demo readiness | Depends on WS-04 | Start after Golden Path is passing locally |

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

- [ ] Add money-request creation route/schema/service.
- [ ] Add incoming pending-request route/schema/service.
- [ ] Add fulfillment route/schema/service.
- [ ] Enforce only designated payer may fulfill.
- [ ] Preserve approved same-key fulfillment replay after request completion.
- [ ] Reject different-key second settlement as `409 REQUEST_ALREADY_COMPLETED`.

### Frontend

- [ ] Add request-money UI using the real endpoint.
- [ ] Add incoming pending-request list.
- [ ] Add fulfill/pay action.
- [ ] Generate and retain idempotency key for active request and fulfillment mutations.
- [ ] Refetch authoritative balance and pending requests after success.
- [ ] Render loading, empty, success, and important error states.

### Persistence

- [ ] Add money-request persistence mapping and constraints.
- [ ] Ensure creation starts `PENDING` and moves no money.
- [ ] Ensure successful fulfillment transfer and `COMPLETED` state update occur atomically.
- [ ] Ensure exactly one successful transfer may be linked to a request.

### Integration

- [ ] Request appears to designated payer.
- [ ] Fulfillment uses the shared transfer operation.
- [ ] UI reflects pending and completed states correctly after refetch/read-back.

### Infrastructure

- [ ] Use isolated PostgreSQL test database for request fulfillment and replay verification.

### Verification

- [ ] Request creation moves no money.
- [ ] Request appears to designated payer.
- [ ] Only payer may fulfill.
- [ ] Successful fulfillment moves money once.
- [ ] Request becomes `COMPLETED` atomically with successful transfer.
- [ ] Legitimate same-key replay returns original result.
- [ ] Different-key second settlement is rejected.
- [ ] Refresh/read-back preserves state.
- [ ] `git diff --check`.
- [ ] `git status`.

Status:
NOT STARTED.

Evidence:
No request or fulfillment implementation or verification yet.

Blocker:
Depends on WS-01 and WS-02.

Next step:
Start after direct transfer slice is verified.

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

- [ ] Reconcile routes, schemas, services, errors, and persistence behavior across the full journey.

### Frontend

- [ ] Reconcile registration, account switching, balance, send, request, incoming request, fulfillment, and refetch behavior.
- [ ] Verify loading, empty, success, and error states used by the Golden Path.

### Persistence

- [ ] Verify persisted state after refresh/read-back across the complete journey.

### Integration

- [ ] Complete Alice/Bob Golden Path through real frontend/API/backend/PostgreSQL.
- [ ] Verify one important invalid or duplicate operation is rejected without corrupting state.
- [ ] Check contract consistency and stale frontend state risks.

### Infrastructure

- [ ] Confirm local runtime startup path is documented and reliable enough for demo.

### Verification

- [ ] Registration.
- [ ] Account switching via credentials.
- [ ] Direct transfer.
- [ ] Request creation.
- [ ] Request fulfillment.
- [ ] Loading/error/success states.
- [ ] Persistence after refresh.
- [ ] Important invalid/duplicate operation.
- [ ] Contract consistency.
- [ ] No stale frontend state.
- [ ] `git diff --check`.
- [ ] `git status`.

Status:
NOT STARTED.

Evidence:
No Golden-Path implementation or verification yet.

Blocker:
Depends on WS-01, WS-02, and WS-03.

Next step:
Start after request/fulfillment slice is verified.

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

- [ ] Verify startup on the selected release path.
- [ ] Verify `/api/health`.

### Frontend

- [ ] Verify the user-facing application loads on the selected release path.
- [ ] Verify frontend calls the correct backend base URL/origin.

### Persistence

- [ ] Verify database connectivity, migrations, and persisted Golden-Path state on the selected release path.

### Integration

- [ ] Local Golden-Path E2E passes before release decision.
- [ ] Chosen-path final E2E passes.
- [ ] Demo path rehearsed.

### Infrastructure

- [ ] Make release decision: protected local demo by default, deployment only if justified and feasible.
- [ ] Confirm no deployment complexity has displaced Golden-Path verification.
- [ ] Confirm source/Git state is safe.

### Verification

- [ ] Local Golden-Path E2E passes.
- [ ] Release decision made.
- [ ] Chosen-path final E2E passes.
- [ ] README final reconciliation occurs after implementation is stable.
- [ ] Known limitations/deferrals documented.
- [ ] Source/Git state safe.
- [ ] Demo rehearsed.
- [ ] `git diff --check`.
- [ ] `git status`.

Status:
NOT STARTED.

Evidence:
No release/demo readiness verification yet.

Blocker:
Depends on WS-04.

Next step:
Start after Golden Path is passing locally.

Deferrals:
Deployment provider selection remains deferred until release decision.

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
