from datetime import datetime
from typing import Optional

from sqlalchemy import String
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import insert, select, update, delete, and_, or_
from sqlalchemy.sql.expression import cast, desc

from watched.domain.dto import (
    AddMediaDTO, UpdateMediaNameDTO, AddFilmRecordDTO,
    AddShowRecordDTO, GetPrevShowRecordDTO, GetRecordsDTO
)
from watched.models import (
    MediaType, Media, Film, Show, BaseRecord, FilmRecord, ShowRecord, Record,
    TypeFilter, StatusFilter
)
from .db.schema import (
    watch_history_table, watch_history_shows_table, media_table
)


class BaseRepository:
    def __init__(self, db_url: str, log_sql: bool = False):
        self._engine = create_async_engine(url=db_url, echo=log_sql)

    async def close(self):
        await self._engine.dispose()

    async def get_record(self, record_id: str) -> Optional[BaseRecord]:
        query = select([
            cast(watch_history_table.c.user_id, String),
            cast(watch_history_table.c.media_id, String),
            watch_history_table.c.datetime,
            media_table.c.type, media_table.c.name
        ]).select_from(
            watch_history_table.join(
                media_table, watch_history_table.c.media_id == media_table.c.id
            )
        ).where(watch_history_table.c.id == int(record_id))

        async with self._engine.begin() as conn:
            result = await conn.execute(query)
        row = result.fetchone()
        if row is None:
            return None

        record = BaseRecord.construct(
            id=record_id, user_id=row.user_id, datetime=row.datetime,
            media=Media(id=row.media_id, type=MediaType(row.type),
                        name=row.name)
        )
        return record

    async def delete_record(self, record_id: str) -> bool:
        query = delete(watch_history_table).where(
            watch_history_table.c.record_id == int(record_id)
        )
        async with self._engine.begin() as conn:
            result = await conn.execute(query)
        return result.rowcount != 0

    async def add_media(self, dto: AddMediaDTO) -> str:
        query = insert(media_table).values(type=dto.type.value, name=dto.name)
        async with self._engine.begin() as conn:
            result = await conn.execute(query)
        media_id = result.inserted_primary_key.id
        return str(media_id)

    async def update_media_name(self, dto: UpdateMediaNameDTO) -> bool:
        query = update(media_table).values(name=dto.name).where(
            media_table.c.id == int(dto.id)
        )
        async with self._engine.begin() as conn:
            result = await conn.execute(query)
        return result.rowcount != 0

    async def delete_media(self, media_id: str) -> bool:
        query = delete(media_table).where(media_table.c.id == int(media_id))
        async with self._engine.begin() as conn:
            result = await conn.execute(query)
        return result.rowcount != 0


class FilmRecordsRepository(BaseRepository):
    async def add_film_record(self, dto: AddFilmRecordDTO) -> str:
        query = insert(watch_history_table).values(
            user_id=int(dto.user_id),
            datetime=dto.datetime,
            media_id=int(dto.media_id)
        )
        async with self._engine.begin() as conn:
            result = await conn.execute(query)
        record_id = result.inserted_primary_key.id
        return str(record_id)

    async def update_film_record_datetime(self, record_id: str,
                                          dt: 'datetime') -> bool:
        query = update(watch_history_table).values(datetime=dt).where(
            watch_history_table.c.id == int(record_id)
        )
        async with self._engine.begin() as conn:
            result = await conn.execute(query)
        return result.rowcount != 0

    async def find_film_record_by_name(self, user_id: str,
                                       name: str) -> Optional[str]:
        query = select([watch_history_table.c.id]).select_from(
            watch_history_table.join(
                media_table,
                watch_history_table.c.media_id == media_table.c.id
            )
        ).where(
            and_(
                watch_history_table.c.user_id == int(user_id),
                media_table.c.name == name
            )
        )
        async with self._engine.begin() as conn:
            result = await conn.execute(query)
        row = result.fetchone()
        if row is None:
            return None
        return str(row.id)


