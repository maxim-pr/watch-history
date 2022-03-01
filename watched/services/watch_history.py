from ..models import (
    WatchHistoryFilmRecord, WatchHistoryShowRecord,
    WatchHistory, WatchHistoryTypeFilter, WatchHistoryStatusFilter,
)
from ..repositories.watch_history import WatchHistoryRepository


class WatchHistoryService:

    def __init__(self, watch_history_repo: WatchHistoryRepository):
        self._watch_history_repo = watch_history_repo

    async def add_film(self, film: WatchHistoryFilmRecord) -> str:
        watch_history_record_id = await self._watch_history_repo.\
            add_film_record(film)
        return watch_history_record_id

    async def update_film(self, record_id: str, film: WatchHistoryFilmRecord):
        if not self._watch_history_repo.film_record_exists(record_id):
            raise RecordDoesNotExistError(record_id)
        await self._watch_history_repo.update_film_record(record_id, film)

    async def add_show(self, show: WatchHistoryShowRecord) -> str:
        watch_history_record_id = await self._watch_history_repo.\
            add_show_record(show)
        return watch_history_record_id

    async def update_show(self, record_id: str, show: WatchHistoryShowRecord):
        if not self._watch_history_repo.show_record_exists(record_id):
            raise RecordDoesNotExistError(record_id)
        await self._watch_history_repo.update_show_record(record_id, show)

    async def get_watch_history(self, user_id: str,
                                type_filter: WatchHistoryTypeFilter,
                                status_filter: WatchHistoryStatusFilter
                                ) -> WatchHistory:
        watch_history_records = await self._watch_history_repo.\
            get_watch_history_records(user_id, type_filter, status_filter)
        return WatchHistory.parse_obj(watch_history_records)


class RecordDoesNotExistError(Exception):
    def __init__(self, record_id: str):
        self.record_id = record_id
        super().__init__(f'watch history record does not exist: {record_id}')
