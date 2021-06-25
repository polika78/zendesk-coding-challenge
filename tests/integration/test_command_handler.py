import json

import pytest

from searchapp.repository.ticket_repo import TicketRepo
from searchapp.repository.user_repo import UserRepo
from searchapp.search_service import SearchService
from searchapp.command_handler import CommandHandler
from searchapp.errors.command_not_found_error import CommandNotFoundError

class TestCommandHandler:

    @pytest.fixture
    def user_repo(self):
        with open('./tests/resources/users.json') as users_file:
            users_records = json.load(users_file)
        user_repo = UserRepo()
        user_repo.load(users_records)
        return user_repo

    @pytest.fixture
    def ticket_repo(self):
        with open('./tests/resources/tickets.json') as tickets_file:
            ticket_records = json.load(tickets_file)
        ticket_repo = TicketRepo()
        ticket_repo.load(ticket_records)
        return ticket_repo

    @pytest.fixture
    def search_service(self, user_repo, ticket_repo):
        return SearchService(user_repo, ticket_repo)

    def test_list_searchable_fields_for_user_returns_search_terms(
        self, capfd,
        search_service):

        command_handler = CommandHandler(search_service)

        command_handler.handle('list_searchable_fields', ['user'])

        out, _ = capfd.readouterr()
        assert out == """
Search Users with
_id
name
created_at
verified
"""

    def test_list_searchable_fields_for_ticket_returns_search_terms(
        self, capfd,
        search_service):

        command_handler = CommandHandler(search_service)

        command_handler.handle('list_searchable_fields', ['ticket'])

        out, _ = capfd.readouterr()
        assert out == """
Search Tickets with
_id
created_at
type
subject
assignee_id
tags
"""

    def test_search_by_term_for_user_returns_users(
        self, capfd,
        search_service):

        command_handler = CommandHandler(search_service)

        command_handler.handle('search_users_by_term', ['name', 'Watkins Hammond'])

        out, _ = capfd.readouterr()

        assert out == """
Searching Users for name with a value Watkins Hammond

_id: 12
name: Watkins Hammond
created_at: 2016-07-21T12:26:16-10:00
verified: False


_id: 35072cd7-e343-4d8e-a967-bbe32eb019cb
created_at: 2016-04-07T05:09:10-10:00
type: task
subject: A Catastrophe in Macau
assignee_id: 12
tags: ['California', 'Palau', 'Kentucky', 'North Carolina']


_id: 50f3fdbd-f8a6-481d-9bf7-572972856628
created_at: 2016-05-19T08:52:06-10:00
type: incident
subject: A Nuisance in Namibia
assignee_id: 12
tags: ['Maine', 'West Virginia', 'Michigan', 'Florida']


_id: 774765fe-7123-4131-8822-e855d3cad14c
created_at: 2016-06-23T06:08:21-10:00
type: task
subject: A Drama in Germany
assignee_id: 12
tags: ['Mississippi', 'Marshall Islands', 'Şouth Dakota', 'Montana']

"""
    def test_search_by_term_for_ticket_returns_tickets(
        self, capfd,
        search_service):

        command_handler = CommandHandler(search_service)

        command_handler.handle('search_tickets_by_term', ['_id', '8ea53283-5b36-4328-9a78-f261ee90f44b'])

        out, _ = capfd.readouterr()

        assert out == """
Searching Tickets for _id with a value 8ea53283-5b36-4328-9a78-f261ee90f44b


_id: 8ea53283-5b36-4328-9a78-f261ee90f44b
created_at: 2016-03-07T03:00:54-11:00
type: task
subject: A Catastrophe in Sierra Leone
assignee_id: 71
tags: ['Washington', 'Wyoming', 'Ohio', 'Pennsylvania']

Assignee User

_id: 71
name: Prince Hinton
created_at: 2016-04-18T11:05:43-10:00
verified: False

"""

    def test_given_undefined_command_handle_raise_not_found_command_except(
        self, search_service):

        command_handler = CommandHandler(search_service)

        with pytest.raises(CommandNotFoundError) as e:
            command_handler.handle('undefined', ['_id', '8ea53283-5b36-4328-9a78-f261ee90f44b'])
