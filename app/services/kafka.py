from confluent_kafka import Producer
from app.core.config import settings
import json


producer = Producer({"bootstrap.servers": settings.kafka_bootstrap_servers})

def publish_price_event(message: dict):
    producer.produce(topic="price-events", key=message["symbol"], value=json.dumps(message))
    producer.flush()
