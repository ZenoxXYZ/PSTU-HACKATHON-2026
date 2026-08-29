"""create transfers table

Revision ID: 0002_transfers
Revises: 0001_accounts
Create Date: 2026-08-29
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0002_transfers"
down_revision: str = "0001_accounts"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "transfers",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "sender_account_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("accounts.id", name="fk_transfers_sender_account"),
            nullable=False,
        ),
        sa.Column(
            "recipient_account_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("accounts.id", name="fk_transfers_recipient_account"),
            nullable=False,
        ),
        sa.Column("amount_paisa", sa.BigInteger(), nullable=False),
        sa.Column("idempotency_key", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("kind", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("amount_paisa > 0", name="ck_transfers_amount_positive"),
        sa.CheckConstraint(
            "sender_account_id != recipient_account_id",
            name="ck_transfers_no_self_transfer",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "sender_account_id",
            "idempotency_key",
            name="uq_transfers_sender_idempotency",
        ),
    )
    op.create_index(
        op.f("ix_transfers_sender_account_id"),
        "transfers",
        ["sender_account_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_transfers_recipient_account_id"),
        "transfers",
        ["recipient_account_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_transfers_recipient_account_id"), table_name="transfers")
    op.drop_index(op.f("ix_transfers_sender_account_id"), table_name="transfers")
    op.drop_table("transfers")
