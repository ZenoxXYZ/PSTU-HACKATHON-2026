# Generic Hackathon Starter

A reusable, backend-first, full-stack-capable foundation for building small, demonstrable projects with AI coding agents, when official rules permit that workflow, while keeping requirements, design decisions, implementation evidence, and review history clear.

Bring official event rules, organizer clarifications, and an authoritative problem statement. This template supplies repeatable engineering infrastructure; it does not decide the product or override competition policy.

> This is a starting point, not a solution generator.

## What It Is

This repository is a problem-agnostic engineering foundation for hackathons, take-home challenges, rapid prototypes, and other time-constrained exercises. It keeps durable project state in the repository so people and fresh AI sessions can reconstruct what is required, what was designed, what was implemented, and what was verified. Reusable starter infrastructure, AI assistance, challenge-specific implementation boundaries, deployment, and submission behavior must follow the relevant official rules.

## Why It Exists

Fast projects often lose context between people, chats, and implementation checkpoints. That can produce invented requirements, unverified code, unnecessary infrastructure, and mismatched frontend and backend behavior.

This template provides a repeatable engineering workflow: understand the problem, identify the MVP Golden Path, approve a small design with important contracts, implement bounded capability-oriented workstreams, verify them with evidence, review meaningful checkpoints independently, reconstruct enough understanding for humans to supervise and explain the system, deploy when a remote demo is needed, and stabilize the demo-critical path.

## Why Start From a Backend Template?

The starter separates two concerns that should not be conflated.

**Repeatable engineering infrastructure** is setup that is useful across many projects: Python application structure, FastAPI startup, environment configuration, SQLAlchemy foundations, Alembic migration wiring, automated-test foundations, a health endpoint, backend-layer organization, a frontend workspace placeholder, and AI engineering workflows.

**Problem-specific product design** must be derived from the actual brief: domain entities, database schema, business rules, APIs, decision algorithms, product validation, frontend framework, and deployment architecture.

Without a reusable foundation, limited project time is repeatedly spent recreating framework structure, configuration, database wiring, migration setup, and test scaffolding before product work can begin. With this starter, work can move earlier into:

```text
requirements -> design -> domain modeling -> implementation -> integration -> verification
```

This is a deliberate starting point, not a claim that the supplied architecture is optimal for every project.

## Why FastAPI?

**[TEMPLATE DESIGN DECISION]** FastAPI is the default backend framework because Python supports rapid prototyping; FastAPI has relatively low ceremony; Pydantic provides typed request and response contracts; it generates OpenAPI schemas and interactive API documentation; and it works directly with SQLAlchemy, Alembic, Uvicorn, and common Python testing tools. It is also practical when data-processing, optimization, or AI-related logic is written in Python.

FastAPI is **not** a [PROBLEM REQUIREMENT]. A future problem statement may justify another architecture or technology. The template chooses a consistent default for speed and clarity, not universal superiority.

## Engineering Model

The repository uses four state files with distinct purposes:

| File | Engineering role |
| ---- | ---------------- |
| `problem.md` | Normalized requirements model: the approved interpretation of the authoritative brief. |
| `plan.md` | Approved solution architecture and design decisions. |
| `execute.md` | Execution and checkpoint tracker. |
| `review.md` | Concise verified engineering and bug history. |

Requirements and design authority flow from:

```text
official event rules / official clarifications
-> official challenge / problem statement
-> approved problem.md
-> approved plan.md
```

Implemented-state truth comes from:

```text
code + tests + migrations + Git evidence + safe runtime verification
```

State files summarize the repository; they do not override contradictory implementation evidence. See [Workflow concepts](docs/guides/WORKFLOW.md) for the detailed model.

## Builder and Reviewer Roles

| Builder | Reviewer |
| ------- | -------- |
| Plans and implements an approved workstream. | Independently reconstructs a checkpoint and audits its evidence. |
| Fixes implementation-time bugs and runs verification. | Searches for defects, regressions, contradictions, missing verification, and requirement drift. |
| Records verified implementation evidence. | Starts read-only and classifies findings before any human-approved correction. |

Separating these roles reduces the risk that an implementation agent merely confirms its own assumptions. Independent review improves scrutiny; it does not guarantee correctness. Humans approve material transitions, design changes, and Git history changes.

## Golden Path and Workstreams

Golden Path means the most important successful user journey that demonstrates the core value of the MVP. It is identified before implementation during problem intake and Master System Design, then used to drive MVP scope, workstream priority, architecture decisions, data/API contracts, frontend views, integration order, E2E verification, and demo preparation.

An engineering workstream is a bounded engineering objective that creates or strengthens meaningful system behavior. A workstream may be backend-only, backend-heavy, frontend-only, frontend-heavy, a full-stack vertical slice, business/decision-logic oriented, integration/hardening oriented, specialized verification, or release/deployment oriented, depending entirely on the approved problem and plan.

Backend-first does not mean backend-complete-first. It means establishing authoritative domain foundations, persistence, major invariants, critical backend capabilities, and sufficiently stable API/data contracts. Frontend work may begin once a relevant contract/capability is stable enough for its approved scope. Bounded workstreams reduce context size and make implementation, debugging, documentation, review, and rollback easier to reason about.

```text
Plan -> Human Approval -> Implement -> Debug -> Verify -> Document -> Review -> Understand
```

## Complete Workflow

