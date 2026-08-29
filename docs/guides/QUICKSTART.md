# Quickstart

Use this guide when a new hackathon brief arrives. The goal is to establish an evidence-backed MVP path without guessing product requirements.

## 1. Create Your Project

First inspect any official event rules or organizer clarifications. Reusable code, boilerplate, starter infrastructure, authentication components, UI libraries, AI-assisted development, deployment, and submission/code-freeze behavior must comply with those rules.

For this PSTU repository, read `../event/PSTU_NATIONAL_HACKATHON_2026_RULES.md` before challenge intake. Keep `problem.md`, `plan.md`, `execute.md`, and `review.md` as challenge-ready templates until the official Challenge Document arrives.

Use GitHub's **Use this template** option if the owner has enabled it, then clone the resulting repository. Alternatively:

```powershell
git clone <template-repository-url> my-hackathon-project
cd my-hackathon-project
```

If the official rules permit starter reuse and you need independent Git history, use the template feature or deliberately reinitialize Git yourself. This template never changes Git history automatically. Do not assume every event permits the same prebuilt starting point.

## 2. Prepare the Local Foundation

Create the local Python environment before product implementation:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest
uvicorn backend.main:app --reload
```

Confirm `http://127.0.0.1:8000/` returns `{"status":"ok"}`. Add `DATABASE_URL` to your process environment only when approved persistence or Alembic work needs it; do not commit credentials.

Do not add problem-specific dependencies until an approved design justifies them.

## 3. Declare Time Constraints When They Matter

At the opening of an AI or team workstream, explicitly state:

```text
STRICT HACKATHON / TIME-CONSTRAINED MODE
```

This asks the team to protect the MVP, correctness, integration, deployment readiness when needed, verification, and demo readiness before detailed documentation, long teaching sessions, or polish. It does not override official event rules, official Code Freeze, or submission deadlines.

## 4. Define the Problem Before Designing

1. Provide official event rules, organizer clarifications, and the authoritative hackathon statement when available.
2. Use Problem Statement Intake in the [Prompt Playbook](PROMPT_PLAYBOOK.md).
3. Use Problem Definition and review the proposed `problem.md`.
4. Approve `problem.md`.
5. Run Master System Design, identify the Golden Path, important API/data contracts, and capability/workstream map, then approve `plan.md`.
6. Initialize or reconcile `execute.md` and `review.md` with repository evidence.

Only then begin product implementation.

## 5. Build, Understand, Integrate, and Deploy

The normal flow is:

```text
create repo from template
-> create/activate .venv
-> install dependencies
-> run starter tests
-> verify health endpoint
-> official event rules / clarifications
-> authoritative problem statement
-> Problem Intake
-> problem.md
-> MVP + Golden Path
-> Master System Design
-> plan.md contracts and workstream map
-> execution state
-> backend/persistence foundation
-> first stable capability and relevant contracts
-> frontend begins where relevant
-> capability-oriented Builder workstreams
-> incremental vertical integration
-> workstream reconstruction
-> Golden Path complete
-> systematic full-stack integration / hardening
-> local Golden-Path E2E
-> Feature Freeze
-> choose local or deployed release path
-> local final E2E or deployment plus deployed verification
-> final review
-> whole-project reconstruction
-> internal Demo Freeze
-> official event freeze/submission
```

For each meaningful Builder workstream:
1. Start a fresh Builder workstream in Plan Mode.
2. Approve its plan before implementation.
3. Implement, debug, test, verify, and record the workstream under `docs/phases/`.
4. Run an independent Reviewer workstream for meaningful or risky checkpoints.
5. Reconstruct the verified workstream so the human understands what was built, where it lives, how it runs, what state it touches, and how it was verified.
6. Close the Builder chat only after the human understanding checkpoint is sufficient.

Golden Path means the most important successful user journey that demonstrates the core value of the MVP. Identify it before implementation and use it to prioritize scope, contracts, workstreams, integration, E2E, and demo preparation.

Backend-first does not mean backend-complete-first. Establish the domain foundations, persistence, invariants, critical backend capabilities, and sufficiently stable API/data contracts first; then frontend work may begin where relevant once the needed contract/capability is stable enough. Local full-stack integration verifies the app on local services. Systematic full-stack integration is a hardening pass after incremental slice integration has already happened. If deployment is officially required, necessary for the demo, or reliable and valuable within remaining time, add a deployment workstream and verify the deployed golden path before internal Demo Freeze. If deployment is not required or not a good tradeoff, reliable local E2E/final verification remains a valid release path.

## 6. Compressed Six-Hour Guidance

| Time | Focus |
| --- | --- |
| 0:00-0:30 | Read brief, define scope, approve `problem.md`. |
| 0:30-1:00 | Master design, Golden Path, important contracts, and workstream map; approve `plan.md`. |
| 1:00-2:15 | Build backend foundation and the first stable capability/contract. |
| 2:15-3:45 | Continue backend/frontend work incrementally; frontend begins where relevant once contracts are stable enough. |
| 3:45-4:45 | Complete the Golden Path, verify focused slices, and harden systematic full-stack integration. |
| 4:45-5:15 | Run local Golden-Path E2E, critical failure checks, and P0/P1 fixes. |
| 5:15-5:35 | Feature Freeze and choose local or deployed release path; deploy only when required, necessary, or valuable within time. |
| 5:35-6:00 | Local final E2E or deployed E2E, final review, whole-project reconstruction, fallback demo path, internal Demo Freeze, and official freeze/submission readiness. |

Learning should be proportional:
- Small reconstruction: 2-3 minutes.
- Meaningful workstream: 5-8 minutes.
- Core business or decision workstream: up to about 8-10 minutes.
- Whole-project reconstruction before demo: about 10-15 minutes.

If time is shorter, reduce scope before reducing verification of the primary flow.
