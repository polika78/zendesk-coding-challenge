import pytest

from searchapp.models.ticket import Ticket
from searchapp.repository.ticket_repo import TicketRepo
from searchapp.errors.unknown_search_term_error import UnknownSearchTermError

class TestTicketRepo:
    @pytest.fixture
    def ticket_records(self):
        return [
            {
                "_id": "436bf9b0-1147-4c0a-8439-6f79833bff5b",
                "created_at": "2016-04-28T11:19:34-10:00",
                "type": "incident",
                "subject": "A Catastrophe in Korea (North)",
                "assignee_id": 24,
                "tags": [
                    "Ohio",
                    "Pennsylvania",
                    "American Samoa",
                    "Northern Mariana Islands"
                ]
            },
            {
                "_id": "6aac0369-a7e5-4417-8b50-92528ef485d3",
                "created_at": "2016-06-15T12:03:55-10:00",
                "type": "question",
                "subject": "A Nuisance in Latvia",
                "assignee_id": 29,
                "tags": [
                    "Washington",
                    "Wyoming",
                    "Ohio",
                    "Pennsylvania"
                ]
            },
            {
                "_id": "8629d5fa-89c4-4e9b-9d9f-221b68b079f4",
                "created_at": "2016-02-03T03:44:33-11:00",
                "subject": "A Drama in Indonesia",
                "tags": [
                    "Ohio",
                    "Pennsylvania",
                    "American Samoa",
                    "Northern Mariana Islands"
                ]
            }
        ]

    def test_given_json_load_sets_tickets_and_indexing(self, ticket_records):
        ticket_repo = TicketRepo()
        expected_tickets = dict([(str(record["_id"]), Ticket(**record)) for record in ticket_records])

        ticket_repo.load(ticket_records)

        assert ticket_repo.tickets == expected_tickets

        assert ticket_repo.indexing == {
            'created_at': {
                "2016-04-28t11:19:34-10:00": ["436bf9b0-1147-4c0a-8439-6f79833bff5b"],
                "2016-06-15t12:03:55-10:00": ["6aac0369-a7e5-4417-8b50-92528ef485d3"],
                "2016-02-03t03:44:33-11:00": ["8629d5fa-89c4-4e9b-9d9f-221b68b079f4"]
            },
            'type': {
                "incident": ["436bf9b0-1147-4c0a-8439-6f79833bff5b"],
                "question": ["6aac0369-a7e5-4417-8b50-92528ef485d3"],
                "": ["8629d5fa-89c4-4e9b-9d9f-221b68b079f4"]
            },
            'subject': {
                "a catastrophe in korea (north)": ["436bf9b0-1147-4c0a-8439-6f79833bff5b"],
                "a nuisance in latvia": ["6aac0369-a7e5-4417-8b50-92528ef485d3"],
                "a drama in indonesia": ["8629d5fa-89c4-4e9b-9d9f-221b68b079f4"]
            },
            'assignee_id': {
                "24": ["436bf9b0-1147-4c0a-8439-6f79833bff5b"],
                "29": ["6aac0369-a7e5-4417-8b50-92528ef485d3"],
                "": ["8629d5fa-89c4-4e9b-9d9f-221b68b079f4"]
            },
            'tags': {
                "american samoa": ["436bf9b0-1147-4c0a-8439-6f79833bff5b", "8629d5fa-89c4-4e9b-9d9f-221b68b079f4"],
                "northern mariana islands": ["436bf9b0-1147-4c0a-8439-6f79833bff5b", "8629d5fa-89c4-4e9b-9d9f-221b68b079f4"],
                "ohio": ["436bf9b0-1147-4c0a-8439-6f79833bff5b", "6aac0369-a7e5-4417-8b50-92528ef485d3", "8629d5fa-89c4-4e9b-9d9f-221b68b079f4"],
                "pennsylvania": ["436bf9b0-1147-4c0a-8439-6f79833bff5b", "6aac0369-a7e5-4417-8b50-92528ef485d3", "8629d5fa-89c4-4e9b-9d9f-221b68b079f4"],
                "washington": ["6aac0369-a7e5-4417-8b50-92528ef485d3"],
                "wyoming": ["6aac0369-a7e5-4417-8b50-92528ef485d3"],
            }
        }

    def test_after_loaded_given_id_term_search_by_term_returns_matched_tickets(self, ticket_records):
        ticket_repo = TicketRepo()
        ticket_repo.load(ticket_records)

        tickets = ticket_repo.search_by_term("_id", "436bf9b0-1147-4c0a-8439-6f79833bff5b")

        assert tickets == [Ticket(**ticket_records[0])]

    def test_after_loaded_given_created_at_term_search_by_term_returns_matched_tickets(self, ticket_records):
        ticket_repo = TicketRepo()
        ticket_repo.load(ticket_records)

        tickets = ticket_repo.search_by_term("created_at", "2016-06-15T12:03:55-10:00")

        assert tickets == [Ticket(**ticket_records[1])]

    def test_after_loaded_given_type_term_search_by_term_returns_matched_tickets(self, ticket_records):
        ticket_repo = TicketRepo()
        ticket_repo.load(ticket_records)

        tickets = ticket_repo.search_by_term("type", "incident")

        assert tickets == [Ticket(**ticket_records[0])]

    def test_after_loaded_given_type_term_with_empty_string_search_by_term_returns_matched_tickets(self, ticket_records):
        ticket_repo = TicketRepo()
        ticket_repo.load(ticket_records)

        tickets = ticket_repo.search_by_term("type", "")

        assert tickets == [Ticket(**ticket_records[2])]

    def test_after_loaded_given_subject_term_search_by_term_returns_matched_tickets(self, ticket_records):
        ticket_repo = TicketRepo()
        ticket_repo.load(ticket_records)

        tickets = ticket_repo.search_by_term("subject", "A Nuisance in Latvia")

        assert tickets == [Ticket(**ticket_records[1])]

    def test_after_loaded_given_assigned_id_term_search_by_term_returns_matched_tickets(self, ticket_records):
        ticket_repo = TicketRepo()
        ticket_repo.load(ticket_records)

        tickets = ticket_repo.search_by_term("assignee_id", "24")

        assert tickets == [Ticket(**ticket_records[0])]

    def test_after_loaded_given_assignee_id_term_with_empty_string_search_by_term_returns_matched_tickets(self, ticket_records):
        ticket_repo = TicketRepo()
        ticket_repo.load(ticket_records)

        tickets = ticket_repo.search_by_term("assignee_id", "")

        assert tickets == [Ticket(**ticket_records[2])]

    def test_after_loaded_given_tags_term_search_by_term_returns_matched_tickets(self, ticket_records):
        ticket_repo = TicketRepo()
        ticket_repo.load(ticket_records)

        tickets = ticket_repo.search_by_term("tags", "ohio")

        assert tickets == [Ticket(**ticket_records[0]), Ticket(**ticket_records[1]), Ticket(**ticket_records[2])]

    def test_after_loaded_given_not_found_term_search_by_term_returns_empty(self, ticket_records):
        ticket_repo = TicketRepo()
        ticket_repo.load(ticket_records)

        tickets = ticket_repo.search_by_term("tags", "foo")

        assert tickets == []

    def test_after_loaded_given_not_found_id_search_by_term_returns_empty(self, ticket_records):
        ticket_repo = TicketRepo()
        ticket_repo.load(ticket_records)

        tickets = ticket_repo.search_by_term("_id", "400")

        assert tickets == []

    def test_after_loaded_given_unknown_search_term_search_by_term_raise_unknown_search_term_error(self, ticket_records):
        ticket_repo = TicketRepo()
        ticket_repo.load(ticket_records)

        with pytest.raises(UnknownSearchTermError) as e:
            ticket_repo.search_by_term("unknown", "900")
