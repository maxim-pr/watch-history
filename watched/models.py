from datetime import datetime
from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, Field


class WatchEvent(BaseModel):
    user_id: str
    name: str
    datetime: 'datetime' = Field(default_factory=datetime.now)
    is_show: bool


class WatchEventWithID(WatchEvent):
    id: str


class WatchEventFilm(WatchEvent):
    is_show: bool = False


class WatchEventFilmWithID(WatchEventWithID, WatchEventFilm):
    pass


class WatchEventShow(WatchEvent):
    is_show: bool = True
    first_episode: Optional[int]
    last_episode: Optional[int]
    season: Optional[int]
    finished_season: bool = False
    finished_show: bool = False


class WatchEventShowWithID(WatchEventWithID, WatchEventShow):
    pass


class WatchHistory(BaseModel):
    __root__: list[Union[WatchEventFilmWithID, WatchEventShowWithID]]


class Watched(BaseModel):
    watch_event_id: str
    watch_event: WatchEvent
    score: Optional[int]
    review: Optional[str]


class WatchedFilm(Watched):
    watch_event: WatchEventFilm


class WatchedShow(Watched):
    watch_event: WatchEventShow


class WatchHistoryTypeFilter(Enum):
    FILMS = 'films'
    SHOWS = 'shows'
    ALL = 'all'


class WatchHistoryStatusFilter(Enum):
    IN_PROGRESS = 'in_progress'
    FINISHED = 'finished'
    ALL = 'all'
