from typing import List

from searchapp.models.user_result import UserResult
from searchapp.repository.user_repo import UserRepo
from searchapp.repository.ticket_repo import TicketRepo
class SearchService:

    def __init__(self, user_repo: UserRepo, ticket_repo: TicketRepo) -> None:
        self.user_repo = user_repo
        self.ticket_repo = ticket_repo

    def search_user(self, term: str, value: str) -> List[UserResult]:
        users = self.user_repo.search_by_term(term, value)
        return [
            UserResult(
                user,
                assigned_tickets=self.ticket_repo.search_by_term('assignee_id', str(user._id))
            ) for user in users
        ]
