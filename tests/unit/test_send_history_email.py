import pytest
from unittest.mock import patch, MagicMock
from bank.src.personal_account import PersonalAccount
from bank.src.company_account import CompanyAccount
from datetime import date

class TestSendHistoryEmail:

    @patch("bank.src.account.SMTPClient.send")
    def test_personal_account_send_history_success(self, mock_send):
        mock_send.return_value = True
        acc = PersonalAccount("John", "Doe", "05242206607")
        acc.history = [100, -1, 500]

        result = acc.send_history_via_email("test@example.com")
        assert result is True

        subject = f"Account Transfer History {date.today().isoformat()}"
        mock_send.assert_called_once_with(subject, "Personal account history: [100, -1, 500]", "test@example.com")

    @patch("bank.src.account.SMTPClient.send")
    def test_personal_account_send_history_failure(self, mock_send):
        mock_send.return_value = False
        acc = PersonalAccount("John", "Doe", "05242206607")
        acc.history = [10, -5]

        result = acc.send_history_via_email("test@example.com")
        assert result is False

    @patch("bank.src.account.SMTPClient.send")
    @patch("bank.src.company_account.CompanyAccount.check_nip_with_mf", return_value=True)  # mockujemy MF
    def test_company_account_send_history_success(self, mock_nip, mock_send):
        mock_send.return_value = True
        acc = CompanyAccount("MyCompany", "1234567890")
        acc.history = [5000, -1000, 500]

        result = acc.send_history_via_email("biz@example.com")
        assert result is True

        subject = f"Account Transfer History {date.today().isoformat()}"
        mock_send.assert_called_once_with(subject, "Company account history: [5000, -1000, 500]", "biz@example.com")

    @patch("bank.src.account.SMTPClient.send")
    @patch("bank.src.company_account.CompanyAccount.check_nip_with_mf", return_value=True)
    def test_company_account_send_history_failure(self, mock_nip, mock_send):
        mock_send.return_value = False
        acc = CompanyAccount("MyCompany", "1234567890")
        acc.history = [200, -50]

        result = acc.send_history_via_email("biz@example.com")
        assert result is False
