from typing import List

from searchapp.models.command_result import CommandResult
from searchapp.search_service import SearchService
class Command:
    
    def __init__(self, search_service: SearchService) -> None:
        self.search_service = search_service

    def run(self, args: List[str]) -> CommandResult:
        raise NotImplementedError()
