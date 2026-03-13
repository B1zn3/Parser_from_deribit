from decimal import Decimal

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.price_snapshot import PriceSnapshot
from app.domain.repositories.price_repository import PriceRepository


class SqlAlchemyPriceRepository(PriceRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add_snapshot(
        self,
        *,
        ticker: str,
        price: Decimal,
        collected_at: int,
    ) -> PriceSnapshot:
        snapshot = PriceSnapshot(
            ticker=ticker,
            price=price,
            collected_at=collected_at,
        )
        self._session.add(snapshot)
        await self._session.flush()
        return snapshot

    async def get_all_by_ticker(self, ticker: str) -> list[PriceSnapshot]:
        stmt = (
            select(PriceSnapshot)
            .where(PriceSnapshot.ticker == ticker)
            .order_by(PriceSnapshot.collected_at.asc())
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_latest_by_ticker(self, ticker: str) -> PriceSnapshot | None:
        stmt = (
            select(PriceSnapshot)
            .where(PriceSnapshot.ticker == ticker)
            .order_by(desc(PriceSnapshot.collected_at))
            .limit(1)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_ticker_and_range(
        self,
        *,
        ticker: str,
        from_ts: int | None = None,
        to_ts: int | None = None,
    ) -> list[PriceSnapshot]:
        stmt = select(PriceSnapshot).where(PriceSnapshot.ticker == ticker)

        if from_ts is not None:
            stmt = stmt.where(PriceSnapshot.collected_at >= from_ts)

        if to_ts is not None:
            stmt = stmt.where(PriceSnapshot.collected_at <= to_ts)

        stmt = stmt.order_by(PriceSnapshot.collected_at.asc())

        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()