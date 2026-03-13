from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class PriceResponse(BaseModel):
    ticker: str = Field(..., examples=["btc_usd"])
    price: Decimal = Field(..., examples=["65000.12345678"])
    timestamp: int = Field(..., examples=[1710000000])

    model_config = ConfigDict(from_attributes=True)


class PriceListResponse(BaseModel):
    items: list[PriceResponse]