# PSTU National Hackathon 2026 Rules And Governance

## Source Verification

This event-governance interpretation was verified directly against the local official source PDF:

- Source file: `docs/event/sources/National_Hackathon.pdf`
- Verification status: directly reviewed during P1 rulebook intake
- Local-source status: the PDF is a trusted local source for this repository and is intentionally ignored by Git
- Commit status: the source PDF is not claimed to be committed

This document summarizes the official rulebook for repository governance. It does not duplicate the full PDF, and it must be updated if official organizer clarifications change the rules.

## Authority Model

```text
Official PSTU Rulebook + official organizer clarifications
-> Official Challenge / Problem Statement
-> approved problem.md
-> approved plan.md
-> actual repository implementation + migrations + tests + safe runtime/API evidence
-> execute.md / review.md / explanatory documentation
```

Official rules constrain the process. The Challenge Document defines the product to build. `problem.md` normalizes the official challenge requirements after human approval. `plan.md` records the approved implementation design. Actual code, migrations, tests, Git evidence, and safe runtime/API checks determine implemented truth. `execute.md` tracks implementation state, and `review.md` summarizes verified engineering and review history.

Generic workflow documents are engineering methodology. They never outrank the official PSTU rulebook or official organizer clarifications.

## Official Event Facts

[OFFICIAL EVENT RULE] PSTU IT Carnival 2026 presents National Hackathon 2026, organized by the CSE Club of Patuakhali Science and Technology University.

[OFFICIAL EVENT RULE] The event date is 29 August 2026.

[OFFICIAL EVENT RULE] This is a software-development hackathon. The actual problem will come from a separately supplied Challenge Document.

[OFFICIAL EVENT RULE] The development window is 9:00 AM to 3:00 PM, for six hours including lunch. Lunch, recess, and ordinary venue-internet problems do not normally extend the development window. Active development stops at 3:00 PM unless organizers authorize an exception.

[OFFICIAL EVENT RULE] After official Code Freeze, teams may be asked to demonstrate the application and explain the solution. Fixing, adding, or substantially modifying functionality is not permitted unless organizers specifically authorize it. Genuine emergencies remain organizer-discretion matters.

Internal engineering checkpoints must not be described as official PSTU scheduling rules.

## Required Application

[OFFICIAL EVENT RULE] The solution must include:

- a user-facing web or mobile application;
- a backend/server-side application responsible for core business logic or data processing;
- appropriate storage/database where required.

[OFFICIAL EVENT RULE] A responsive, mobile-compatible web application is acceptable.

[ENGINEERING INTERPRETATION] PSTU requires a frontend or user-facing application, but this does not mean frontend-first implementation. It also does not mean all backend work must finish before frontend work begins.

[ENGINEERING METHODOLOGY] Preserve the repository method:

```text
Golden Path / Master System Design
-> backend/persistence foundations
-> relevant API contract becomes stable
-> frontend for that capability begins
-> vertical slice is integrated where appropriate
-> focused verification
-> next capability
```

Backend-first does not mean backend-complete-first. This is repository methodology, not an official PSTU-prescribed process.

## Technology And Architecture Freedom

[OFFICIAL EVENT RULE] Languages and frameworks are unrestricted. Architecture is not prescribed. Complexity itself does not improve the solution. Teams should be able to explain why their architecture fits the problem.

[ENGINEERING METHODOLOGY] For a six-hour MVP, prefer the simplest explainable architecture that satisfies the official challenge. A modular monolith is often a good default, but it is not a PSTU requirement.

FastAPI, React, PostgreSQL, SQLAlchemy, Alembic, modular-monolith separation, and any other starter defaults are repository design choices unless the later Challenge Document or organizer clarification makes something mandatory.

## AI Rules

[OFFICIAL EVENT RULE] AI development tools are allowed. The official source lists examples including ChatGPT, Claude, Gemini, GitHub Copilot, Cursor, coding assistants, conversational AI, and AI IDEs.

