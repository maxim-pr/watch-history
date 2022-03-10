from typing import Union, Optional

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.sql import insert, select, update, delete, and_
from sqlalchemy.sql.expression import desc

from watched.db.schema import watch_history_table, watch_history_films_table, \
    watch_history_shows_table, shows_table
from watched.models import (
    WatchHistoryFilmRecord, WatchHistoryShowRecord,
    WatchHistoryTypeFilter, WatchHistoryStatusFilter
)
from .errors import InvalidRecordID


class WatchHistoryBaseRepository:

    def __init__(self, db_engine: AsyncEngine):
        self._db_engine = db_engine

    async def delete_record(self, record_id: str):
        query = delete(watch_history_table).where(
            watch_history_table.c.id == int(record_id)
        )
        async with self._db_engine.begin() as db_conn:
            await db_conn.execute(query)

    async def is_show_record(self, record_id: str) -> bool:
        """
        :raises InvalidRecordID:
        """
        query = select([watch_history_table.c.is_show]).where(
            watch_history_table.c.id == int(record_id)
        )
        async with self._db_engine.begin() as db_conn:
            result = await db_conn.execute(query)
        row = result.fetchone()
        if row is None:
            raise InvalidRecordID(record_id)
        return row.is_show


class WatchHistoryFilmsRepository(WatchHistoryBaseRepository):

    def __init__(self, db_engine: AsyncEngine):
        super().__init__(db_engine)

    async def add_film_record(self, record: WatchHistoryFilmRecord) -> str:
        query1 = insert(watch_history_table).values(
            user_id=int(record.user_id),
            datetime=record.datetime,
            is_show=False
        )
        query2 = insert(watch_history_films_table).values(
            film_name=record.film_name
        )
        async with self._db_engine.begin() as db_conn:
            result = await db_conn.execute(query1)
            record_id = result.inserted_primary_key.id
            query2 = query2.values(id=record_id)
            await db_conn.execute(query2)
        return str(record_id)

    async def update_film_record(self, record: WatchHistoryFilmRecord):
        query1 = update(watch_history_table).where(
            watch_history_table.c.id == int(record.id)
        ).values(
            user_id=int(record.user_id),
            datetime=record.datetime,
            is_show=False
        )
        query2 = update(watch_history_films_table).where(
            watch_history_table.c.id == int(record.id)
        ).values(
            film_name=record.film_name
        )
        async with self._db_engine.begin() as db_conn:
            await db_conn.execute(query1)
            await db_conn.execute(query2)

    async def film_record_exists(self, record_id: str) -> bool:
        try:
            is_show = await super().is_show_record(record_id)
        except InvalidRecordID:
            return False
        return not is_show

    async def find_film_record_by_name(self, user_id: str,
                                       film_name: str) -> Optional[str]:
        query = select([watch_history_table.c.id]).select_from(
            watch_history_table.join(
                watch_history_films_table,
                watch_history_table.c.id == watch_history_films_table.c.id
            )
        ).where(
            and_(
                watch_history_table.c.user_id == int(user_id),
                watch_history_films_table.c.film_name == film_name
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

    async def add_show(self, user_id: str, name: str) -> str:
        query = insert(shows_table).values(
            user_id=int(user_id),
            name=name
        )
        async with self._db_engine.begin() as db_conn:
            result = await db_conn.execute(query)
        show_id = result.inserted_primary_key.id
        return str(show_id)

    async def add_show_record(self, record: WatchHistoryShowRecord) -> str:
        if record.show_id is None:
            raise ValueError()

        query1 = insert(watch_history_table).values(
            user_id=int(record.user_id),
            datetime=record.datetime,
            is_show=True
        )
        query2 = insert(watch_history_shows_table).values(
            show_id=int(record.show_id),
            first_episode=record.first_episode,
            last_episode=record.last_episode,
            season=record.season,
            finished_season=record.finished_season,
            finished_show=record.finished_show
        )
        async with self._db_engine.begin() as db_conn:
            result = await db_conn.execute(query1)
            record_id = result.inserted_primary_key.id
            query2 = query2.values(
                id=record_id
            )
            await db_conn.execute(query2)
        return str(record_id)

    async def update_show_record(self, record: WatchHistoryShowRecord):
        if record.show_id is None:
            raise ValueError()

        query1 = update(watch_history_table).where(
            watch_history_table.c.id == int(record.id)
        ).values(
            user_id=int(record.user_id),
            datetime=record.datetime,
            is_show=True
        )
        query2 = update(watch_history_shows_table).where(
            watch_history_table.c.id == int(record.id)
        ).values(
            show_id=record.show_id,
            first_episode=record.first_episode,
            last_episode=record.last_episode,
            season=record.season,
            finished_season=record.finished_season,
            finished_show=record.finished_show
        )
        async with self._db_engine.begin() as db_conn:
            await db_conn.execute(query1)
            await db_conn.execute(query2)

    async def show_record_exists(self, record_id: str) -> bool:
        try:
            is_show = await super().is_show_record(record_id)
        except InvalidRecordID:
            return False
        return is_show

    async def get_last_show_record(
            self,
            user_id: str,
            show_id: str
    ) -> Optional[WatchHistoryShowRecord]:
        query = select([
            watch_history_table.c.id,
            watch_history_table.c.datetime,
            watch_history_shows_table.c.first_episode,
            watch_history_shows_table.c.last_episode,
            watch_history_shows_table.c.season,
            watch_history_shows_table.c.finished_season,
            watch_history_shows_table.c.finished_show
        ]).select_from(
            watch_history_table.join(
                watch_history_shows_table,
                watch_history_table.c.id == watch_history_shows_table.c.id
            )
        ).where(
            and_(
                watch_history_table.c.user_id == int(user_id),
                watch_history_films_table.c.show_id == int(show_id)
            )
        ).order_by(desc(watch_history_table.c.datetime)).limit(1)

        async with self._db_engine.begin() as db_conn:
            result = await db_conn.execute(query)
        row = result.fetchone()
        if row is None:
            return None

        return WatchHistoryShowRecord.construct(
                id=str(row.id),
                datetime=row.datetime,
                is_show=True,
                show_id=show_id,
                first_episode=row.first_episode,
                last_episode=row.last_episode,
                season=row.season,
                finished_season=row.finished_season,
                finished_show=row.finished_show
            )


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
            watch_history_table.c.datetime,
            watch_history_table.c.is_show
        ]
        table = watch_history_table
        condition = watch_history_table.c.user_id == int(user_id)
        ordering_column = desc(watch_history_table.c.datetime)

        if type_filter != WatchHistoryTypeFilter.FILMS:
            columns += [watch_history_shows_table.c.show_id,
                        shows_table.c.name.label('show_name'),
                        watch_history_shows_table.c.first_episode,
                        watch_history_shows_table.c.last_episode,
                        watch_history_shows_table.c.season,
                        watch_history_shows_table.c.finished_season,
                        watch_history_shows_table.c.finished_show]

            if type_filter == WatchHistoryTypeFilter.ALL:
                table = table.outerjoin(
                    watch_history_shows_table,
                    watch_history_table.c.id == watch_history_shows_table.c.id
                )
            elif type_filter == WatchHistoryTypeFilter.SHOWS:
                table = table.join(
                    watch_history_shows_table,
                    watch_history_table.c.id == watch_history_shows_table.c.id
                )
                condition = and_(
                    condition,
                    watch_history_table.c.is_show
                )

            table = table.join(
                shows_table,
                watch_history_shows_table.c.show_id == shows_table.c.id
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
                datetime=row.datetime,
                is_show=False,
                film_name=row.film_name
            ) if not row.is_show else
            WatchHistoryShowRecord.construct(
                id=str(row.id),
                datetime=row.datetime,
                is_show=True,
                show_id=str(row.show_id),
                show_name=row.show_name,
                first_episode=row.first_episode,
                last_episode=row.last_episode,
                season=row.season,
                finished_season=row.finished_season,
                finished_show=row.finished_show
            ) for row in rows
        ]
        return records
