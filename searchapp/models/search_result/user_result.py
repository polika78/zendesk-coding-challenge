from dataclasses import dataclass
from typing import List

from searchapp.models.user import User
from searchapp.models.ticket import Ticket

@dataclass
class UserResult:
    user: User
    assigned_tickets: List[Ticket]

    def __str__(self):
        return '\n'.join([
            f"{self.user}",
            *[f"{ticket}" for ticket in self.assigned_tickets]
        ])
