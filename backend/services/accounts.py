from __future__ import annotations

import hashlib
import secrets

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.errors import AppError
from backend.logic.money import INITIAL_BALANCE_PAISA
from backend.logic.validation import validate_search_fragment
from backend.models import Account
from backend.schemas.account import RegisterAccountRequest


def token_hash(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


def public_user(account: Account) -> dict[str, str]:
    return {"handle": account.handle, "display_name": account.display_name}


def register_account(db: Session, request: RegisterAccountRequest) -> tuple[Account, str]:
    raw_token = secrets.token_urlsafe(32)
    account = Account(
        handle=request.handle,
        display_name=request.display_name,
        balance_paisa=INITIAL_BALANCE_PAISA,
        token_hash=token_hash(raw_token),
    )

    db.add(account)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise AppError(409, "HANDLE_ALREADY_EXISTS", "An account with this handle already exists.") from exc

    db.refresh(account)
    return account, raw_token


def find_account_by_raw_token(db: Session, raw_token: str) -> Account | None:
    stmt = select(Account).where(Account.token_hash == token_hash(raw_token))
    return db.scalar(stmt)


def search_public_users(db: Session, actor: Account, query: str) -> list[Account]:
    fragment = validate_search_fragment(query)
    stmt = (
        select(Account)
        .where(Account.handle.like(f"{fragment}%"), Account.id != actor.id)
        .order_by(Account.handle.asc())
        .limit(20)
    )
    return list(db.scalars(stmt))
