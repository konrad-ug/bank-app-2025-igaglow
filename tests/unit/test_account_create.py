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

    def test_pesel_is_None(self):
        account = Account("Jane", "Doe", None)
        assert account.pesel == "Invalid"

    def test_promo(self):
        account = Account("John", "Doe", "11111111111", PROM_XYZ)
        assert account.balance == 50.0

    def test_promo(self):
        account = Account("John", "Doe", "11111111111", PRO)
        assert account.balance == 0.0

    def test_promo(self):
        account = Account("John", "Doe", "11111111111", None)
        assert account.balance == 0.0