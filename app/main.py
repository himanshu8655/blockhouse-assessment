from fastapi import FastAPI
from app.api.price import router as prices_router

app = FastAPI(title= "BlockHouse Assignment")

app.include_router(prices_router, prefix="/prices", tags=["prices"])