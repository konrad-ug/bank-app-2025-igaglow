from pymongo import MongoClient
from bank.src.personal_account import PersonalAccount

class MongoAccountsRepository:
    def __init__(self):
        self._client = MongoClient("mongodb://localhost:27017/")
        self._db = self._client["bank"]
        self._collection = self._db["accounts"]

    def save_all(self, accounts):
        self._collection.delete_many({})
        for account in accounts:
            self._collection.insert_one(account.to_dict())

    def load_all(self):
        accounts_data = self._collection.find({})
        loaded_accounts = []
        for data in accounts_data:
            acc = PersonalAccount(data["name"], data["surname"], data["pesel"])
            acc.balance = data["balance"]
            acc.history = data["history"]
            loaded_accounts.append(acc)
        return loaded_accounts