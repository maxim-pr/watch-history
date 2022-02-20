from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class WatchEvent(BaseModel):
    user_id: str
    name: str
    datetime: 'datetime' = Field(default_factory=datetime.now)


class WatchEventFilm(WatchEvent):
    pass


class WatchEventShow(WatchEvent):
    first_episode: Optional[int]
    last_episode: Optional[int]
    season: Optional[int]
    finished_season: Optional[bool] = False
    finished_show: Optional[bool] = False


class Watched(BaseModel):
    watch_event_id: str
    watch_event: WatchEvent
    score: Optional[int]
    review: Optional[str]


class WatchedFilm(Watched):
    watch_event: WatchEventFilm


class WatchedShow(Watched):
    watch_event: WatchEventShow
