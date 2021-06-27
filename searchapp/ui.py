
from searchapp.models.command_result import CommandResult

class UI:
    WELCOME_MESSAGE="""
Welcome to Zendesk Search
Type 'quit' to exit at any time, Press 'Enter' to continue
"""
    INSTRUCTION_MESSAGE="""
            Select Search options:
             * Press 1 to search Zendesk
             * Press 2 to view a list of searchable fields
             * Type 'quit' to exit
"""

    def display_welcome_message(self):
        print(UI.WELCOME_MESSAGE)

    def display_intro(self):
        print(UI.INSTRUCTION_MESSAGE)

    def input_handler(self):
        entry = input("")

        if entry == '1':
            repo = input("Select 1) Users or 2) Tickets\n")
            if repo == 'quit':
                return 'quit', None
            if repo not in ('1', '2'):
                return 'unknown', None
            search_term = input("Enter search term\n")
            if search_term == 'quit':
                return 'quit', None
            value = input("Enter search value\n")
            return entry, (repo, search_term, value)

        return entry, None

    def parse_command(self, entry, sub_entries):
        if entry == '1':
            repo, term, value = sub_entries
            if repo == '1':
                return 'search_users_by_term', [term, value]
            if repo == '2':
                return 'search_tickets_by_term', [term, value]
        elif entry == '2':
            return 'list_searchable_fields', []
        return 'undefined', []

    def display_command_result(self, command_result: CommandResult) ->  None:
        if command_result.title:
            print(command_result.title)
        if not command_result.result_list:
            print("No results found")
        for result in command_result.result_list:
            print(result)
