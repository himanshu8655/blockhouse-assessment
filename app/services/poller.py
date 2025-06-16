import time, json
from uuid import uuid4
from app.services.kafka import publish_price_event
from app.services.market import get_latest_price
from app.core.config import settings

def start_polling_job(symbols: list[str], interval: int, provider: str | None):
    while True:
        for symbol in symbols:
            price, ts = get_latest_price(symbol)
            msg = {"symbol": symbol, "price": price, "timestamp": ts.isoformat(), "source": provider or settings.provider, "raw_response_id": uuid4().hex}
            publish_price_event(msg)
        time.sleep(interval)