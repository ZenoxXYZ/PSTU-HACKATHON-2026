# Prompt Playbook

Use these prompts as copy/paste lifecycle handoffs. Replace bracketed placeholders. Each agent must read `AGENTS.md` and the governing workflow before acting. Planning prompts use Plan Mode; implementation begins only after explicit human approval.

PSTU repository note: before challenge work, read `../event/PSTU_NATIONAL_HACKATHON_2026_RULES.md`. Treat it as the canonical event-governance overlay, and do not write pre-event governance into `problem.md`, `plan.md`, `execute.md`, or `review.md`.

## Essential Set Under Time Pressure

Use the smallest sequence that protects the critical path:

1. Starter Check
2. Official Rules and Problem Statement Intake
3. Problem Definition
4. Master System Design
5. Plan Pre-Implementation Review
6. Initialize Execution State
7. New Builder Workstream
8. Approve and Implement
9. Independent Review for meaningful checkpoints
10. Post-Implementation Workstream Reconstruction
11. Frontend Workstream if needed and relevant contracts are stable enough
12. Systematic Full-Stack Integration / Hardening
13. Release Path Decision
14. Local E2E or Deployment Workstream
15. Local/Deployed Verification / Final E2E Review
16. Whole-Project Engineering Reconstruction
17. Internal Demo Freeze and Official Event Freeze/Submission

Not every tiny task requires a fresh Reviewer or long reconstruction. Golden Path means the most important successful user journey that demonstrates the core value of the MVP. Identify it before implementation, use it to drive workstream priority and contracts, and refine it only when legitimate evidence or approved design changes require that. Public deployment is conditional, and local E2E remains a valid final path when official rules and demo needs allow it. Do not compress away verification of the critical path.

## 1. Starter Check

### Role

Repository maintainer.

### When to Use

Before accepting a new problem statement or starting a new project from the template.

### Mode

Plan Mode / read-only.

### Prompt

```text
Read AGENTS.md, docs/AGENT_WORKFLOW.md, docs/REPO_REVIEW_WORKFLOW.md, official event rules or organizer clarifications if supplied, problem.md, plan.md, execute.md, review.md, relevant phase/review records, code, tests, migrations, configuration, and Git evidence. Verify that this starter is problem-agnostic and report its actual readiness, drift, existing worktree changes, event-rule constraints on starter use or AI assistance, and decisions required. Do not modify files, install dependencies, commit, or push.
```

## 2. Problem Statement Intake / Source Analysis

### Role

Requirements analyst.

### When to Use

When official event rules, organizer clarifications, the challenge/problem statement, or other source artifacts arrive.

### Mode

Plan Mode / read-only.

### Prompt

```text
Read AGENTS.md and inspect the supplied source material: [OFFICIAL EVENT RULES, ORGANIZER CLARIFICATIONS, AUTHORITATIVE PROBLEM STATEMENT, OR ARTIFACTS]. Identify which supplied sources are authoritative. Produce an intake analysis for human review that extracts only explicit evidence: competition constraints, starter/prebuilt-code policy, AI-assistance policy, submission/code-freeze policy, deployment/demo requirements, objectives, actors, inputs, outputs, constraints, mandatory capabilities, evaluation criteria, stated technology constraints, ambiguities, contradictions, and missing information.

For every material conclusion, cite its source and distinguish [OFFICIAL EVENT RULE], [PROBLEM REQUIREMENT], and [UNSPECIFIED]. Do not design architecture, choose entities, APIs, schema, algorithms, deployment, or frontend technology. Do not edit repository files. Stop for human review.
```

## 3. Problem Definition

### Role

Requirements analyst.

### When to Use

After source intake is reviewed, or when a clear authoritative text brief is supplied directly.

### Mode

Plan Mode.

### Prompt

