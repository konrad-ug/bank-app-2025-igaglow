from bank.src.account import Account

class CompanyAccount(Account):
    def __init__(self, company_name, nip):
        self.company_name = company_name
        self.nip = nip if self.is_nip_valid(nip) else "Invalid"
        self.history = []

    def is_nip_valid(self, nip):
        if isinstance(nip, str) and len(nip) == 10:
            return True
        return False

    def transfer_express(self, sum):
        if sum <= 0 or self.balance - sum < 0:
            return
        self.balance -= sum + 5.0
        self.history.append(sum * (-1))
        self.history.append(-5.0)

    def check_history_for_ZUS_transfer(self):
        for i in self.history:
            if i == -1775.0:
                return True
        return False

    def take_loan(self, amount):
        if self.balance > amount * 2 and self.check_history_for_ZUS_transfer():
            self.balance += amount
            return True
        return False