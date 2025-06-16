from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from aioredis import Redis
import json, uuid

from app.api.dependency import get_db, get_redis
from app.services.market import get_latest_price
from app.services.kafka import publish_price_event
from app.models.raw_price import RawPrice
from app.schemas.prices import PollRequest
from app.services.poller import start_polling_job
from app.core.config import settings
from app.models.stock import Stock

router = APIRouter()

@router.get("/latest")
async def stock_price(symbol: str, provider: str | None = None, db: Session = Depends(get_db), redis: Redis = Depends(get_redis)):
    cache_key = f"price:{symbol}"
    cached_data:Stock = await redis.get(cache_key)
    if cached_data:
        return json.loads(cached_data)

    try:
        price, ts = get_latest_price(symbol)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    raw = RawPrice(symbol=symbol, price=price, timestamp=ts, source=provider or settings.provider)
    db.add(raw)
    db.commit()
    publish_price_event({
        "symbol": symbol,
        "price": price,
        "timestamp": ts.isoformat(),
        "source": provider or settings.provider,
        "raw_response_id": raw.id.hex,
    })

    res: Stock = Stock(symbol=symbol, price=price, timestamp=ts.isoformat(), provider=provider or settings.provider)
    await redis.set(cache_key, res.model_dump_json(), ex=60)
    return res

@router.post("/poll", status_code=202)
async def poll_prices(
    req: PollRequest,
    background_tasks: BackgroundTasks
):
    job_id = f"poll_{uuid.uuid4().hex[:8]}"
    background_tasks.add_task(
        start_polling_job,
        req.symbols,
        req.interval,
        req.provider,
    )
    return {
        "job_id": job_id,
        "status": "accepted",
        "config": {
            "symbols": req.symbols,
            "interval": req.interval,
        },
    }
