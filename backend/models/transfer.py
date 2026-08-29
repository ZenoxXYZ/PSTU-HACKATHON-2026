from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKey, Index, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base


class Transfer(Base):
    __tablename__ = "transfers"
    __table_args__ = (
        CheckConstraint("amount_paisa > 0", name="ck_transfers_amount_positive"),
        CheckConstraint("sender_account_id != recipient_account_id", name="ck_transfers_no_self_transfer"),
        UniqueConstraint("sender_account_id", "idempotency_key", name="uq_transfers_sender_idempotency"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    sender_account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("accounts.id", name="fk_transfers_sender_account"),
        nullable=False,
        index=True,
    )
    recipient_account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("accounts.id", name="fk_transfers_recipient_account"),
        nullable=False,
        index=True,
    )
    amount_paisa: Mapped[int] = mapped_column(BigInteger, nullable=False)
    idempotency_key: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
    )
    kind: Mapped[str] = mapped_column(String(32), nullable=False)
    linked_request_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("money_requests.id", name="fk_transfers_linked_request"),
        nullable=True,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
