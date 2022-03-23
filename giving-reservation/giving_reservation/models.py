from dataclasses import dataclass
from datetime import datetime


@dataclass
class Reservation:
    id: int
    name: str
    purpose: str
    created_by: int
    created_at: datetime
    updated_at: datetime
