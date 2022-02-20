from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncEngine

from ..db.schema import watch_history_table, watch_history_shows_table
from ..models import WatchEvent, WatchEventFilm, WatchEventShow


class WatchHistoryRepository:

    def __init__(self, db_engine: AsyncEngine):
        self._db_engine = db_engine

    async def add_film(self, film: WatchEventFilm) -> str:
        watch_event_id = await self._add(film)
        return watch_event_id

    async def add_show(self, show: WatchEventShow) -> str:
        watch_event_id = await self._add(show)

        query = insert(watch_history_shows_table).values(
            watch_event_id=int(watch_event_id),
            first_episode=show.first_episode,
            last_episode=show.last_episode,
            season=show.season,
            finished_season=show.finished_season,
            finished_show=show.finished_show
        )
        async with self._db_engine.begin() as db_conn:
            await db_conn.execute(query)

        return watch_event_id

    async def _add(self, watch_event: WatchEvent) -> str:
        query = insert(watch_history_table).values(
            user_id=int(watch_event.user_id),
            name=watch_event.name,
            datetime=watch_event.datetime
        )
        async with self._db_engine.begin() as db_conn:
            result = await db_conn.execute(query)
        row = result.inserted_primary_key
        return str(row.id)
