import json
from datetime import datetime, timezone
from confluent_kafka import Consumer
from sqlalchemy import select, desc
from app.core.database import SessionLocal, engine, Base
from app.models.raw_price import RawPrice
from app.models.symbol_average import SymbolAverage
from app.core.config import settings

Base.metadata.create_all(bind=engine)

def run_ma_consumer():
    c = Consumer({"bootstrap.servers": settings.kafka_bootstrap_servers, "group.id": "ma-consumer", "auto.offset.reset": "earliest"})
    c.subscribe(["price-events"])
    while True:
        msg = c.poll(1.0)
        if msg is None or msg.error(): continue
        data = json.loads(msg.value())
        symbol = data["symbol"]
        session = SessionLocal()
        try:
            prices = session.execute(
                select(RawPrice.price).where(RawPrice.symbol==symbol).order_by(desc(RawPrice.timestamp)).limit(5)
            ).scalars().all()
            if prices:
                avg = sum(prices)/len(prices)
                now = datetime.now(timezone.utc)
                ma = SymbolAverage(symbol=symbol, window_size=5, average=avg, timestamp=now)
                session.merge(ma)
                session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()