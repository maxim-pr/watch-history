from watched.models import MediaType, ShowRecord


class DomainError(Exception):
    pass


class RecordDoesNotExist(DomainError):
    def __init__(self, record_id: str):
        self.record_id = record_id
        super().__init__(f'watch history record does not exist: {record_id}')


class AccessError(DomainError):
    def __init__(self, record_id: str, user_id: str):
        self.record_id = record_id
        self.user_id = user_id
        super().__init__(f'user id={user_id} tried to access '
                         f'record id={record_id}')


class MediaTypeInconsistency(DomainError):
    def __init__(self, expected_type: MediaType, got_type: MediaType):
        self.expected_type = expected_type
        self.got_type = got_type
        super().__init__(f'expected {expected_type}, got {got_type}')


class FilmAlreadyWatched(DomainError):
    def __init__(self, user_id: str, name: str, record_id: str):
        self.user_id = user_id
        self.name = name
        self.record_id = record_id
        super().__init__()


class ShowRecordInconsistency(DomainError):
    def __init__(self, prev_record: ShowRecord):
        self.prev_record = prev_record
        super().__init__('show record to be inserted is not consistent'
                         'with previous one')