```text
Read AGENTS.md, docs/AGENT_WORKFLOW.md, the official event rules/clarifications, authoritative challenge/problem source or approved intake analysis, and current repository state. Produce a proposed problem.md only; do not edit it.

Use sections appropriate to the brief, including as applicable: official event constraints that affect requirements; problem objective; actors/users; required capabilities; entities or concepts explicitly implied by the brief; inputs; outputs; constraints; stated validation or business requirements; stated external systems; evaluation or success criteria; deployment or remote-demo requirement if explicitly stated; ambiguities; unspecified decisions; and explicit deferrals only where the brief supports them.

Mark every important conclusion as [PROBLEM REQUIREMENT], [UNSPECIFIED], or [DESIGN DECISION]. Avoid [DESIGN DECISION] at this stage unless it is clearly identified as unapproved. Do not design architecture, APIs, persistence, algorithms, deployment, or frontend behavior. Stop for human review and approval.
```

## 4. Approve and Write `problem.md`

### Role

Builder.

### When to Use

After the proposed interpretation is explicitly approved.

### Mode

Implementation.

### Prompt

```text
The proposed problem interpretation is approved. Update problem.md exactly to the approved interpretation. Preserve the distinction between [PROBLEM REQUIREMENT], [UNSPECIFIED], and [DESIGN DECISION]. Do not begin product design or implementation. Do not modify unrelated files, commit, or push.
```

## 5. Master System Design

### Role

Lead Builder.

### When to Use

After `problem.md` is approved.

### Mode

Plan Mode.

### Prompt

```text
Read AGENTS.md, docs/AGENT_WORKFLOW.md, approved problem.md, plan.md, execute.md, review.md, relevant phase/review records, code, tests, migrations, dependencies, configuration, and Git evidence. Reconstruct the current repository state before designing.

Produce the smallest coherent MVP plan that covers only approved requirements and complies with official event rules/clarifications. Identify the Golden Path before implementation and use it to drive scope, architecture, contracts, workstream order, integration, E2E, and demo preparation.

Address, where applicable: system boundary; actors; architecture; major components; domain model; database schema and relationships; important API/data contracts needed by the MVP and Golden Path; endpoint methods, paths, request shapes, response shapes, meaningful status/error behavior, and consuming frontend views/components where known; validation; service boundaries; business or decision logic; state transitions; error behavior; frontend requirements; frontend/backend contracts; migration strategy; integration strategy with contract integration, feature/slice integration, systematic hardening, and Golden-Path E2E as distinct stages; release path options; deployment strategy only if officially required, necessary for the demo, or reliable and valuable within remaining time; testing and verification strategy; capability-oriented workstream map with involved layers, dependencies, major contracts, verification expectations, and exit criteria; dependency decisions; external-service justification and fallback; problem-justified security requirements; official Code Freeze/submission constraints; explicit deferrals; risks; and unresolved decisions.

Label each non-obvious choice [DESIGN DECISION], never as a problem requirement. Do not implement or edit files. Stop for human approval.
```

## 6. Plan Pre-Implementation Review

### Role

Senior architecture reviewer.

### When to Use

Before implementation begins on a proposed master plan.

### Mode

Plan Mode / read-only.

### Prompt

```text
Read AGENTS.md, docs/AGENT_WORKFLOW.md, approved problem.md, the proposed plan, current repository evidence, and relevant guidance. Review the proposed plan without editing files.

Check official-rule compliance, requirement coverage, invented requirements, unnecessary complexity, Golden Path clarity, missing entities or relationships, API and schema consistency, planned contract completeness, frontend/backend contract completeness, failure behavior, migration implications, conditional deployment implications, local release path viability, external-service risks/fallbacks, testability, feasibility for the available time, capability-oriented workstream ordering, critical path, official Code Freeze/submission constraints, explicit deferrals, overengineering, under-design, and unresolved design decisions.

Report strengths, contradictions, missing decisions, overengineering, under-design, and recommended corrections. Produce a revised plan only if requested. Stop for human approval.
```

## 7. Initialize Execution State

### Role

Builder.

### When to Use

After the master plan is approved.

### Mode

Implementation.

### Prompt

```text
Read AGENTS.md, docs/AGENT_WORKFLOW.md, official event rules/clarifications when supplied, approved problem.md and plan.md, current state files, and repository evidence. Initialize or reconcile execute.md and review.md only where verified evidence supports it. In execute.md, derive the compact workstream status summary from plan.md and track each workstream by capability, Golden-Path relationship, dependencies, relevant contracts, involved layers, verification expectation, evidence, blockers, next step, and deferrals. Use N/A for layers outside the approved scope. Do not implement product behavior, change architecture, commit, or push.
```

