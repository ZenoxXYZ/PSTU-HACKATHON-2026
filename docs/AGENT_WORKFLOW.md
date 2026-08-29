Builder Agent Engineering Workstream Workflow
1. Purpose
This workflow enables a fresh Builder Agent chat to reconstruct project state from repository evidence and safely continue the next engineering workstream without depending on previous chat context. It defines the procedure for planning, implementing, debugging, verifying, documenting, reconstructing, and handing off work. Stable repository rules remain in AGENTS.md.

2. Repository State Reconstruction
Every fresh Builder workstream begins by reading or inspecting the following when present and relevant:
For this PSTU repository, read `docs/event/PSTU_NATIONAL_HACKATHON_2026_RULES.md` before challenge work. It records the official rulebook interpretation and the boundary between PSTU rules and reusable engineering methodology.

- Official event rules and organizer clarifications
- Official challenge or problem statement
- AGENTS.md
- docs/AGENT_WORKFLOW.md
- problem.md
- plan.md
- execute.md
- review.md
- Relevant docs/phases/
- Relevant docs/reviews/
- Current Git status
- Recent Git history
- Actual repository structure
- Implementation
- Tests
- Migrations
- Dependency and configuration files

Apply the two-axis model in AGENTS.md: use official event rules/clarifications, the official challenge/problem statement, approved problem.md, and approved plan.md for competition constraints, requirements, and design authority; use code, tests, migrations, Git history/status, and safe runtime verification for implemented-state evidence. execute.md, review.md, phase documentation, and review documentation are summaries, not overriding evidence.

Do not trust execute.md or other documentation blindly. Cross-check important completion claims against code, tests, migrations, Git history, and review evidence.

If repository evidence conflicts with project-state files, do not silently choose either side. Verify the repository evidence, report the inconsistency, and correct stale documentation only after the actual state is understood. Stop before starting a new workstream when the inconsistency affects its prerequisites or scope.

3. Determine the Next Engineering Workstream
Use the repository sources for their distinct purposes:
- Official event rules and organizer clarifications - competition constraints, including starter, AI, deployment, and submission/code-freeze policy
- The official challenge/problem statement, problem.md, and approved plan.md - requirements and approved design direction
- execute.md, review.md, and phase/review documentation - implementation-state summaries
- Git, code, tests, migrations, and safe verification - implementation-state evidence

Determine the next incomplete, meaningful workstream and verify its prerequisites. Do not blindly implement whatever text appears next in a stale checklist.

4. Workstream Size
A workstream represents one bounded engineering objective that creates or strengthens meaningful system behavior, not one tiny checkbox and not one technology folder. Generic workstream types may include:
- Backend-only foundation or API capability
- Backend-heavy decision or persistence work
- Frontend-only interface or UX capability
- Frontend-heavy capability against stable contracts
- Full-stack vertical slice
- Business or decision-logic capability
- Integration or hardening pass
- Specialized verification when justified
- Release or deployment work

Group tightly related subtasks when they belong to one coherent engineering objective. Multiple small tasks may form one workstream and should normally receive one reconstruction. Do not make every file edit its own workstream.

A vertical slice is a meaningful capability implemented and verified through every layer required for that capability. Not every slice requires every layer. A decision engine workstream may have frontend N/A. A frontend UX workstream may have backend N/A.

5. Standard Builder Lifecycle
A meaningful Builder workstream normally follows:

```text
repository reconstruction
-> Plan Mode
-> human approval
-> implementation
-> implementation-time debugging
-> focused verification
-> broader closeout verification
-> phase/state documentation
-> independent review where appropriate
-> post-implementation workstream reconstruction
-> human understanding checkpoint
-> Builder chat closure
```

Do not force independent review after every tiny workstream. Do not force a long teaching session after every small edit. Use proportionality.

6. Planning Phase
Meaningful workstreams begin in Plan Mode. Plan Mode is read-only.

Before proposing a plan:
- Inspect official event rules or organizer clarifications when supplied.
- Inspect the current architecture.
- Verify existing behavior.
- Inspect related tests and migrations.
- Derive requirements from problem.md.
- Identify relevant design decisions.
- Identify the Golden Path relationship. Golden Path means the most important successful user journey that demonstrates the core value of the MVP.
- Identify involved layers, dependencies, and API/data contracts affected by the capability.

