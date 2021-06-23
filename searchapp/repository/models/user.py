from dataclasses import dataclass

@dataclass
class User:
    _id: int
    name: str
    created_at: str
    verified: bool
