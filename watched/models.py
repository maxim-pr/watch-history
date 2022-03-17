from datetime import datetime
from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, Field, root_validator


class WatchHistoryRecord(BaseModel):
    id: Optional[str]
    user_id: str
    datetime: 'datetime' = Field(default_factory=datetime.now)
    is_show: bool


class WatchHistoryFilmRecord(WatchHistoryRecord):
    is_show: bool = False
    film_name: str


class WatchHistoryShowRecord(WatchHistoryRecord):
    is_show: bool = True
    show_id: Optional[str]
    show_name: Optional[str]
    season: Optional[int]
    first_episode: Optional[int]
    last_episode: Optional[int]
    finished_season: bool = False
    finished_show: bool = False

    @root_validator
    def validate_1(cls, v: dict) -> dict:
        if v['first_episode'] is not None and v['last_episode'] is not None \
                and v['first_episode'] >= v['last_episode']:
            raise ValueError()
        return v

    @root_validator
    def validate_2(cls, v: dict) -> dict:
        if v['first_episode'] is None and v['last_episode'] is None and \
                v['season'] is None and not v['finished_show']:
            raise ValueError()
        return v

    @root_validator
    def validate_3(cls, v: dict) -> dict:
        if v['season'] is not None and v['first_episode'] is None and \
                not v['finished_season']:
            raise ValueError()
        return v

    @root_validator
    def validate_4(cls, v: dict) -> dict:
        if v['finished_season'] and v['season'] is None:
            raise ValueError()
        return v


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
