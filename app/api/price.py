from fastapi import APIRouter

router = APIRouter()

@router.get("/latest")
async def stock_price(symbol:str, provider:str):
    return {symbol,provider}

@router.post("/poll", status_code=202)
async def poll_prices():
    return {}