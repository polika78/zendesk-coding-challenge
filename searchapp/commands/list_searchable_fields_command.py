from typing import List

from searchapp.models.search_result.command_result import CommandResult
from searchapp.commands.command import Command

class ListSearchableFieldsCommand(Command):

    def run(self, args: List) -> CommandResult:

        user_terms = self.search_service.get_user_search_terms()
        ticket_terms = self.search_service.get_ticket_search_terms()

        return CommandResult(
            title=None,
            result_list=(user_terms, ticket_terms)
        )
