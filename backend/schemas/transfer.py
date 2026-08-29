from __future__ import annotations

from pydantic import BaseModel, field_validator

from backend.logic.money import parse_paisa


class TransferRequest(BaseModel):
    recipient_handle: str
    amount: str

    @field_validator("recipient_handle")
    @classmethod
    def validate_recipient_handle(cls, value: str) -> str:
        handle = value.strip().lower()
        if not handle:
            raise ValueError("Recipient handle must not be empty.")
        return handle

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, value: str) -> str:
        # Parse to validate; the service will also parse.
        parse_paisa(value)
        return value.strip()


class PublicRecipient(BaseModel):
    handle: str
    display_name: str


class TransferSummary(BaseModel):
    id: str
    recipient: PublicRecipient
    amount: str
    kind: str
    created_at: str


class TransferResponse(BaseModel):
    transfer: TransferSummary
