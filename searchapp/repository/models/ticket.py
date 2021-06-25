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

    def __str__(self):
        return f"""
_id: {self._id}
created_at: {self.created_at}
type: {self.type}
subject: {self.subject}
assignee_id: {self.assignee_id}
tags: {self.tags}
"""
