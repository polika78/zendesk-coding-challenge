from typing import List

from searchapp.repository.models.user import User
from searchapp.repository.repo_builder import RepoBuilder

class UserRepo:

    def __init__(self):
        self.indexes = ["name", "created_at", "verified"]
        self.users = {}
        self.indexing = {}
    
    def create_user(self, record):
        return User(**record)

    def load(self, records: List[dict]) -> None:
        self.users = RepoBuilder.build_data(records, self.create_user)
        for term in self.indexes:
            self.indexing[term] = RepoBuilder.build_search_index(term, self.users)

    def search_by_term(self, term: str, value: str) -> List[User]:
        if term == "_id":
            return [self.users[value]]
        return [self.users[id] for id in self.indexing[term][value.lower()]]
