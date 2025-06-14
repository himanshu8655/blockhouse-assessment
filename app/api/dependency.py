from app.core.database import SessionLocal
from fastapi import Request

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_redis(request: Request):
    return request.app.state.redis