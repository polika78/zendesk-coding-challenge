from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass
class Ticket:
    _id: int
    created_at: str
    subject: str
    tags: List[str]
    type: Optional[str] = ''
    assignee_id: Optional[Union[int, str]] = ''
