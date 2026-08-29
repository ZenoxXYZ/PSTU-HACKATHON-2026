from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base


class MoneyRequest(Base):
    __tablename__ = "money_requests"
    __table_args__ = (
        CheckConstraint("amount_paisa > 0", name="ck_money_requests_amount_positive"),
        CheckConstraint(
            "requester_account_id != payer_account_id",
            name="ck_money_requests_no_self_request",
        ),
        UniqueConstraint(
            "requester_account_id",
            "creation_idempotency_key",
            name="uq_money_requests_requester_idempotency",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    requester_account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("accounts.id", name="fk_money_requests_requester_account"),
        nullable=False,
        index=True,
    )
    payer_account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("accounts.id", name="fk_money_requests_payer_account"),
        nullable=False,
        index=True,
    )
    amount_paisa: Mapped[int] = mapped_column(BigInteger, nullable=False)
    state: Mapped[str] = mapped_column(String(32), nullable=False, default="PENDING")
    creation_idempotency_key: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