## 8. New Builder Workstream

### Role

Builder.

### When to Use

For each new approved implementation slice.

### Mode

Plan Mode.

### Prompt

```text
In a fresh session, read AGENTS.md and docs/AGENT_WORKFLOW.md. Reconstruct authoritative requirements, approved design, the execution checkpoint, relevant code, tests, migrations, configuration, dependencies, phase/review records, and Git evidence. Do not rely on prior chat memory.

Propose a bounded capability-oriented plan for [WORKSTREAM NAME] with: objective/capability; Golden-Path relationship; official event constraints; requirements addressed; verified current state; design decisions; scope; explicit deferrals; files and layers likely affected; data/schema changes; API/data contracts affected and whether they are implementation-ready; service or logic changes; frontend impact or N/A; backend impact or N/A; persistence impact or N/A; integration impact or N/A; infrastructure/deployment impact if any; external-service dependencies and fallback if any; validation and error behavior; migration implications; implementation tasks; focused slice verification; API/frontend/backend/persistence verification where applicable; reconstruction topics; risks; and completion criteria. Stop before implementation for human approval.
```

## 9. Approve and Implement Workstream

### Role

Builder.

### When to Use

Only after the workstream plan is explicitly approved.

### Mode

Implementation.

### Prompt

```text
Exit Plan Mode and implement exactly the approved [WORKSTREAM NAME] scope. Follow AGENTS.md and docs/AGENT_WORKFLOW.md. Preserve layer boundaries and existing compatible behavior unless the approved plan says otherwise. Implement against the relevant approved contract; if material contract changes are required, stop for approval and propagate the approved change to every affected layer. Create migrations for approved persistence changes; do not run migrations automatically at startup or mutate real databases.

Reproduce and fix implementation-time bugs with evidence, add regression coverage, run focused checks during implementation and broader relevant verification at closeout. Create proportional docs/phases documentation, reconcile execute.md/review.md only with verified evidence, and prepare for post-implementation workstream reconstruction. Under strict hackathon mode, keep documentation and learning concise.

Report changed files, database changes, request/data flow, verification results, remaining deferrals, reconstruction summary, and anything not verified. Stop before commit or push for human review.
```

## 10. Implementation-Time Bug Investigation

### Role

Builder.

### When to Use

When a failure is discovered while implementing an approved workstream.

### Mode

Implementation.

### Prompt

```text
For [SYMPTOM], reproduce or verify the failure, record expected and actual behavior, inspect repository evidence, locate the responsible layer, and identify the root cause. Propose the smallest design-preserving fix. Add regression coverage, run focused and broader relevant verification, and record a stable BUG-ID only after the bug is verified. Escalate any material architecture, schema, API, policy, deployment, or scope change for human approval before implementing it.
```

## 11. Builder Closeout

### Role

Builder.

### When to Use

At a verified workstream checkpoint.

### Mode

Implementation.

### Prompt

```text
Audit [WORKSTREAM NAME] against AGENTS.md and docs/AGENT_WORKFLOW.md. Reconcile completion claims against code, tests, migrations, safe runtime checks, documentation, and Git evidence. Report changed files, implementation, request/data flow, verification, verified bugs, deferrals, risks, exact checkpoint scope, and what should be reconstructed for human understanding. Update only repository records that the evidence supports. Do not commit or push.
```

## 12. Independent Repository Review

### Role

Independent Reviewer.

### When to Use

After a meaningful workstream or named checkpoint.

### Mode

Read-only initial review.

### Prompt

