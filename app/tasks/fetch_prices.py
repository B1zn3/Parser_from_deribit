import asyncio

from app.core.celery_app import celery_app
from app.core.database import AsyncSessionLocal
from app.domain.services.market_data_service import MarketDataService
from app.infrastructure.clients.deribit_client import DeribitClient


async def _run() -> None:
    async with AsyncSessionLocal() as session:
        client = DeribitClient()
        service = MarketDataService(client)
        await service.collect_prices(session)


@celery_app.task(name="fetch_prices_task")
def fetch_prices_task() -> None:
    asyncio.run(_run())