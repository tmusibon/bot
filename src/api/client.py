import aiohttp
import logging
from ..config import DEX_SCREENER_API, RUGCHECK_API, API_KEY

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self):
        self.session = None

    async def init_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession()

    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None

    async def get_pair_data(self, pair_address):
        if not self.session:
            await self.init_session()
        
        url = f"{DEX_SCREENER_API}{pair_address}"
        headers = {'Authorization': f'Bearer {API_KEY}'} if API_KEY else {}
        
        try:
            async with self.session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Failed to fetch pair data: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Error fetching pair data: {e}")
            return None

    async def get_security_data(self, token_address):
        if not self.session:
            await self.init_session()
        
        url = f"{RUGCHECK_API}{token_address}/report/summary"
        headers = {'Authorization': f'Bearer {API_KEY}'} if API_KEY else {}
        
        try:
            async with self.session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    logger.error(f"Failed to fetch security data: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Error fetching security data: {e}")
            return None
