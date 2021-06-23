from typing import Callable, Dict, List, Union

class RepoBuilder:

    @staticmethod
    def build_data(records: List[dict], model_func: Callable) -> Dict[str, object]:
        return dict(
            [(str(record['_id']).lower(), model_func(record)) for record in records]
        )
