# Engineering Plan

## Status

[x] Approved Money Movement Application Master System Design.

This file records the approved HOW for implementing the approved WHAT in `problem.md`. Design choices remain distinct from problem requirements.

## Repository Baseline Reconstruction

- [PROBLEM REQUIREMENT] `problem.md` is the approved Money Movement Application problem definition.
- [IMPLEMENTATION] The repository is currently a generic FastAPI, SQLAlchemy, Alembic, PostgreSQL-capable starter.
- [IMPLEMENTATION] `backend/main.py` exposes only the generic starter health behavior at `/`.
- [IMPLEMENTATION] No product domain models, migrations, services, routes, schemas, business rules, or frontend application have been implemented yet.
- [IMPLEMENTATION] `frontend/README.md` is a placeholder and no frontend framework is selected.
- [IMPLEMENTATION] Existing tests verify only starter import, starter health behavior, OpenAPI generation, and environment-based database URL selection.
- [IMPLEMENTATION] Alembic is wired, but no challenge-specific migration exists yet.
- [IMPLEMENTATION] The starter currently has a SQLite in-memory fallback for generic tests; the approved product design requires PostgreSQL for authoritative money movement and concurrency verification.
- [IMPLEMENTATION] `review.md` still reflects the generic starter foundation because no product implementation has been verified.

## Problem / MVP Summary

Build a simulated-money Money Movement Application MVP where users can register, receive an initial simulated BDT 100,000 balance, view their balance, send money to another valid user, request money from another valid user, and fulfill valid pending requests.

The backend is authoritative for identity, validation, balances, request state, atomic money movement, sufficient funds, idempotency, and concurrency integrity.

The product uses fake/simulated BDT only. Real banks, cards, payment gateways, payment processors, KYC, deposits, withdrawals, and real financial integrations are outside the MVP.

## Golden Path

1. Alice registers and receives simulated BDT 100,000.
2. Bob registers and receives simulated BDT 100,000.
3. Alice sends BDT 2,500 to Bob.
4. The transfer succeeds exactly once and balances become correct.
5. Bob requests BDT 1,200 from Alice.
6. The request becomes pending without moving money.
7. Alice sees and fulfills the request.
8. BDT 1,200 moves exactly once from Alice to Bob.
9. The request becomes completed.
10. Refresh/read-back proves the resulting state persists.
11. One important invalid or duplicate operation is rejected without corrupting financial state.

## Architecture

[DESIGN DECISION] Use a modular monolith:

```text
browser responsive HTML/CSS/JavaScript application
-> same-origin HTTP/JSON
-> FastAPI
-> Pydantic
-> services/business logic
-> SQLAlchemy
-> PostgreSQL
```

FastAPI serves both the static user-facing application and `/api/...` endpoints.

Use `/api/health` for health/readiness. The user-facing dashboard is served at `/`.

[DESIGN DECISION] Do not add React, Vite, or another frontend build tool unless separately replanned.

Reasons:

- Existing starter has no frontend framework selected.
- Same-origin UI avoids unnecessary frontend-server and CORS complexity.
- One deployable application is appropriate for the remaining hackathon time.
- Business authority remains backend-side.

## Identity / Authority

[DESIGN DECISION] Use lightweight opaque bearer-token identity for the simulated-money MVP.

Registration:

- creates an account;
- provisions the approved simulated BDT 100,000 starting balance;
- generates an opaque bearer token;
- returns the raw bearer token to the browser;
- stores only a secure representation or hash of the token in the database.

Authenticated requests:

- browser sends the bearer token;
- backend resolves the authenticated account;
- authenticated account determines the actor, sender, payer, or requester.

[DESIGN DECISION] The frontend must not determine spending authority by merely sending a payer or sender ID.

[MVP DECISION] No password login, account recovery, token revocation, or production-grade multi-device account security is required.

## Major Entities / Relationships

### Account

Purpose: authenticated application user and owner of a simulated balance.

Conceptual fields:

- internal ID;
- unique normalized handle;
- display name;
- balance in integer minor units/paisa;
- bearer-token hash or secure representation;
- created timestamp.

Important invariants:

- handle is unique;
- balance cannot become negative;
- raw bearer token is not persisted;
- account creation provisions BDT 100,000 once.

