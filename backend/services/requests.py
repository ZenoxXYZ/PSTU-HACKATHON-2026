from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.errors import AppError
from backend.logic.money import parse_paisa
from backend.models import Account, MoneyRequest, Transfer
from backend.schemas.request import CreateRequestRequest


def create_money_request(
    db: Session,
    requester: Account,
    request: CreateRequestRequest,
    creation_idempotency_key: uuid.UUID,
) -> tuple[MoneyRequest, bool]:
    """Create a pending money request. Moves no money.

    Returns (request, is_new) where is_new is True for 201 and False for 200 replay.
    """
    # Parse amount
    amount_paisa = parse_paisa(request.amount)

    # Resolve payer
    payer = db.scalar(
        select(Account).where(Account.handle == request.payer_handle)
    )
    if payer is None:
        raise AppError(404, "PAYER_NOT_FOUND", "The specified payer account does not exist.")

    # Reject self-request
    if requester.id == payer.id:
        raise AppError(400, "SELF_REQUEST", "Cannot request money from yourself.")

    # Initial idempotency check (before locking)
    existing = db.scalar(
        select(MoneyRequest).where(
            MoneyRequest.requester_account_id == requester.id,
            MoneyRequest.creation_idempotency_key == creation_idempotency_key,
        )
    )
    if existing is not None:
        if (
            existing.payer_account_id == payer.id
            and existing.amount_paisa == amount_paisa
        ):
            return existing, False  # 200 replay
        raise AppError(409, "IDEMPOTENCY_KEY_REUSED", "This idempotency key has been used for a different operation.")

    # Insert the request
    money_request = MoneyRequest(
        requester_account_id=requester.id,
        payer_account_id=payer.id,
        amount_paisa=amount_paisa,
        state="PENDING",
        creation_idempotency_key=creation_idempotency_key,
    )
    db.add(money_request)

    try:
        db.flush()
    except Exception as exc:
        db.rollback()
        raise AppError(
            409,
            "REQUEST_CONFLICT",
            "A request conflict occurred. Please retry with a different idempotency key.",
        ) from exc

    return money_request, True


def list_incoming_pending_requests(
    db: Session,
    payer: Account,
) -> list[MoneyRequest]:
    """List pending requests addressed to the current actor."""
    stmt = (
        select(MoneyRequest)
        .where(
            MoneyRequest.payer_account_id == payer.id,
            MoneyRequest.state == "PENDING",
        )
        .order_by(MoneyRequest.created_at.asc())
    )
    return list(db.scalars(stmt))


