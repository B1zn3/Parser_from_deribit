from decimal import Decimal
from types import SimpleNamespace

import pytest

import app.domain.services.market_data_service as service_module
from app.domain.services.market_data_service import MarketDataService


class FakeDeribitClient:
    async def get_index_price(self, index_name: str):
        data = {
            "btc_usd": SimpleNamespace(
                price=Decimal("71298.35"),
                server_timestamp_us=1773427020171269,
            ),
            "eth_usd": SimpleNamespace(
                price=Decimal("4012.77"),
                server_timestamp_us=1773427020179999,
            ),
        }
        return data[index_name]


class FakePriceRepository:
    def __init__(self, session):
        self.session = session
        self.saved = []
        self.committed = False

    async def add_snapshot(self, ticker: str, price: Decimal, collected_at: int):
        self.saved.append(
            {
                "ticker": ticker,
                "price": price,
                "collected_at": collected_at,
            }
        )

    async def commit(self):
        self.committed = True


@pytest.mark.asyncio
async def test_collect_prices_saves_btc_and_eth(monkeypatch):
    fake_repo = FakePriceRepository(session=object())

    monkeypatch.setattr(
        service_module,
        "SqlAlchemyPriceRepository",
        lambda session: fake_repo,
    )

    service = MarketDataService(FakeDeribitClient())

    await service.collect_prices(session=object())

    assert fake_repo.committed is True
    assert fake_repo.saved == [
        {
            "ticker": "btc_usd",
            "price": Decimal("71298.35"),
            "collected_at": 1773427020171269,
        },
        {
            "ticker": "eth_usd",
            "price": Decimal("4012.77"),
            "collected_at": 1773427020179999,
        },
    ]