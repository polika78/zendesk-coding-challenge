import pytest

from searchapp.models.user import User
from searchapp.repository.user_repo import UserRepo

class TestUserRepo:
    @pytest.fixture
    def user_records(self):
        return [
            {
                "_id": 1,
                "name": "Francisca Rasmussen",
                "created_at": "2016-04-15T05:19:46-10:00",
                "verified": True
            },
            {
                "_id": 2,
                "name": "Cross Barlow",
                "created_at": "2016-06-23T10:31:39-10:00",
            }
        ]

    def test_given_json_load_sets_users_and_indexing(self, user_records):
        user_repo = UserRepo()
        expected_users = dict([(str(record["_id"]), User(**record)) for record in user_records])

        user_repo.load(user_records)

        assert user_repo.users == expected_users

        assert user_repo.indexing == {
            'name': {
                "francisca rasmussen": ["1"],
                "cross barlow": ["2"]
            },
            'created_at': {
                "2016-04-15t05:19:46-10:00": ["1"],
                "2016-06-23t10:31:39-10:00": ["2"]
            },
            'verified': {
                "true": ["1"],
                "": ["2"]
            }
        }

    def test_after_loaded_given_id_term_search_by_term_returns_matched_users(self, user_records):
        user_repo = UserRepo()
        user_repo.load(user_records)

        users = user_repo.search_by_term("_id", "1")

        assert users == [User(**user_records[0])]

    def test_after_loaded_given_name_term_search_by_term_returns_matched_users(self, user_records):
        user_repo = UserRepo()
        user_repo.load(user_records)

        users = user_repo.search_by_term("name", "Cross Barlow")

        assert users == [User(**user_records[1])]

    def test_after_loaded_given_created_at_term_search_by_term_returns_matched_users(self, user_records):
        user_repo = UserRepo()
        user_repo.load(user_records)

        users = user_repo.search_by_term("created_at", "2016-04-15T05:19:46-10:00")

        assert users == [User(**user_records[0])]

    def test_after_loaded_given_verified_term_search_by_term_returns_matched_users(self, user_records):
        user_repo = UserRepo()
        user_repo.load(user_records)

        users = user_repo.search_by_term("verified", "True")

        assert users == [User(**user_records[0])]

    def test_after_loaded_given_verified_empty_term_search_by_term_returns_matched_users(self, user_records):
        user_repo = UserRepo()
        user_repo.load(user_records)

        users = user_repo.search_by_term("verified", "")

        assert users == [User(**user_records[1])]

    def test_after_loaded_given_not_found_term_search_by_term_returns_empty_users(self, user_records):
        user_repo = UserRepo()
        user_repo.load(user_records)

        users = user_repo.search_by_term("name", "Foo")

        assert users == []

    def test_after_loaded_given_not_found_id_search_by_term_returns_empty_users(self, user_records):
        user_repo = UserRepo()
        user_repo.load(user_records)

        users = user_repo.search_by_term("_id", "900")

        assert users == []