[OFFICIAL EVENT RULE] Organizers do not guarantee subscriptions, API keys, credits, tokens, paid accounts, or other paid AI/service access. Teams using AI are responsible for arranging access beforehand.

[OFFICIAL EVENT RULE] The participant/team remains responsible for understanding and explaining code, architecture, algorithms, database design, and engineering decisions.

## AI Workflow Interpretation

[ENGINEERING METHODOLOGY] This repository may use this internal workflow:

- Codex: repository implementation agent.
- GPT Control Room: architecture, critique, supervision, reconstruction, teaching, and workflow control.
- Human participant: accountable decision-maker who must understand and explain the system.

This is our workflow. It is not an officially prescribed PSTU agent architecture.

## Human Learning And Understanding Model

[ENGINEERING METHODOLOGY] Meaningful workstreams should eventually be reconstructable for the human operator in terms of:

| Area | Question |
| --- | --- |
| What | What concept or capability exists? |
| Why | Why does it exist? |
| Analogy | What simple real-world analogy makes it intuitive? |
| Technical meaning | What is actually happening in software terms? |
| Repository location | Which files and layers implement it? |
| Relationships | What comes before and after it? |
| Runtime / data flow | How does data move through the system? |
| Engineering decision | Why was this approach chosen? |
| Alternatives | What else could have been chosen? |
| Tradeoff | What did the chosen option gain or lose? |
| Verification | What evidence proves it works? |
| Failure mode | What could break? |
| Judge explanation | How can the human explain it concisely? |

Do not turn repository documentation into a giant classroom textbook. Codex should build efficiently, GPT should reconstruct and teach efficiently, and the human should develop real understanding.

## Prebuilt Code And Starters

[OFFICIAL EVENT RULE] Generic reusable material may be used, including boilerplate, starters, utilities, personal libraries, authentication components, and UI libraries.

[OFFICIAL EVENT RULE] A substantially complete challenge-solving application must not be presented as event-built work. The challenge-specific core solution must be developed during the event.

[EXPLANATORY ANALOGY] The generic starter is the workshop: bench, tools, shelves, and measuring equipment. The Challenge Document tells us what machine to build. That challenge-specific machine must be designed and built during the event.

## Challenge Neutrality Before Release

[REPOSITORY GOVERNANCE] Until the official Challenge Document is received, this repository must not introduce:

- speculative domain entities;
- challenge-specific tables;
- challenge-specific APIs;
- challenge-specific business logic;
- challenge-specific frontend pages;
- speculative algorithms;
- assumptions imported from practice projects.

Do not contaminate this repository with assumptions from StockFlow, emergency response, previous practice problems, or any other earlier domain.

## Internet And Preparation

[OFFICIAL EVENT RULE] Venue internet is intended, but congestion, interruption, or outage may occur. Teams are strongly requested to bring mobile internet backup. Venue internet problems do not normally provide extra development time.

[OFFICIAL EVENT RULE] Teams should prepare development tools beforehand, including IDE/editor, runtimes, SDKs, package managers, database tools, mobile tooling, Git, Docker if used, frameworks, and common dependencies. Participants must bring the laptops and normal computing equipment required for development, and teams are responsible for ensuring devices are charged and operational. Chargers, adapters, and cables should also be prepared.

[ENGINEERING INTERPRETATION] Every unnecessary external dependency creates another failure surface. A local dependency is equipment already inside the workshop. An external API is a supplier outside the building. If the supplier becomes unreachable, the workflow may stop.

Prefer locally runnable core behavior, prepared dependencies, mobile backup, known credentials/configuration, and fallbacks or degraded behavior where justified. Fallback/degraded operation is engineering guidance, not an official PSTU requirement unless explicitly announced.

## External APIs And Cloud

[OFFICIAL EVENT RULE] External APIs and cloud services may be used where legally accessible. Examples include hosting, cloud databases, authentication, maps, and notification services.

