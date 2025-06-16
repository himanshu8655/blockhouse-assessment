import yfinance as yf
from datetime import datetime, timezone
from typing import Tuple

def get_latest_price(symbol: str) -> Tuple[float, datetime]:
    ticker = yf.Ticker(symbol)
    df = ticker.history(period="1d", interval="1m")
    if df.empty:
        raise ValueError(f"No data for '{symbol}'")
    row = df.iloc[-1]
    price = float(row["Close"])
    ts = row.name.to_pydatetime().replace(tzinfo=timezone.utc)
    return price, ts