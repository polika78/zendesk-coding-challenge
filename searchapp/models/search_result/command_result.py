from dataclasses import dataclass
from typing import List, Optional, Union, Tuple

from searchapp.models.search_result.user_searchable_fields import UserSearchableFields
from searchapp.models.search_result.ticket_searchable_fields import TicketSearchableFields
from searchapp.models.search_result.user_result import UserResult
from searchapp.models.search_result.ticket_result import TicketResult

@dataclass
class CommandResult:
    title: Optional[str]
    result_list: Union[Tuple[UserSearchableFields, TicketSearchableFields], List[UserResult], List[TicketResult]]
