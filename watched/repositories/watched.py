from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.sql import insert

from ..db.schema import watched_table
from ..models import Watched


class WatchedRepository:

    def __init__(self, db_engine: AsyncEngine):
        self._db_engine = db_engine

    async def add(self, watched: Watched) -> str:
        query = insert(watched_table).values(
            watch_event_id=int(watched.watch_event_id),
            score=watched.score,
            review=watched.review
        )
        async with self._db_engine.begin() as db_conn:
            result = await db_conn.execute(query)
        row = result.inserted_primary_key

        return str(row.id)
