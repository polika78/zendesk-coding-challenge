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

    @pytest.fixture
    def input_data(self):
        return {
            "1": TestModel(
                _id=1,
                name="James",
                tags=["Foo", "bar"],
                foreign_id=100,
                active=True
            )
        }

    @pytest.fixture
    def input_multiple_records(self):
        return [
            {
                "_id": 1,
                "name": "James",
                "tags": ["Foo", "bar"],
                "foreign_id": 100,
                "active": True
            },
            {
                "_id": 5,
                "name": "Tom",
                "tags": ["Bar", "foo"],
                "foreign_id": 200,
                "active": True
            }
        ]

    @pytest.fixture
    def input_multiple_data(self):
        return {
            "1": TestModel(
                _id=1,
                name="James",
                tags=["Foo", "bar"],
                foreign_id=100,
                active=True
            ),
            "5": TestModel(
                _id=5,
                name="Tom",
                tags=["Bar", "foo"],
                foreign_id=200,
                active=True
            )
        }

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

    def test_given_data_and_string_type_term_build_search_index_returns_term_indexed_map(self, input_data):
        indexed_map = RepoBuilder.build_search_index('name', input_data)

        assert indexed_map == {
            'james': ["1"]
        }

    def test_given_data_and_int_type_term_build_search_index_returns_term_indexed_map(self, input_data):
        indexed_map = RepoBuilder.build_search_index('foreign_id', input_data)

        assert indexed_map == {
            "100": ["1"]
        }

    def test_given_data_and_array_type_term_build_search_index_returns_indexed_map(self, input_data):
        indexed_map = RepoBuilder.build_search_index('tags', input_data)

        assert indexed_map == {
            'foo': ["1"],
            'bar': ["1"]
        }

    def test_given_multiple_records_and_model_func_build_data_returns_id_indexed_data(self, input_multiple_records):
        def create_test_model(raw):
            return TestModel(**raw)

        data = RepoBuilder.build_data(input_multiple_records, create_test_model)

        assert data == {
            "1": TestModel(
                _id=1,
                name="James",
                tags=["Foo", "bar"],
                foreign_id=100,
                active=True
            ),
            "5": TestModel(
                _id=5,
                name="Tom",
                tags=["Bar", "Foo"],
                foreign_id=100,
                active=True
            )
        }

    def test_given_multiple_data_and_string_type_term_build_search_index_returns_term_indexed_map(self, input_multiple_data):
        indexed_map = RepoBuilder.build_search_index('name', input_multiple_data)

        assert indexed_map == {
            'james': ["1"],
            'tom': ["5"]
        }

    def test_given_multiple_data_and_int_type_term_build_search_index_returns_term_indexed_map(self, input_multiple_data):
        indexed_map = RepoBuilder.build_search_index('foreign_id', input_multiple_data)

        assert indexed_map == {
            "100": ["1"],
            "200": ["5"]
        }

    def test_given_multiple_data_and_array_type_term_build_search_index_returns_indexed_map(self, input_multiple_data):
        indexed_map = RepoBuilder.build_search_index('tags', input_multiple_data)

        assert indexed_map == {
            'foo': ["1", "5"],
            'bar': ["1", "5"]
        }