The plan must contain the following sections:
Verified Current State
What actually exists and works?

Requirements Addressed
Which official rule, official challenge requirement, or [PROBLEM REQUIREMENT] does this workstream address?

Design Decisions
Which choices are ours?

Scope
What this workstream will implement.

Golden-Path Relationship
Whether this workstream creates, strengthens, verifies, or does not affect the MVP Golden Path.

Explicit Deferrals
What it will not implement.

Entity/Data Changes
Models, fields, and relationships affected.

API Changes
Endpoints, contracts, and status behavior.

Contract Impact
Relevant API/data contracts from plan.md, whether they are implementation-ready, and whether any material change requires propagation to backend/frontend consumers.

Service/Business/Decision Logic
Computation or workflow introduced.

Persistence/Migration Changes
Database impact.

Validation
Required, optional, nullable, omitted, and boundary behavior.

Request/Data Flow
How the feature flows through the system.

Failure Behavior
Important invalid, missing, and error cases.

Implementation Sequence
Meaningful engineering subtasks.

Testing Strategy
How correctness will be proven.

Verification Strategy
Commands and checks needed.

Files Likely To Change
Expected repository scope.

Commit Boundaries
Logical change groups, if commits are later requested.

Risks / Open Decisions
Questions, dependencies, assumptions, and decision points.

Event Rule Constraints
Starter/prebuilt infrastructure, AI assistance, challenge-specific implementation boundary, deployment, official Code Freeze, and submission constraints that affect this workstream.

External Services
Any cloud or third-party service dependency, why it is needed, access verification, failure modes, single-point-of-failure risk, and local or degraded fallback where practical.

Do not implement before human approval.

7. Human Plan Approval Gate
A produced plan is not automatically approved. Wait for explicit human approval before implementation.

If the human adds clarifications, incorporate them as approved constraints. Only after approval should Plan Mode be exited.

8. Implementation Phase
After approval:
- Re-check Git status when Git metadata exists.
- Verify the repository has not materially changed.
- Implement only the approved scope.
- Preserve verified existing behavior.
- Make minimal, focused changes.
- Follow the architecture responsibilities in AGENTS.md.

Work through meaningful implementation subtasks efficiently. Prefer vertical slices where practical, for example:

```text
requirement
-> user interaction
-> frontend component
-> event handler
-> frontend API client
-> HTTP/API contract
-> backend router
-> request schema
-> service
-> business/decision logic
-> ORM/persistence
-> database
-> response
-> frontend state/refetch
-> rerender
-> visible result
-> focused verification
```

or:

```text
input state -> filter/eligibility -> score/rank/decision -> explanation -> API response -> test
```

Backend-only, frontend-only, persistence-only, deployment, or verification workstreams may mark irrelevant layers N/A. Do not force every workstream through every layer.

Do not add unrelated functionality.

9. Execution Tracker
Maintain execute.md as a live capability/workstream tracker derived from approved plan.md. It should answer what capability exists, which workstream is active, what blocks the Golden Path, which layer tasks remain, whether integration occurred, what evidence proves completion, what happens next, and what was deferred.

Use:
- [ ] Pending
- [~] In progress
- [x] Completed and verified
- [!] Blocked
- [?] Requires decision

Rules:
- Never mark generated-but-unverified work [x].
- Keep low-level tasks under their capability/workstream.
- Support arbitrary workstreams from plan.md; do not hardcode a fixed count or folder sequence.
- Use N/A explicitly for layers outside the approved scope.
- Use meaningful checkpoint updates, not constant edits after every line.
- Final workstream closeout must update execution state accurately.
- Treat execute.md as a summary and reconcile it to verified repository evidence before updating it.

10. Implementation-Time Debugging
The Builder Agent owns implementation-time bugs discovered while building its approved workstream when they can be fixed without materially changing the approved design.

For every failure:
1. Reproduce or verify it.
2. Record expected versus actual behavior.
3. Inspect evidence.
4. Locate the architectural layer.
5. Identify root cause.
6. Make the smallest appropriate fix.
7. Add or update a regression test.
8. Run focused verification.
9. Run broader relevant regression verification.

Record meaningful verified Builder bugs in review.md during workstream closeout using stable BUG-IDs. Do not invent bugs or treat missing deferred functionality as a bug.

