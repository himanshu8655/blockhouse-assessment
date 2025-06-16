import uuid
from sqlalchemy import Column, String, Float, DateTime, Integer
from app.core.database import Base

class SymbolAverage(Base):
    __tablename__ = "symbol_averages"

    symbol      = Column(String, primary_key=True, nullable=False, index=True)
    window_size = Column(Integer, primary_key=True, default=5)
    average     = Column(Float, nullable=False)
    timestamp   = Column(DateTime, nullable=False)
