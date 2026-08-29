from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.errors import AppError
from backend.logic.money import format_paisa, parse_paisa
from backend.models import Account, Transfer
from backend.schemas.transfer import TransferRequest


def _sort_account_ids(id_a: uuid.UUID, id_b: uuid.UUID) -> tuple[uuid.UUID, uuid.UUID]:
    """Return account IDs in canonical ascending order for deadlock prevention."""
    if id_a.int <= id_b.int:
        return id_a, id_b
    return id_b, id_a


def execute_direct_transfer(
    db: Session,
    sender: Account,
    request: TransferRequest,
    idempotency_key: uuid.UUID,
) -> tuple[Transfer, bool]:
    """Execute a direct money transfer within the current session.

    Returns (transfer, is_new) where is_new is True for 201 and False for 200 replay.

    Steps:
    1. Parse amount
    2. Resolve recipient
    3. Reject self-transfer
    4. Check idempotency (before locking)
    5. Lock both accounts in canonical order
    6. Re-check idempotency after locks
    7. Check sender balance
    8. Debit sender, credit recipient
    9. Insert Transfer record
    10. Return (transfer, is_new)
    """
    # Step 1: Parse amount
    amount_paisa = parse_paisa(request.amount)

    # Step 2: Resolve recipient
    recipient = db.scalar(
        select(Account).where(Account.handle == request.recipient_handle)
    )
    if recipient is None:
        raise AppError(404, "RECIPIENT_NOT_FOUND", "The specified recipient account does not exist.")

    # Step 3: Reject self-transfer
    if sender.id == recipient.id:
        raise AppError(400, "SELF_TRANSFER", "Cannot transfer money to yourself.")

    # Step 4: Initial idempotency check (before locking)
    existing = db.scalar(
        select(Transfer).where(
            Transfer.sender_account_id == sender.id,
            Transfer.idempotency_key == idempotency_key,
        )
    )
    if existing is not None:
        # Verify it matches this exact operation
        if (
            existing.recipient_account_id == recipient.id
            and existing.amount_paisa == amount_paisa
            and existing.kind == "DIRECT"
        ):
            return existing, False  # 200 replay
        raise AppError(409, "IDEMPOTENCY_KEY_REUSED", "This idempotency key has been used for a different operation.")

    # Step 5: Sort both account UUIDs deterministically
    first_id, second_id = _sort_account_ids(sender.id, recipient.id)

    # Step 6: Acquire PostgreSQL row locks in canonical order using SELECT ... FOR UPDATE
    # populate_existing=True forces SQLAlchemy to refresh the identity-mapped instance
    # from the committed DB state after the lock is acquired, preventing stale reads.
    first_account: Account = db.scalar(
        select(Account).where(Account.id == first_id).with_for_update().execution_options(populate_existing=True)
    )
    second_account: Account = db.scalar(
        select(Account).where(Account.id == second_id).with_for_update().execution_options(populate_existing=True)
    )

    # Ensure we have the correct sender/recipient references after locking
    if first_id == sender.id:
        locked_sender = first_account
        locked_recipient = second_account
    else:
        locked_sender = second_account
        locked_recipient = first_account

    # Step 7: Re-check idempotency AFTER locks
    existing_after_lock = db.scalar(
        select(Transfer).where(
            Transfer.sender_account_id == sender.id,
            Transfer.idempotency_key == idempotency_key,
        )
    )
    if existing_after_lock is not None:
        if (
            existing_after_lock.recipient_account_id == recipient.id
            and existing_after_lock.amount_paisa == amount_paisa
            and existing_after_lock.kind == "DIRECT"
        ):
            return existing_after_lock, False  # 200 replay
        raise AppError(409, "IDEMPOTENCY_KEY_REUSED", "This idempotency key has been used for a different operation.")

    # Step 8: Check sufficient funds
    if locked_sender.balance_paisa < amount_paisa:
        raise AppError(409, "INSUFFICIENT_FUNDS", "The sender has insufficient funds.")

    # Step 9: Debit sender, credit recipient
    locked_sender.balance_paisa -= amount_paisa
    locked_recipient.balance_paisa += amount_paisa

    # Step 10: Insert immutable Transfer record
    transfer = Transfer(
        sender_account_id=sender.id,
        recipient_account_id=recipient.id,
        amount_paisa=amount_paisa,
        idempotency_key=idempotency_key,
        kind="DIRECT",
    )
    db.add(transfer)

    try:
        db.flush()
    except IntegrityError as exc:
        db.rollback()
        raise AppError(
            409,
            "TRANSFER_CONFLICT",
            "A transfer conflict occurred. Please retry with a different idempotency key.",
        ) from exc

    return transfer, True
