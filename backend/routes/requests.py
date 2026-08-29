from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Header, Query, Response, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.dependencies import get_current_account
from backend.errors import AppError
from backend.logic.money import format_paisa
from backend.models import Account
from backend.schemas.request import (
    CreateRequestRequest,
    CreateRequestResponse,
    FulfillResponse,
    IncomingRequestsResponse,
)
from backend.services.accounts import public_user
from backend.services.requests import (
    create_money_request,
    fulfill_money_request,
    list_incoming_pending_requests,
)

router = APIRouter(prefix="/api/requests", tags=["requests"])


@router.post("", response_model=CreateRequestResponse, status_code=status.HTTP_201_CREATED)
def create_request(
    request: CreateRequestRequest,
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

    money_request, is_new = create_money_request(db, account, request, key)

    if is_new:
        db.commit()

    db.refresh(money_request)

    # Fetch payer for response
    from backend.models import Account as AccountModel
    payer = db.get(AccountModel, money_request.payer_account_id)
    requester = db.get(AccountModel, money_request.requester_account_id)

    response.status_code = status.HTTP_201_CREATED if is_new else status.HTTP_200_OK

    return {
        "request": {
            "id": str(money_request.id),
            "requester": public_user(requester),
            "payer": public_user(payer),
            "amount": format_paisa(money_request.amount_paisa),
            "state": money_request.state,
            "created_at": money_request.created_at.isoformat(),
        }
    }


@router.get("/incoming", response_model=IncomingRequestsResponse)
def get_incoming_requests(
    status_filter: str | None = Query(None, alias="status"),
    account: Account = Depends(get_current_account),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    if status_filter is not None and status_filter.lower() != "pending":
        raise AppError(422, "INVALID_STATUS_FILTER", "Only 'pending' status is supported.")

    requests = list_incoming_pending_requests(db, account)

    # Enrich with account details
    from backend.models import Account as AccountModel
    result = []
    for mr in requests:
        requester = db.get(AccountModel, mr.requester_account_id)
        payer = db.get(AccountModel, mr.payer_account_id)
        result.append({
            "id": str(mr.id),
            "requester": public_user(requester),
            "payer": public_user(payer),
            "amount": format_paisa(mr.amount_paisa),
            "state": mr.state,
            "created_at": mr.created_at.isoformat(),
        })

    return {"requests": result}


@router.post("/{request_id}/fulfill", response_model=FulfillResponse)
def fulfill_request(
    request_id: uuid.UUID,
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

    money_request, transfer, is_new = fulfill_money_request(db, account, request_id, key)

    if is_new:
        db.commit()

    db.refresh(money_request)
    db.refresh(transfer)

    # Fetch accounts for response
    from backend.models import Account as AccountModel
    requester = db.get(AccountModel, money_request.requester_account_id)
    payer = db.get(AccountModel, money_request.payer_account_id)

    response.status_code = status.HTTP_201_CREATED if is_new else status.HTTP_200_OK

    return {
        "request": {
            "id": str(money_request.id),
            "requester": public_user(requester),
            "payer": public_user(payer),
            "amount": format_paisa(money_request.amount_paisa),
            "state": money_request.state,
            "created_at": money_request.created_at.isoformat(),
        },
        "transfer": {
            "id": str(transfer.id),
            "amount": format_paisa(transfer.amount_paisa),
            "kind": transfer.kind,
            "created_at": transfer.created_at.isoformat(),
        },
    }