[OFFICIAL EVENT RULE] The team is responsible for accounts, credentials, configuration, availability, and costs. Paid credits/services are not guaranteed unless separately announced.

[ENGINEERING METHODOLOGY] External services should be justified by the approved challenge design, have access verified before reliance, and avoid becoming unnecessary single points of failure.

## Source Control

[OFFICIAL EVENT RULE] Teams must maintain source code throughout development. Git is strongly recommended. Organizers or judges may ask to access or inspect source during or after development.

[OFFICIAL EVENT RULE] Creating and pushing a repository before event time ends is recommended/good practice where the rulebook uses recommendation language. Do not upgrade this recommendation into a mandatory rule.

[ENGINEERING METHODOLOGY] Use frequent coherent source checkpoints without excessive commit ceremony. Commits and pushes remain human-controlled in this repository.

## Deployment And Local Demo

[OFFICIAL EVENT RULE] Public deployment is welcome/useful but not mandatory unless separately announced. A successful local development environment may be demonstrated.

If a later official announcement changes deployment or submission requirements, that clarification outranks this interpretation.

[ENGINEERING METHODOLOGY] Preserve the generic release model:

```text
local Golden-Path E2E
-> Feature Freeze
-> release / deployment decision
   -> LOCAL path: final local E2E
   -> DEPLOYED path: configure hosts + env variables + production DB + migrations + API URL + CORS -> deployed E2E
```

Feature Freeze is internal. Release decision criteria are internal engineering guidance. Deployment configuration steps are engineering methodology, not official PSTU rules.

## Freeze Concepts

[ENGINEERING METHODOLOGY] Feature Freeze is an internal engineering checkpoint: stop adding normal features so integration and release can stabilize.

[ENGINEERING METHODOLOGY] Demo Freeze is an internal engineering checkpoint: stop risky changes and protect the working demo.

[OFFICIAL EVENT RULE] Official Code Freeze is the PSTU rule: active development stops at 3:00 PM unless organizers authorize an exception. After official freeze, teams may be asked to demonstrate the application and explain the solution. Do not fix, add, or substantially modify functionality unless authorized.

[EXPLANATORY ANALOGY] Official Freeze means the building closes. Feature Freeze means we stop adding rooms. Demo Freeze means we stop moving furniture before inspection.

## Judge And Organizer Interaction

[OFFICIAL EVENT RULE] Judges or organizers may visit during development and ask questions about what the team is building, what currently works, the approach, which parts were implemented by the team, and why important decisions were made.

[ENGINEERING INTERPRETATION] Human reconstruction helps the team answer those questions, but the specific reconstruction format in this repository is not an official PSTU requirement.

## Evaluation Factors

[OFFICIAL EVENT RULE] Evaluation factors include code structure, architecture, readability, maintainability, design patterns, useful comments, developer understanding, simplicity, scalability, concurrency, useful features, explanations, extensibility, algorithm choice and justification, and other stated factors.

[ENGINEERING INTERPRETATION] Evaluation categories should guide appropriate decisions, not artificial overengineering.

Scalability mentioned does not mean microservices are required. Concurrency mentioned does not mean asynchronous workers are required. Design patterns mentioned does not mean unnecessary patterns should be forced. The correct question is: does this engineering choice fit the actual challenge?

## Official Clarifications

[OFFICIAL EVENT RULE] Official organizer clarifications made to all teams become part of the rules. For uncovered cases, organizer decisions are authoritative/final as stated.

[ENGINEERING WORKFLOW] If an official clarification arrives:

1. Record it.
2. Determine which current assumptions it changes.
3. Update event or challenge documents as necessary.
4. Adjust `plan.md` or `execute.md` only if the clarification is relevant to the active challenge.

## Conduct, Recess, And Emergency

[OFFICIAL EVENT RULE] Teams are expected to act with honesty, professionalism, respect, and courtesy toward organizers, judges, mentors, and other teams.