class ShowRecordsRepository(BaseRepository):
    async def add_show_record(self, dto: AddShowRecordDTO) -> str:
        query1 = insert(watch_history_table).values(
            user_id=int(dto.user_id),
            datetime=dto.datetime,
            media_id=int(dto.media_id)
        )
        query2 = insert(watch_history_shows_table).values(
            season=dto.season, ep1=dto.ep1, ep2=dto.ep2,
            finished_season=dto.finished_season,
            finished_show=dto.finished_show
        )
        async with self._engine.begin() as conn:
            result = await conn.execute(query1)
            record_id = result.inserted_primary_key.id
            await conn.execute(query2, {'id': record_id})
        return str(record_id)

    async def get_prev_show_record(
            self, dto: GetPrevShowRecordDTO) -> Optional[ShowRecord]:
        query = select([
            cast(watch_history_table.c.id, String),
            watch_history_table.c.datetime,
            watch_history_shows_table.c.season,
            watch_history_shows_table.c.ep1,
            watch_history_shows_table.c.ep2,
            watch_history_shows_table.c.finished_season,
            watch_history_shows_table.c.finished_show
        ]).select_from(
            watch_history_table.join(
                watch_history_shows_table,
                watch_history_table.c.id == watch_history_shows_table.c.id
            )
        ).where(
            and_(
                watch_history_table.c.user_id == int(dto.user_id),
                watch_history_table.c.media_id == int(dto.media_id),
                watch_history_table.c.datetime < dto.datetime
            )
        ).order_by(desc(watch_history_table.c.datetime)).limit(1)

        async with self._engine.begin() as conn:
            result = await conn.execute(query)
        row = result.fetchone()
        if row is None:
            return None

        # show name is not set(
        return ShowRecord.construct(**row, user_id=dto.user_id,
                                    media=Show.construct(id=row.media_id))


class Storage(FilmRecordsRepository, ShowRecordsRepository):
    async def get_records(self,
                          dto: GetRecordsDTO) -> list[Record]:
        columns = [
            cast(watch_history_table.c.id, String),
            watch_history_table.c.datetime,
            cast(watch_history_table.c.media_id, String),
            media_table.c.type,
            media_table.c.name
        ]
        table = watch_history_table.join(
            media_table, watch_history_table.c.media_id == media_table.c.id
        )
        condition = watch_history_table.c.user_id == int(dto.user_id)
        ordering_column = desc(watch_history_table.c.datetime)

        if dto.type_filter != TypeFilter.FILMS:
            columns += [watch_history_shows_table.c.season,
                        watch_history_shows_table.c.ep1,
                        watch_history_shows_table.c.ep2,
                        watch_history_shows_table.c.finished_season,
                        watch_history_shows_table.c.finished_show]

            if dto.type_filter == TypeFilter.SHOWS:
                table = table.join(
                    watch_history_shows_table,
                    watch_history_table.c.id == watch_history_shows_table.c.id
                )
                condition = and_(
                    condition, media_table.c.type == MediaType.FILM.value
                )
            elif dto.type_filter == TypeFilter.ALL:
                table = table.outerjoin(
                    watch_history_shows_table,
                    watch_history_table.c.id == watch_history_shows_table.c.id
                )

            if dto.status_filter == StatusFilter.FINISHED:
                condition = and_(
                    condition,
                    or_(media_table.c.type == MediaType.FILM.value,
                        watch_history_shows_table.c.finished_show)
                )
            elif dto.status_filter == StatusFilter.IN_PROGRESS:
                condition = and_(
                    condition,
                    watch_history_shows_table.c.finished_show == False
                )

        if dto.type_filter == TypeFilter.FILMS:
            condition = and_(
                condition, media_table.c.type == MediaType.FILM.value
            )

        query = select(columns).select_from(table).where(condition).order_by(
            ordering_column
        )
        async with self._engine.begin() as conn:
            result = await conn.execute(query)
        rows = result.fetchall()

        records = [
            FilmRecord.construct(
                id=row.id,
                user_id=dto.user_id,
                datetime=row.datetime,
                media=Film.construct(id=row.media_id, name=row.name)
            ) if row.type == MediaType.FILM.value else
            ShowRecord.construct(
                id=row.id,
                user_id=dto.user_id,
                datetime=row.datetime,
                media=Show.construct(id=row.media_id, name=row.name),
                season=row.season, ep1=row.ep1, ep2=row.ep2,
                finished_season=row.finished_season,
                finished_show=row.finished_show
            ) for row in rows
        ]
        return records
