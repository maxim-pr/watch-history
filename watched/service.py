from dataclasses import asdict

from sqlalchemy.ext.asyncio import AsyncEngine

from .db.schema import watched_table
from .models import WatchedFilm


class Service:
    def __init__(self, db_engine: AsyncEngine):
        self._db_engine = db_engine

    async def add_watched_film(self, film: WatchedFilm):
        query = watched_table.insert().values(asdict(film))
        async with self._db_engine.begin() as db_conn:
            result = await db_conn.execute(query)
