import searchapp.ui

from searchapp.runner import main

class TestRunner:

    def test_given_inputs_for_searching_user_by_term_when_main_calls_then_it_displays_expected_results(self, capfd):

        input_values = ['1', '1', '_id', '5', 'quit']
    
        def mock_input(s):
            return input_values.pop(0)

        searchapp.ui.input = mock_input
        main()

        out, _ = capfd.readouterr()

        assert out == """
Welcome to Zendesk Search
Type 'quit' to exit at any time, Press 'Enter' to continue


            Select Search options:
             * Press 1 to search Zendesk
             * Press 2 to view a list of searchable fields
             * Type 'quit' to exit

Searching Users for _id with a value 5

_id: 5
name: Loraine Pittman
created_at: 2016-06-12T08:49:19-10:00
verified: False

Assigned Tickets

_id: de70eb6b-0717-40f9-9322-75f1262cda12
created_at: 2016-01-31T10:26:16-11:00
type: incident
subject: A Drama in Saudi Arabia
assignee_id: 5
tags: ['Rhode Island', 'Kansas', 'Guam', 'Colorado']


_id: 6a075290-6f77-4d70-87f2-e4867591772c
created_at: 2016-01-11T05:43:49-11:00
type: problem
subject: A Drama in Botswana
assignee_id: 5
tags: ['South Carolina', 'Indiana', 'New Mexico', 'Nebraska']


_id: f1fafe1e-6328-4c51-970b-fc743917ce4e
created_at: 2016-01-13T11:04:00-11:00
type: problem
subject: A Drama in Cameroon
assignee_id: 5
tags: ['Iowa', 'North Dakota', 'California', 'Palau']


_id: 53867869-0db0-4b8d-9d6c-9d1c0af4e693
created_at: 2016-05-14T09:19:56-10:00
type: task
subject: A Drama in Gabon
assignee_id: 5
tags: ['Utah', 'Hawaii', 'Alaska', 'Maryland']


            Select Search options:
             * Press 1 to search Zendesk
             * Press 2 to view a list of searchable fields
             * Type 'quit' to exit

Bye!~
"""

    def test_given_inputs_for_searching_ticket_by_term_when_main_calls_then_it_displays_expected_results(self, capfd):
    
        input_values = ['1', '2', 'assignee_id', '5', 'quit']
    
        def mock_input(s):
            return input_values.pop(0)

        searchapp.ui.input = mock_input
        main()

        out, _ = capfd.readouterr()

        assert out == """
Welcome to Zendesk Search
Type 'quit' to exit at any time, Press 'Enter' to continue


            Select Search options:
             * Press 1 to search Zendesk
             * Press 2 to view a list of searchable fields
             * Type 'quit' to exit

Searching Tickets for assignee_id with a value 5


_id: de70eb6b-0717-40f9-9322-75f1262cda12
created_at: 2016-01-31T10:26:16-11:00
type: incident
subject: A Drama in Saudi Arabia
assignee_id: 5
tags: ['Rhode Island', 'Kansas', 'Guam', 'Colorado']

Assignee

_id: 5
name: Loraine Pittman
created_at: 2016-06-12T08:49:19-10:00
verified: False



_id: 6a075290-6f77-4d70-87f2-e4867591772c
created_at: 2016-01-11T05:43:49-11:00
type: problem
subject: A Drama in Botswana
assignee_id: 5
tags: ['South Carolina', 'Indiana', 'New Mexico', 'Nebraska']

Assignee

_id: 5
name: Loraine Pittman
created_at: 2016-06-12T08:49:19-10:00
verified: False



_id: f1fafe1e-6328-4c51-970b-fc743917ce4e
created_at: 2016-01-13T11:04:00-11:00
type: problem
subject: A Drama in Cameroon
assignee_id: 5
tags: ['Iowa', 'North Dakota', 'California', 'Palau']

Assignee

_id: 5
name: Loraine Pittman
created_at: 2016-06-12T08:49:19-10:00
verified: False



_id: 53867869-0db0-4b8d-9d6c-9d1c0af4e693
created_at: 2016-05-14T09:19:56-10:00
type: task
subject: A Drama in Gabon
assignee_id: 5
tags: ['Utah', 'Hawaii', 'Alaska', 'Maryland']

Assignee

_id: 5
name: Loraine Pittman
created_at: 2016-06-12T08:49:19-10:00
verified: False


            Select Search options:
             * Press 1 to search Zendesk
             * Press 2 to view a list of searchable fields
             * Type 'quit' to exit

Bye!~
"""

    def test_given_inputs_for_list_searchable_fields_when_main_calls_then_it_displays_expected_results(self, capfd):
        
        input_values = ['2', 'quit']
    
        def mock_input(s):
            return input_values.pop(0)

        searchapp.ui.input = mock_input
        main()

        out, _ = capfd.readouterr()

        assert out == """
Welcome to Zendesk Search
Type 'quit' to exit at any time, Press 'Enter' to continue


            Select Search options:
             * Press 1 to search Zendesk
             * Press 2 to view a list of searchable fields
             * Type 'quit' to exit


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

            Select Search options:
             * Press 1 to search Zendesk
             * Press 2 to view a list of searchable fields
             * Type 'quit' to exit

Bye!~
"""

    def test_given_unknown_inputs_when_main_calls_then_it_displays_error_message(self, capfd):
        
        input_values = ['3', 'quit']
    
        def mock_input(s):
            return input_values.pop(0)

        searchapp.ui.input = mock_input
        main()

        # assert False
        out, _ = capfd.readouterr()

        assert out == """
Welcome to Zendesk Search
Type 'quit' to exit at any time, Press 'Enter' to continue


            Select Search options:
             * Press 1 to search Zendesk
             * Press 2 to view a list of searchable fields
             * Type 'quit' to exit

You selected wrong command. Please follow the instructions.

            Select Search options:
             * Press 1 to search Zendesk
             * Press 2 to view a list of searchable fields
             * Type 'quit' to exit

Bye!~
"""

    def test_given_unknown_field_term_when_main_calls_then_it_displays_error_message(self, capfd):
        
        input_values = ['1', '1', 'foo', '1', 'quit']
    
        def mock_input(s):
            return input_values.pop(0)

        searchapp.ui.input = mock_input
        main()

        out, _ = capfd.readouterr()

        assert out == """
Welcome to Zendesk Search
Type 'quit' to exit at any time, Press 'Enter' to continue


            Select Search options:
             * Press 1 to search Zendesk
             * Press 2 to view a list of searchable fields
             * Type 'quit' to exit

You entered unknown searching term. Please check the list of searchable fields.

            Select Search options:
             * Press 1 to search Zendesk
             * Press 2 to view a list of searchable fields
             * Type 'quit' to exit

Bye!~
"""
