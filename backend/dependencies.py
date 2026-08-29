from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Header
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.errors import AppError
from backend.models import Account
from backend.services.accounts import find_account_by_raw_token


def get_current_account(
    authorization: Annotated[str | None, Header()] = None,
    db: Session = Depends(get_db),
) -> Account:
    if authorization is None:
        raise AppError(401, "AUTHENTICATION_REQUIRED", "Bearer authentication is required.")

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token.strip():
        raise AppError(401, "AUTHENTICATION_REQUIRED", "Bearer authentication is required.")

    account = find_account_by_raw_token(db, token.strip())
    if account is None:
        raise AppError(401, "INVALID_ACCESS_TOKEN", "The supplied access token is invalid.")
    return account
