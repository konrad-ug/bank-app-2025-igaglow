from bank.src.personal_account import PersonalAccount
import pytest


class TestAccount:

    @pytest.mark.parametrize(
        "pesel, expected",
        [
            ("111", "Invalid"),
            ("1111111111111111111", "Invalid"),
            (None, "Invalid"),
        ]
    )
    def test_pesel_invalid(self, pesel, expected):
        acc = PersonalAccount("Jane", "Doe", pesel)
        assert acc.pesel == expected

    def test_account_creation(self):
        account = PersonalAccount("John", "Doe", "05242206607")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "05242206607"

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

    @pytest.mark.parametrize(
        "start_balance, amount, expected_balance",
        [
            (100.0, 20.0, 79.0),
            (100.0, 200.0, 100.0),
            (100.0, 100.0, -1.0),
        ]
    )
    def test_transfer_express(self, start_balance, amount, expected_balance):
        acc = PersonalAccount("John", "Doe", "05242206607", "PROM_ABC")
        acc.balance = start_balance
        acc.transfer_express(amount)
        assert acc.balance == expected_balance

    def test_submit_for_loan_returns_false_if_conditions_not_met(self):
        account = PersonalAccount("John", "Doe", "05242206607")
        account.history = []
        result = account.submit_for_loan(100)  # amount > 0
        assert result is False

    def test_is_eligible_for_promo_invalid_month(self):
        account = PersonalAccount("John", "Doe", "99132206607")
        assert account.is_eligible_for_promo("99132206607") is False

