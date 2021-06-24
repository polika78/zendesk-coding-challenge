from unittest.mock import patch

from searchapp.search_service import SearchService
from searchapp.repository.ticket_repo import TicketRepo
from searchapp.repository.user_repo import UserRepo
from searchapp.repository.models.user import User
from searchapp.repository.models.ticket import Ticket
from searchapp.models.user_result import UserResult
from searchapp.models.ticket_result import TicketResult
from searchapp.models.user_terms import UserTerms
from searchapp.models.ticket_terms import TicketTerms


class TestSearchService:

    @patch.object(UserRepo, 'search_by_term')
    @patch.object(TicketRepo, 'search_by_term')
    def test_given_a_user_with_single_assigned_ticket_search_users_returns_correct_search_result(
        self,
        mock_ticket_repo_search_by_term,
        mock_user_repo_search_by_term):
        user_search_result = [
            User(
                _id=1, name='test', created_at='2016-02-09T07:52:10-11:00', verified=True
            )
        ]
        ticket_search_result = [
            Ticket(
                _id="x",
                created_at="2016-02-09T07:52:10-11:00",
                subject="test",
                tags=["x"],
                type="option",
                assignee_id=1
            )
        ]
        expected_search_result = [
            UserResult(
                user=user_search_result[0],
                assigned_tickets=ticket_search_result
            )
        ]
        mock_user_repo_search_by_term.return_value = user_search_result
        mock_ticket_repo_search_by_term.return_value = ticket_search_result
        user_repo = UserRepo()
        ticket_repo = TicketRepo()
        search_service = SearchService(user_repo, ticket_repo)

        assert search_service.search_user('name', "test") == expected_search_result
        mock_user_repo_search_by_term.assert_called_once_with('name', 'test')
        mock_ticket_repo_search_by_term.assert_called_once_with('assignee_id', '1')

    @patch.object(UserRepo, 'search_by_term')
    @patch.object(TicketRepo, 'search_by_term')
    def test_given_a_user_without_assigned_ticket_search_users_returns_correct_search_result(
        self,
        mock_ticket_repo_search_by_term,
        mock_user_repo_search_by_term):
        user_search_result = [
            User(
                _id=1, name='test', created_at='2016-02-09T07:52:10-11:00', verified=True
            )
        ]
        ticket_search_result = []
        expected_search_result = [
            UserResult(
                user=user_search_result[0],
                assigned_tickets=[]
            )
        ]
        mock_user_repo_search_by_term.return_value = user_search_result
        mock_ticket_repo_search_by_term.return_value = ticket_search_result
        user_repo = UserRepo()
        ticket_repo = TicketRepo()
        search_service = SearchService(user_repo, ticket_repo)

        assert search_service.search_user('name', "test") == expected_search_result
        mock_user_repo_search_by_term.assert_called_once_with('name', 'test')
        mock_ticket_repo_search_by_term.assert_called_once_with('assignee_id', '1')

    @patch.object(UserRepo, 'search_by_term')
    @patch.object(TicketRepo, 'search_by_term')
    def test_given_two_matched_user_with_assigned_ticket_search_users_returns_correct_search_result(
        self,
        mock_ticket_repo_search_by_term,
        mock_user_repo_search_by_term):
        user_search_result = [
            User(
                _id=1, name='test 1', created_at='2016-02-08T07:52:10-11:00', verified=True
            ),
            User(
                _id=2, name='test 2', created_at='2016-02-09T07:52:10-11:00', verified=False
            )
        ]
        ticket_search_result_1 = [
            Ticket(
                _id="x",
                created_at="2016-02-09T07:52:10-11:00",
                subject="test",
                tags=["x"],
                type="option",
                assignee_id=1
            )
        ]
        ticket_search_result_2 = [
            Ticket(
                _id="y",
                created_at="2016-02-07T07:52:10-11:00",
                subject="test 2",
                tags=["i"],
                type="multi",
                assignee_id=2
            )
        ]
        expected_search_result = [
            UserResult(
                user=user_search_result[0],
                assigned_tickets=ticket_search_result_1
            ),
            UserResult(
                user=user_search_result[1],
                assigned_tickets=ticket_search_result_2
            )
        ]
        mock_user_repo_search_by_term.return_value = user_search_result
        mock_ticket_repo_search_by_term.side_effect = [
            ticket_search_result_1,
            ticket_search_result_2
        ]
        user_repo = UserRepo()
        ticket_repo = TicketRepo()
        search_service = SearchService(user_repo, ticket_repo)

        assert search_service.search_user('name', "test") == expected_search_result

    @patch.object(UserRepo, 'search_by_term')
    @patch.object(TicketRepo, 'search_by_term')
    def test_given_not_matched_user_search_users_returns_empty(
        self,
        mock_ticket_repo_search_by_term,
        mock_user_repo_search_by_term):
        user_search_result = []
        
        expected_search_result = []
        mock_user_repo_search_by_term.return_value = user_search_result
        mock_ticket_repo_search_by_term.return_value = []
        user_repo = UserRepo()
        ticket_repo = TicketRepo()
        search_service = SearchService(user_repo, ticket_repo)

        assert search_service.search_user('name', "test") == expected_search_result
        mock_user_repo_search_by_term.assert_called_once_with('name', 'test')
        mock_ticket_repo_search_by_term.assert_not_called()

    @patch.object(UserRepo, 'search_by_term')
    @patch.object(TicketRepo, 'search_by_term')
    def test_given_a_ticket_with_user_assignee_search_tickets_returns_correct_search_result(
        self,
        mock_ticket_repo_search_by_term,
        mock_user_repo_search_by_term):
        user_search_result = [
            User(
                _id=1, name='test', created_at='2016-02-09T07:52:10-11:00', verified=True
            )
        ]
        ticket_search_result = [
            Ticket(
                _id="x",
                created_at="2016-02-09T07:52:10-11:00",
                subject="test",
                tags=["x"],
                type="option",
                assignee_id=1
            )
        ]
        expected_search_result = [
            TicketResult(
                ticket=ticket_search_result[0],
                assignee=user_search_result[0]
            )
        ]
        mock_user_repo_search_by_term.return_value = user_search_result
        mock_ticket_repo_search_by_term.return_value = ticket_search_result
        user_repo = UserRepo()
        ticket_repo = TicketRepo()
        search_service = SearchService(user_repo, ticket_repo)
        result = search_service.search_tickets('_id', "x")

        assert result == expected_search_result
        mock_ticket_repo_search_by_term.assert_called_once_with('_id', 'x')
        mock_user_repo_search_by_term.assert_called_once_with('_id', '1')

    @patch.object(UserRepo, 'search_by_term')
    @patch.object(TicketRepo, 'search_by_term')
    def test_given_a_ticket_without_assignee_search_tickets_returns_correct_search_result(
        self,
        mock_ticket_repo_search_by_term,
        mock_user_repo_search_by_term):
        user_search_result = []
        ticket_search_result = [
            Ticket(
                _id="x",
                created_at="2016-02-09T07:52:10-11:00",
                subject="test",
                tags=["x"],
                type="option",
                assignee_id=1
            )
        ]
        expected_search_result = [
            TicketResult(
                ticket=ticket_search_result[0],
                assignee=None
            )
        ]
        mock_user_repo_search_by_term.return_value = user_search_result
        mock_ticket_repo_search_by_term.return_value = ticket_search_result
        user_repo = UserRepo()
        ticket_repo = TicketRepo()
        search_service = SearchService(user_repo, ticket_repo)

        assert search_service.search_tickets('_id', "x") == expected_search_result
        mock_ticket_repo_search_by_term.assert_called_once_with('_id', 'x')
        mock_user_repo_search_by_term.assert_called_once_with('_id', '1')

    @patch.object(UserRepo, 'search_by_term')
    @patch.object(TicketRepo, 'search_by_term')
    def test_given_two_matched_tickets_with_assignee_search_tickets_returns_correct_search_result(
        self,
        mock_ticket_repo_search_by_term,
        mock_user_repo_search_by_term):
        
        ticket_search_result = [
            Ticket(
                _id="x",
                created_at="2016-02-09T07:52:10-11:00",
                subject="test",
                tags=["x"],
                type="option",
                assignee_id=1
            ),
            Ticket(
                _id="y",
                created_at="2016-02-07T07:52:10-11:00",
                subject="test 2",
                tags=["i"],
                type="multi",
                assignee_id=2
            )
        ]

        user_search_result = [
            User(
                _id=1, name='test 1', created_at='2016-02-08T07:52:10-11:00', verified=True
            ),
            User(
                _id=2, name='test 2', created_at='2016-02-09T07:52:10-11:00', verified=False
            )
        ]
        expected_search_result = [
            TicketResult(
                ticket=ticket_search_result[0],
                assignee=user_search_result[0]
            ),
            TicketResult(
                ticket=ticket_search_result[1],
                assignee=user_search_result[1]
            )
        ]
        mock_ticket_repo_search_by_term.return_value = ticket_search_result
        mock_user_repo_search_by_term.side_effect = [
            [user_search_result[0]],
            [user_search_result[1]],
        ]
        user_repo = UserRepo()
        ticket_repo = TicketRepo()
        search_service = SearchService(user_repo, ticket_repo)

        assert search_service.search_tickets('_id', "x") == expected_search_result

    @patch.object(UserRepo, 'search_by_term')
    @patch.object(TicketRepo, 'search_by_term')
    def test_given_not_matched_ticket_search_tickets_returns_empty(
        self,
        mock_ticket_repo_search_by_term,
        mock_user_repo_search_by_term):
        
        expected_search_result = []
        mock_ticket_repo_search_by_term.return_value = []
        mock_user_repo_search_by_term.return_value = []
        user_repo = UserRepo()
        ticket_repo = TicketRepo()
        search_service = SearchService(user_repo, ticket_repo)

        assert search_service.search_tickets('_id', "x") == expected_search_result
        mock_ticket_repo_search_by_term.assert_called_once_with('_id', 'x')
        mock_user_repo_search_by_term.assert_not_called()

    def test_get_user_search_terms_returns_user_terms(self):

        user_repo = UserRepo()
        ticket_repo = TicketRepo()
        search_service = SearchService(user_repo, ticket_repo)
        expected_result = UserTerms(
            terms=["_id", "name", "created_at", "verified"]
        )
        assert search_service.get_user_search_terms() == expected_result

    def test_get_ticket_search_terms_returns_ticket_terms(self):
    
        user_repo = UserRepo()
        ticket_repo = TicketRepo()
        search_service = SearchService(user_repo, ticket_repo)
        expected_result = TicketTerms(
            terms=["_id", "created_at", "type", "subject", "assignee_id", "tags"]
        )
        assert search_service.get_ticket_search_terms() == expected_result
