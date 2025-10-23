from src.personal_account import PersonalAccount


class TestAccount:
    def test_account_creation(self):
        account = PersonalAccount("John", "Doe", "05242206607")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "05242206607"

    def test_pesel_too_short(self):
        account = PersonalAccount("Jane", "Doe", "111")
        assert account.pesel == "Invalid"

    def test_pesel_too_long(self):
        account = PersonalAccount("Jane", "Doe", "1111111111111111111")
        assert account.pesel == "Invalid"

    def test_pesel_is_None(self):
        account = PersonalAccount("Jane", "Doe", None)
        assert account.pesel == "Invalid"

    # def test_promo(self):
    #     account = Account("John", "Doe", "11111111111", "PROM_XYZ)
    #     assert account.balance == 50.0
    #
    # def test_promo(self):
    #     account = Account("John", "Doe", "11111111111", PRO)
    #     assert account.balance == 0.0
    #
    # def test_promo(self):
    #     account = Account("John", "Doe", "11111111111", None)
    #     assert account.balance == 0.0

    # def test_valid_promo_and_eligible_year(self):
    #     account = PersonalAccount("John", "Doe", "05242206607", "PROM_ABC")
    #     assert account.balance == 50.0

    def test_valid_promo_but_not_eligible_year(self):
        account = PersonalAccount("Jan", "Kowalski", "55010112345", "PROM_ABC")
        assert account.balance == 0.0

    def test_invalid_promo_format(self):
        account = PersonalAccount("John", "Doe", "05242206607", "PRO")
        assert account.balance == 0.0

    def test_no_promo_code(self):
        account = PersonalAccount("John", "Doe", "05242206607", None)
        assert account.balance == 0.0

    def test_invalid_pesel_with_valid_promo(self):
        account = PersonalAccount("John", "Doe", "123", "PROM_ABC")
        assert account.pesel == "Invalid"
        assert account.balance == 0.0

    def test_promo_case_sensitive(self):
        account = PersonalAccount("John", "Doe", "05242206607", "prom_abc")
        assert account.balance == 0.0