from typing import Optional

from ..models import (
    WatchHistoryFilmRecord, WatchHistoryShowRecord,
    WatchHistory, WatchHistoryTypeFilter, WatchHistoryStatusFilter,
    WatchedFilm, WatchedShow
)
from ..repositories.watch_history import WatchHistoryRepository
from ..repositories.watched import WatchedRepository


class WatchHistoryService:

    def __init__(self,
                 watch_history_repo: WatchHistoryRepository,
                 watched_repo: WatchedRepository):
        self._watch_history_repo = watch_history_repo
        self._watched_repo = watched_repo

    async def add_film(self, film: WatchHistoryFilmRecord) -> tuple[str, str]:
        watch_history_record_id = await self._watch_history_repo.add_film(film)
        watched_id = await self._watched_repo.add(
            WatchedFilm(
                watch_history_record_id=watch_history_record_id,
                watch_event=film
            )
        )
        return watch_history_record_id, watched_id

    async def add_show(self, show: WatchHistoryShowRecord) -> tuple[str, Optional[str]]:
        watch_history_record_id = await self._watch_history_repo.add_show(show)
        if show.finished_show:
            watched_id = await self._watched_repo.add(
                WatchedShow(
                    watch_history_record_id=watch_history_record_id,
                    watch_event=show
                )
            )
            return watch_history_record_id, watched_id

        return watch_history_record_id, None

    async def get_watch_history(
            self, user_id: str,
            type_filter: WatchHistoryTypeFilter,
            status_filter: WatchHistoryStatusFilter
    ) -> WatchHistory:
        watch_history_records = await self._watch_history_repo.get_watch_history_records(
            user_id, type_filter, status_filter
        )
        return WatchHistory.parse_obj(watch_history_records)
