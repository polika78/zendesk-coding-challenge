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

    def test_list_searchable_fields_returns_searchable_fields(
        self, capfd,
        search_service):

        command_handler = CommandHandler(search_service)

        command_handler.handle('list_searchable_fields', [])

        out, _ = capfd.readouterr()
        assert out == """
Search Users with
_id
name
created_at
verified

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


_id: 774765fe-7123-4131-8822-e855d3cad14c
created_at: 2016-06-23T06:08:21-10:00
type: task
subject: A Drama in Germany
assignee_id: 12
tags: ['Mississippi', 'Marshall Islands', 'Şouth Dakota', 'Montana']


_id: 50f3fdbd-f8a6-481d-9bf7-572972856628
created_at: 2016-05-19T08:52:06-10:00
type: incident
subject: A Nuisance in Namibia
assignee_id: 12
tags: ['Maine', 'West Virginia', 'Michigan', 'Florida']

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

    def test_given_unmatched_term_search_by_term_for_user_returns_not_found(
        self, capfd,
        search_service):

        command_handler = CommandHandler(search_service)

        command_handler.handle('search_users_by_term', ['name', 'Foo'])

        out, _ = capfd.readouterr()

        assert out == """
Searching Users for name with a value Foo
No results found
"""

    def test_given_unmatched_term_search_by_term_for_ticket_returns_not_found(
        self, capfd,
        search_service):

        command_handler = CommandHandler(search_service)

        command_handler.handle('search_tickets_by_term', ['_id', 'xxx'])

        out, _ = capfd.readouterr()

        assert out == """
Searching Tickets for _id with a value xxx
No results found
"""

    def test_given_empty_term_search_by_term_for_user_returns_missing_value_users(
        self, capfd,
        search_service):

        command_handler = CommandHandler(search_service)

        command_handler.handle('search_users_by_term', ['verified', ''])

        out, _ = capfd.readouterr()

        assert out == """
Searching Users for verified with a value 

_id: 54
name: Spence Tate
created_at: 2016-01-03T02:38:58-11:00
verified: 


_id: 828c158a-91e3-42b9-8aed-ac97407a150f
created_at: 2016-04-10T11:55:28-10:00
type: task
subject: A Drama in Israel
assignee_id: 54
tags: ['Missouri', 'Alabama', 'Virginia', 'Virgin Islands']


_id: e0e5ab4a-a776-40ec-8768-64d83a342d82
created_at: 2016-07-26T03:22:46-10:00
type: task
subject: A Drama in Albania
assignee_id: 54
tags: ['South Carolina', 'Indiana', 'New Mexico', 'Nebraska']


_id: 50dfc8bc-31de-411e-92bf-a6d6b9dfa490
created_at: 2016-03-08T09:44:54-11:00
type: task
subject: A Problem in South Africa
assignee_id: 54
tags: ['Georgia', 'Tennessee', 'Mississippi', 'Marshall Islands']


_id: 55
name: Thelma Wong
created_at: 2016-04-24T03:09:27-10:00
verified: 


_id: c22aaced-7faa-4b5c-99e5-1a209500ff16
created_at: 2016-07-11T08:52:25-10:00
type: incident
subject: A Problem in Ethiopia
assignee_id: 55
tags: ['Minnesota', 'New Jersey', 'Texas', 'Nevada']


_id: c48bf827-fc45-4158-b7ce-70784509f562
created_at: 2016-05-18T12:13:28-10:00
type: incident
subject: A Catastrophe in New Zealand
assignee_id: 55
tags: ['Georgia', 'Tennessee', 'Mississippi', 'Marshall Islands']

"""

    def test_given_empty_term_search_by_term_for_ticket_returns_missing_value_tickets(
        self, capfd,
        search_service):

        command_handler = CommandHandler(search_service)

        command_handler.handle('search_tickets_by_term', ['assignee_id', ''])

        out, _ = capfd.readouterr()

        assert out == """
Searching Tickets for assignee_id with a value 


_id: e68d8bfd-9826-42fd-9692-add445aa7430
created_at: 2016-06-30T06:59:04-10:00
type: question
subject: A Catastrophe in Falkland Islands (Malvinas)
assignee_id: 
tags: ['Georgia', 'Tennessee', 'Mississippi', 'Marshall Islands']

Assignee User
None


_id: c68cb7d7-b517-4d0b-a826-9605423e78c2
created_at: 2016-03-09T01:39:48-11:00
type: task
subject: A Problem in Western Sahara
assignee_id: 
tags: ['Massachusetts', 'New York', 'Minnesota', 'New Jersey']

Assignee User
None


_id: 17951590-6a78-49e8-8e45-1d4326ba49cc
created_at: 2016-06-28T03:29:34-10:00
type: incident
subject: A Nuisance in Kenya
assignee_id: 
tags: ['District Of Columbia', 'Wisconsin', 'Illinois', 'Fédératéd Statés Of Micronésia']

Assignee User
None


_id: 3ff0599a-fe0f-4f8f-ac31-e2636843bcea
created_at: 2016-05-15T12:59:16-10:00
type: question
subject: A Problem in Antigua and Barbuda
assignee_id: 
tags: ['American Samoa', 'Northern Mariana Islands', 'Puerto Rico', 'Idaho']

Assignee User
None
"""
