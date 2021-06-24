from dataclasses import dataclass
from typing import List

from searchapp.repository.models.user import User
from searchapp.repository.models.ticket import Ticket

@dataclass
class UserResult:
    user: User
    assigned_tickets: List[Ticket]
