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