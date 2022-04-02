from datetime import datetime
from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel


class MediaType(Enum):
    FILM = 'film'
    SHOW = 'show'


class Media(BaseModel):
    id: str
    type: MediaType
    name: str


class Film(Media):
    type = MediaType.FILM


class Show(Media):
    type = MediaType.SHOW


class BaseRecord(BaseModel):
    id: str
    user_id: str
    datetime: datetime
    media: Media


class FilmRecord(BaseRecord):
    media: Film


class ShowRecord(BaseRecord):
    media: Show
    season: Optional[int]
    ep1: Optional[int]
    ep2: Optional[int]
    finished_season: bool = False
    finished_show: bool = False


Record = Union[FilmRecord, ShowRecord]


class WatchHistory(BaseModel):
    __root__: list[Record]


class TypeFilter(Enum):
    FILMS = 'films'
    SHOWS = 'shows'
    ALL = 'all'


class StatusFilter(Enum):
    IN_PROGRESS = 'in_progress'
    FINISHED = 'finished'
    ALL = 'all'


class Review(BaseModel):
    score: Optional[int]
    review: Optional[str]
