from typing import Callable, Union

from searchapp.search_service import SearchService
from searchapp.repository.user_repo import UserRepo
from searchapp.repository.ticket_repo import TicketRepo

class CommandHandler:

    def __init__(self, search_service: SearchService) -> None:
        self.search_service = search_service

    def command_parser(self, command: str) -> Callable:
        command_map = {
            'get_search_terms': self.get_search_terms,
        }
        return command_map[command]

    def get_search_terms(self, repo: Union[UserRepo, TicketRepo]) -> None:
        if repo == 'user':
            print(self.search_service.get_user_search_terms())
        elif repo == 'ticket':
            print(self.search_service.get_ticket_search_terms())

    def handle(self, command: str, args: str) -> None:
        command_func = self.command_parser(command)

        command_func(args)
