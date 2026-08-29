# Problem Definition

## Status

[x] Approved Money Movement Application problem definition.

## Source And Classification

This file records the approved normalized WHAT from the GPT Control Room for the Money Movement Application MVP.

- [PROBLEM REQUIREMENT] The application must support simulated money movement between valid application users.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] Backend authority must protect balance correctness, request correctness, retry safety, and concurrent state changes because the product changes financial-like simulated state.
- [MVP DECISION] The MVP/demo uses fake BDT balances only, including an initial simulated BDT 100,000 balance for newly created users.
- [DEFERRED FEATURE] Real banks, cards, payment gateways, and real financial integrations are outside the MVP.

No implementation design is approved in this file.

## Objective

Build a user-facing Money Movement Application MVP where registered users can view a simulated BDT balance, send simulated money to another valid user, request simulated money from another valid user, and fulfill valid pending requests while preserving persistent and correct balances.

The product must demonstrate money movement behavior using simulated/fake money only.

## Actors / Users

- [PROBLEM REQUIREMENT] Application user: a person with an application account who can hold a simulated balance.
- [PROBLEM REQUIREMENT] Sender: a valid user who sends simulated money to another valid user.
- [PROBLEM REQUIREMENT] Recipient: a valid user who receives simulated money from another valid user.
- [PROBLEM REQUIREMENT] Requester: a valid user who requests simulated money from another valid user.
- [PROBLEM REQUIREMENT] Requested payer: a valid user who can see and fulfill a pending request addressed to them.

## Core Workflows

### Account Registration

- [PROBLEM REQUIREMENT] Users can register or create an application account.
- [MVP DECISION] For MVP/demo use, each newly created user receives an initial simulated BDT 100,000 balance.

### Balance Viewing

- [PROBLEM REQUIREMENT] A user can view their current simulated balance.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] The displayed/read balance must reflect the persisted balance after completed money movements.

### Send Money

- [PROBLEM REQUIREMENT] A user can send money to another valid user.
- [PROBLEM REQUIREMENT] A successful send moves the requested amount from the sender to the recipient.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] A send must be rejected when the users are invalid, the amount is invalid, or the sender has insufficient funds.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] A send must succeed exactly once under duplicate or retry conditions.

### Request Money

- [PROBLEM REQUIREMENT] A user can request money from another valid user.
- [PROBLEM REQUIREMENT] Creating a request makes the request pending and does not move money.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] A request must be rejected when the users are invalid or the amount is invalid.

### Fulfill Request

- [PROBLEM REQUIREMENT] The requested payer can see and fulfill a valid pending request.
- [PROBLEM REQUIREMENT] Fulfilling a request performs the corresponding money movement from the requested payer to the requester.
- [PROBLEM REQUIREMENT] A fulfilled request becomes completed.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] A request can be fulfilled only from a valid pending state.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] Fulfilling a request must be rejected when the payer has insufficient funds.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] Fulfillment must succeed exactly once under duplicate or retry conditions.

## Frontend Requirements

- [PROBLEM REQUIREMENT] Provide a user-facing interface for registration/account creation.
- [PROBLEM REQUIREMENT] Provide a user-facing interface for viewing the current simulated balance.
- [PROBLEM REQUIREMENT] Provide a user-facing interface for sending simulated money to another valid user.
- [PROBLEM REQUIREMENT] Provide a user-facing interface for requesting simulated money from another valid user.
- [PROBLEM REQUIREMENT] Provide a user-facing interface for the requested payer to see pending requests.
- [PROBLEM REQUIREMENT] Provide a user-facing interface for fulfilling a valid pending request.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] The interface must communicate important rejected operations without implying money moved when it did not.

## Backend Requirements

- [PROBLEM REQUIREMENT] The backend must be the authority for money movement and request state changes.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] The backend must validate users and amounts for sends, requests, and fulfillments.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] The backend must enforce sufficient funds before any operation that moves money.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] The backend must ensure money movement is atomic: both affected balances change together, or neither balance changes.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] The backend must protect request state transitions so invalid transitions cannot complete money movement.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] The backend must reject invalid or duplicate operations without corrupting balances or request state.

## Persistence Requirements

- [PROBLEM REQUIREMENT] User account state must persist.
- [PROBLEM REQUIREMENT] Simulated balances must persist.
- [PROBLEM REQUIREMENT] Money request state must persist.
- [PROBLEM REQUIREMENT] Balances and request status must remain persistent and correct after read-back or refresh.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] Persisted state must remain internally consistent after accepted, rejected, duplicate, or retried state-changing operations.

