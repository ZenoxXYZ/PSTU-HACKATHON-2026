# Money Movement Application

PSTU National Hackathon 2026

This repository is now the challenge-specific workspace for a simulated-money Money Movement Application. The approved product is planned, but product implementation has not yet begun.

## Problem Summary

The application will let registered users send and request simulated BDT while the backend preserves financial correctness under invalid input, retries, duplicate actions, and relevant concurrent activity.

The MVP uses fake money only. It does not integrate with real banks, cards, payment gateways, deposits, withdrawals, KYC, or real financial systems.

## Approved / Planned MVP

The approved MVP includes:

- lightweight account registration;
- simulated BDT 100,000 starting balance for each newly created user;
- current balance viewing;
- sending simulated money to another valid user;
- requesting simulated money from another valid user;
- viewing and fulfilling pending requests addressed to the current payer;
- persistent authoritative balances and request state;
- backend enforcement of important money invariants.

This section describes approved/planned behavior. It is not implemented yet.

## Golden Path

The approved Golden Path is:

```text
Alice registers
-> Bob registers
-> Alice sends BDT 2,500 to Bob
-> balances update correctly
-> Bob requests BDT 1,200 from Alice
-> the request remains pending without moving money
-> Alice fulfills the request
-> money moves exactly once
-> the request becomes completed
-> refresh/read-back proves persistence
-> one invalid or duplicate operation is rejected safely
```

This E2E journey is approved and planned. It does not currently pass because the product workstreams are not implemented yet.

## Approved Architecture

The approved architecture is a modular monolith:

```text
responsive same-origin HTML/CSS/JavaScript frontend
-> FastAPI
-> Pydantic
-> services/business logic
-> SQLAlchemy
-> PostgreSQL
```

FastAPI will serve both the static user-facing application and `/api/...` endpoints. The planned health/readiness endpoint is `/api/health`.

This design keeps one application boundary for the hackathon demo, avoids unnecessary frontend-server and CORS complexity, and preserves clear backend authority for money movement and state changes.

## Important Approved Design Decisions

These are approved design decisions, not completed implementation:

- use integer paisa internally for exact authoritative money arithmetic;
- expose authoritative money values at the API boundary as fixed decimal BDT strings;
- use PostgreSQL transactions for atomic debit, credit, and transfer recording;
- use PostgreSQL row-level locking through SQLAlchemy `FOR UPDATE` for concurrent spending protection;
- lock multiple account rows in canonical account-ID order to reduce deadlock risk;
- use `Idempotency-Key` headers for retry and duplicate safety on state-changing operations;
- use lightweight opaque bearer-token identity for the simulated-money MVP;
- resolve spending authority from the authenticated backend identity, not from frontend-supplied sender or payer IDs;
- share authoritative money-transfer logic between direct transfers and request fulfillment.

## Actual Project Structure

Current repository structure:

```text
backend/          Current FastAPI starter application and empty domain layer packages
frontend/         Placeholder only; no Money Movement frontend exists yet
migrations/       Alembic migration wiring; no challenge-specific migration exists yet
tests/            Starter tests only
docs/event/       PSTU event rule interpretation
docs/guides/      Workflow and onboarding guides
docs/phases/      Phase records
docs/reviews/     Review records

problem.md        Approved WHAT for the Money Movement Application
plan.md           Approved HOW / Master System Design
execute.md        Live workstream status and evidence tracker
review.md         Current verified review summary
README.md         Project-facing repository explanation
```

Planned backend responsibilities follow the approved modular layout:

- `backend/routes/` for HTTP paths, status codes, dependencies, and domain-error translation;
- `backend/schemas/` for Pydantic request and response contracts;
- `backend/services/` for application operations and transaction orchestration;
- `backend/logic/` for exact money parsing/formatting and reusable business logic where useful;
- `backend/models/` for SQLAlchemy mappings and constraints;
- `backend/database.py` for configured engine/session behavior.

Those product responsibilities are planned. The current files do not yet implement the Money Movement domain.

## Local Setup

Use PowerShell from the repository root.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest
```

In this workspace, the verified test command was:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Result during README Pass 1: 5 starter tests passed. Running `python -m pytest` without activating the virtual environment used the system Python and failed because `pytest` was not installed there.

## Database / Environment

Current environment behavior:

- `backend/config.py` reads `DATABASE_URL` from the process environment.
- Without `DATABASE_URL`, the current starter falls back to `sqlite+pysqlite:///:memory:` so starter tests can run without a live PostgreSQL database.
- `.env.example` contains a safe placeholder PostgreSQL URL.
- No real secrets are stored in the repository.

Approved product behavior requires PostgreSQL for authoritative persistence and concurrency verification, but the application/test PostgreSQL `DATABASE_URL` values have not yet been configured or verified. WS-01 must resolve safe app/test database configuration before persistence work mutates data.

## Migrations

Alembic is present and wired to SQLAlchemy metadata. `migrations/env.py` requires `DATABASE_URL` before running migrations.

No Money Movement migration exists yet. Migrations must not be replaced with runtime `create_all()` as the normal shared/demo schema-management path.

## Running The Current Application

The current runtime is still the generic starter app. It exposes only:

```text
GET / -> {"status": "ok"}
```

After activating the virtual environment, run:

```powershell
python -m uvicorn backend.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/
```

The approved `/api/...` Money Movement endpoints and static Money Movement dashboard are planned, not currently available.

## Testing

Current tests are starter tests:

- FastAPI app imports;
- `GET /` returns `{"status":"ok"}`;
- OpenAPI schema builds;
- database URL uses a safe fallback when unset;
- database URL can come from the environment.

Run tests after activating the virtual environment:

```powershell
python -m pytest
```

Challenge-specific financial, concurrency, idempotency, API, migration, frontend, and full-stack verification will be introduced through the planned workstreams.

## Current Implementation Status

Completed documentation/planning state:

- official challenge normalization;
- `problem.md` approval/write;
- Master System Design approval;
- `plan.md` approval/write;
- `execute.md` initialization.

Not yet implemented:

- WS-01 - Authoritative Account Foundation;
- WS-02 - Direct Transfer Vertical Slice;
- WS-03 - Money Request + Fulfillment Vertical Slice;
- WS-04 - Golden-Path Integration + Hardening;
- WS-05 - Release + Demo Readiness.

Product implementation has not yet begun.

## Workstream Overview

- WS-01 - Authoritative Account Foundation
- WS-02 - Direct Transfer Vertical Slice
- WS-03 - Money Request + Fulfillment Vertical Slice
- WS-04 - Golden-Path Integration + Hardening
- WS-05 - Release + Demo Readiness

See `execute.md` for live status and verification evidence.

## Documentation Map

- `problem.md` = WHAT the product must do.
- `plan.md` = approved HOW / Master System Design.
- `execute.md` = live implementation status and evidence.
- `README.md` = project-facing explanation of the repository.
- actual code, tests, migrations, and runtime behavior = implemented truth.

## Current Non-Claims

The following are approved/planned where described, but do not currently exist in implementation:

- `Account` model;
- `Transfer` model;
- `MoneyRequest` model;
- registration API;
- bearer authentication;
- transfer API;
- request API;
- concurrency locking implementation;
- idempotency implementation;
- static Money Movement frontend;
- challenge-specific migration;
- Golden-Path E2E;
- deployment.

## Event And Source-Control Notes

PSTU rules and official organizer clarifications govern starter use, AI assistance, deployment, and freeze/submission behavior. Public deployment is welcome/useful but not mandatory unless separately announced; local demonstration remains valid when it is the safer release path.

Agents do not commit or push automatically. Human operators control Git checkpoints.