[OFFICIAL EVENT RULE] Harassment, discrimination, disruption, and misrepresentation of contributions or technical decisions may lead to warnings, point deductions, or disqualification at organizer discretion.

[OFFICIAL EVENT RULE] Teams may take short recesses for personal needs, prayer, meals, or medical needs, and should tell an organizer before stepping away where stated. Recess does not extend the window. Genuine emergencies may be handled flexibly at organizer discretion.

## Capability-Oriented Workstream Model

[ENGINEERING METHODOLOGY] Preserve the inherited generic methodology:

```text
Golden Path identified early
-> Master System Design
-> important entities/invariants/contracts
-> capability/workstream map
-> backend/persistence foundation
-> relevant contract becomes implementation-ready
-> frontend begins where relevant
-> capability-oriented workstream
-> incremental integration
-> focused verification
-> next capability
```

A workstream may be backend-only, frontend-only, backend-heavy, frontend-heavy, a full-stack vertical slice, a decision/business-logic workstream, an integration/hardening workstream, or a deployment/release workstream. Do not force frontend and backend edits into every workstream.

## Vertical Slice Model

[ENGINEERING METHODOLOGY] For a full-stack capability, the conceptual path may be:

```text
requirement
-> user interaction
-> frontend component
-> event handler
-> frontend API client
-> HTTP/API contract
-> FastAPI router
-> Pydantic schema
-> service
-> business/decision logic
-> ORM
-> database
-> response
-> frontend state/refetch
-> rerender
-> visible result
-> verification
```

Not every workstream requires every layer. This is engineering methodology, not a PSTU-prescribed architecture.

## Challenge-State Files

[REPOSITORY GOVERNANCE] Before the official Challenge Document arrives, keep these files as generic challenge-ready templates:

- `problem.md`: later becomes the normalized official challenge requirements.
- `plan.md`: later becomes the approved challenge-specific Master System Design.
- `execute.md`: later becomes the live challenge-specific workstream tracker.
- `review.md`: later becomes verified final engineering and review history.

Do not place pre-event governance content in those files.

## Internal Time Management Recommendation

[ENGINEERING RECOMMENDATION - INTERNAL TIME MANAGEMENT] The six-hour implementation window can be managed as follows. These are internal guide rails, not official PSTU time blocks.

| Time | Internal focus |
| --- | --- |
| 9:00-9:25 | Challenge intake, requirement normalization, MVP and Golden Path. |
| 9:25-9:50 | Master System Design, contracts, and workstream map. |
| 9:50 onward | Backend/persistence foundations, then frontend begins as soon as relevant API contracts stabilize. |
| Middle window | Capability-oriented vertical workstreams and incremental integration. |
| Before release decision | Golden Path assembled, systematic full-stack hardening, and local Golden-Path E2E. |
| Release window | Feature Freeze, local/deployment decision, and final chosen-path E2E. |
| Final protected time | Review, whole-project reconstruction, demo rehearsal, Git/source checkpoint, Demo Freeze, safety buffer, and official 3:00 PM freeze. |

Do not imply frontend begins only after the entire backend is complete.

## Human And Judge Ready Decision Format

[ENGINEERING METHODOLOGY] For important decisions, use this concise explanation pattern when useful:

| Field | Meaning |
| --- | --- |
| Decision | What did we choose? |
| Problem | What requirement/problem required a choice? |
| Options | What reasonable alternatives existed? |
| Analogy | Simple analogy when helpful. |
| Choice | What did we implement? |
| Why it fits | Why is it appropriate for this challenge? |
| Tradeoff | What do we gain or lose? |
| Repo impact | Where is it implemented? |
| Verification | How do we know it works? |
| Failure impact | What happens if it fails? |
| Judge explanation | 20-30 second explanation. |

This pattern is inspired by PSTU's understanding and explanation expectations. It is not a prescribed official response format.
