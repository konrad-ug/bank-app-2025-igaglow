import unittest
from unittest.mock import MagicMock, patch
from bank.src.accounts_repository import MongoAccountsRepository
from bank.src.personal_account import PersonalAccount


class TestMongoAccountsRepository(unittest.TestCase):

    @patch("bank.src.accounts_repository.MongoClient")
    def test_save_all_calls_delete_and_insert(self, mock_client):
        mock_db = mock_client.return_value["bank"]
        mock_collection = mock_db["accounts"]

        repo = MongoAccountsRepository()
        acc = PersonalAccount("Jan", "Kowalski", "11111111111")

        repo.save_all([acc])

        mock_collection.delete_many.assert_called_once_with({})
        mock_collection.insert_one.assert_called_once()

    @patch("bank.src.accounts_repository.MongoClient")
    def test_load_all_converts_data_to_objects(self, mock_client):
        mock_db = mock_client.return_value["bank"]
        mock_collection = mock_db["accounts"]

        mock_collection.find.return_value = [
            {
                "name": "Kurt",
                "surname": "Cobain",
                "pesel": "89092909246",
                "balance": 100.0,
                "history": [100.0]
            },
            {
                "name": "Tadeusz",
                "surname": "Szcześniak",
                "pesel": "79101011234",
                "balance": 50.0,
                "history": [50.0]
            }
        ]

        repo = MongoAccountsRepository()
        loaded = repo.load_all()

        assert len(loaded) == 2
        assert isinstance(loaded[0], PersonalAccount)
        assert loaded[0].first_name == "Kurt"
        assert loaded[0].balance == 100.0
        assert loaded[1].pesel == "79101011234"

        mock_collection.find.assert_called_once_with({})