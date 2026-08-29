from __future__ import annotations

from pydantic import BaseModel, field_validator

from backend.logic.money import parse_paisa


class CreateRequestRequest(BaseModel):
    payer_handle: str
    amount: str

    @field_validator("payer_handle")
    @classmethod
    def validate_payer_handle(cls, value: str) -> str:
        handle = value.strip().lower()
        if not handle:
            raise ValueError("Payer handle must not be empty.")
        return handle

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, value: str) -> str:
        parse_paisa(value)
        return value.strip()


class PublicPayer(BaseModel):
    handle: str
    display_name: str


class MoneyRequestSummary(BaseModel):
    id: str
    requester: PublicPayer
    payer: PublicPayer
    amount: str
    state: str
    created_at: str


class CreateRequestResponse(BaseModel):
    request: MoneyRequestSummary


class IncomingRequestsResponse(BaseModel):
    requests: list[MoneyRequestSummary]


class FulfillTransferSummary(BaseModel):
    id: str
    amount: str
    kind: str
    created_at: str


class FulfillResponse(BaseModel):
    request: MoneyRequestSummary
    transfer: FulfillTransferSummary
