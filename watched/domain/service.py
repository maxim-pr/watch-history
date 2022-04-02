from watched.api import dto as in_dto
from watched.api.errors import (
    AccessError, RecordDoesNotExist, FilmAlreadyWatched,
    ShowRecordInconsistency, MediaTypeInconsistency
)
from watched.models import MediaType, ShowRecord, WatchHistory
from .dto import AddMediaDTO, AddFilmRecordDTO, AddShowRecordDTO,\
    GetPrevShowRecordDTO, GetRecordsDTO
from .storage import Storage


class Service:
    def __init__(self, storage: Storage):
        self._storage = storage

    async def add_film_record(self, dto: in_dto.AddFilmRecordDTO) -> str:
        record_id = await self._storage.find_film_record_by_name(dto.user_id,
                                                                 dto.name)
        if record_id is not None:
            raise FilmAlreadyWatched(dto.user_id, dto.name, record_id)

        add_media_dto = AddMediaDTO(type=MediaType.FILM, name=dto.name)
        media_id = await self._storage.add_media(add_media_dto)

        add_film_record_dto = AddFilmRecordDTO(
            user_id=dto.user_id, datetime=dto.datetime, media_id=media_id
        )
        record_id = await self._storage.add_film_record(add_film_record_dto)
        return record_id

    async def update_film_record(self, dto: in_dto.UpdateFilmRecordDTO):
        record = await self._storage.get_record(dto.record_id)
        if record is None:
            raise RecordDoesNotExist(dto.record_id)
        if record.user_id != dto.user_id:
            raise AccessError(dto.record_id, dto.user_id)
        if record.media.type != MediaType.FILM:
            raise MediaTypeInconsistency(MediaType.FILM, record.media.type)

        if dto.name != record.media.name:
            await self._storage.update_media_name(media_id=record.media.id,
                                                  name=dto.name)
        if dto.datetime != record.datetime:
            await self._storage.update_film_record_datetime(
                record_id=dto.record_id, dt=dto.datetime
            )

    async def add_show_record(self,
                              dto: in_dto.AddShowRecordDTO) -> tuple[str, str]:
        if dto.media_id is None:
            add_media_dto = AddMediaDTO(type=MediaType.SHOW, name=dto.name)
            media_id = await self._storage.add_media(add_media_dto)
        else:
            media_id = dto.media_id
            get_prev_show_record_dto = GetPrevShowRecordDTO(
                user_id=dto.user_id, datetime=dto.datetime,
                media_id=dto.media_id
            )
            prev_record = await self._storage.get_prev_show_record(
                get_prev_show_record_dto
            )
            if not self._validate_against_prev_record(dto, prev_record):
                raise ShowRecordInconsistency(prev_record)

        add_show_record_dto = AddShowRecordDTO(
            user_id=dto.user_id, datetime=dto.datetime, media_id=media_id,
            season=dto.season, ep1=dto.ep1, ep2=dto.ep2,
            finished_season=dto.finished_season,
            finished_show=dto.finished_season
        )
        record_id = await self._storage.add_show_record(add_show_record_dto)
        return record_id, media_id

    @staticmethod
    def _validate_against_prev_record(dto: in_dto.AddShowRecordDTO,
                                      prev_record: ShowRecord) -> bool:
        if prev_record.finished_show:
            return False

        if prev_record.season is None and dto.season is not None:
            return False
        if prev_record.season is not None and dto.season is None:
            return False

        if prev_record.season is not None and dto.season is not None:
            if prev_record.season > dto.season:
                return False
            if prev_record.season == dto.season:
                if prev_record.finished_season:
                    return False
                if dto.ep1 is not None:
                    last_watched_ep = prev_record.ep2 or prev_record.ep1
                    if dto.ep1 <= last_watched_ep:
                        return False

        return True

    async def get_watch_history(
            self, dto: in_dto.GetWatchHistoryDTO) -> WatchHistory:
        get_records_dto = GetRecordsDTO(
            user_id=dto.user_id, type_filter=dto.type_filter,
            status_filter=dto.status_filter
        )
        records = await self._storage.get_records(get_records_dto)
        return WatchHistory.parse_obj(records)
