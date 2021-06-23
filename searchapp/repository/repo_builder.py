from itertools import groupby
from typing import Callable, Dict, List

class RepoBuilder:

    @staticmethod
    def build_data(records: List[dict], model_func: Callable) -> Dict[str, object]:
        return dict(
            [(str(record['_id']).lower(), model_func(record)) for record in records]
        )

    @staticmethod
    def build_search_index(term: str, data: Dict[str, object]) -> Dict[str, List[str]]:
        indexing = {}
        map_data_with_term_value = [(getattr(data[id], term), id) for id in iter(data)]

        for value, groupby_term_value in groupby(map_data_with_term_value, lambda x: x[0]):
            indexing[str(value).lower()] = list(map(lambda x: x[1], list(groupby_term_value)))

        return indexing
