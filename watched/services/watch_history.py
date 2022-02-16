from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncEngine

from ..db.schema import watch_history_table
from ..models import watch_history


class WatchHistory:
    def __init__(self, db_engine: AsyncEngine):
        self._db_engine = db_engine

    async def add_film(self, film: watch_history.Film) -> str:
        query = insert(watch_history_table).values(
            user_id=int(film.user_id),
            **film.dict(exclude={'user_id'})
        )
        async with self._db_engine.begin() as db_conn:
            result = await db_conn.execute(query)
        row = result.inserted_primary_key

        return str(row.id)
