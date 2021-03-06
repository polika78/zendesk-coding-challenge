from dataclasses import dataclass
from typing import List, Optional

from searchapp.models.user import User
from searchapp.models.ticket import Ticket

@dataclass
class TicketResult:
    ticket: Ticket
    assignee: Optional[User] = None

    def __str__(self):
        return f"""
{self.ticket}
Assignee
{self.assignee}"""