```text
Read AGENTS.md and docs/REPO_REVIEW_WORKFLOW.md. Establish the exact [CHECKPOINT] and diff scope, including the baseline commit and uncommitted changes if applicable. Independently reconstruct requirements and implemented state from repository evidence; do not rely on Builder claims.

Trace requirement coverage and inspect architecture, schema/migration consistency, API contracts, validation, business or decision logic, failure handling, tests, regression risk, configuration/security concerns relevant to scope, documentation drift, frontend/backend compatibility where applicable, and deployed verification where deployment is in scope. Classify each finding exactly as a verified bug, design issue, documentation drift, missing verification, deferred feature, or optional improvement, following the Reviewer workflow. The initial pass is read-only: do not fix, commit, or push. End with the required review status and stop.
```

## 13. Approve Local Review Fixes

### Role

Reviewer.

### When to Use

After a human accepts specific local, design-preserving findings.

### Mode

Implementation.

### Prompt

```text
Human approval: correct only [FINDING IDs]. Follow docs/REPO_REVIEW_WORKFLOW.md: reproduce each accepted finding, identify the root cause, make the smallest design-preserving correction, add regression coverage where appropriate, verify it, and update accepted review evidence. Do not widen scope, redesign architecture, commit, or push.
```

## 14. Corrective Builder Workstream

### Role

Builder.

### When to Use

For a human-approved correction that materially affects architecture, data, API, policy, deployment, or scope.

### Mode

Plan Mode.

### Prompt

```text
Read AGENTS.md, docs/AGENT_WORKFLOW.md, the approved review finding [FINDING IDs OR EVIDENCE], approved requirements/design, and repository evidence. Produce a corrective Builder plan covering the violated invariant, affected architecture/data/API/policy/deployment behavior, decisions required, scope, explicit deferrals, migration and compatibility implications, tests, verification, and risks. Do not implement until the human approves the plan.
```

## 15. Frontend Workstream

### Role

Frontend Builder.

### When to Use

After UI requirements and the relevant backend/API contracts are approved and stable enough for the frontend scope. Frontend does not need to wait for every backend workstream to finish.

### Mode

Plan Mode.

### Prompt

```text
Read AGENTS.md, docs/AGENT_WORKFLOW.md, docs/guides/FULL_STACK_GUIDE.md, approved problem.md and plan.md, current backend contracts, tests, and repository evidence. Plan the smallest frontend capability or slice for the actual user workflow: required pages/views/components, frontend state model, API calls, loading, empty, success, validation, failure, recovery, Golden-Path relationship, and minimal visual polish.

Keep business and decision logic in the backend. Identify any missing or incompatible contract before implementation. State scope, deferrals, affected files, tests, verification, environment configuration for API base URL, deployment implications, and risks. Stop for human approval.
```

## 16. Systematic Full-Stack Integration / Hardening Workstream

### Role

Integration Builder.

### When to Use

After relevant frontend/backend slices have already had incremental feature/slice integration and the assembled Golden Path needs systematic hardening.

### Mode

Plan Mode.

### Prompt

```text
Read AGENTS.md, docs/AGENT_WORKFLOW.md, docs/guides/FULL_STACK_GUIDE.md, approved problem.md and plan.md, frontend and backend code, contracts, tests, migrations, configuration, and Git evidence. Plan systematic hardening of the assembled Golden Path. This is not the first time frontend and backend meet.

User action -> frontend state -> HTTP request -> FastAPI route -> validation -> service -> business logic -> persistence -> response -> frontend rendering.

Inspect endpoint/path mismatch, HTTP method mismatch, request-field mismatch, response-field mismatch, status/error handling, frontend API base URL, CORS, environment configuration, loading state, empty state, error state, success state, mutation/refetch behavior, stale frontend state, backend validation, persistent state, refresh/reload correctness, cross-page continuity, and Golden-Path continuity. Identify each contract boundary, error propagation path, mismatch risk, test approach, affected files, scope, deferrals, verification commands, deployment implications, and completion criteria. Stop before implementation for human approval.
```

## 17. Integration Debugging

### Role

Integration Builder.

### When to Use

When an approved end-to-end path fails.

### Mode

Implementation.

### Prompt

```text
Reproduce [INTEGRATION SYMPTOM] across user action, frontend state, request, route, validation, service/logic, persistence, response, and rendering. Compare expected and actual behavior at each boundary, isolate the root cause, and implement only an approved design-preserving correction. Verify the full path, contract compatibility, error propagation, and relevant regression checks. Escalate material contract, deployment, or architecture changes for approval. Do not commit or push.
```

