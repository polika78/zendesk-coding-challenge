from dataclasses import dataclass
from typing import List


@dataclass
class TicketTerms:
    terms: List[str]

    def __str__(self):
        list_terms = '\n'.join(self.terms)
        return f"""
Search Tickets with
{list_terms}"""
