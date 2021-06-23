from itertools import groupby
from typing import Callable, Dict, Generator, Iterable, List 

class RepoBuilder:

    @staticmethod
    def build_data(records: List[dict], model_func: Callable) -> Dict[str, object]:
        return dict(
            [(str(record['_id']).lower(), model_func(record)) for record in records]
        )

    @staticmethod
    def build_search_index(term: str, data: Dict[str, object]) -> Dict[str, List[str]]:
        def generate_map_data_with_term_value(term: str, id: str, ids: Iterable[str], data: object) -> Generator:
            if isinstance(getattr(data[id], term), list):
                for value in getattr(data[id], term):
                    yield (value, id)
            else:
                yield (getattr(data[id], term), id)

            next_id = next(ids, None)
            if next_id:
                return generate_map_data_with_term_value(term, next_id, ids, data)

        indexing = {}
        ids = iter(data)
        id = next(ids)
        map_data_with_term_value = generate_map_data_with_term_value(term, id, ids, data)

        for value, groupby_term_value in groupby(map_data_with_term_value, lambda x: x[0]):
            indexing[str(value).lower()] = list(map(lambda x: x[1], list(groupby_term_value)))

        return indexing
