from fastapi import APIRouter, Depends, HTTPException
from fastapi import Depends
from app.api.dependency import get_db, get_redis
from aioredis import Redis
from sqlalchemy import text

router = APIRouter()

@router.get("/latest")
async def stock_price(
    symbol: str,
    provider: str,
    db = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    try:
        result = db.execute(text("SELECT 1")).scalar()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {e}")

    await redis.set("__ping__", "pong", ex=5)
    pong = await redis.get("__ping__")

    return {
        "symbol": symbol,
        "provider": provider,
        "db_test": result,         
        "redis_test": pong,
    }

@router.post("/poll", status_code=202)
async def poll_prices():
    return "name"
