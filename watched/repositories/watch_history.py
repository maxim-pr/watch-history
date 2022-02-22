from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.sql import insert, select, and_, Insert
from sqlalchemy.sql.expression import desc

from ..db.schema import watch_history_table, watch_history_shows_table
from ..models import (
    WatchEvent, WatchEventWithID,
    WatchEventFilm, WatchEventFilmWithID,
    WatchEventShow, WatchEventShowWithID,
    WatchHistoryTypeFilter, WatchHistoryStatusFilter
)


class WatchHistoryRepository:

    def __init__(self, db_engine: AsyncEngine):
        self._db_engine = db_engine

    async def add_film(self, film: WatchEventFilm) -> str:
        query = WatchHistoryRepository._insert_watch_event_query(film)
        query = query.values(is_show=False)

        async with self._db_engine.begin() as db_conn:
            result = await db_conn.execute(query)

        row = result.inserted_primary_key
        return str(row.id)

    async def add_show(self, show: WatchEventShow) -> str:
        query1 = WatchHistoryRepository._insert_watch_event_query(show)
        query1 = query1.values(is_show=True)

        query2 = insert(watch_history_shows_table).values(
            first_episode=show.first_episode,
            last_episode=show.last_episode,
            season=show.season,
            finished_season=show.finished_season,
            finished_show=show.finished_show
        )

        async with self._db_engine.begin() as db_conn:
            result = await db_conn.execute(query1)
            row = result.inserted_primary_key
            watch_event_id = row.id
            query2 = query2.values(watch_event_id=watch_event_id)
            await db_conn.execute(query2)

        return str(watch_event_id)

    @staticmethod
    def _insert_watch_event_query(watch_event: WatchEvent) -> Insert:
        query = insert(watch_history_table).values(
            user_id=int(watch_event.user_id),
            name=watch_event.name,
            datetime=watch_event.datetime
        )
        return query

    async def get_watch_events(
            self,
            user_id: str,
            type_filter: WatchHistoryTypeFilter,
            status_filter: WatchHistoryStatusFilter
    ) -> list[WatchEventWithID]:
        columns = [
            watch_history_table.c.id,
            watch_history_table.c.name,
            watch_history_table.c.datetime,
            watch_history_table.c.is_show
        ]
        table = watch_history_table
        condition = watch_history_table.c.user_id == int(user_id)
        ordering_column = desc(watch_history_table.c.datetime)

        if type_filter != WatchHistoryTypeFilter.FILMS:
            columns += [watch_history_shows_table.c.first_episode,
                        watch_history_shows_table.c.last_episode,
                        watch_history_shows_table.c.season,
                        watch_history_shows_table.c.finished_season,
                        watch_history_shows_table.c.finished_show]

            if type_filter == WatchHistoryTypeFilter.ALL:
                table = table.outerjoin(
                    watch_history_shows_table,
                    watch_history_table.c.id == watch_history_shows_table.c.watch_event_id
                )
            elif type_filter == WatchHistoryTypeFilter.SHOWS:
                table = table.join(
                    watch_history_shows_table,
                    watch_history_table.c.id == watch_history_shows_table.c.watch_event_id
                )
                condition = and_(
                    condition,
                    watch_history_table.c.is_show
                )

            if status_filter == WatchHistoryStatusFilter.FINISHED:
                condition = and_(
                    condition,
                    watch_history_shows_table.c.finished_show
                )
            elif status_filter == WatchHistoryStatusFilter.IN_PROGRESS:
                condition = and_(
                    condition,
                    watch_history_shows_table.c.finished_show == False
                )

        if type_filter != WatchHistoryTypeFilter.SHOWS:
            if type_filter == WatchHistoryTypeFilter.FILMS:
                condition = and_(
                    condition,
                    watch_history_table.c.is_show == False
                )

        query = select(columns).select_from(table).where(condition).order_by(
            ordering_column
        )

        async with self._db_engine.begin() as db_conn:
            result = await db_conn.execute(query)
        rows = result.fetchall()

        watch_events = [
            WatchEventFilmWithID.construct(
                id=str(row.id),
                name=row.name,
                datetime=row.datetime,
                is_show=False
            ) if not row.is_show else
            WatchEventShowWithID.construct(
                id=str(row.id),
                name=row.name,
                datetime=row.datetime,
                is_show=True,
                first_episode=row.first_episode,
                last_episode=row.last_episode,
                season=row.season,
                finished_season=row.finished_season,
                finished_show=row.finished_show
            ) for row in rows
        ]
        return watch_events
