from src.account import Account

class PersonalAccount(Account):
    def __init__(self, first_name, last_name, pesel, promo_code = None):
        self.first_name = first_name
        self.last_name = last_name
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
        self.balance = 50.0 if (self.is_eligible_for_promo(self.pesel) and self.check_promo(promo_code)) else 0
        self.history = []

    def is_pesel_valid(self, pesel):
        if isinstance(pesel, str) and len(pesel) == 11:
            return True
        return False

    def check_promo(self, promo_code):
        if not isinstance(promo_code, str):
            return False
        if not promo_code.startswith("PROM_"):
            return False
        return len(promo_code) == len("PROM_XYZ")

    def is_eligible_for_promo(self, pesel):
        if not self.is_pesel_valid(pesel):
            return False

        year = int(pesel[0:2])
        month = int(pesel[2:4])

        if 1 <= month <= 12:
            year += 1900
        elif 21 <= month <= 32:
            year += 2000
        else:
            return False

        return year > 1960

    def transfer_express(self, sum):
        if sum <= 0 or self.balance - sum < 0:
            return
        self.balance -= sum + 1.0
        self.history.append(sum * (-1))
        self.history.append(-1.0)

    def submit_for_loan(self, amount):
        if amount <= 0:
            return False
        if self.history[-1] > 0 and self.history[-2] > 0 and self.history[-3] > 0:
            self.balance += amount
            return True
        elif len(self.history) >=5:
            if self.history[-1] + self.history[-2] + self.history[-3] + self.history[-4] + self.history[-5] > amount:
                self.balance += amount
                return True
        return False