### Transfer

Purpose: immutable record of successful simulated money movement.

Conceptual fields:

- ID;
- sender account;
- recipient account;
- amount in paisa;
- idempotency key;
- movement kind: `DIRECT` or `REQUEST_FULFILLMENT`;
- optional linked money-request ID;
- created timestamp.

Important constraints:

- amount is positive;
- sender and recipient are different accounts;
- idempotency uniqueness is scoped to the authenticated sending account;
- request-linked successful transfer is unique per request.

### MoneyRequest

Purpose: persisted request from requester to designated payer.

Conceptual fields:

- ID;
- requester;
- payer;
- amount in paisa;
- state;
- request-creation idempotency key;
- created timestamp;
- completion timestamp.

Important constraints:

- amount is positive;
- requester and payer are different accounts;
- request creation idempotency uniqueness is scoped to requester;
- initial state is `PENDING`;
- at most one successful fulfillment transfer can exist.

[DESIGN DECISION] Do not add unnecessary challenge entities.

## Money Representation

[DESIGN DECISION] Use exact integer minor units internally.

- Python/service representation: integer paisa.
- PostgreSQL representation: `BIGINT`-compatible integer minor units.
- API representation: fixed decimal BDT strings such as `"2500.00"`.

Reject:

- zero amounts;
- negative amounts;
- malformed monetary strings;
- more than two fractional digits.

[DESIGN DECISION] Do not use float for authoritative money arithmetic.

## Important Invariants

- [PROBLEM REQUIREMENT] All money is simulated/fake BDT only.
- [MVP DECISION] New users receive simulated BDT 100,000 for MVP/demo use.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] Money movement must preserve total simulated value except for the approved initial balance grant.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] Accepted money movement must atomically debit one account, credit the other account, and record the transfer.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] A user's balance must never become negative.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] Request creation moves no money.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] Request fulfillment moves money at most once.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] Rejected invalid, duplicate, or retried operations must not partially change balances or request state.

## Transfer Transaction Design

[DESIGN DECISION] A direct transfer is one database transaction.

Logical flow:

1. Authenticate sender from bearer token.
2. Validate recipient.
3. Validate amount.
4. Reject self-transfer.
5. Inspect idempotency state.
6. Lock relevant account rows using PostgreSQL row-level `FOR UPDATE` semantics.
7. Acquire multiple account locks in canonical ascending account-ID order.
8. Re-check current authoritative state after locks.
9. Re-check idempotency state as needed.
10. Reject insufficient funds without changing balances.
11. Debit sender.
12. Credit recipient.
13. Insert immutable `Transfer` record.
14. Commit all changes together.
15. Roll back on failure.

Invariant: debit, credit, and successful transfer record are one atomic logical operation.

## Concurrency / Integrity

[DESIGN DECISION] Use PostgreSQL row-level locking through SQLAlchemy `FOR UPDATE` support.

For two concurrent spends from the same account:

- first transaction locks the sender account;
- second transaction waits;
- first transaction commits;
- second transaction observes the new committed balance;
- second transaction re-runs sufficient-funds validation;
- overspend cannot occur.

When locking more than one account, lock in canonical ascending internal-ID order to reduce deadlock risk.

[DESIGN DECISION] Do not introduce distributed locking, Redis, queues, or serializable isolation without a separately approved replan.

## Idempotency / Retry Safety

[DESIGN DECISION] Every money-moving or state-creating POST that requires retry safety uses a client-generated UUID in the `Idempotency-Key` header.

Direct transfers:

- persist idempotency key on `Transfer`;
- scope uniqueness to authenticated sender;
- same actor plus same key plus same payload returns the original successful operation without moving money again;
- same key plus incompatible payload returns `409 IDEMPOTENCY_KEY_REUSED`.

Money-request creation:

- persist request idempotency key on `MoneyRequest`;
- scope uniqueness to requester;
- identical replay returns the original request;
- incompatible reuse returns `409`.

Request fulfillment approved clarification:

