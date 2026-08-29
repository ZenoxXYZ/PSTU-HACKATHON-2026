"""create money_requests and link transfers

Revision ID: 0003_money_requests
Revises: 0002_transfers
Create Date: 2026-08-29
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0003_money_requests"
down_revision: str = "0002_transfers"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "money_requests",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "requester_account_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("accounts.id", name="fk_money_requests_requester_account"),
            nullable=False,
        ),
        sa.Column(
            "payer_account_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("accounts.id", name="fk_money_requests_payer_account"),
            nullable=False,
        ),
        sa.Column("amount_paisa", sa.BigInteger(), nullable=False),
        sa.Column("state", sa.String(length=32), nullable=False, server_default="PENDING"),
        sa.Column("creation_idempotency_key", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("amount_paisa > 0", name="ck_money_requests_amount_positive"),
        sa.CheckConstraint(
            "requester_account_id != payer_account_id",
            name="ck_money_requests_no_self_request",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "requester_account_id",
            "creation_idempotency_key",
            name="uq_money_requests_requester_idempotency",
        ),
    )
    op.create_index(
        op.f("ix_money_requests_requester_account_id"),
        "money_requests",
        ["requester_account_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_money_requests_payer_account_id"),
        "money_requests",
        ["payer_account_id"],
        unique=False,
    )

    # Add linked_request_id to transfers table
    op.add_column(
        "transfers",
        sa.Column(
            "linked_request_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("money_requests.id", name="fk_transfers_linked_request"),
            nullable=True,
        ),
    )
    op.create_index(
        op.f("ix_transfers_linked_request_id"),
        "transfers",
        ["linked_request_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_transfers_linked_request_id"), table_name="transfers")
    op.drop_column("transfers", "linked_request_id")
    op.drop_index(op.f("ix_money_requests_payer_account_id"), table_name="money_requests")
    op.drop_index(op.f("ix_money_requests_requester_account_id"), table_name="money_requests")
    op.drop_table("money_requests")
