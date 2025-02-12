import numpy as np
from typing import Tuple, List

def calculate_rsi(prices: np.array, period: int = 14) -> np.array:
    deltas = np.diff(prices)
    seed = deltas[:period+1]
    up = seed[seed >= 0].sum()/period
    down = -seed[seed < 0].sum()/period
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:period] = 100. - 100./(1.+rs)

    for i in range(period, len(prices)):
        delta = deltas[i-1]
        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(period-1) + upval)/period
        down = (down*(period-1) + downval)/period
        rs = up/down
        rsi[i] = 100. - 100./(1.+rs)

    return rsi

def calculate_macd(prices: np.array) -> Tuple[np.array, np.array, np.array]:
    exp1 = prices.ewm(span=12, adjust=False).mean()
    exp2 = prices.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    hist = macd - signal
    return macd, signal, hist

def check_support_resistance(prices: np.array) -> Tuple[List[float], List[float]]:
    # Simple implementation - you might want to use more sophisticated methods
    window = 20
    supports = []
    resistances = []
    
    for i in range(window, len(prices)-window):
        if all(prices[i] <= prices[i-window:i]) and all(prices[i] <= prices[i+1:i+window+1]):
            supports.append(prices[i])
        if all(prices[i] >= prices[i-window:i]) and all(prices[i] >= prices[i+1:i+window+1]):
            resistances.append(prices[i])
    
    return supports, resistances

def calculate_volume_profile(prices: np.array, volumes: np.array) -> dict:
    # Simple volume profile implementation
    price_levels = np.linspace(min(prices), max(prices), 10)
    volume_profile = {}
    
    for price, volume in zip(prices, volumes):
        level = np.digitize(price, price_levels)
        if level in volume_profile:
            volume_profile[level] += volume
        else:
            volume_profile[level] = volume
            
    return volume_profile
