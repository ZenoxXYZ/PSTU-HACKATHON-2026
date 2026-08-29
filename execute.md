# Execution Tracker

## Markers

- [ ] Pending
- [~] In progress
- [x] Completed and verified
- [!] Blocked by a known issue or bug
- [?] Requires clarification or an engineering/design decision

## Current Status

[ ] Product implementation NOT STARTED.

`problem.md` contains the approved Money Movement Application problem definition. `plan.md` contains the approved Master System Design and capability-oriented workstream map. No product entities, tables, migrations, APIs, business rules, frontend behavior, or product tests have been implemented yet.

## Repository Reality At Initialization

- [x] Generic starter foundation exists.
- [x] Generic starter tests exist.
- [x] Approved `problem.md` exists.
- [x] Approved `plan.md` exists.
- [ ] Product-specific implementation pending.
- [ ] Product-specific verification pending.

## Workstream Status Summary

| Workstream | Capability | Status | Golden Path | Blocker | Next |
| ---------- | ---------- | ------ | ----------- | ------- | ---- |
| WS-01 | Authoritative Account Foundation | NOT STARTED | Supports Alice/Bob setup | Safe app/test PostgreSQL configuration must be confirmed before persistence work mutates data | Begin WS-01 planning, then implement only after approval |
| WS-02 | Direct Transfer Vertical Slice | NOT STARTED | Alice sends BDT 2,500 to Bob | Depends on WS-01 | Start after account foundation is verified |
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

- [ ] Add account registration use case.
- [ ] Add bearer-token generation, storage hash/secure representation, and authentication dependency.
- [ ] Add current-user resolution.
- [ ] Add user discovery/search behavior.

### Frontend

- [ ] N/A until the account contracts are stable enough for the approved same-origin dashboard scope.

### Persistence

- [ ] Add account persistence mapping and constraints.
- [ ] Add explicit Alembic migration.
- [ ] Ensure registration provisions BDT 100,000 exactly once.

### Integration

- [ ] Registration endpoint returns token, user summary, and balance.
- [ ] Current-user endpoint returns authenticated user and authoritative balance.
- [ ] User search endpoint returns selectable public user summaries.

### Infrastructure

- [ ] Confirm safe app/test PostgreSQL URLs before running migrations or database tests.

### Verification

- [ ] Safe app/test DB configuration verified.
- [ ] Migration applies.
- [ ] Registration provisions BDT 100,000 exactly once.
- [ ] Duplicate handles rejected.
- [ ] Bearer token resolves current actor.
- [ ] Current balance returned correctly.
- [ ] User lookup works.
- [ ] `git diff --check`.
- [ ] `git status`.

Status:
NOT STARTED.

Evidence:
No product implementation or verification yet.

Blocker:
Safe app/test PostgreSQL configuration must be confirmed before persistence work mutates data.

Next step:
Begin WS-01 planning and approval.

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

- [ ] Add direct transfer route/schema/service.
- [ ] Enforce authenticated sender authority from bearer token.
- [ ] Validate recipient, amount, self-transfer, sufficient funds, and idempotency behavior.
- [ ] Translate domain errors to stable API errors.

### Frontend

- [ ] Add send-money UI using the real endpoint.
- [ ] Generate and retain idempotency key for active mutation/retry.
- [ ] Refetch authoritative balance after success.
- [ ] Render loading, success, and important error states.

### Persistence

- [ ] Add transfer persistence mapping and constraints.
- [ ] Persist immutable successful transfers.
- [ ] Use PostgreSQL row-level `FOR UPDATE` locking through SQLAlchemy.
- [ ] Lock multiple account rows in canonical ascending account-ID order.

### Integration

- [ ] Real send form calls real API.
- [ ] Backend persists one atomic debit/credit/transfer.
- [ ] Frontend displays refreshed authoritative balances.

### Infrastructure

- [ ] Use isolated PostgreSQL test database for concurrency verification.

### Verification

- [ ] Exact money math.
- [ ] Atomic debit/credit.
- [ ] Insufficient funds changes nothing.
- [ ] Same idempotency key does not double-transfer.
- [ ] Incompatible key reuse rejected.
- [ ] Concurrent BDT 800 + BDT 800 attempts against BDT 1,000 allow at most one success.
- [ ] Real send form calls real endpoint.
- [ ] Balance refetch/display is correct.
- [ ] `git diff --check`.
- [ ] `git status`.

Status:
NOT STARTED.

Evidence:
No direct-transfer implementation or verification yet.

Blocker:
Depends on WS-01.

Next step:
Start after account foundation is verified.

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
