import searchapp.ui
from searchapp.models.command_result import CommandResult
from searchapp.models.search_result.user_result import UserResult
from searchapp.models.search_result.ticket_result import TicketResult
from searchapp.models.search_result.user_searchable_fields import UserSearchableFields
from searchapp.models.search_result.ticket_searchable_fields import TicketSearchableFields
from searchapp.models.user import User
from searchapp.models.ticket import Ticket


class TestUI:

    def test_given_inputs_when_input_handler_calls_returns_first_entry_and_sub_entries(self):
        input_values = ['1', '1', '_id', '5']
    
        def mock_input(s):
            return input_values.pop(0)

        searchapp.ui.input = mock_input
        ui = searchapp.ui.UI()

        assert ui.input_handler() == ('1', ('1', '_id', '5'))

    def test_given_quit_input_when_input_handler_calls_stops_input_and_returns_quit_entry(self):
        input_values = ['quit', '1', '_id', '5']
    
        def mock_input(s):
            return input_values.pop(0)

        searchapp.ui.input = mock_input
        ui = searchapp.ui.UI()

        assert ui.input_handler() == ('quit', None)
        assert len(input_values) == 3

    def test_given_quit_input_in_first_sub_entries_when_input_handler_calls_stops_input_and_returns_quit_entry(self):
        input_values = ['1', 'quit', '_id', '5']
    
        def mock_input(s):
            return input_values.pop(0)

        searchapp.ui.input = mock_input
        ui = searchapp.ui.UI()

        assert ui.input_handler() == ('quit', None)
        assert len(input_values) == 2

    def test_given_quit_input_in_second_sub_entries_when_input_handler_calls_stops_input_and_returns_quit_entry(self):
        input_values = ['1', '1', 'quit', '5']

        def mock_input(s):
            return input_values.pop(0)

        searchapp.ui.input = mock_input
        ui = searchapp.ui.UI()

        assert ui.input_handler() == ('quit', None)
        assert len(input_values) == 1

    def test_given_entries_for_searching_users_when_parse_command_calls_returns_searching_users_command_string_and_args(self):
        ui = searchapp.ui.UI()

        assert ui.parse_command('1', ('1', 'verified', 'true')) \
            == ('search_users_by_term', ['verified', 'true'])

    def test_given_entries_for_searching_tickets_parse_command_returns_searching_tickets_command_string_and_args(self):
        ui = searchapp.ui.UI()

        assert ui.parse_command('1', ('2', 'assignee_id', '5')) \
            == ('search_tickets_by_term', ['assignee_id', '5'])

    def test_given_entries_for_listing_searchable_fields_command_parse_returns_listing_searchable_command_string_and_empty_args(self):
        ui = searchapp.ui.UI()

        assert ui.parse_command('2', None) \
            == ('list_searchable_fields', [])

    def test_given_entries_with_unknown_entry_command_repo_command_parse_returns_undefined_command_string_and_empty_args(self):
        ui = searchapp.ui.UI()

        assert ui.parse_command('foo', None) \
            == ('undefined', [])

    def test_given_entries_with_unknown_searching_repo_repo_command_parse_returns_undefined_command_string_and_empty_args(self):
        ui = searchapp.ui.UI()

        assert ui.parse_command('1', ('foo', '_id', '1')) \
            == ('undefined', [])

    def test_given_command_result_with_title_and_result_list_for_user_when_display_command_result_then_it_displays_title_and_result_list(self, capfd):
        ui = searchapp.ui.UI()

        command_result = CommandResult(
            title="Searching Users for name with a value Watkins Hammond",
            result_list=[
                UserResult(
                    user=User(_id=12, name="Watkins Hammond", created_at="2016-07-21T12:26:16-10:00", verified=False),
                    assigned_tickets=[
                        Ticket(
                            _id="35072cd7-e343-4d8e-a967-bbe32eb019cb",
                            created_at="2016-04-07T05:09:10-10:00",
                            type="task",
                            subject="A Catastrophe in Macau",
                            assignee_id=12,
                            tags=['California', 'Palau', 'Kentucky', 'North Carolina']
                        )
                    ]
                )
            ]
        )

        ui.display_command_result(command_result)

        out, _ = capfd.readouterr()

        assert out == """Searching Users for name with a value Watkins Hammond

_id: 12
name: Watkins Hammond
created_at: 2016-07-21T12:26:16-10:00
verified: False

Assigned Tickets

_id: 35072cd7-e343-4d8e-a967-bbe32eb019cb
created_at: 2016-04-07T05:09:10-10:00
type: task
subject: A Catastrophe in Macau
assignee_id: 12
tags: ['California', 'Palau', 'Kentucky', 'North Carolina']

"""

    def test_given_command_result_with_title_and_result_list_for_ticket_when_display_command_result_then_it_displays_title_and_result_list(self, capfd):
        ui = searchapp.ui.UI()

        command_result = CommandResult(
            title="Searching Tickets for _id with a value 35072cd7-e343-4d8e-a967-bbe32eb019cb",
            result_list=[
                TicketResult(
                    ticket=Ticket(
                        _id="35072cd7-e343-4d8e-a967-bbe32eb019cb",
                        created_at="2016-04-07T05:09:10-10:00",
                        type="task",
                        subject="A Catastrophe in Macau",
                        assignee_id=12,
                        tags=['California', 'Palau', 'Kentucky', 'North Carolina']
                    ),
                    assignee=User(_id=12, name="Watkins Hammond", created_at="2016-07-21T12:26:16-10:00", verified=False)
                )
            ]
        )

        ui.display_command_result(command_result)

        out, _ = capfd.readouterr()

        assert out == """Searching Tickets for _id with a value 35072cd7-e343-4d8e-a967-bbe32eb019cb


_id: 35072cd7-e343-4d8e-a967-bbe32eb019cb
created_at: 2016-04-07T05:09:10-10:00
type: task
subject: A Catastrophe in Macau
assignee_id: 12
tags: ['California', 'Palau', 'Kentucky', 'North Carolina']

Assignee

_id: 12
name: Watkins Hammond
created_at: 2016-07-21T12:26:16-10:00
verified: False

"""

    def test_given_command_result_without_title_when_display_command_result_then_it_displays_result_list(self, capfd):
        ui = searchapp.ui.UI()

        command_result = CommandResult(
            title=None,
            result_list=(
                UserSearchableFields(terms=["_id", "name"]),
                TicketSearchableFields(terms=["_id", "subject"])
            )
        )

        ui.display_command_result(command_result)

        out, _ = capfd.readouterr()

        assert out == """
Search Users with
_id
name

Search Tickets with
_id
subject
"""

    def test_given_command_result_with_title_and_empty_result_list_when_display_command_result_then_it_displays_no_result(self, capfd):
        ui = searchapp.ui.UI()

        command_result = CommandResult(
            title="Searching Users for name with a value Foo",
            result_list=[]
        )

        ui.display_command_result(command_result)

        out, _ = capfd.readouterr()

        assert out == """Searching Users for name with a value Foo
No results found
"""
