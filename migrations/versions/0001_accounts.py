"""create accounts table

Revision ID: 0001_accounts
Revises:
Create Date: 2026-08-29
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001_accounts"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "accounts",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("handle", sa.String(length=32), nullable=False),
        sa.Column("display_name", sa.String(length=80), nullable=False),
        sa.Column("balance_paisa", sa.BigInteger(), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("balance_paisa >= 0", name="ck_accounts_balance_non_negative"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_accounts_handle"), "accounts", ["handle"], unique=True)
    op.create_index(op.f("ix_accounts_token_hash"), "accounts", ["token_hash"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_accounts_token_hash"), table_name="accounts")
    op.drop_index(op.f("ix_accounts_handle"), table_name="accounts")
    op.drop_table("accounts")
