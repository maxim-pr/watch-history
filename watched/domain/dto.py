from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from watched.models import MediaType, TypeFilter, StatusFilter


@dataclass(slots=True)
class AddMediaDTO:
    type: MediaType
    name: str


@dataclass(slots=True)
class UpdateMediaNameDTO:
    id: str
    name: str


@dataclass(slots=True)
class AddFilmRecordDTO:
    user_id: str
    datetime: 'datetime'
    media_id: str


@dataclass(slots=True)
class UpdateFilmRecordDTO:
    record_id: str
    user_id: str
    datetime: 'datetime'
    media_id: str


@dataclass(slots=True)
class AddShowRecordDTO:
    user_id: str
    datetime: 'datetime'
    media_id: str
    season: Optional[int]
    ep1: Optional[int]
    ep2: Optional[int]
    finished_season: Optional[bool]
    finished_show: bool


@dataclass(slots=True)
class UpdateShowRecordDTO:
    record_id: str
    user_id: str
    datetime: 'datetime'
    media_id: str
    season: Optional[int]
    ep1: Optional[int]
    ep2: Optional[int]
    finished_season: Optional[bool]
    finished_show: bool


@dataclass(slots=True)
class GetPrevShowRecordDTO:
    user_id: str
    datetime: 'datetime'
    media_id: str


@dataclass(slots=True)
class GetRecordsDTO:
    user_id: str
    type_filter: TypeFilter
    status_filter: StatusFilter
