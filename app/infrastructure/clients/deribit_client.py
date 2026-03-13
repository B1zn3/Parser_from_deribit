from dataclasses import dataclass
from decimal import Decimal
from typing import Any

import aiohttp

from app.core.config import get_settings


class DeribitClientError(Exception):
    """Base exception for Deribit client errors."""


class DeribitBadResponseError(DeribitClientError):
    """Raised when Deribit returns an invalid response."""
    
@dataclass(slots=True)
class DeribitIndexPrice:
    price: Decimal
    server_timestamp_us: int

class DeribitClient:
    def __init__(self) -> None:
        settings = get_settings()
        self._base_url = settings.deribit_base_url.rstrip("/")
        self._timeout = aiohttp.ClientTimeout(total=settings.deribit_timeout_seconds)

    async def get_index_price(self, index_name: str) -> Decimal:
        url = f"{self._base_url}/api/v2/public/get_index_price"
        params = {"index_name": index_name}

        async with aiohttp.ClientSession(timeout=self._timeout) as session:
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    body = await response.text()
                    raise DeribitBadResponseError(
                        f"Deribit вернул статуы {response.status}: {body}"
                    )

                data: dict[str, Any] = await response.json()

        result = data.get("result")
        if not isinstance(result, dict):
            raise DeribitBadResponseError("Поле 'result' не найдено в ответе Deribit")

        index_price = result.get("index_price")
        if index_price is None:
            raise DeribitBadResponseError(
                "Поле 'index_price' не найдено в ответе Deribit"
            )

        us_out = data.get("usOut")
        if us_out is None:
            raise DeribitBadResponseError("Поле 'usOut' не найдено в ответе Deribit")

        try:
            return DeribitIndexPrice(
                price=Decimal(str(index_price)),
                server_timestamp_us=int(us_out),
            )
        except Exception as exc:
            raise DeribitBadResponseError(
                f"Некорректное значение index_price: {index_price}"
            ) from exc