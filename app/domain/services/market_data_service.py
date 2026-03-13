from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.clients.deribit_client import DeribitClient
from app.infrastructure.repositories.price_repository_impl import (
    SqlAlchemyPriceRepository,
)


class MarketDataService:
    def __init__(self, deribit_client: DeribitClient) -> None:
        self._deribit_client = deribit_client

    async def collect_prices(self, session: AsyncSession) -> None:
        repo = SqlAlchemyPriceRepository(session)

        btc_data = await self._deribit_client.get_index_price("btc_usd")
        eth_data = await self._deribit_client.get_index_price("eth_usd")

        await repo.add_snapshot(
            ticker="btc_usd",
            price=btc_data.price,
            collected_at=btc_data.server_timestamp_us,
        )
        await repo.add_snapshot(
            ticker="eth_usd",
            price=eth_data.price,
            collected_at=eth_data.server_timestamp_us,
        )

        await repo.commit()