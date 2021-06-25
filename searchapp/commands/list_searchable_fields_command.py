from typing import List, Union

from searchapp.models.user_terms import UserTerms
from searchapp.models.ticket_terms import TicketTerms
from searchapp.commands.command import Command

class ListSearchableFieldsCommand(Command):

    def display(self, result: List[Union[UserTerms, TicketTerms]]) -> None:
        print(result)

    def run(self, args: List[str]) -> None:
        repo, = args

        if repo == 'user':
            result = self.search_service.get_user_search_terms()
        elif repo == 'ticket':
            result = self.search_service.get_ticket_search_terms()

        self.display(result)