- same authenticated payer plus same request plus same fulfillment `Idempotency-Key` plus same logical operation/payload returns the original successful fulfillment result without a second transfer, even though the `MoneyRequest` is already `COMPLETED`;
- a replay with the same successful key must not be rejected merely because the request is now `COMPLETED`;
- an already `COMPLETED` request with a different fulfillment idempotency key returns `409 REQUEST_ALREADY_COMPLETED`;
- same idempotency key reused for an incompatible operation or payload returns `409 IDEMPOTENCY_KEY_REUSED`;
- the final service ordering and lookup strategy must preserve these semantics.

## Money Request State Model

Use only:

```text
PENDING -> COMPLETED
```

Creation:

- always starts `PENDING`;
- moves no money.

Fulfillment:

- only the designated payer may fulfill;
- request must be valid for fulfillment unless the call is a legitimate idempotent replay;
- financial movement uses the same authoritative transfer operation as direct transfer;
- successful transfer and request completion occur in the same overall transaction;
- exactly one successful transfer may be linked to the request.

Deferred:

- cancellation;
- rejection;
- expiry;
- editing;
- partial payment.

## API / Data Contracts

All authoritative money fields use decimal BDT strings at the HTTP boundary.

Important application errors should use a stable shape:

```json
{
  "code": "...",
  "message": "..."
}
```

Pydantic/schema validation failures may use normal FastAPI `422` responses.

| Method | Path | Request shape | Response shape | Status/error behavior | Consuming frontend view/component |
| ------ | ---- | ------------- | -------------- | --------------------- | --------------------------------- |
| `GET` | `/api/health` | Public | Readiness status | `200` when app is reachable | Runtime readiness check |
| `POST` | `/api/auth/register` | `handle`, `display_name` | `access_token`, user summary, balance | `201`; duplicate handle; malformed fields | Registration form |
| `GET` | `/api/auth/me` | Bearer authenticated | Current user and current balance | `200`; invalid/missing auth | Authenticated dashboard restore/refresh |
| `GET` | `/api/users?query=...` | Bearer authenticated, query text | Matching public user summaries; exclude current actor where useful | `200`; invalid/missing auth; invalid query | Recipient/payer search |
| `POST` | `/api/transfers` | Bearer authenticated; `Idempotency-Key`; `recipient_handle`, `amount` | Transfer details and resulting sender balance where useful | `201` new transfer; `200` legitimate replay; auth, unknown recipient, insufficient funds, self-transfer, invalid amount, idempotency-key reuse conflict | Send-money form |
| `POST` | `/api/requests` | Bearer authenticated; `Idempotency-Key`; `payer_handle`, `amount` | Pending request details | `201` new request; `200` legitimate replay; unknown payer, invalid/self request, key-reuse conflict | Request-money form |
| `GET` | `/api/requests/incoming?status=pending` | Bearer authenticated | Pending requests addressed to current actor | `200`; invalid/missing auth | Incoming request list |
| `POST` | `/api/requests/{request_id}/fulfill` | Bearer authenticated; `Idempotency-Key` | Completed request, linked transfer, resulting payer balance where useful | `201` first fulfillment; `200` legitimate same-operation replay; unauthorized/non-payer, unknown request, completed request with different key, insufficient funds, incompatible key reuse | Fulfill/pay action |

[DESIGN DECISION] Do not add generic CRUD endpoints unless required by the approved Golden Path.

## Frontend / User-Facing Structure

[DESIGN DECISION] Use one responsive same-origin dashboard at `/`.

Unauthenticated state:

- registration form;
- locally saved demo-account/credential selector for switching between Alice and Bob.

The selector is UI convenience only. The bearer token is the backend identity authority.

Authenticated state:

- current account identity;
- current authoritative balance;
- user search/select capability;
- send-money form;
- request-money form;
- incoming pending-request list;
- fulfill/pay action;
- loading states;
- empty states;
- success states;
- important error states.

Frontend local state:

- selected locally stored bearer credential;
- current form input;
- search text;
- loading/error/success flags;
- idempotency key for each active mutation/retry.

Server state:

- authenticated account;
- authoritative balance;
- searchable users;
- pending requests.

After successful mutations, refetch authoritative server state where practical.

[DESIGN DECISION] Do not calculate authoritative balances in frontend code and do not duplicate important financial invariants in JavaScript.

## Backend Responsibility Map

Map onto the repository's actual starter conventions.