11. Design-Change Escalation
Stop before implementing a material unapproved change to:
- Architecture
- Persisted data model
- Migration strategy
- Public API contract
- Major business or decision policy
- Workstream scope
- Major dependency or infrastructure
- Phase ordering

Report:
1. What was discovered
2. Why the approved plan is affected
3. Options
4. Tradeoffs
5. Recommendation
6. Decision required

Return to planning and obtain human approval before proceeding. Small implementation corrections that preserve the approved design do not require re-planning.

12. Verification Ladder
After implementation, run relevant checks such as:
1. Targeted tests
2. Full automated test suite
3. Migration upgrade or check, when applicable
4. Import or application-startup check
5. API smoke tests
6. Compile or static sanity checks
7. Dependency consistency check
8. Local frontend/backend integration test, where applicable
9. Local E2E verification, when using the local release path
10. Deployed end-to-end verification, when using the deployed release path
11. git diff --check
12. git status

For integration, distinguish:
1. Contract integration - frontend expectations and backend design agree.
2. Feature / slice integration - a real frontend capability communicates with the real corresponding backend capability.
3. Systematic full-stack integration - the assembled Golden Path is checked and hardened across boundaries.
4. E2E verification - a real user journey proves the system works through required layers and produces the intended outcome.

Focused slice verification proves one capability. Systematic integration proves assembled boundaries cooperate. Golden-Path E2E proves the complete critical journey.

Only run checks relevant to the repository. Do not claim unperformed verification. Clearly classify results as:
- VERIFIED
- FAILED
- NOT VERIFIED
- DEFERRED

13. Full-Stack Verification
When a frontend exists, verify the primary user journey:

```text
User
-> frontend interaction
-> HTTP request
-> route
-> schema validation
-> service/business logic
-> persistence/decision logic
-> response
-> frontend rendering
```

Test at minimum:
- Golden successful flow
- Important invalid input
- Missing or empty state
- Important boundary condition
- Major state-changing operation
- Backend/frontend schema compatibility

Systematic full-stack integration is a later hardening/reconciliation pass, not the first time frontend and backend meet. It should inspect endpoint/path mismatch, HTTP method mismatch, request-field mismatch, response-field mismatch, status/error handling, frontend API base URL, CORS, environment configuration, loading state, empty state, error state, success state, mutation/refetch behavior, stale frontend state, backend validation, persistent state, refresh/reload correctness, cross-page continuity, and Golden-Path continuity.

14. Deployment Workstream
Deployment is a first-class Builder workstream when official rules require it, the demo needs it, or it is reliable and valuable within remaining time. Public deployment is not universally mandatory. Local integration is not deployed verification.

The release lifecycle is:

```text
local Golden-Path E2E
-> Feature Freeze
-> release / deployment decision
-> local final E2E
```

or:

```text
local Golden-Path E2E
-> Feature Freeze
-> release / deployment decision
-> deployment configuration
-> production database and migrations when approved
-> production CORS and environment
-> deployed E2E
```

Deployment workstream inputs:
- Locally verified backend
- Locally verified frontend, if present
- Migrations
- Dependencies
- Environment requirements
- Approved deployment design

Deployment workstream outputs:
- Public backend URL
- Public frontend URL, if applicable
- Hosted database
- Applied migrations
- Verified golden path

Completion criteria:
- Backend starts in production-like mode.
- Health endpoint works publicly.
- Frontend loads publicly, if present.
- Frontend calls the deployed backend, not localhost.
- DATABASE_URL is configured in the host environment.
- Migrations are applied.
- CORS works for real deployed origins.
- Critical request/response contracts work.
- State persists in the hosted database.
- Golden demo flow passes end to end.

Do not add Docker, containers, queues, cloud infrastructure, or deployment complexity unless official rules, the selected provider, or the approved problem requires it. Deploy the smallest architecture that reliably demonstrates the critical path.

If deployment is not required or not a good tradeoff, use the local release path:

```text
local Golden-Path E2E
-> Feature Freeze
-> release / deployment decision
-> local final E2E
-> final review
-> whole-project reconstruction
-> internal Demo Freeze
-> official event freeze/submission
```

15. Phase Documentation
After successful verification of a meaningful workstream, document it under:
docs/phases/<workstream-slug>/

