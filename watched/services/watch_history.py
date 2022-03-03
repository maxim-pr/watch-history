from ..models import (
    WatchHistoryFilmRecord, WatchHistoryShowRecord,
    WatchHistory, WatchHistoryTypeFilter, WatchHistoryStatusFilter,
)
from ..repositories.watch_history import WatchHistoryRepository


class WatchHistoryService:

    def __init__(self, watch_history_repo: WatchHistoryRepository):
        self._watch_history_repo = watch_history_repo

    async def add_film(self, film: WatchHistoryFilmRecord) -> str:
        record_id = await self._watch_history_repo.\
            find_film_record_by_name(film.user_id, film.name)
        if record_id is not None:
            raise FilmAlreadyWatchedError(film.user_id, film.name, record_id)

        watch_history_record_id = await self._watch_history_repo.\
            add_film_record(film)
        return watch_history_record_id

    async def update_film(self, film: WatchHistoryFilmRecord):
        """
        :raises RecordDoesNotExistError:
        """
        if not (await self._watch_history_repo.film_record_exists(film.id)):
            raise RecordDoesNotExistError(film.id)
        await self._watch_history_repo.update_film_record(film)

    async def add_show(self, show: WatchHistoryShowRecord) -> str:
        watch_history_record_id = await self._watch_history_repo.\
            add_show_record(show)
        return watch_history_record_id

    async def update_show(self, show: WatchHistoryShowRecord):
        """
        :raises RecordDoesNotExistError:
        """
        if not (await self._watch_history_repo.show_record_exists(show.id)):
            raise RecordDoesNotExistError(show.id)
        await self._watch_history_repo.update_show_record(show)

    async def delete_record(self, record_id: str):
        await self._watch_history_repo.delete_record(record_id)

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


class FilmAlreadyWatchedError(Exception):
    def __init__(self, user_id: str, name: str, record_id: str):
        self.user_id = user_id
        self.name = name
        self.record_id = record_id
        super().__init__(f'film <{name}> already watched by user <{user_id}>: '
                         f'record_id=<{record_id}>')
