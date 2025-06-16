from fastapi import FastAPI
from app.api.price import router as prices_router
from contextlib import asynccontextmanager
from app.core.config import settings
import aioredis
from app.core.database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    app.state.redis = await aioredis.from_url(settings.redis_url, encoding="utf8", decode_responses=True)
    try:
        yield
    finally:
        await app.state.redis.close()

app = FastAPI(title= "BlockHouse Assignment", lifespan=lifespan)
app.include_router(prices_router, prefix="/prices", tags=["prices"])
