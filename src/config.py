import os
from dotenv import load_dotenv

load_dotenv()

# API Endpoints
DEX_SCREENER_API = os.getenv('DEX_SCREENER_API_URL', 'https://api.dexscreener.com/latest/dex/tokens/')
RUGCHECK_API = os.getenv('RUGCHECK_API_URL', 'https://rugcheck.xyz/api/v1/tokens/')
API_KEY = os.getenv('API_KEY', '')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')

# Trading Parameters
MIN_MARKET_CAP = float(os.getenv('MIN_MARKET_CAP', 400000))
MIN_LIQUIDITY = float(os.getenv('MIN_LIQUIDITY', 100000))
MIN_VOLUME = float(os.getenv('MIN_VOLUME', 50000))

# Technical Analysis Parameters
STOCH_RSI_LENGTH = int(os.getenv('STOCH_RSI_LENGTH', 14))
SMOOTH_K = int(os.getenv('SMOOTH_K', 3))
SMOOTH_D = int(os.getenv('SMOOTH_D', 3))
