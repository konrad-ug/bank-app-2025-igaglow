from bank.src.company_account import CompanyAccount
import pytest

@pytest.fixture
def account():
    return CompanyAccount("Company", "1234567890", validate_mf=False)

class TestTakeloan:

    @pytest.mark.parametrize(
        "history, balance, amount, expected_balance",
        [
            ([-1775.0, 100.0, 50.0], 200.0, 50.0, 250.0),  # udzielona
            ([-50, 100, 50, -10, -20], 200.0, 50.0, 200.0),  # brak -1775 → brak pożyczki
            ([-1775.0, -100, 50, -10, -20], 50.0, 50.0, 50.0),  # zły balance → brak pożyczki
            ([-100, 50, -10, -20], 300.0, 50.0, 300.0),  # brak -1775 → brak pożyczki
        ]
    )
    def test_take_loan(self, account, history, balance, amount, expected_balance):
        account.history = history
        account.balance = balance
        account.take_loan(amount)
        assert account.balance == expected_balance