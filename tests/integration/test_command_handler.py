import json

import pytest

from searchapp.repository.ticket_repo import TicketRepo
from searchapp.repository.user_repo import UserRepo
from searchapp.search_service import SearchService
from searchapp.command_handler import CommandHandler
from searchapp.errors.command_not_found_error import CommandNotFoundError
from searchapp.models.search_result.user_searchable_fields import UserSearchableFields
from searchapp.models.search_result.ticket_searchable_fields import TicketSearchableFields


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

    def test_given_list_searchable_fields_command_string_when_handle_calls_then_it_returns_searchable_fields_result(
        self, search_service):

        command_handler = CommandHandler(search_service)

        command_result = command_handler.handle('list_searchable_fields', [])

        assert command_result.title == None
        assert command_result.result_list == (
            UserSearchableFields(["_id", "name", "created_at", "verified"]),
            TicketSearchableFields(["_id", "created_at", "type", "subject", "assignee_id", "tags"]))


    def test_given_search_users_by_term_command_string_when_handler_calls_then_it_returns_command_result_with_list_of_user_results(
        self, search_service):

        command_handler = CommandHandler(search_service)

        command_result = command_handler.handle('search_users_by_term', ['name', 'Watkins Hammond'])

        assert command_result.title == "Searching Users for name with a value Watkins Hammond"
        assert len(command_result.result_list) == 1
        assert command_result.result_list[0].user._id == 12
        assert [ticket._id for ticket in command_result.result_list[0].assigned_tickets] \
            == ["35072cd7-e343-4d8e-a967-bbe32eb019cb", "774765fe-7123-4131-8822-e855d3cad14c", "50f3fdbd-f8a6-481d-9bf7-572972856628"]

    def test_given_search_tickets_by_term_command_string_when_handle_calls_then_it_returns_command_result_with_list_of_ticket_results(
        self, search_service):

        command_handler = CommandHandler(search_service)

        command_result = command_handler.handle('search_tickets_by_term', ['_id', '8ea53283-5b36-4328-9a78-f261ee90f44b'])

        assert command_result.title == "Searching Tickets for _id with a value 8ea53283-5b36-4328-9a78-f261ee90f44b"
        assert len(command_result.result_list) == 1
        assert command_result.result_list[0].ticket._id == "8ea53283-5b36-4328-9a78-f261ee90f44b"
        assert command_result.result_list[0].assignee._id == 71

    def test_given_undefined_command_string_when_handle_calls_then_it_raise_not_found_command_except(
        self, search_service):

        command_handler = CommandHandler(search_service)

        with pytest.raises(CommandNotFoundError) as e:
            command_handler.handle('undefined', ['_id', '8ea53283-5b36-4328-9a78-f261ee90f44b'])

    def test_given_search_users_by_term_with_unmatched_value_when_handle_calls_then_it_returns_command_result_with_empty_result_list(
        self, search_service):

        command_handler = CommandHandler(search_service)

        command_result = command_handler.handle('search_users_by_term', ['name', 'Foo'])

        assert len(command_result.result_list) == 0

    def test_given_search_tickets_by_term_with_unmatched_value_when_handle_calls_then_it_returns_command_result_with_empty_result_list(
        self, capfd,
        search_service):

        command_handler = CommandHandler(search_service)

        command_result = command_handler.handle('search_tickets_by_term', ['_id', 'xxx'])

        assert len(command_result.result_list) == 0

    def test_given_search_users_by_term_with_empty_string_value_when_handle_calls_then_it_returns_command_result_with_missing_value_users(
        self, search_service):

        command_handler = CommandHandler(search_service)

        command_result = command_handler.handle('search_users_by_term', ['verified', ''])

        assert command_result.title == "Searching Users for verified with a value "
        assert len(command_result.result_list) == 2
        assert [result.user._id for result in command_result.result_list] == [54, 55]

    def test_given_search_tickets_by_term_with_empty_string_value_when_handle_calls_then_it_returns_command_result_with_missing_value_tickets(
        self, capfd,
        search_service):

        command_handler = CommandHandler(search_service)

        command_result = command_handler.handle('search_tickets_by_term', ['assignee_id', ''])

        assert command_result.title == "Searching Tickets for assignee_id with a value "
        assert len(command_result.result_list) == 4
        assert [result.ticket._id for result in command_result.result_list] \
            == ["e68d8bfd-9826-42fd-9692-add445aa7430", "c68cb7d7-b517-4d0b-a826-9605423e78c2", "17951590-6a78-49e8-8e45-1d4326ba49cc", "3ff0599a-fe0f-4f8f-ac31-e2636843bcea"]
