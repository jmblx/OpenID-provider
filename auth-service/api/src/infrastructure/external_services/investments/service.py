import json
import logging
from datetime import datetime, timedelta, date
from typing import List, Dict

import pytz
import redis.asyncio as aioredis

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)  # Можно менять на INFO или ERROR в зависимости от нужд
logger = logging.getLogger(__name__)


class InvestmentsService:
    def __init__(self, redis: aioredis.Redis):
        self.redis = redis

    async def get_investments(self) -> dict[str, dict]:
        investments = await self.redis.get("data")
        investments_dict = json.loads(investments)
        return investments_dict
