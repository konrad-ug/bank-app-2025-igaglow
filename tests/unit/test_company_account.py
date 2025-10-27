from src.company_account import CompanyAccount

class TestCompanyAccount:
    def test_nip_too_short(self):
        account = CompanyAccount("Company", "111")
        assert account.nip == "Invalid"

    def test_nip_too_long(self):
        account = CompanyAccount("Company", "1111111111111111111")
        assert account.nip == "Invalid"

    def test_nip_is_None(self):
        account = CompanyAccount("Company", None)
        assert account.nip == "Invalid"

    def test_transfer_express_enough_balance(self):
        account = CompanyAccount("Company", "111")
        account.balance = 100.0
        account.transfer_express(20.0)
        assert account.balance == 75.0

    def test_transfer_express_not_enough_balance(self):
        account = CompanyAccount("Company", "111")
        account.balance = 100.0
        account.transfer_express(200.0)
        assert account.balance == 100.0

    def test_transfer_express_fee_over_balance(self):
        account = CompanyAccount("Company", "111")
        account.balance = 100.0
        account.transfer_express(100.0)
        assert account.balance == -5.0