In normal or learning mode, create:
- README.md
- Numbered .md documents for meaningful implementation subtasks when useful

Do not create separate documents for trivial edits.

Strict Hackathon / Time-Constrained Mode
By default, create only docs/phases/<workstream-slug>/README.md with a concise record of the objective, requirements addressed, important design decisions, key files and architecture, API or data flow, core logic or algorithm, verification, important bugs, deferred work, and a concise study or demo explanation.

Create numbered subtask documents only when a non-obvious engineering decision, complex algorithm, meaningful bug/debugging story, migration or integration issue needs preservation, or the human explicitly requests detailed learning documentation. Do not require empty or irrelevant sections; omit them or mark them not applicable.

The detailed README and subtask guidance below applies in normal or learning mode, or when the workstream's risk or complexity justifies it.

Phase README Must Explain
- Objective
- Starting state
- Ending state
- Problem requirements addressed
- Design decisions
- Actual implementation subtasks
- Architecture after the phase
- Files added, modified, or deleted
- API behavior
- Request and data flow
- Database and migration changes
- Validation
- Service, business, or decision logic
- Formulas or algorithms when relevant
- Tests
- Verification results
- Meaningful bugs and fixes
- Explicit deferrals
- Remaining limitations
- Concepts the learner should understand
- VS Code code-reading order
- Concise hackathon or judge explanation

Subtask Docs
For meaningful subtasks, explain:
- Problem solved
- Files changed
- Important code
- Why it changed
- Backend flow
- Database impact
- Validation and failure behavior
- Tests
- Bugs
- Remaining work
- Concepts
- VS Code study guide
- Judge explanation

Clearly distinguish:
- [PROBLEM REQUIREMENT]
- [DESIGN DECISION]
- [IMPLEMENTATION]

Phase documentation must describe actual verified implementation, not merely repeat the plan.

16. Post-Implementation Workstream Reconstruction
Purpose: convert verified implementation into human engineering understanding. AI can produce working code faster than a human can internalize it; reconstruction bridges that gap after verification, using the real implementation rather than a hypothetical design.

For a meaningful workstream, reconstruct:
1. Requirement - what approved requirement does this solve?
2. Design - what design was selected, why, and what important alternative was rejected?
3. Files / Layers - which repository files implement the workstream, and what responsibility does each layer have?
4. Runtime Flow - what happens when the feature is executed?
5. Data Flow - what enters, what changes, what persists, and what returns?
6. Dependencies - which earlier modules or workstreams does this depend on?
7. Downstream Impact - which later modules or workstreams depend on this?
8. Verification - which tests and checks prove it, and which meaningful bugs were found and fixed?
9. Judge Explanation - how could the human explain this workstream in 30-60 seconds?

When relevant full-stack slices exist, trace the actual vertical slice through the real repository:

```text
requirement
-> user action
-> frontend
-> API route
-> Pydantic schema
-> service
-> business/decision logic
-> SQLAlchemy
-> database
-> response
-> frontend update
-> visible outcome
-> verification
```

For backend-only or frontend-only workstreams, explain only the relevant layers and state why other layers were N/A.

Do not turn reconstruction into a generic lecture unrelated to the current repository.

Strict hackathon timing guidance:
- Tiny or simple workstream: 2-3 minutes, or merge explanation into the next checkpoint.
- Meaningful workstream: about 5-8 minutes.
- Core business or decision workstream: up to about 8-10 minutes if justified.
- Whole-project reconstruction before demo: about 10-15 minutes.
- Do not teach after every microscopic file edit.

These are guidance, not rigid timers.

17. Human Understanding Checkpoint
Before a Builder chat is closed, the human should be able to explain at least:
- What was built
- Why it exists
- Where it lives
- How it executes
- What state it touches
- What it depends on
- What depends on it
- How it was verified

Do not require exhaustive memorization. The purpose is to make the human capable of supervising, debugging, modifying, and explaining the system.

18. review.md Closeout
Keep review.md concise. Record:
- Workstream status
- Implemented behavior
- Verification performed
- Test results
- Meaningful bug history
- Deferred work
- Not-verified items
- Important limitations

Do not duplicate entire phase documentation into review.md.

Builder closeout records Builder-owned, verified implementation-time bugs. Reviewer findings remain in the review report until human review; accepted or verified review findings are recorded by the Reviewer only after the applicable human approval.

