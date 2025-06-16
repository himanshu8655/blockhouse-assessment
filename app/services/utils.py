from typing import List

def calculate_moving_average(prices: List[float]) -> float:
    return sum(prices) / len(prices)
