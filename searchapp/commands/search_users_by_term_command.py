from typing import List

from searchapp.models.search_result.user_result import UserResult
from searchapp.commands.command import Command

class SearchUsersByTermCommand(Command):

    def display(self, term: str, value: str, results: List[UserResult]) -> None:
        print(f"\nSearching Users for {term} with a value {value}")
        if not results:
            print("No results found")
        else:
            for result in results:
                print(result)

    def run(self, args: List[str]) -> None:
        term, value = args
        results = self.search_service.search_user(term, value)

        self.display(term, value, results)
