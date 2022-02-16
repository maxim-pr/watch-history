from aioredis import Redis


class InvalidUserSession(Exception):
    def __init__(self, session_id: str):
        super().__init__('invalid session id', session_id)


class Users:

    def __init__(self, redis: Redis):
        self._redis = redis

    async def get_user_id(self, session_id: str) -> str:
        user_id = await self._redis.get(f'user_id:{session_id}')
        if user_id is None:
            raise InvalidUserSession(session_id)
        return user_id.decode('utf-8')
