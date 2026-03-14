from decimal import Decimal
from types import SimpleNamespace

import pytest

import app.api.routers.prices as prices_router


@pytest.mark.asyncio
async def test_get_latest_price_returns_data(client, monkeypatch):
    class FakeRepo:
        def __init__(self, session):
            self.session = session

        async def get_latest_by_ticker(self, ticker: str):
            return SimpleNamespace(
                ticker=ticker,
                price=Decimal("71298.35"),
                collected_at=1773427020171269,
            )

    monkeypatch.setattr(prices_router, "SqlAlchemyPriceRepository", FakeRepo)

    response = await client.get(
        "/prices/latest",
        params={"ticker": "btc_usd"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "ticker": "btc_usd",
        "price": "71298.35",
        "timestamp": 1773427020171269,
    }


@pytest.mark.asyncio
async def test_get_latest_price_returns_404_when_no_data(client, monkeypatch):
    class FakeRepo:
        def __init__(self, session):
            self.session = session

        async def get_latest_by_ticker(self, ticker: str):
            return None

    monkeypatch.setattr(prices_router, "SqlAlchemyPriceRepository", FakeRepo)

    response = await client.get(
        "/prices/latest",
        params={"ticker": "btc_usd"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Нет сохраненных данных для пары 'btc_usd'"
    }


@pytest.mark.asyncio
async def test_get_all_prices_returns_list(client, monkeypatch):
    class FakeRepo:
        def __init__(self, session):
            self.session = session

        async def get_all_by_ticker(self, ticker: str):
            return [
                SimpleNamespace(
                    ticker=ticker,
                    price=Decimal("71298.35"),
                    collected_at=1773427020171269,
                ),
                SimpleNamespace(
                    ticker=ticker,
                    price=Decimal("71310.10"),
                    collected_at=1773427080000000,
                ),
            ]

    monkeypatch.setattr(prices_router, "SqlAlchemyPriceRepository", FakeRepo)

    response = await client.get(
        "/prices",
        params={"ticker": "btc_usd"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "ticker": "btc_usd",
                "price": "71298.35",
                "timestamp": 1773427020171269,
            },
            {
                "ticker": "btc_usd",
                "price": "71310.10",
                "timestamp": 1773427080000000,
            },
        ]
    }


@pytest.mark.asyncio
async def test_get_prices_filter_returns_data(client, monkeypatch):
    class FakeRepo:
        def __init__(self, session):
            self.session = session

        async def get_by_ticker_and_range(
            self,
            ticker: str,
            from_ts: int | None,
            to_ts: int | None,
        ):
            return [
                SimpleNamespace(
                    ticker=ticker,
                    price=Decimal("71298.35"),
                    collected_at=1773427020171269,
                )
            ]

    monkeypatch.setattr(prices_router, "SqlAlchemyPriceRepository", FakeRepo)

    response = await client.get(
        "/prices/filter",
        params={
            "ticker": "btc_usd",
            "from_ts": 1773427000000000,
            "to_ts": 1773428000000000,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "ticker": "btc_usd",
                "price": "71298.35",
                "timestamp": 1773427020171269,
            }
        ]
    }


@pytest.mark.asyncio
async def test_get_prices_filter_returns_422_for_invalid_range(client):
    response = await client.get(
        "/prices/filter",
        params={
            "ticker": "btc_usd",
            "from_ts": 200,
            "to_ts": 100,
        },
    )

    assert response.status_code == 422
    assert response.json() == {
        "detail": "'from_ts' должно быть меньше или равно 'to_ts'"
    }