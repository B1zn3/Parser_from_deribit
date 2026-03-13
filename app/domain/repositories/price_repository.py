from abc import ABC, abstractmethod
from decimal import Decimal

from app.domain.models.price_snapshot import PriceSnapshot


class PriceRepository(ABC):
    @abstractmethod
    async def add_snapshot(
        self,
        *,
        ticker: str,
        price: Decimal,
        collected_at: int,
    ) -> PriceSnapshot:
        pass

    @abstractmethod
    async def get_all_by_ticker(self, ticker: str) -> list[PriceSnapshot]:
        pass

    @abstractmethod
    async def get_latest_by_ticker(self, ticker: str) -> PriceSnapshot | None:
        pass

    @abstractmethod
    async def get_by_ticker_and_range(
        self,
        *,
        ticker: str,
        from_ts: int | None = None,
        to_ts: int | None = None,
    ) -> list[PriceSnapshot]:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass