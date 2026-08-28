# Full-Stack Guide

The template does not choose a frontend framework. Choose the smallest UI stack that matches official event rules, the approved problem, team skills, and available time.

## Contract-First Integration

Master System Design should identify the important API/data contracts needed by the MVP and Golden Path before implementation starts. Workstreams may stabilize or refine the relevant contract details, but material contract changes must be propagated to both backend and frontend consumers.

Backend-first does not mean backend-complete-first. Establish domain foundations, persistence, major invariants, critical backend capabilities, and sufficiently stable API/data contracts; then frontend work may begin where relevant once the needed contract/capability is stable enough.

Define the API request and response contracts before connecting the interface. Backend routes, Pydantic contracts, services, and logic remain the source of backend behavior; the frontend should not duplicate core business or decision logic.

```text
User
  -> Frontend
  -> Fetch / API Client
  -> FastAPI Route
  -> Pydantic
  -> Service
  -> Logic
  -> SQLAlchemy
  -> Database
  -> Response
  -> Frontend Rendering
```

Configure backend URLs through environment-aware frontend configuration when appropriate. Do not hardcode deployment-specific URLs or credentials into a public client.

## Integration Levels

Use progressively stronger evidence:

1. Level 1 - Contract integration: frontend expectations and backend design agree.
2. Level 2 - Feature / slice integration: a real frontend capability communicates with the real corresponding backend capability.
3. Level 3 - Systematic full-stack integration: the assembled Golden Path is checked and hardened across boundaries.
4. Level 4 - E2E verification: a real user journey proves the system works through required layers and produces the intended outcome.

Focused slice verification proves one capability. Systematic integration proves assembled boundaries cooperate. Golden-Path E2E proves the complete critical user journey. Heavyweight browser automation is not mandatory by default; manual E2E can be acceptable under time constraints when evidence is clear.

## Minimum UI States

For each real interaction, design and verify:

- Loading
- Successful result
- Request or server error
- Validation feedback
- Empty or unavailable state

## Local vs Deployed Full-Stack Integration

Local integration proves the system works across local services:

```text
LOCAL:
browser
-> frontend dev server
-> local backend
-> local/test DB
```

Deployed integration proves the public demo path works across hosted services:

```text
DEPLOYED:
browser
-> hosted frontend
-> production API base URL
-> hosted FastAPI
-> hosted PostgreSQL
```

When deployment is officially required, necessary for the demo, or reliable and valuable within remaining time, verify both. Local success does not prove deployed success. When deployment is not required or not a good tradeoff, reliable local E2E/final verification remains a valid release path.

Deployment-specific integration should cover:
- `API_BASE_URL` or equivalent environment configuration.
- No hard-coded localhost dependency in production frontend code.
- CORS for the real deployed frontend origin.
- HTTPS origin and protocol differences.
- Public backend health.
- Hosted persistence.
- Production error behavior.
- Deployed contract testing.
- Deployment-specific integration failures such as missing environment variables, unapplied migrations, blocked cross-origin requests, wrong route prefixes, or frontend builds pointing at local services.

If external, cloud, or third-party services are part of the full-stack path, justify why they are needed, verify credentials/access before relying on them, understand failure modes, avoid unnecessary single points of failure, and preserve a local or degraded fallback where practical.

## Integration Checklist

- [ ] Release path is explicit: local E2E or deployed E2E.
- [ ] Golden Path is identified before implementation and still matches approved scope.
- [ ] Important MVP contracts are recorded in `plan.md`.
- [ ] Frontend API base URL is the production URL when deployed.
- [ ] Endpoint path matches.
- [ ] HTTP method matches.
- [ ] Request fields and types match.
- [ ] Response structure matches.
- [ ] Status codes are handled.
- [ ] Error format is handled.
- [ ] CORS works.
- [ ] No localhost dependency remains in deployed code.
- [ ] Hosted DB persists state.
- [ ] Local golden request tested when using the local release path.
- [ ] Deployed golden request tested when using the deployed release path.

## Workstreams and Review

A frontend Builder workstream should first inspect the approved problem, plan, API contracts, and current backend behavior. It plans UI scope and states, receives human approval, then implements and verifies the interface. It does not need to wait for every backend workstream to finish when the relevant contract is stable enough.

A full-stack vertical slice verifies the actual path from user input through backend behavior and back to rendering for that capability. A later systematic full-stack integration workstream is a hardening/reconciliation pass across the assembled Golden Path; it should inspect endpoint/path mismatch, HTTP method mismatch, request-field mismatch, response-field mismatch, status/error handling, frontend API base URL, CORS, environment configuration, loading state, empty state, error state, success state, mutation/refetch behavior, stale frontend state, backend validation, persistent state, refresh/reload correctness, cross-page continuity, and Golden-Path continuity.

If deployment is officially required, necessary for the demo, or reliable and valuable within remaining time, the deployment decision follows local Golden-Path E2E and Feature Freeze. The release path is then either local final verification or deployment plus deployed E2E, covering hosted services, environment variables, migrations, production API URL, and CORS when deployment is selected.

An independent Reviewer checks contract compatibility, loading/error/empty behavior, stale state risks, accidental duplication of backend decision logic, and deployed integration evidence when deployment is in scope. It does not invent a framework or redesign the product without approval.

## Demo-First UI Priorities

1. Main input or action
2. Current system state
3. Core decision or output
4. Explanation
5. Error and recovery
6. Deployed access, when the demo is remote
7. Polish

Protect the first six before spending time on visual refinement.
