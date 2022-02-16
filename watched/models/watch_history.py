from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class WatchEvent(BaseModel):
    user_id: str
    name: str
    datetime: 'datetime' = Field(default_factory=datetime.now)
    is_show: bool


class Film(WatchEvent):
    pass


class Show(WatchEvent):
    first_episode: int
    last_episode: int
    season: Optional[int] = None
    finished_season: Optional[bool] = False
    finished_show: Optional[bool] = False
