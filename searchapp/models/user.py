from dataclasses import dataclass
from typing import List, Optional, Union

@dataclass
class User:
    _id: int
    name: str
    created_at: str
    verified: Optional[Union[bool, str]] = ''

    def __str__(self):
        return f"""
_id: {self._id}
name: {self.name}
created_at: {self.created_at}
verified: {self.verified}
"""