## 18. Deployment Workstream Plan

### Role

Deployment Builder.

### When to Use

After local backend and local frontend integration are verified, when deployment is officially required, necessary for the demo, or reliable and valuable within remaining time.

### Mode

Plan Mode.

### Prompt

```text
Read AGENTS.md, docs/AGENT_WORKFLOW.md, docs/guides/FULL_STACK_GUIDE.md, official event rules/clarifications when supplied, approved problem.md, approved plan.md, execute.md, review.md, relevant phase/review docs, frontend code, backend code, configuration, migrations, dependencies, tests, and Git evidence. Reconstruct the locally verified state, including local Golden-Path E2E and Feature Freeze status, before proposing deployment.

First verify that deployment is allowed and justified by official rules, demo needs, reliability, and remaining time. If local E2E is the better release path, recommend that and stop for human approval. If deployment should proceed, propose the smallest deployment architecture for [DEPLOYMENT TARGET OR OPTIONS]. Identify provider-specific requirements only after provider choice. Cover backend hosting, hosted database, environment variables, production start command, database and migration steps, frontend hosting if present, frontend production API URL, CORS requirements, external-service access and failure modes, secret handling, verification plan, fallback demo path, affected files, risks, and explicit deferrals.

Do not add Docker, containers, queues, cloud infrastructure, or deployment complexity unless the selected provider or approved problem requires it. Do not edit files, commit, push, or mutate a real hosted database. Stop for human approval before implementation.
```

## 19. Approve and Implement Deployment

### Role

Deployment Builder.

### When to Use

Only after the deployment workstream plan is explicitly approved.

### Mode

Implementation.

### Prompt

```text
Exit Plan Mode and implement only the approved deployment changes. Follow AGENTS.md and docs/AGENT_WORKFLOW.md. Confirm deployment remains allowed by official rules and organizer clarifications. Configure environment appropriately, preserve secret hygiene, avoid committing real credentials, and keep the deployment architecture as small as approved.

Apply or verify migrations only against the approved deployment database and only with explicit human approval for real hosted state. Verify the public backend health endpoint, public frontend if present, frontend calls to the deployed backend rather than localhost, CORS, hosted database connectivity, state persistence, and the deployed golden flow.

Report public backend URL, public frontend URL if applicable, hosted database/migration status, environment variables configured by name only, verification evidence, known risks, fallback demo path, and anything not verified. Do not commit or push.
```

## 20. Post-Implementation Workstream Reconstruction

### Role

Technical explainer / Builder handoff.

### When to Use

After a meaningful workstream is implemented and verified.

### Mode

Read-only explanation. Do not modify code.

### Prompt

```text
Do not modify code, configuration, dependencies, migrations, tests, project-state files, commit, or push.

Read AGENTS.md, docs/AGENT_WORKFLOW.md, approved problem.md, approved plan.md, execute.md, review.md, relevant phase/review documentation, code, tests, migrations, configuration, and Git evidence. Teach and reconstruct the completed [WORKSTREAM NAME] from the actual repository, not from memory or a generic lecture.

Cover: 1. requirement solved; 2. capability/objective; 3. Golden-Path relationship; 4. design chosen and why; 5. important files; 6. layer responsibilities and N/A layers; 7. runtime flow; 8. data flow; 9. DB/API impact; 10. dependencies; 11. downstream consumers; 12. verification/tests; 13. meaningful bugs/fixes; 14. assumptions/deferrals; 15. a 30-60 second judge explanation.

Link theory directly to the actual implementation. For relevant full-stack slices, trace requirement -> user action -> frontend -> API route -> schema -> service -> business or decision logic -> SQLAlchemy/database -> response -> frontend update -> visible outcome -> verification. For backend-only or frontend-only workstreams, explain only relevant layers and why other layers were N/A. Use concise hackathon mode unless the human asks for deeper teaching. Ask/check whether the human can explain the workstream, then stop once understanding is sufficient.
```

## 21. Whole-Project Engineering Reconstruction / Judge Readiness

