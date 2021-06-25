from typing import List

from searchapp.models.ticket import Ticket
from searchapp.repository.repo_builder import RepoBuilder


class TicketRepo:

    def __init__(self):
        self.indexes = ["created_at", "type", "subject", "assignee_id", "tags"]
        self.tickets = {}
        self.indexing = {}
    
    def create_ticket(self, record):
        return Ticket(**record)

    def load(self, records: List[dict]) -> None:
        self.tickets = RepoBuilder.build_data(records, self.create_ticket)
        for term in self.indexes:
            self.indexing[term] = RepoBuilder.build_search_index(term, self.tickets)

    def search_by_term(self, term: str, value: str) -> List[Ticket]:
        if term == "_id":
            return [self.tickets.get(value)] if self.tickets.get(value) else []
        return [self.tickets[id] for id in self.indexing[term].get(value.lower(), [])]
