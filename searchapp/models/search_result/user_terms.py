from dataclasses import dataclass
from typing import List


@dataclass
class UserTerms:
    terms: List[str]

    def __str__(self):
        list_terms = '\n'.join(self.terms)
        return f"""
Search Users with
{list_terms}"""
