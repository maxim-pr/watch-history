from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, root_validator


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
    finished_season: bool = False
    finished_show: bool = False

    @root_validator
    def validate_media_id_name(cls, v: dict) -> dict:
        if v['media_id'] is None and v['name'] is None:
            raise ValueError()
        if v['media_id'] is not None and v['name'] is not None:
            raise ValueError()
        return v
