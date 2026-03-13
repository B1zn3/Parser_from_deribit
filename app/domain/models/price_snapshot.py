from decimal import Decimal

from sqlalchemy import BigInteger, CheckConstraint, Index, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class PriceSnapshot(Base):
    __tablename__ = "price_snapshots"

    __table_args__ = (
        CheckConstraint(
            "ticker IN ('btc_usd', 'eth_usd')",
            name="ticker_allowed_values",
        ),
        Index("ix_price_snapshots_ticker_collected_at", "ticker", "collected_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ticker: Mapped[str] = mapped_column(String(16), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)
    collected_at: Mapped[int] = mapped_column(BigInteger, nullable=False)