```text
Official Event / Challenge Intake
        |
        v
Problem Normalization
        |
        v
MVP + Golden Path -> Master System Design
        |
        v
Architecture + data model + API/data contracts
        |
        v
plan.md workstream map -> execute.md tracker
        |
        v
Backend/persistence foundation -> relevant contracts stabilize
        |
        v
Frontend begins where relevant -> capability workstreams
        |
        v
Incremental vertical integration -> Golden Path complete
        |
        v
Systematic full-stack integration / hardening
        |
        v
Local Golden-Path E2E -> Feature Freeze -> release decision
        |
        v
Local final E2E or deployment + deployed E2E
        |
        v
P0/P1 fixes -> final review -> whole-project understanding
        |
        v
internal Demo Freeze -> official event freeze/submission
```

## Repository Structure

```text
backend/          FastAPI application foundation
frontend/         Placeholder for a future, problem-driven interface
migrations/       Alembic database-schema migration foundation
tests/            Automated verification
docs/guides/      Usage guides and reusable AI prompts
docs/phases/      Builder workstream records
docs/reviews/     Independent review records (created when reviews run)

problem.md        Approved problem interpretation
plan.md           Approved design and roadmap
execute.md        Current engineering checkpoint
review.md         Verified review and bug summary
```

## Technology Foundation

The generic defaults are Python, FastAPI, Pydantic, SQLAlchemy, PostgreSQL-ready configuration, Alembic, Uvicorn, and isolated automated tests. These are template design defaults, not requirements for every future problem.

The current app intentionally exposes only `GET /`, which returns `{"status":"ok"}`. It does not create tables, run migrations at startup, or require a real database connection for the health response.

## Full-Stack Positioning

This is currently a **backend-first, full-stack-capable** starter. Frontend technology is intentionally unspecified because UI choices depend more strongly on real interaction requirements and available constraints than the generic backend foundation does.

When a frontend is in scope, the contract boundary is:

```text
Frontend -> HTTP request -> FastAPI route -> Pydantic validation
-> service / business logic -> SQLAlchemy / persistence
-> response schema -> frontend state and rendering
```

Integration should grow in stages: contract agreement, feature/slice integration, systematic full-stack hardening, and Golden-Path E2E verification. Later full-stack integration is a hardening/reconciliation pass, not the first time frontend and backend meet. Public deployment is not universally mandatory; use the release path that official rules, demo needs, reliability, and remaining time justify. The frontend should use approved backend contracts rather than duplicate backend business or decision logic. See the [full-stack guide](docs/guides/FULL_STACK_GUIDE.md).

## Quick Start

1. Use the repository as a GitHub template, or clone/copy it deliberately.
2. Create and activate a virtual environment.
3. Install dependencies and verify the starter.
4. Provide official event rules, organizer clarifications, and the authoritative problem statement when available.
5. Run Problem Statement Intake, then Problem Definition; review and approve `problem.md`.
6. Run Master System Design; identify the Golden Path, important contracts, and workstream map; review and approve `plan.md`.
7. Initialize execution state.
8. Plan, approve, implement, and verify capability-oriented Builder workstreams.
9. Use independent reviews for meaningful checkpoints.
10. Reconstruct meaningful workstreams so humans understand what was built and verified.
11. Build frontend and local integration work only when the approved problem requires it and relevant contracts are stable enough.
12. Choose local or deployed release path according to official rules, demo needs, reliability, and remaining time.
13. Run final review, whole-project engineering reconstruction, internal Demo Freeze, and official event freeze/submission.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest
uvicorn backend.main:app --reload
```

Confirm [http://127.0.0.1:8000/](http://127.0.0.1:8000/) returns `{"status":"ok"}`. Set `DATABASE_URL` in the process environment only when approved persistence or Alembic work needs it; never commit credentials.

For step-by-step onboarding, read [Quickstart](docs/guides/QUICKSTART.md). For copy/paste lifecycle handoffs, open the [Prompt Playbook](docs/guides/PROMPT_PLAYBOOK.md).

## Hackathon Engineering Priority

```text
working MVP -> correctness -> integration -> verification -> demo readiness -> documentation depth
```

This is an engineering prioritization rule under time pressure. It does not mean skipping validation, ignoring bugs, omitting critical tests, or accepting broken integration. It means not spending scarce time on speculative infrastructure or documentation polish while the critical product path is incomplete.

## What This Template Does Not Predetermine

- Domain entities, database schema, or domain APIs
- Business rules, decision algorithms, or product-specific validation
- A frontend framework or real interface
- Deployment architecture or distributed infrastructure
- ML systems, optimization infrastructure, caches, queues, or background workers

Those choices must come from official event rules, the official challenge/problem statement, and approved design.

## Documentation

- [Quickstart](docs/guides/QUICKSTART.md)
- [Workflow concepts](docs/guides/WORKFLOW.md)
- [Prompt Playbook](docs/guides/PROMPT_PLAYBOOK.md)
- [Full-stack guide](docs/guides/FULL_STACK_GUIDE.md)
- [Builder workflow](docs/AGENT_WORKFLOW.md)
- [Reviewer workflow](docs/REPO_REVIEW_WORKFLOW.md)

Reusable methodology lives in `AGENTS.md`, `docs/AGENT_WORKFLOW.md`, `docs/REPO_REVIEW_WORKFLOW.md`, and `docs/guides/`. Project-specific state lives in `problem.md`, `plan.md`, `execute.md`, `review.md`, phase/review records, and the implementation that an approved problem justifies.

Demo Freeze is this workflow's internal stability gate. Official Code Freeze or submission deadlines are external event boundaries and take precedence.

## Git Workflow

Agents do not commit or push automatically. Humans review verified work, approve checkpoints, and control history changes.

## License

No license is included yet. Choose one deliberately before publishing the repository.
