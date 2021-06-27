import searchapp.ui


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

    def test_given_quit_input_in_sub_entries_when_input_handler_calls_stops_input_and_returns_quit_entry(self):
        input_values = ['1', 'quit', '_id', '5']
    
        def mock_input(s):
            return input_values.pop(0)

        searchapp.ui.input = mock_input
        ui = searchapp.ui.UI()

        assert ui.input_handler() == ('quit', None)
        assert len(input_values) == 2

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
