import pytest
from src.accounts_registry import AccountsRegistry
from src.personal_account import PersonalAccount


@pytest.fixture
def registry():
    return AccountsRegistry()


@pytest.fixture
def sample_account():
    return PersonalAccount("John", "Doe", "05242206607")


class TestAccountsRegistry:

    def test_add_account(self, registry, sample_account):
        registry.add_account(sample_account)
        assert registry.count_accounts() == 1
        assert registry.get_all_accounts()[0] == sample_account

    def test_find_existing_pesel(self, registry, sample_account):
        registry.add_account(sample_account)
        result = registry.find_by_pesel("05242206607")
        assert result is not None
        assert result.pesel == "05242206607"

    def test_find_non_existing_pesel(self, registry):
        result = registry.find_by_pesel("99999999999")
        assert result is None

    def test_get_all_accounts(self, registry, sample_account):
        registry.add_account(sample_account)
        accounts = registry.get_all_accounts()
        assert isinstance(accounts, list)
        assert len(accounts) == 1
        assert accounts[0] == sample_account

    def test_count_accounts(self, registry, sample_account):
        assert registry.count_accounts() == 0
        registry.add_account(sample_account)
        assert registry.count_accounts() == 1
        registry.add_account(PersonalAccount("Alice", "Smith", "01234567890"))
        assert registry.count_accounts() == 2