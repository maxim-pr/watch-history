from typing import Union, Optional

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.sql import insert, select, update, delete, and_
from sqlalchemy.sql.expression import desc

from ..db.schema import watch_history_table, watch_history_shows_table
from ..models import (
    WatchHistoryFilmRecord, WatchHistoryShowRecord,
    WatchHistoryTypeFilter, WatchHistoryStatusFilter
)


class WatchHistoryBaseRepository:

    def __init__(self, db_engine: AsyncEngine):
        self._db_engine = db_engine

    async def delete_record(self, record_id: str):
        query = delete(watch_history_table).where(
            watch_history_table.c.id == int(record_id)
        )
        async with self._db_engine.begin() as db_conn:
            await db_conn.execute(query)

    async def is_show_record(self, record_id: str) -> Optional[bool]:
        query = select([watch_history_table.c.is_show]).where(
            watch_history_table.c.id == int(record_id)
        )
        async with self._db_engine.begin() as db_conn:
            result = await db_conn.execute(query)
        row = result.fetchone()
        if row is None:
            return None
        return row.is_show


class WatchHistoryFilmsRepository(WatchHistoryBaseRepository):

    def __init__(self, db_engine: AsyncEngine):
        super().__init__(db_engine)

    async def add_film_record(self, film: WatchHistoryFilmRecord) -> str:
        query = insert(watch_history_table).values(
            user_id=int(film.user_id),
            name=film.name,
            datetime=film.datetime,
            is_show=False
        )
        async with self._db_engine.begin() as db_conn:
            result = await db_conn.execute(query)
        row = result.inserted_primary_key
        return str(row.id)

    async def update_film_record(self, film: WatchHistoryFilmRecord):
        query = update(watch_history_table).where(
            watch_history_table.c.id == int(film.id)
        ).values(
            user_id=int(film.user_id),
            name=film.name,
            datetime=film.datetime,
            is_show=False
        )
        async with self._db_engine.begin() as db_conn:
            await db_conn.execute(query)

    async def film_record_exists(self, record_id: str) -> bool:
        is_show = await super().is_show_record(record_id)
        if is_show is None or is_show:
            return False
        return True

    async def find_film_record_by_name(self, user_id: str,
                                       name: str) -> Optional[str]:
        query = select([watch_history_table.c.id]).where(
            and_(
                watch_history_table.c.user_id == int(user_id),
                watch_history_table.c.name == name,
                watch_history_table.c.is_show == False
            )
        )
        async with self._db_engine.begin() as db_conn:
            result = await db_conn.execute(query)
        row = result.fetchone()
        if row is None:
            return None
        return str(row.id)


class WatchHistoryShowsRepository(WatchHistoryBaseRepository):

    def __init__(self, db_engine: AsyncEngine):
        super().__init__(db_engine)

    async def add_show_record(self, show: WatchHistoryShowRecord) -> str:
        query1 = insert(watch_history_table).values(
            user_id=int(show.user_id),
            name=show.name,
            datetime=show.datetime,
            is_show=True
        )

        query2 = insert(watch_history_shows_table).values(
            first_episode=show.first_episode,
            last_episode=show.last_episode,
            season=show.season,
            finished_season=show.finished_season,
            finished_show=show.finished_show
        )

        async with self._db_engine.begin() as db_conn:
            result = await db_conn.execute(query1)
            watch_history_record_id = result.inserted_primary_key.id
            query2 = query2.values(
                watch_history_record_id=watch_history_record_id
            )
            await db_conn.execute(query2)

        return str(watch_history_record_id)

    async def update_show_record(self, show: WatchHistoryShowRecord):
        query1 = update(watch_history_table).where(
            watch_history_table.c.id == int(show.id)
        ).values(
            user_id=int(show.user_id),
            name=show.name,
            datetime=show.datetime,
            is_show=True
        )

        query2 = update(watch_history_shows_table).where(
            watch_history_table.c.id == int(show.id)
        ).values(
            first_episode=show.first_episode,
            last_episode=show.last_episode,
            season=show.season,
            finished_season=show.finished_season,
            finished_show=show.finished_show
        )

        async with self._db_engine.begin() as db_conn:
            await db_conn.execute(query1)
            await db_conn.execute(query2)

    async def show_record_exists(self, record_id: str) -> bool:
        is_show = await super().is_show_record(record_id)
        if is_show is None or not is_show:
            return False
        return True


class WatchHistoryRepository(WatchHistoryFilmsRepository,
                             WatchHistoryShowsRepository):

    def __init__(self, db_engine: AsyncEngine):
        super().__init__(db_engine)

    async def get_watch_history_records(
            self,
            user_id: str,
            type_filter: WatchHistoryTypeFilter,
            status_filter: WatchHistoryStatusFilter
    ) -> list[Union[WatchHistoryFilmRecord, WatchHistoryShowRecord]]:
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
                    watch_history_table.c.id ==
                    watch_history_shows_table.c.watch_history_record_id
                )
            elif type_filter == WatchHistoryTypeFilter.SHOWS:
                table = table.join(
                    watch_history_shows_table,
                    watch_history_table.c.id ==
                    watch_history_shows_table.c.watch_history_record_id
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

        records = [
            WatchHistoryFilmRecord.construct(
                id=str(row.id),
                name=row.name,
                datetime=row.datetime,
                is_show=False
            ) if not row.is_show else
            WatchHistoryShowRecord.construct(
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
        return records