`backend/main.py`:

- application composition;
- static UI serving;
- API router registration;
- health endpoint.

`backend/routes/`:

- HTTP methods and paths;
- auth dependency;
- headers;
- status codes;
- domain-error translation.

`backend/schemas/`:

- request/response contracts;
- monetary string validation/serialization;
- account, transfer, and request API shapes.

`backend/services/`:

- account registration;
- current-user resolution/use cases;
- user search;
- direct transfer orchestration;
- request creation;
- request fulfillment;
- transaction coordination.

`backend/logic/`:

- exact money parsing/formatting;
- reusable shared money-transfer operation if consistent with starter architecture.

`backend/models/`:

- `Account`;
- `Transfer`;
- `MoneyRequest`;
- relationships and constraints.

`backend/database.py`:

- configured PostgreSQL engine/session;
- safe test session override or pattern.

`migrations/`:

- explicit Alembic schema migration(s).

[DESIGN DECISION] Migrations must not be replaced with runtime `create_all()` as the normal shared/demo schema-management path.

## Business / Decision Logic

Business authority lives in backend services and logic, not routes or frontend code.

Core policies:

- normalize handles before uniqueness and lookup checks;
- provision exactly BDT 100,000 once at registration;
- parse and format money through exact integer-paisa helpers;
- reject invalid users, self-transfer/self-request, invalid amounts, insufficient funds, unauthorized fulfillment, incompatible idempotency-key reuse, and invalid request state transitions;
- preserve idempotent replay behavior for completed request fulfillment when the replay is the same payer, request, key, and logical operation.

## Workstream Map

| ID / name | Capability / objective | Golden-Path relevance | Involved layers | Dependencies | Major contracts | Verification expectation | Exit criteria |
| --------- | ---------------------- | --------------------- | --------------- | ------------ | --------------- | ------------------------ | ------------- |
| WS-01 - Authoritative Account Foundation | Establish PostgreSQL persistence, accounts, lightweight token identity, registration, current balance, and user discovery. | Supports Alice/Bob setup. | Backend + Persistence; frontend may begin only where relevant contracts become stable. | Approved `problem.md`, approved `plan.md`, safe app/test DB configuration. | Account entity, registration, current-user, user-search contracts. | Migration applies; registration provisions BDT 100,000 exactly once; duplicate handles rejected; bearer token resolves current actor; current balance and user lookup work. | Account foundation implemented, tested, migrated, and ready for transfer work. |
| WS-02 - Direct Transfer Vertical Slice | Deliver exact, atomic, idempotent, concurrency-safe direct money transfer through the real frontend/API/backend/database path. | Alice sends BDT 2,500 to Bob. | Backend + Persistence + Frontend + Integration. | WS-01. | Transfer entity, `POST /api/transfers`, money representation, idempotency key behavior. | Exact math; atomic debit/credit; insufficient funds changes nothing; same key does not double-transfer; incompatible reuse rejected; concurrent BDT 800 + BDT 800 against BDT 1,000 allows at most one success; real send form calls real endpoint. | Direct transfer slice works through UI/API/db with focused verification. |
| WS-03 - Money Request + Fulfillment Vertical Slice | Allow requester to create a pending request and designated payer to fulfill it through the shared money-transfer operation. | Bob requests BDT 1,200 from Alice; Alice fulfills it. | Backend + Persistence + Frontend + Integration. | WS-01, WS-02 shared transfer operation. | MoneyRequest entity, request creation, incoming requests, fulfillment, fulfillment idempotency. | Request creation moves no money; request appears to payer; only payer may fulfill; successful fulfillment moves once; request becomes `COMPLETED` atomically; same-key replay returns original result; different-key second settlement rejected; refresh/read-back preserves state. | Request and fulfillment slice works through UI/API/db with focused verification. |
| WS-04 - Golden-Path Integration + Hardening | Assemble and harden the complete Alice/Bob journey. | Full end-to-end Golden Path. | Frontend + Backend + Persistence + Integration. | WS-01, WS-02, WS-03. | All approved MVP contracts. | Registration; account switching via credentials; direct transfer; request creation; request fulfillment; loading/error/success states; persistence after refresh; important invalid/duplicate operation; contract consistency; no stale frontend state. | Complete Golden Path passes and demo-critical failure case is safe. |
| WS-05 - Release + Demo Readiness | Stop feature growth, verify chosen runtime, reconcile project docs, perform final review/readiness, and protect demo state. | Final demo readiness. | Integration + Infrastructure/Runtime + Documentation as relevant. | WS-04 passing. | Runtime/release documentation and selected release path. | Local Golden-Path E2E passes; release decision made; chosen-path final E2E passes; README final reconciliation occurs after implementation is stable; known limitations/deferrals documented; source/Git state safe; demo rehearsed. | Repository is ready for final review, reconstruction, and demo freeze. |

