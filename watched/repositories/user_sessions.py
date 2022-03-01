from typing import Optional

from aioredis import Redis


class UserSessionsRepository:

    def __init__(self, redis: Redis):
        self._redis = redis

    async def get_user_id(self, session_id: str) -> Optional[str]:
        user_id = await self._redis.get(f'user_id:{session_id}')
        if user_id is not None:
            return user_id.decode('utf-8')
        return None
