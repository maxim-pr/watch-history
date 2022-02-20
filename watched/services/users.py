from ..repositories.user_sessions import UserSessionsRepository


class UsersService:

    def __init__(self, user_sessions_repo: UserSessionsRepository):
        self._user_sessions_repo = user_sessions_repo

    async def get_user_id(self, session_id: str) -> str:
        user_id = await self._user_sessions_repo.get_user_id(session_id)
        return user_id
