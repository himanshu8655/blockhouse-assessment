from pydantic import BaseModel

class Stock(BaseModel):
    symbol:str
    price:int
    timestamp:str
    provider:str