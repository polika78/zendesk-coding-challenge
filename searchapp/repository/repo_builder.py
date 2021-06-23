from itertools import groupby
from typing import Callable, Dict, Generator, List, Tuple

class RepoBuilder:

    @staticmethod
    def build_data(records: List[dict], model_func: Callable) -> Dict[str, object]:
        return dict(
            [(str(record['_id']).lower(), model_func(record)) for record in records]
        )

    @staticmethod
    def build_search_index(term: str, data: Dict[str, object]) -> Dict[str, List[str]]:
        def generate_map_data_with_term_value(result_map: List[Tuple[str, str]], term: str, id: str, ids: List[str], data: dict) -> List[Tuple[str, str]]:
            if isinstance(getattr(data[id], term), list):
                value_map = [(str(value).lower(), id) for value in getattr(data[id], term)]
            else:
                value_map = [(getattr(data[id], term), id)]

            new_result_map = [
                *result_map,
                *value_map
            ]
            
            if ids:
                next_id, *rest_ids = ids
                return generate_map_data_with_term_value(new_result_map, term, next_id, rest_ids, data)

            return new_result_map

        indexing = {}
        id, *ids = iter(data)
        map_data_with_term_value = generate_map_data_with_term_value([], term, id, ids, data)

        for value, groupby_term_value in groupby(sorted(map_data_with_term_value), lambda x: x[0]):
            indexing[str(value).lower()] = list(map(lambda x: x[1], list(groupby_term_value)))

        return indexing
