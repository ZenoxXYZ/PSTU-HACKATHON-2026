from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Header, Response, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.dependencies import get_current_account
from backend.errors import AppError
from backend.logic.money import format_paisa
from backend.models import Account
from backend.schemas.transfer import TransferRequest, TransferResponse
from backend.services.transfers import execute_direct_transfer

router = APIRouter(prefix="/api/transfers", tags=["transfers"])


@router.post("", response_model=TransferResponse)
def create_transfer(
    request: TransferRequest,
    response: Response,
    idempotency_key: Annotated[str | None, Header()] = None,
    account: Account = Depends(get_current_account),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    # Validate idempotency key
    if idempotency_key is None or not idempotency_key.strip():
        raise AppError(422, "IDEMPOTENCY_KEY_REQUIRED", "An Idempotency-Key header is required.")

    try:
        key = uuid.UUID(idempotency_key.strip())
    except ValueError:
        raise AppError(422, "INVALID_IDEMPOTENCY_KEY", "The Idempotency-Key must be a valid UUID.")

    transfer, is_new = execute_direct_transfer(db, account, request, key)

    if is_new:
        db.commit()
    # For replay (is_new=False), the transfer was found but no mutation occurred.
    # No commit needed; session remains clean.

    db.refresh(transfer)

    # Fetch recipient for response
    from backend.services.accounts import public_user
    from backend.models import Account as AccountModel

    recipient = db.get(AccountModel, transfer.recipient_account_id)

    response.status_code = status.HTTP_201_CREATED if is_new else status.HTTP_200_OK

    return {
        "transfer": {
            "id": str(transfer.id),
            "recipient": public_user(recipient),
            "amount": format_paisa(transfer.amount_paisa),
            "kind": transfer.kind,
            "created_at": transfer.created_at.isoformat(),
        }
    }
