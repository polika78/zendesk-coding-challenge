from typing import List

from searchapp.models.search_result.ticket_result import TicketResult
from searchapp.commands.command import Command

class SearchTicketsByTermCommand(Command):

    def display(self, term: str, value: str, results: List[TicketResult]) -> None:
        print(f"\nSearching Tickets for {term} with a value {value}")
        if not results:
            print("No results found")
        else:
            for result in results:
                print(result)

    def run(self, args: List[str]) -> None:
        term, value = args
        results = self.search_service.search_tickets(term, value)

        self.display(term, value, results)
