# Execution Tracker

## Markers

- [ ] Pending
- [~] In progress
- [x] Completed and verified
- [!] Blocked by a known issue or bug
- [?] Requires clarification or an engineering/design decision

## Current Status

[?] Product-specific execution requires approved `problem.md` and `plan.md`.

No product entities, tables, APIs, business rules, decision logic, deployment behavior, or frontend functionality have been implemented.

## Workstream Status Summary

Actual workstreams must come from the approved `plan.md`. Keep this table compact and update it only when evidence changes.

| Workstream | Capability | Status | Golden Path | Blocker | Next |
| ---------- | ---------- | ------ | ----------- | ------- | ---- |
| WS-XX | TBD from approved `plan.md` | NOT STARTED | TBD | TBD | TBD |

## Workstream Template

Use this reusable template for each approved workstream. Keep useful low-level technical tasks, but nest them under the capability/workstream rather than replacing the capability with folder-based checklists.

## WS-XX - <Name>

Objective / capability:

Golden-Path relationship:

Dependencies:

Relevant contracts:

### Backend

- [ ] TBD

Or:

Backend: N/A

### Frontend

- [ ] TBD

Or:

Frontend: N/A

### Persistence

- [ ] TBD

Or:

Persistence: N/A

### Integration

- [ ] TBD

Or:

Integration: N/A

### Infrastructure

- [ ] TBD

Or:

Infrastructure: N/A

### Verification

- [ ] Focused tests
- [ ] API verification where applicable
- [ ] Real frontend/backend request where applicable
- [ ] Persistence verification where applicable
- [ ] Focused slice E2E where applicable
- [ ] `git diff --check`
- [ ] `git status`

Status:

Evidence:

Blocker:

Next step:

Deferrals:

## Tracker Questions

This file should answer quickly:

- What capability exists?
- What workstream is active?
- What blocks the Golden Path?
- Which layer tasks remain?
- Has integration occurred?
- What evidence proves completion?
- What happens next?
- What was deferred?

## Current Verified Foundation

- [x] Generic starter foundation created and verified.
- [x] Public template onboarding and workflow guides created and verified.
- [?] Product-specific planning pending approved `problem.md`.
- [ ] Product implementation pending approved `plan.md`.
