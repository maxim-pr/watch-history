from ...models import WatchHistoryShowRecord


class RecordDoesNotExist(Exception):
    def __init__(self, record_id: str):
        self.record_id = record_id
        super().__init__(f'watch history record does not exist: {record_id}')


class FilmAlreadyWatched(Exception):
    def __init__(self, user_id: str, name: str, record_id: str):
        self.user_id = user_id
        self.name = name
        self.record_id = record_id
        super().__init__(f'film <{name}> already watched by user <{user_id}>: '
                         f'record_id=<{record_id}>')


class InconsistentShowRecord(Exception):
    def __init__(self, last_show_record: WatchHistoryShowRecord):
        self.last_show_record = last_show_record
        super().__init__('show record to be inserted is not consistent'
                         'with last one')
