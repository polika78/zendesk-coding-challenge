from dataclasses import dataclass
from typing import List, Optional, Union

@dataclass
class User:
    _id: int
    name: str
    created_at: str
    verified: Optional[Union[bool, str]] = ''
