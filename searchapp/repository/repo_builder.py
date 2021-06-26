from typing import Callable, Dict, List, Union
from searchapp.models.user import User
from searchapp.models.ticket import Ticket

def list_value_indexing(indexing: dict, term: str, record: Union[User, Ticket]) -> Dict[str, List[str]]:
    return dict([
        (
            str(value).lower(),
            [
                *indexing.setdefault(term, {}).setdefault(str(value).lower(), []),
                str(record._id)
            ]
        )
        for value in getattr(record, term)
    ])

def value_indexing(indexing: dict, term: str, record: Union[User, Ticket]) -> Dict[str, List[str]]:
    return {
        str(getattr(record, term)).lower(): [
            *indexing.setdefault(term, {}).setdefault(str(getattr(record, term)).lower(), []),
            str(record._id)
        ]            
    }
    
def generate_new_term_index(indexing: dict, term: str, record: Union[User, Ticket]) -> Dict[str, Dict[str, List[str]]]:
    if isinstance(getattr(record, term), list):
        return {
            term: {
                **indexing.setdefault(term, {}),
                **list_value_indexing(indexing, term, record)
            }
        }
    return {
        term: {
            **indexing.setdefault(term, {}),
            **value_indexing(indexing, term, record)
        }
    }

def generate_indexing(indexing: dict, record: Union[User, Ticket], records: List[Union[User, Ticket]], term: str) \
        -> Dict[str, List[str]]:
    new_indexing = generate_new_term_index(indexing, term, record)

    if not records:
        return new_indexing[term]

    next_record, *rest = records
    return generate_indexing(new_indexing, next_record, rest, term)

class RepoBuilder:

    @staticmethod
    def build_data(records: List[dict], model_func: Callable) -> Dict[str, Union[User, Ticket]]:
        return dict(
            [(str(record['_id']).lower(), model_func(record)) for record in records]
        )

    @staticmethod
    def build_search_index(term: str, data: Dict[str, Union[User, Ticket]]) -> Dict[str, List[str]]:
        record, *records = data.values()
        return generate_indexing({}, record, records, term)
