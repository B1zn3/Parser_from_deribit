"""create price_snapshots table

Revision ID: 20260313_01
Revises:
Create Date: 2026-03-13 12:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "20260313_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "price_snapshots",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("ticker", sa.String(length=16), nullable=False),
        sa.Column("price", sa.Numeric(18, 8), nullable=False),
        sa.Column("collected_at", sa.BigInteger(), nullable=False),
        sa.CheckConstraint(
            "ticker IN ('btc_usd', 'eth_usd')",
            name="ck_price_snapshots_ticker_allowed_values",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_price_snapshots"),
    )

    op.create_index(
        "ix_price_snapshots_ticker_collected_at",
        "price_snapshots",
        ["ticker", "collected_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_price_snapshots_ticker_collected_at", table_name="price_snapshots")
    op.drop_table("price_snapshots")