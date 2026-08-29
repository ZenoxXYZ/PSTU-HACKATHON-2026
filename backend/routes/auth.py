from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.dependencies import get_current_account
from backend.logic.money import format_paisa
from backend.models import Account
from backend.schemas.account import CurrentAccountResponse, RegisterAccountRequest, RegisterAccountResponse
from backend.services.accounts import public_user, register_account

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=RegisterAccountResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterAccountRequest, db: Session = Depends(get_db)) -> dict[str, object]:
    account, raw_token = register_account(db, request)
    return {
        "access_token": raw_token,
        "token_type": "bearer",
        "user": public_user(account),
        "balance": format_paisa(account.balance_paisa),
    }


@router.get("/me", response_model=CurrentAccountResponse)
def me(account: Account = Depends(get_current_account)) -> dict[str, object]:
    return {
        "user": public_user(account),
        "balance": format_paisa(account.balance_paisa),
    }
