from src.personal_account import PersonalAccount
import pytest

@pytest.fixture
def account():
    return PersonalAccount("John", "Doe", "05242206607")

class TestSubmitForLoan:

    @pytest.mark.parametrize(
        "history, amount, expected_balance",
        [
            ([50.0, 100.0, 50.0], 50.0, 50.0),
            ([-50, 100, 50, -10, -20], 50.0, 50.0),
            ([-50, -100, 50, -10, -20], 50.0, 0.0),
            ([-50, 100, 50], 50.0, 0.0),
            ([50, 100, 50], -50.0, 0.0),
        ]
    )
    def test_submit_for_loan(self, account, history, amount, expected_balance):
        account.history = history
        account.submit_for_loan(amount)
        assert account.balance == expected_balance