### Role

Technical explainer / demo readiness coach.

### When to Use

After major workstreams and final review, before Demo Freeze or judge presentation.

### Mode

Read-only explanation. Do not modify code.

### Prompt

```text
Do not modify code, configuration, dependencies, migrations, tests, project-state files, commit, or push.

Read AGENTS.md, docs/AGENT_WORKFLOW.md, docs/REPO_REVIEW_WORKFLOW.md, approved problem.md, approved plan.md, execute.md, review.md, phase/review docs, code, tests, migrations, frontend, deployment configuration, public URLs if available, and Git evidence. Reconstruct the whole project from repository evidence for judge readiness.

Cover: project objective; actors; MVP and Golden Path; architecture; capability-oriented workstreams; entity/domain relationships; database; API/data contracts; request flows; service boundaries; business/decision logic; dynamic updates or re-evaluation when present; frontend; frontend/backend contracts; integration stages; selected release path; deployment if selected; tests; known limitations; major engineering decisions; why modular monolith; why FastAPI/Pydantic/SQLAlchemy/Alembic if those remain the chosen stack; and what would change for production.

Produce a whole-repo map, a 2-minute technical explanation, a 30-second architecture explanation, likely judge questions, concise answers, critical files to know, and the golden demo flow. Keep it concise enough for hackathon use and stop for human review.
```

## 22. Final End-to-End Review

### Role

Independent Reviewer.

### When to Use

Before a demonstration or delivery checkpoint.

### Mode

Read-only initial review.

### Prompt

```text
Read AGENTS.md, docs/REPO_REVIEW_WORKFLOW.md, and official event rules/clarifications when supplied. Reconstruct the current verified state and run the final repository review for [CHECKPOINT]. Prioritize official-rule compliance, startup, the approved golden user flow, core correctness, persistence/state, frontend/backend compatibility, selected release-path evidence, critical validation and error behavior, test evidence, configuration relevant to the demo, and P0/P1 findings.

When using the local release path, verify or inspect evidence for local integration, local E2E/final verification, final review readiness, and fallback/demo reliability. When using the deployed release path, distinguish local verification from deployed verification and verify or inspect evidence for public backend startup, public health endpoint, frontend production API URL, no hard-coded localhost dependency, CORS, hosted database connectivity, applied migrations, and the deployed golden user flow. Classify missing selected-release-path evidence as [MISSING VERIFICATION] unless there is a verified defect.

The initial review is read-only. Classify evidence and findings under the Reviewer workflow, report the required review status, and stop without fixing, committing, or pushing.
```

## 23. Demo Freeze

### Role

Release coordinator.

### When to Use

When preparing the final demonstration or delivery.

### Mode

Implementation.

### Prompt

```text
Enter STRICT HACKATHON / TIME-CONSTRAINED MODE. Read AGENTS.md, the governing workflows, official event rules/clarifications when supplied, approved requirements/design, current state files, code, tests, migrations, configuration, deployment records if applicable, public URLs if available, and Git evidence to reconstruct what is verified. Identify the golden demo path and freeze optional feature development.

Identify P0/P1 blockers. Verify startup; required database and migrations; backend behavior; frontend behavior; selected release path; local full-stack integration; local E2E when using the local path; deployed URLs, hosted DB, applied migrations, environment configuration, production API URL, CORS, and deployed golden path when using the deployed path; fallback demo path; known limitations; official Code Freeze/submission readiness; and critical validation and error behavior.

Demo Freeze is an internal stability gate, not the official deadline. Official Code Freeze and submission deadlines are external event boundaries and take precedence. Do not perform speculative refactoring, add features, commit, or push. Stop for human approval of the checkpoint.
```

## 24. Optional Post-Hackathon Hardening

### Role

Maintainer.

### When to Use

After the time-constrained event.

### Mode

Plan Mode.

### Prompt

```text
Read repository evidence, approved requirements/design, review findings, deployment findings, and demo risks. Propose a prioritized hardening roadmap for reliability, security, maintainability, and deployment. Do not reclassify design decisions as problem requirements. Stop for approval before implementation.
```
