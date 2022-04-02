from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, root_validator, validator

from watched.models import TypeFilter, StatusFilter


class BaseDTO(BaseModel):
    class Config:
        extra = 'forbid'


class AddFilmRecordDTO(BaseDTO):
    user_id: str
    datetime: 'datetime' = Field(default_factory=datetime.now)
    name: str


class UpdateFilmRecordDTO(BaseDTO):
    record_id: str
    user_id: str
    datetime: 'datetime'
    name: str


class AddShowRecordDTO(BaseDTO):
    user_id: str
    datetime: 'datetime' = Field(default_factory=datetime.now)
    media_id: Optional[str]
    name: Optional[str]
    season: Optional[int]
    ep1: Optional[int]
    ep2: Optional[int]
    finished_season: Optional[bool]
    finished_show: bool = False

    @root_validator
    def validate_media_id_name(cls, v: dict) -> dict:
        if v['media_id'] is None and v['name'] is None:
            raise ValueError()
        if v['media_id'] is not None and v['name'] is not None:
            raise ValueError()
        return v

    @root_validator
    def set_finished_season(cls, v: dict) -> dict:
        if v['season'] is not None and v['finished_season'] is None:
            v['finished_season'] = False
        return v


class GetWatchHistoryDTO(BaseDTO):
    user_id: str
    type_filter: TypeFilter
    status_filter: StatusFilter

    @validator('type_filter', pre=True)
    def set_type_filter(cls, v: Optional[str]) -> TypeFilter:
        if v is None:
            return TypeFilter.ALL
        return TypeFilter(v)

    @validator('status_filter', pre=True)
    def set_status_filter(cls, v: Optional[str]) -> StatusFilter:
        if v is None:
            return StatusFilter.ALL
        return StatusFilter(v)
