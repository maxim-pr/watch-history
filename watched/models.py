from datetime import datetime
from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, Field


class WatchHistoryRecord(BaseModel):
    id: Optional[str]
    user_id: str
    name: str
    datetime: 'datetime' = Field(default_factory=datetime.now)
    is_show: bool


class WatchHistoryFilmRecord(WatchHistoryRecord):
    is_show: bool = False


class WatchHistoryShowRecord(WatchHistoryRecord):
    is_show: bool = True
    first_episode: Optional[int]
    last_episode: Optional[int]
    season: Optional[int]
    finished_season: bool = False
    finished_show: bool = False


class WatchHistory(BaseModel):
    __root__: list[Union[WatchHistoryFilmRecord, WatchHistoryShowRecord]]


class WatchHistoryTypeFilter(Enum):
    FILMS = 'films'
    SHOWS = 'shows'
    ALL = 'all'


class WatchHistoryStatusFilter(Enum):
    IN_PROGRESS = 'in_progress'
    FINISHED = 'finished'
    ALL = 'all'


class Watched(BaseModel):
    watch_history_record_id: str
    watch_history_record: WatchHistoryRecord
    score: Optional[int]
    review: Optional[str]


class WatchedFilm(Watched):
    watch_history_record: WatchHistoryFilmRecord


class WatchedShow(Watched):
    watch_history_record: WatchHistoryShowRecord
