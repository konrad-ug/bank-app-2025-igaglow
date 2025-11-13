from src.personal_account import PersonalAccount
import pytest

class TestSubmitForLoan:

    @pytest.fixture()
    def account(self):
        account = PersonalAccount("John", "Doe", "05242206607")

    def test_submit_for_loan_latest_transfers_incoming(self, account):
        account = PersonalAccount("John", "Doe", "05242206607")
        account.history = [50.0, 100.0, 50.0]
        account.submit_for_loan(50.0)
        assert account.balance == 50.0

    def test_submit_for_loan_latest_five_transfers_valid(self, account):
        account = PersonalAccount("John", "Doe", "05242206607")
        account.history = [-50.0, 100.0, 50.0, -10.0, -20.0]
        account.submit_for_loan(50.0)
        assert account.balance == 50.0

    def test_submit_for_loan_latest_five_transfers_invalid(self, account):
        account = PersonalAccount("John", "Doe", "05242206607")
        account.history = [-50.0, -100.0, 50.0, -10.0, -20.0]
        account.submit_for_loan(50.0)
        assert account.balance == 0

    def test_submit_for_loan_latest_transfers_not_incoming(self, account):
        account = PersonalAccount("John", "Doe", "05242206607")
        account.history = [-50.0, 100.0, 50.0]
        account.submit_for_loan(50.0)
        assert account.balance == 0

    def test_submit_for_loan_amount_negative(self, account):
        account = PersonalAccount("John", "Doe", "05242206607")
        account.history = [50.0, 100.0, 50.0]
        account.submit_for_loan(-50.0)
        assert account.balance == 0