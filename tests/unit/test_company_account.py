from bank.src.company_account import CompanyAccount
from unittest.mock import patch
import pytest
import requests

class TestCompanyAccount:
    @pytest.mark.parametrize("nip", ["111", "1111111111111111111", None])
    def test_invalid_nip(self, nip):
        # account = CompanyAccount("Company", nip)
        account = CompanyAccount("Company", nip, validate_mf=False)
        assert account.nip == "Invalid"

    @pytest.mark.parametrize(
        "start_balance, amount, expected_balance",
        [
            (100.0, 20.0, 75.0),
            (100.0, 200.0, 100.0),
            (100.0, 100.0, -5.0),
        ]
    )

    def test_transfer_express(self, start_balance, amount, expected_balance):
        account = CompanyAccount("Company", "1234567890", validate_mf=False)
        account.balance = start_balance
        account.transfer_express(amount)
        assert account.balance == expected_balance

    def test_check_nip_with_mf_api_error(self):
        account = CompanyAccount("Company", "1234567890", validate_mf=False)

        with patch("requests.get", side_effect=requests.exceptions.RequestException):
            result = account.check_nip_with_mf("1234567890")

        assert result is False