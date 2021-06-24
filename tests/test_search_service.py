from unittest.mock import patch

from searchapp.search_service import SearchService
from searchapp.repository.ticket_repo import TicketRepo
from searchapp.repository.user_repo import UserRepo
from searchapp.repository.models.user import User
from searchapp.repository.models.ticket import Ticket
from searchapp.models.user_result import UserResult


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