## Business Rules / Invariants

- [PROBLEM REQUIREMENT] All money is simulated/fake money only.
- [MVP DECISION] New users start with simulated BDT 100,000 for MVP/demo use.
- [PROBLEM REQUIREMENT] Money may move only between valid application users.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] Money movement must preserve total simulated value except for the MVP-approved initial balance grant on account creation.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] Amounts must be valid before any request or transfer is accepted.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] A user's balance must not be reduced below zero by an accepted money movement.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] A pending request does not move money.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] A completed request must not be fulfilled again.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] Rejected operations must not partially change balances or request status.

## Reliability / Concurrency Expectations

- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] Concurrent sends, request fulfillments, duplicate submissions, or retries must not double-spend a balance.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] Concurrent or repeated fulfillment attempts for the same request must complete at most once.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] Read-back after successful or rejected operations must show the correct persisted state.

## Scalability Consideration

- [PROBLEM REQUIREMENT] The application should be explainable and credible for a hackathon MVP involving multiple users and repeated money movements.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] Correctness under multiple users, repeated operations, and concurrent attempts matters more than speculative scale features.
- [DEFERRED FEATURE] Large-scale financial infrastructure, distributed systems, and real payment-network integrations are outside the MVP unless separately approved later.

## Assumptions

- [MVP DECISION] The currency label for simulated balances is BDT.
- [MVP DECISION] The initial BDT 100,000 balance is a demo seed for newly created users, not real money and not a real deposit.
- [MVP DECISION] The product is intended for demonstration of account, balance, send, request, fulfill, persistence, and correctness behavior.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] Users must have a reliable way to identify the target valid user for sends and requests.

## Explicit Deferrals

- [DEFERRED FEATURE] No real banks.
- [DEFERRED FEATURE] No real cards.
- [DEFERRED FEATURE] No payment gateways.
- [DEFERRED FEATURE] No real financial integrations.
- [DEFERRED FEATURE] No real money custody, deposits, withdrawals, settlement, KYC, card issuing, bank linking, or regulatory payment processing.
- [DEFERRED FEATURE] No implementation design or infrastructure design is decided in this file.

## MVP Boundary

The MVP includes:

- [PROBLEM REQUIREMENT] User registration/account creation.
- [MVP DECISION] Initial simulated BDT 100,000 balance for newly created users.
- [PROBLEM REQUIREMENT] Current simulated balance viewing.
- [PROBLEM REQUIREMENT] Sending simulated money to another valid user.
- [PROBLEM REQUIREMENT] Requesting simulated money from another valid user.
- [PROBLEM REQUIREMENT] Viewing and fulfilling valid pending requests addressed to the payer.
- [PROBLEM REQUIREMENT] Persistent, correct balances and request statuses.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] Backend-enforced validation, atomicity, concurrency integrity, duplicate/retry safety, and valid request state transitions.

The MVP excludes all real-money and real-financial-integration behavior.

## Golden Path Summary

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

## Acceptance Criteria

- [PROBLEM REQUIREMENT] A user can register/create an application account.
- [MVP DECISION] A newly created user receives an initial simulated BDT 100,000 balance for MVP/demo use.
- [PROBLEM REQUIREMENT] A user can view their current simulated balance.
- [PROBLEM REQUIREMENT] A user can send money to another valid user.
- [PROBLEM REQUIREMENT] A user can request money from another valid user.
- [PROBLEM REQUIREMENT] The requested payer can see and fulfill a valid pending request.
- [PROBLEM REQUIREMENT] Fulfilling a request performs the corresponding simulated money movement.
- [PROBLEM REQUIREMENT] Balances and request status persist correctly after read-back or refresh.
- [LOGICALLY INFERRED CORRECTNESS REQUIREMENT] Invalid users, invalid amounts, insufficient funds, invalid request states, duplicate operations, retry attempts, and relevant concurrent attempts are rejected or handled without corrupting balances or request state.
- [PROBLEM REQUIREMENT] The Golden Path completes with the expected balances and request status.
- [PROBLEM REQUIREMENT] At least one important invalid or duplicate operation is rejected without corrupting financial state.
- [DEFERRED FEATURE] The product does not use or imply real banks, cards, payment gateways, or real financial integrations in the MVP.
