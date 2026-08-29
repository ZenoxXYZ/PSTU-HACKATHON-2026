from __future__ import annotations

from pydantic import BaseModel, field_validator

from backend.logic.validation import validate_display_name, validate_handle


class RegisterAccountRequest(BaseModel):
    handle: str
    display_name: str

    @field_validator("handle")
    @classmethod
    def validate_handle_field(cls, value: str) -> str:
        return validate_handle(value)

    @field_validator("display_name")
    @classmethod
    def validate_display_name_field(cls, value: str) -> str:
        return validate_display_name(value)


class PublicUser(BaseModel):
    handle: str
    display_name: str


class RegisterAccountResponse(BaseModel):
    access_token: str
    token_type: str
    user: PublicUser
    balance: str


class CurrentAccountResponse(BaseModel):
    user: PublicUser
    balance: str


class UserSearchResponse(BaseModel):
    users: list[PublicUser]
