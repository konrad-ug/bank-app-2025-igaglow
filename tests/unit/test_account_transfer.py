from src.account import Account

class TestAccountTransfer:
    def test_transfer_incoming(self):
        account = Account()
        account.transfer_ingoing(1000)
        assert account.balance == 1000

    def test_transfer_incoming_negative_amount(self):
        account = Account()
        account.transfer_ingoing(-1000)
        assert account.balance == 0.0

    def test_transfer_outgoing(self):
        account = Account()
        account.balance = 1000
        account.transfer_outgoing(100)
        assert account.balance == 900

    def test_transfer_outgoing_exceeding_balance(self):
        account = Account()
        account.balance = 1000
        account.transfer_outgoing(10000)
        assert account.balance == 1000

    def test_transfer_outgoing_negative_amount(self):
        account = Account()
        account.balance = 1000
        account.transfer_outgoing(-100)
        assert account.balance == 1000