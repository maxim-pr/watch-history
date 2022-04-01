from abc import ABC, abstractmethod

from watched.models import WatchHistory
from .dto import AddFilmRecordDTO, UpdateFilmRecordDTO, AddShowRecordDTO


class Service(ABC):
    @abstractmethod
    async def add_film_record(self, dto: AddFilmRecordDTO) -> str:
        """
        Raises :class:`FilmAlreadyWatched`

        :return: id of added record
        """
        raise NotImplementedError()

    @abstractmethod
    async def update_film_record(self, dto: UpdateFilmRecordDTO):
        """
        Raises :class:`RecordDoesNotExist`, :class:`AccessError`,
        :class:`MediaTypeInconsistency`
        """
        raise NotImplementedError()

    @abstractmethod
    async def add_show_record(self, dto: AddShowRecordDTO) -> str:
        """
        Raises :class:`InconsistentShowRecord`

        :return: id of added record
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_watch_history(self) -> WatchHistory:
        raise NotImplementedError()
