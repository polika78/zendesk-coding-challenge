from dataclasses import dataclass
from typing import List


@dataclass
class Ticket:
    _id: int
    created_at: str
    type: str
    subject: str
    assignee_id: int
    tags: List[str]
