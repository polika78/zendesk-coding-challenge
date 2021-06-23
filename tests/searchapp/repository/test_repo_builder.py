from typing import List
from dataclasses import dataclass
import pytest

from searchapp.repository.repo_builder import RepoBuilder

@dataclass
class TestModel:
    _id: str
    name: str
    tags: List[str]
    foreign_id: int
    active: bool

class TestRepoBuilder:
    
    @pytest.fixture
    def input_records(self):
        return [
            {
                "_id": 1,
                "name": "James",
                "tags": ["Foo", "bar"],
                "foreign_id": 100,
                "active": True
            }
        ]

    def test_given_records_and_model_func_build_data_returns_id_indexed_data(self, input_records):
        def create_test_model(raw):
            return TestModel(**raw)

        data = RepoBuilder.build_data(input_records, create_test_model)

        assert data == {
            "1": TestModel(
                _id=1,
                name="James",
                tags=["Foo", "bar"],
                foreign_id=100,
                active=True
            )
        }
