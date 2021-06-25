from typing import List, Union

from searchapp.search_service import SearchService
from searchapp.commands.list_searchable_fields_command import ListSearchableFieldsCommand
from searchapp.commands.search_users_by_term_command import SearchUsersByTermCommand
from searchapp.commands.search_tickets_by_term_command import SearchTicketsByTermCommand
from searchapp.errors.command_not_found_error import CommandNotFoundError

class CommandHandler:

    def __init__(self, search_service: SearchService) -> None:
        self.search_service = search_service

    def command_parser(self, command_str: str) -> \
        Union[ListSearchableFieldsCommand, SearchUsersByTermCommand, SearchTicketsByTermCommand]:
        if command_str == "list_searchable_fields":
            return ListSearchableFieldsCommand(self.search_service)
        elif command_str == "search_users_by_term":
            return SearchUsersByTermCommand(self.search_service)
        elif command_str == "search_tickets_by_term":
            return SearchTicketsByTermCommand(self.search_service)
        raise CommandNotFoundError()

    def handle(self, command_str: str, args: List[str]) -> None:
        command = self.command_parser(command_str)

        command.run(args)
