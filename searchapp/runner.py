import json

from searchapp.repository.user_repo import UserRepo
from searchapp.repository.ticket_repo import TicketRepo
from searchapp.search_service import SearchService
from searchapp.command_handler import CommandHandler
from searchapp.ui import UI
from searchapp.errors.command_not_found_error import CommandNotFoundError
from searchapp.errors.unknown_search_term_error import UnknownSearchTermError


def create_repos():
    with open('./searchapp/repository/data/users.json') as users_file:
        users_records = json.load(users_file)
    user_repo = UserRepo()
    user_repo.load(users_records)
    with open('./searchapp/repository/data/tickets.json') as tickets_file:
        ticket_records = json.load(tickets_file)
    ticket_repo = TicketRepo()
    ticket_repo.load(ticket_records)
    return user_repo, ticket_repo

def main():
    user_repo, ticket_repo = create_repos()
    search_service = SearchService(user_repo, ticket_repo)
    command_handler = CommandHandler(search_service)
    ui = UI()

    ui.display_welcome_message()
    while True:
        ui.display_intro()
        entry, sub_entries = ui.input_handler()

        if entry == 'quit':
            break

        command, args = ui.parse_command(entry, sub_entries)

        try:
            command_result = command_handler.handle(command, args)
            ui.display_command_result(command_result)
        except CommandNotFoundError:
            print("You selected wrong command. Please follow the instructions.")
        except UnknownSearchTermError:
            print("You entered unknown searching term. Please check the list of searchable fields.")

    print("Bye!~")

    