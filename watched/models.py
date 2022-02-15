from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class BaseWatched:
    name: str
    datetime: datetime
    user_id: str
    score: Optional[int] = None
    review: Optional[str] = None


@dataclass
class WatchedFilm(BaseWatched):
    pass


@dataclass
class WatchedShow(BaseWatched):
    season: Optional[int] = None
    first_episode: Optional[int] = None
    last_episode: Optional[int] = None
