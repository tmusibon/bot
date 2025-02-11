import asyncio
import logging
from .config import TELEGRAM_BOT_TOKEN
from .bot import TradingBot

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def main():
    bot = TradingBot(TELEGRAM_BOT_TOKEN)
    try:
        await bot.run()
    except KeyboardInterrupt:
        await bot.shutdown()

if __name__ == '__main__':
    asyncio.run(main())
