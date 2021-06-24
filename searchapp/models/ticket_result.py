from dataclasses import dataclass
from typing import List, Optional

from searchapp.repository.models.user import User
from searchapp.repository.models.ticket import Ticket

@dataclass
class TicketResult:
    ticket: Ticket
    assignee: Optional[User] = None