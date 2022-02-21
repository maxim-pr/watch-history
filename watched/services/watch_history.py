from typing import Optional

from ..models import (
    WatchHistory, WatchEventFilm, WatchEventShow,
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

    async def add_film(self, film: WatchEventFilm) -> tuple[str, str]:
        # TODO: add checks
        watch_event_id = await self._watch_history_repo.add_film(film)
        watched_id = await self._watched_repo.add(
            WatchedFilm(
                watch_event_id=watch_event_id,
                watch_event=film
            )
        )
        return watch_event_id, watched_id

    async def add_show(self, show: WatchEventShow) -> tuple[str, Optional[str]]:
        # TODO: add checks
        watch_event_id = await self._watch_history_repo.add_show(show)
        if show.finished_show:
            watched_id = await self._watched_repo.add(
                WatchedShow(
                    watch_event_id=watch_event_id,
                    watch_event=show
                )
            )
            return watch_event_id, watched_id

        return watch_event_id, None

    async def get(self, user_id: str, filters: dict[str, bool]) -> WatchHistory:
        if filters.get('only_films'):
            films = await self._watch_history_repo.get_films(user_id)
            return WatchHistory.parse_obj(films)
        elif filters.get('only_shows'):
            shows = await self._watch_history_repo.get_shows(user_id)
            return WatchHistory.parse_obj(shows)

        watch_events = await self._watch_history_repo.get_watch_events(user_id)
        return WatchHistory.parse_obj(watch_events)