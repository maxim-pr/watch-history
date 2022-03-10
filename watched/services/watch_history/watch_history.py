from watched.models import (
    WatchHistoryFilmRecord, WatchHistoryShowRecord,
    WatchHistory, WatchHistoryTypeFilter, WatchHistoryStatusFilter,
)
from watched.repositories.watch_history import WatchHistoryRepository
from .errors import RecordDoesNotExist, FilmAlreadyWatched, InconsistentShowRecord


class WatchHistoryService:

    def __init__(self, watch_history_repo: WatchHistoryRepository):
        self._watch_history_repo = watch_history_repo

    async def add_film_record(self, record: WatchHistoryFilmRecord) -> str:
        """
        :raises FilmAlreadyWatched:
        """
        record_id = await self._watch_history_repo.\
            find_film_record_by_name(record.user_id, record.film_name)
        if record_id is not None:
            raise FilmAlreadyWatched(record.user_id, record.film_name, record_id)

        record_id = await self._watch_history_repo.add_film_record(record)
        return record_id

    async def update_film_record(self, record: WatchHistoryFilmRecord):
        """
        :raises RecordDoesNotExist:
        """
        if not (await self._watch_history_repo.film_record_exists(record.id)):
            raise RecordDoesNotExist(record.id)
        await self._watch_history_repo.update_film_record(record)

    async def add_show_record(self, record: WatchHistoryShowRecord) -> str:
        """
        :raises InvalidShowRecord:
        """
        if record.show_id is None:
            record.show_id = await self._watch_history_repo.add_show(
                record.user_id, record.show_name
            )
        else:
            last_record = await self._watch_history_repo.\
                get_last_show_record(record.user_id, record.show_id)
            if not self._validate_show_record(record, last_record):
                raise InconsistentShowRecord(last_record)

        record_id = await self._watch_history_repo.add_show_record(record)
        return record_id

    @staticmethod
    def _validate_show_record(record: WatchHistoryShowRecord,
                              last_record: WatchHistoryShowRecord) -> bool:
        if last_record.finished_show:
            return False
        if last_record.season is not None and record.season is not None:
            if last_record.season > record.season:
                return False
            if last_record.season == record.season and last_record.finished_season:
                return False

            if last_record.first_episode is not None and record.first_episode is not None:
                last_watched_episode = last_record.first_episode
                if last_record.last_episode is not None:
                    last_watched_episode = last_record.last_episode
                if record.first_episode <= last_watched_episode:
                    return False

        return True

    async def update_show_record(self, record: WatchHistoryShowRecord):
        """
        :raises RecordDoesNotExist:
        """
        if not (await self._watch_history_repo.show_record_exists(record.id)):
            raise RecordDoesNotExist(record.id)
        await self._watch_history_repo.update_show_record(record)

    async def delete_record(self, record_id: str):
        await self._watch_history_repo.delete_record(record_id)

    async def get_watch_history(self, user_id: str,
                                type_filter: WatchHistoryTypeFilter,
                                status_filter: WatchHistoryStatusFilter
                                ) -> WatchHistory:
        records = await self._watch_history_repo.\
            get_watch_history_records(user_id, type_filter, status_filter)
        return WatchHistory.parse_obj(records)
