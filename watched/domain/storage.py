from abc import ABC, abstractmethod
from typing import Optional

from watched.models import BaseRecord, ShowRecord, Record
from .dto import (
    AddMediaDTO, AddFilmRecordDTO, UpdateFilmRecordDTO,
    AddShowRecordDTO, UpdateShowRecordDTO, GetPrevShowRecordDTO,
    GetWatchHistoryRecordsDTO
)


class Storage(ABC):
    @abstractmethod
    async def close(self):
        raise NotImplementedError()

    @abstractmethod
    async def get_record(self, record_id: str) -> Optional[BaseRecord]:
        raise NotImplementedError()

    @abstractmethod
    async def delete_record(self, record_id: str) -> bool:
        """
        :return: flag whether record_id refers to existent record
        (i.e. that the record was indeed deleted)
        """
        raise NotImplementedError()

    @abstractmethod
    async def add_media(self, dto: AddMediaDTO) -> str:
        """
        :return: id of added media (film/show)
        """
        raise NotImplementedError()

    @abstractmethod
    async def delete_media(self, media_id: str) -> bool:
        """
        :return: flag whether media_id refers to existent media
        (i.e. that the media was indeed deleted)
        """
        raise NotImplementedError()

    @abstractmethod
    async def add_film_record(self, dto: AddFilmRecordDTO) -> str:
        """
        :return: id of added record
        """
        raise NotImplementedError()

    @abstractmethod
    async def update_film_record(self, dto: UpdateFilmRecordDTO) -> bool:
        """
        :return: flag whether dto.record_id refers to existent record
        (i.e. that the update was indeed performed)
        """
        raise NotImplementedError()

    @abstractmethod
    async def find_film_record_by_name(self, user_id: str,
                                       name: str) -> Optional[str]:
        """
        :return: id of found record (if found such) or None otherwise
        """
        raise NotImplementedError()

    @abstractmethod
    async def add_show_record(self, dto: AddShowRecordDTO) -> str:
        """
        :return: id of added record
        """
        raise NotImplementedError()

    @abstractmethod
    async def update_show_record(self, dto: UpdateShowRecordDTO) -> bool:
        """
        :return: flag whether dto.record_id refers to existent record
        (i.e. that the update was indeed performed)
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_prev_show_record(
            self, dto: GetPrevShowRecordDTO) -> Optional[ShowRecord]:
        raise NotImplementedError()

    @abstractmethod
    async def get_watch_history_records(
            self, dto: GetWatchHistoryRecordsDTO) -> list[Record]:
        raise NotImplementedError()
