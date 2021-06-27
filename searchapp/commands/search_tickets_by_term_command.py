from typing import List

from searchapp.models.command_result import CommandResult
from searchapp.commands.command import Command

class SearchTicketsByTermCommand(Command):

    def run(self, args: List[str]) -> CommandResult:
        term, value = args
        results = self.search_service.search_tickets(term, value)

        return CommandResult(
            title=f"Searching Tickets for {term} with a value {value}",
            result_list=results
        )
