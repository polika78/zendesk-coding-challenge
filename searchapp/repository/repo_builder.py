from typing import Callable, Dict, List

class RepoBuilder:

    @staticmethod
    def build_data(records: List[dict], model_func: Callable) -> Dict[str, object]:
        return dict(
            [(str(record['_id']).lower(), model_func(record)) for record in records]
        )

    @staticmethod
    def build_search_index(term: str, data: Dict[str, object]) -> Dict[str, List[str]]:
        indexing: Dict[str, List[str]] = {}
        for id, record in data.items():
            if isinstance(getattr(record, term), list):
                for value in getattr(data[id], term):
                    indexing.setdefault(str(value).lower(), []).append(id)
            else:
                indexing.setdefault(str(getattr(data[id], term)).lower(), []).append(id)

        return indexing
