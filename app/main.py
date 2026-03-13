from fastapi import FastAPI

from app.api.routers.prices import router as prices_router


app = FastAPI()

app.include_router(prices_router)