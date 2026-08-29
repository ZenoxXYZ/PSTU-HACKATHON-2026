from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.dependencies import get_current_account
from backend.models import Account
from backend.schemas.account import UserSearchResponse
from backend.services.accounts import public_user, search_public_users

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("", response_model=UserSearchResponse)
def search_users(
    query: str = Query(...),
    account: Account = Depends(get_current_account),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    try:
        users = search_public_users(db, account, query)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"users": [public_user(user) for user in users]}
