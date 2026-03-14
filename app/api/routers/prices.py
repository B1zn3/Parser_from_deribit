from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.price import PriceListResponse, PriceResponse
from app.core.database import get_db_session
from app.infrastructure.repositories.price_repository_impl import (
    SqlAlchemyPriceRepository,
)

router = APIRouter(prefix="/prices", tags=["prices"])


def _validate_time_range(from_ts: int | None, to_ts: int | None) -> None:
    if from_ts is not None and to_ts is not None and from_ts > to_ts:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="'from_ts' должно быть меньше или равно 'to_ts'",
        )


@router.get(
    "",
    response_model=PriceListResponse,
    summary="Получить все сохраненные данные по валюте",
)
async def get_all_prices(
    ticker: str = Query(..., pattern="^(btc_usd|eth_usd)$"),
    session: AsyncSession = Depends(get_db_session),
) -> PriceListResponse:
    repo = SqlAlchemyPriceRepository(session)
    items = await repo.get_all_by_ticker(ticker)

    return PriceListResponse(
        items=[
            PriceResponse(
                ticker=item.ticker,
                price=item.price,
                timestamp=item.collected_at,
            )
            for item in items
        ]
    )


@router.get(
    "/latest",
    response_model=PriceResponse,
    summary="Получить последнюю цену валюты",
)
async def get_latest_price(
    ticker: str = Query(..., pattern="^(btc_usd|eth_usd)$"),
    session: AsyncSession = Depends(get_db_session),
) -> PriceResponse:
    repo = SqlAlchemyPriceRepository(session)
    item = await repo.get_latest_by_ticker(ticker)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Нет сохраненных данных для пары '{ticker}'",
        )

    return PriceResponse(
        ticker=item.ticker,
        price=item.price,
        timestamp=item.collected_at,
    )


@router.get(
    "/filter",
    response_model=PriceListResponse,
    summary="Получить цены валюты с фильтром по дате",
)
async def get_prices_by_range(
    ticker: str = Query(..., pattern="^(btc_usd|eth_usd)$"),
    from_ts: int | None = Query(default=None, ge=0),
    to_ts: int | None = Query(default=None, ge=0),
    session: AsyncSession = Depends(get_db_session),
) -> PriceListResponse:
    _validate_time_range(from_ts, to_ts)

    repo = SqlAlchemyPriceRepository(session)
    items = await repo.get_by_ticker_and_range(
        ticker=ticker,
        from_ts=from_ts,
        to_ts=to_ts,
    )

    return PriceListResponse(
        items=[
            PriceResponse(
                ticker=item.ticker,
                price=item.price,
                timestamp=item.collected_at,
            )
            for item in items
        ]
    )