def fulfill_money_request(
    db: Session,
    payer: Account,
    request_id: uuid.UUID,
    idempotency_key: uuid.UUID,
) -> tuple[MoneyRequest, Transfer, bool]:
    """Fulfill a pending money request atomically.

    The fulfillment commits exactly once after:
    payer debit + requester credit + fulfillment Transfer + request COMPLETED.

    Returns (request, transfer, is_new) where is_new is True for 201 and False for 200 replay.
    """
    # Resolve the request
    money_request = db.get(MoneyRequest, request_id)
    if money_request is None:
        raise AppError(404, "REQUEST_NOT_FOUND", "The specified money request does not exist.")

    # Reject non-payer
    if money_request.payer_account_id != payer.id:
        raise AppError(403, "NOT_DESIGNATED_PAYER", "Only the designated payer may fulfill this request.")

    # Check fulfillment idempotency (before locking request)
    existing_transfer = db.scalar(
        select(Transfer).where(
            Transfer.sender_account_id == payer.id,
            Transfer.idempotency_key == idempotency_key,
        )
    )
    if existing_transfer is not None:
        if existing_transfer.linked_request_id == money_request.id:
            return money_request, existing_transfer, False  # 200 replay
        raise AppError(409, "IDEMPOTENCY_KEY_REUSED", "This idempotency key has been used for a different operation.")

    # Lock request FOR UPDATE
    # populate_existing=True forces SQLAlchemy to refresh the identity-mapped instance
    # from the committed DB state after the lock is acquired, preventing stale reads.
    locked_request: MoneyRequest = db.scalar(
        select(MoneyRequest).where(MoneyRequest.id == request_id).with_for_update().execution_options(populate_existing=True)
    )

    # Re-check fulfillment idempotency after request lock
    existing_transfer_after_lock = db.scalar(
        select(Transfer).where(
            Transfer.sender_account_id == payer.id,
            Transfer.idempotency_key == idempotency_key,
        )
    )
    if existing_transfer_after_lock is not None:
        if existing_transfer_after_lock.linked_request_id == locked_request.id:
            return locked_request, existing_transfer_after_lock, False  # 200 replay
        raise AppError(409, "IDEMPOTENCY_KEY_REUSED", "This idempotency key has been used for a different operation.")

    # Check request state
    if locked_request.state == "COMPLETED":
        raise AppError(409, "REQUEST_ALREADY_COMPLETED", "This money request has already been fulfilled.")

    # Verify sender is designated payer
    if locked_request.payer_account_id != payer.id:
        raise AppError(403, "NOT_DESIGNATED_PAYER", "Only the designated payer may fulfill this request.")

    # Resolve both accounts
    payer_account = db.get(Account, locked_request.payer_account_id)
    requester_account = db.get(Account, locked_request.requester_account_id)

    # Sort account IDs for deadlock prevention
    first_id, second_id = _sort_account_ids(payer_account.id, requester_account.id)

    # Lock both accounts in canonical order
    # populate_existing=True forces SQLAlchemy to refresh identity-mapped instances
    # from the committed DB state after locks are acquired, preventing stale reads.
    first_account: Account = db.scalar(
        select(Account).where(Account.id == first_id).with_for_update().execution_options(populate_existing=True)
    )
    second_account: Account = db.scalar(
        select(Account).where(Account.id == second_id).with_for_update().execution_options(populate_existing=True)
    )

    # Re-check idempotency after acquiring all locks
    existing_transfer_final = db.scalar(
        select(Transfer).where(
            Transfer.sender_account_id == payer.id,
            Transfer.idempotency_key == idempotency_key,
        )
    )
    if existing_transfer_final is not None:
        if existing_transfer_final.linked_request_id == locked_request.id:
            return locked_request, existing_transfer_final, False  # 200 replay
        raise AppError(409, "IDEMPOTENCY_KEY_REUSED", "This idempotency key has been used for a different operation.")

    # Determine locked payer/requester references
    if first_id == payer.id:
        locked_payer = first_account
        locked_requester = second_account
    else:
        locked_payer = second_account
        locked_requester = first_account

    # Check sufficient funds
    if locked_payer.balance_paisa < locked_request.amount_paisa:
        raise AppError(409, "INSUFFICIENT_FUNDS", "The payer has insufficient funds.")

    # Debit payer, credit requester
    locked_payer.balance_paisa -= locked_request.amount_paisa
    locked_requester.balance_paisa += locked_request.amount_paisa

    # Insert fulfillment Transfer record
    transfer = Transfer(
        sender_account_id=payer.id,
        recipient_account_id=locked_request.requester_account_id,
        amount_paisa=locked_request.amount_paisa,
        idempotency_key=idempotency_key,
        kind="REQUEST_FULFILLMENT",
        linked_request_id=locked_request.id,
    )
    db.add(transfer)

    # Mark request as COMPLETED
    locked_request.state = "COMPLETED"
    from datetime import datetime, timezone
    locked_request.completed_at = datetime.now(timezone.utc)

    try:
        db.flush()
    except Exception as exc:
        db.rollback()
        raise AppError(
            409,
            "FULFILLMENT_CONFLICT",
            "A fulfillment conflict occurred. Please retry with a different idempotency key.",
        ) from exc

    return locked_request, transfer, True


def _sort_account_ids(id_a: uuid.UUID, id_b: uuid.UUID) -> tuple[uuid.UUID, uuid.UUID]:
    """Return account IDs in canonical ascending order for deadlock prevention."""
    if id_a.int <= id_b.int:
        return id_a, id_b
    return id_b, id_a
