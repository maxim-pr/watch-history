

class InvalidRecordID(Exception):
    def __init__(self, record_id: str):
        self.record_id = record_id
        super().__init__(f'invalid record id: {record_id}')