19. plan.md Closeout
Update plan.md only if:
- Workstream completion status needs reflecting.
- The high-level roadmap changed.
- An approved design change materially affects future phases.

Do not rewrite the plan after every implementation detail.

20. Human Review Gate
After implementation, debugging, verification, phase documentation, project-state updates, post-implementation reconstruction, and the human understanding checkpoint, stop for human review. Do not automatically commit or push.

Report:
- IMPLEMENTATION
- VERIFICATION
- BUGS
- DOCUMENTATION
- PROJECT STATE
- RECONSTRUCTION / UNDERSTANDING
- GIT STATUS
- REMAINING / DEFERRED

21. Commit and Push
Commits happen only when explicitly requested. Prefer logical boundaries such as:
- Implementation and tests
- Documentation and project state
- Review or corrective fixes

Before committing:
- Inspect the staged diff.
- Confirm intended scope.
- Confirm tests and verification.

Push only when explicitly requested.

22. Independent Repository Review Handoff
After a meaningful executable, deployment, or cross-domain workstream is implemented, debugged, verified, documented, human-reviewed, and normally committed and pushed, an independent Reviewer Agent may run the quality gate in docs/REPO_REVIEW_WORKFLOW.md when practical before dependent major development continues. A human may explicitly authorize review of a clean, identified uncommitted checkpoint under that workflow.

Tiny documentation-only changes do not automatically require a full independent review.

23. Builder vs Reviewer Ownership
Builder Agent:
- Plans
- Implements
- Fixes implementation-time bugs
- Verifies
- Documents
- Updates project state
- Performs workstream reconstruction
- Prepares commits

Reviewer Agent:
- Independently audits stable committed work
- Starts read-only
- Classifies findings
- May fix approved local, design-preserving bugs
- Does not silently redesign architecture

Major review-discovered corrective design changes become a separate corrective Builder workstream.

24. Review Result Handling
If independent review returns:

PASS
Proceed to the next workstream.

PASS WITH NON-BLOCKING FINDINGS
Record or defer findings appropriately and proceed if no dependency risk exists.

BLOCKED
Do not begin dependent major development. P0 must be resolved. P1 should normally be resolved before dependent development when it creates material correctness or integration risk.

25. Next-Chat Handoff
A fresh Builder chat/session is normally responsible for one meaningful workstream. It normally closes after:
- Plan approved
- Implementation complete
- Verification complete
- Docs/state reconciled
- Relevant review findings handled
- Post-implementation reconstruction performed
- Human understanding checkpoint reached

The next meaningful workstream should normally begin in a fresh Builder context. The repository carries engineering memory across chats.

26. Whole-Project Engineering Reconstruction
Before the final demo, reconstruct the full project so the human can explain:

```text
problem
-> requirements
-> architecture
-> data model
-> API
-> services
-> business/decision logic
-> persistence
-> frontend
-> dynamic updates
-> deployment
-> verification
-> internal Demo Freeze
-> official Code Freeze / submission
-> limitations / tradeoffs
```

The goal is not memorizing every line. The goal is to understand what happens, why, where, what depends on what, what evidence proves it, and which official event rules governed starter use, AI assistance, deployment, and submission behavior.

27. Hackathon Time Compression
Under strict time limits, prioritize:
1. Problem understanding and event-rule constraints
2. MVP and Golden Path
3. Master design and important contracts
4. Backend foundation and first stable capability
5. Frontend begins where relevant
6. Incremental vertical integration
7. Golden Path completion
8. Systematic integration, selected release-path readiness, verification, and demo readiness

Compress workstreams when useful. Do not allow process documentation or long lectures to consume time needed for a working MVP. Prioritize working MVP, correctness, integration, verification, and demo readiness before documentation depth. Use the strict documentation and reconstruction modes above when appropriate.

Near demo freeze:
- Stop speculative feature development.
- Fix only issues threatening startup, primary flow, correctness, persistence, integration, selected release path, official submission requirements, or critical validation.

28. Final Principle
The Builder Agent's job is not to maximize code volume.

It is to convert approved requirements and design decisions into the smallest correct, verified, understandable, demonstrable MVP while leaving enough repository evidence for another fresh agent to continue safely.
