from typing import List

from searchapp.models.search_result.command_result import CommandResult
from searchapp.commands.command import Command

class SearchUsersByTermCommand(Command):

    def run(self, args: List[str]) -> CommandResult:
        term, value = args
        results = self.search_service.search_user(term, value)

        return CommandResult(
            title=f"Searching Users for {term} with a value {value}",
            result_list=results
        )
