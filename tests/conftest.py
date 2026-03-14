import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.core.database import get_db_session
from app.main import app


async def _fake_db_session():
    yield object()


@pytest_asyncio.fixture
async def client():
    app.dependency_overrides[get_db_session] = _fake_db_session

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as test_client:
        yield test_client

    app.dependency_overrides.clear()