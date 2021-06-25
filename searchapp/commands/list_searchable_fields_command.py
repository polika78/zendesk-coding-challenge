from typing import List

from searchapp.models.search_result.user_terms import UserTerms
from searchapp.models.search_result.ticket_terms import TicketTerms
from searchapp.commands.command import Command

class ListSearchableFieldsCommand(Command):

    def display(self, user_terms: UserTerms, ticket_terms: TicketTerms) -> None:
        print(user_terms)
        print(ticket_terms)

    def run(self, args: List) -> None:

        user_terms = self.search_service.get_user_search_terms()
        ticket_terms = self.search_service.get_ticket_search_terms()

        self.display(user_terms, ticket_terms)
