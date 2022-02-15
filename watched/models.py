from dataclasses import dataclass
from datetime import datetime


@dataclass
class Film:
    user_id: str
    name: str
    watched_at: datetime
