from pydantic import BaseModel
from typing import List, Optional

class PollRequest(BaseModel):
    symbols: List[str]
    interval: int
    provider: Optional[str] = None
