# Engineering Plan

## Status

[?] Requires approved problem definition.

No product architecture, schema, API surface, frontend behavior, business rules, decision logic, deployment path, or challenge-specific workstream map is approved yet.

## Problem / MVP Summary

Capture the approved problem interpretation from `problem.md`, the smallest viable MVP, and any official event constraints that affect architecture, starter use, AI assistance, deployment, or submission.

## Golden Path

Golden Path = the most important successful user journey that demonstrates the core value of the MVP.

Identify the Golden Path before implementation during problem intake and Master System Design. It should drive MVP scope, workstream priority, architecture, data/API contracts, required frontend views, integration order, E2E verification, and demo preparation. It may be refined only when legitimate new evidence or approved design changes require it.

## Architecture

Record the approved high-level architecture, major components, selected technology, runtime boundaries, and why the choices satisfy the approved problem without unnecessary infrastructure.

## Major Entities / Relationships

List approved domain entities, persistence models, important relationships, ownership rules, and state transitions. Leave this section empty or mark it pending until `problem.md` and design approval justify real domain concepts.

## Important Invariants

Record rules that must remain true across the system, including business, decision, validation, state, persistence, security, or event-rule constraints.

## API / Data Contracts

Master System Design should identify the important API/data contracts needed by the MVP and Golden Path. Each capability workstream may stabilize or refine the relevant contract for implementation, but material contract changes must be propagated to all consumers and recorded as approved design changes.

For important endpoints, capture:

| Method | Path | Request shape | Response shape | Status/error behavior | Consuming frontend view/component |
| ------ | ---- | ------------- | -------------- | --------------------- | --------------------------------- |
| TBD | TBD | TBD | TBD | TBD | TBD |

Also record non-HTTP data contracts, event payloads, file formats, or external-service contracts when approved.

## Frontend / User-Facing Structure

At architecture level, record major pages/views, important user actions, state responsibilities, loading/empty/error/success states, and relationships to API/data contracts. No frontend framework is mandatory unless the approved problem or plan justifies one.

## Business / Decision Logic

Record approved policies, formulas, ranking rules, eligibility checks, workflows, explainability requirements, deterministic ordering, and boundary behavior. Distinguish problem requirements from design decisions.

## Workstream Map

Actual workstreams come from this approved plan. A workstream is a bounded engineering objective that creates or strengthens meaningful system behavior. Workstreams may be backend-only, backend-heavy, frontend-only, frontend-heavy, full-stack vertical slices, business/decision-logic oriented, integration/hardening oriented, specialized verification, or release/deployment oriented.

For each workstream, capture:

| ID / name | Capability / objective | Golden-Path relevance | Involved layers | Dependencies | Major contracts | Verification expectation | Exit criteria |
| --------- | ---------------------- | --------------------- | --------------- | ------------ | --------------- | ------------------------ | ------------- |
| WS-XX | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

Do not force every workstream to touch every layer. The boundary follows the capability or objective, not a technology folder.

## Integration Strategy

Use progressively stronger integration stages:

1. Level 1 - Contract integration: frontend expectations and backend design agree.
2. Level 2 - Feature / slice integration: a real frontend capability communicates with the real corresponding backend capability.
3. Level 3 - Systematic full-stack integration: the assembled Golden Path is checked and hardened across boundaries.
4. Level 4 - E2E verification: a real user journey proves the system works through required layers and produces the intended outcome.

Backend-first does not mean backend-complete-first. Backend-first means establishing authoritative domain foundations, persistence, major invariants, critical backend capabilities, and sufficiently stable API/data contracts. Frontend work may begin once a relevant contract/capability is stable enough for its approved scope.

## E2E Strategy

Separate focused slice verification from systematic integration and Golden-Path E2E.

Where relevant, Golden-Path E2E should verify:

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

Include proportionate failure-path verification. Heavyweight browser automation is useful when justified, but manual E2E may be acceptable under time constraints.

## Release / Deployment Decision Criteria

Deployment is conditional. Choose the local or deployed release path according to official rules, demo needs, reliability, and remaining time.

Local path:

```text
local Golden-Path E2E
-> Feature Freeze
-> release decision
-> local final E2E
```

Deployed path:

```text
local Golden-Path E2E
-> Feature Freeze
-> release decision
-> deployment configuration
-> production database/migrations when approved
-> production CORS/env
-> deployed E2E
```

Local runtime usually means browser -> frontend development server -> local backend -> local database. Deployed runtime usually means browser -> hosted frontend -> hosted backend -> hosted database. Business/domain architecture should ideally remain substantially unchanged between them.

## Assumptions

Record assumptions that are not problem requirements and need confirmation or future validation.

## Explicit Deferrals

Record intentionally postponed features, integrations, validations, hardening, deployment choices, or polish so they are not misclassified as bugs.
