import pytest
from unittest.mock import patch
from bank.src.company_account import CompanyAccount

class TestCompanyAccountMF:
    @patch("bank.src.company_account.requests.get")
    def test_nip_valid_czynny(self, mock_get):
        # symulujemy odpowiedź MF
        mock_get.return_value.json.return_value = {
            "result": [{"statusVat": "Czynny"}]
        }
        mock_get.return_value.raise_for_status = lambda: None

        account = CompanyAccount("MyCompany", "1234567890")
        assert account.company_name == "MyCompany"

    @patch("bank.src.company_account.requests.get")
    def test_nip_invalid_not_registered(self, mock_get):
        # MF zwraca nieaktywny status
        mock_get.return_value.json.return_value = {
            "result": [{"statusVat": "Nieaktywny"}]
        }
        mock_get.return_value.raise_for_status = lambda: None

        with pytest.raises(ValueError, match="Company not registered!!"):
            CompanyAccount("BadCompany", "1234567890")

    def test_short_nip_skips_mf(self):
        # NIP nie ma 10 znaków → API MF NIE jest wywoływane
        account = CompanyAccount("ShortNip", "123")
        assert account.nip == "Invalid"