## Integration Strategy

Use progressively stronger integration stages:

1. Level 1 - Contract integration: frontend expectations and backend design agree.
2. Level 2 - Feature / slice integration: a real frontend capability communicates with the real corresponding backend capability.
3. Level 3 - Systematic full-stack integration: the assembled Golden Path is checked and hardened across boundaries.
4. Level 4 - E2E verification: a real user journey proves the system works through required layers and produces the intended outcome.

Backend-first means establishing authoritative domain foundations, persistence, major invariants, critical backend capabilities, and sufficiently stable API/data contracts. Frontend work may begin once a relevant contract/capability is stable enough for its approved scope.

## Verification Strategy

Plan proportional verification.

Unit:

- money string parsing;
- paisa conversion;
- formatting;
- monetary validation.

Service/database:

- registration seed balance;
- transfer math;
- rollback behavior;
- insufficient funds;
- request transitions;
- idempotency match/mismatch behavior.

Concurrency:

Use two independent PostgreSQL sessions/transactions:

```text
Alice = BDT 1,000
Transfer A = BDT 800
Transfer B = BDT 800
```

Expected:

- exactly one succeeds;
- the other fails insufficient funds;
- Alice final balance is BDT 200.

Never run destructive concurrency tests against an important external or production DB.

API:

- auth;
- malformed input;
- unknown users;
- self payment/request;
- insufficient funds;
- unauthorized request fulfillment;
- idempotent replay;
- completed request.

Integration:

- real frontend request to real backend;
- response consumed by UI;
- refetch/read-back.

Final local E2E:

1. Alice registers -> BDT 100,000.
2. Bob registers -> BDT 100,000.
3. Alice sends BDT 2,500 to Bob.
4. Correct balances shown.
5. Bob requests BDT 1,200 from Alice.
6. No money moves yet.
7. Alice sees pending request.
8. Alice fulfills it.
9. Correct final balances/request state.
10. Refresh/reload proves persistence.
11. Important duplicate/invalid operation is rejected without state corruption.

## E2E Strategy

Separate focused slice verification from systematic integration and Golden-Path E2E.

Golden-Path E2E should verify:

```text
user action
-> frontend
-> API
-> backend
-> persistence
-> response
-> visible result
-> refresh/reload
-> persisted result remains correct
```

Manual E2E is acceptable under time constraints if the real browser, backend, and PostgreSQL database are used and the observed state is recorded.

## Release / Deployment Decision Criteria

[DESIGN DECISION] Default recommendation: protected local demo.

Deployment remains conditional.

Choose deployment later only if:

- official organizers require it;
- or it materially improves judging/demo;
- hosting/database/accounts are already prepared;
- sufficient time remains;
- local Golden-Path E2E is already passing;
- deployed E2E can still be completed.

Do not let deployment displace Golden-Path verification.

## Assumptions

- The approved challenge uses simulated BDT balances only.
- Human/operator will configure safe local PostgreSQL application and test database URLs before persistence implementation.
- Opaque bearer tokens are acceptable only for the simulated-money MVP and local/demo security posture.
- No deployment provider is selected yet.

## Explicit Deferrals

- real bank/card/payment gateway;
- passwords/recovery;
- token revocation;
- production authentication hardening;
- KYC;
- request cancel/reject/expiry;
- partial payment;
- transaction-history UI unless later needed;
- notifications;
- real-time updates;
- rate limiting;
- admin tooling;
- advanced fraud/ML;
- multiple currencies;
- queues;
- caches;
- microservices;
- distributed locks;
- containerization unless required;
- deployment provider selection until release decision.
