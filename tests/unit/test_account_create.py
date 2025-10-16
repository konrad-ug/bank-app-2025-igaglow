from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "05242206607")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "05242206607"

    def test_pesel_too_short(self):
        account = Account("Jane", "Doe", "111")
        assert account.pesel == "Invalid"

    def test_pesel_too_long(self):
        account = Account("Jane", "Doe", "1111111111111111111")
        assert account.pesel == "Invalid"