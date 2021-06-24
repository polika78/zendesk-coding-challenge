import json

import pytest

from searchapp.repository.ticket_repo import TicketRepo
from searchapp.repository.user_repo import UserRepo
from searchapp.search_service import SearchService
from searchapp.command_handler import CommandHandler


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

    def test_get_terms_for_user_returns_search_terms(
        self, capfd,
        search_service):

        command_handler = CommandHandler(search_service)

        command_handler.handle('get_search_terms', 'user')

        out, _ = capfd.readouterr()
        assert out == """
Search Users with
_id
name
created_at
verified
"""

    def test_get_terms_for_ticket_returns_search_terms(
        self, capfd,
        search_service):

        command_handler = CommandHandler(search_service)

        command_handler.handle('get_search_terms', 'ticket')

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
