from src.account import Account

class PersonalAccount(Account):
    def __init__(self, first_name, last_name, pesel, promo_code = None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0.0
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"


    def is_pesel_valid(self, pesel):
        if isinstance(pesel, str) and len(pesel) == 11:
            return True
        return False

    # def check_promo(self, promo_code):
    #     if promo_code is None:
    #
    #     return False

    def check_promo(self, promo_code):
        if not isinstance(promo_code, str):
            return False
        if not promo_code.startswith("PROM_"):
            return False
        return len(promo_code) > len("PROM_")

    def is_eligible_for_promo(self, pesel):
        if not self.is_pesel_valid(pesel):
            return False

        year = int(pesel[0:2])
        month = int(pesel[2:4])

        if 1 <= month <= 12:
            year += 1900
        elif 21 <= month <= 32:
            year += 2000
        elif 41 <= month <= 52:
            year += 2100
        elif 61 <= month <= 72:
            year += 2200
        elif 81 <= month <= 92:
            year += 1800
        else:
            return False

        return year > 1960

    # def transfer_ingoing(self, sum):
    #     if sum <= 0:
    #         return
    #     self.balance += sum
    #
    # def transfer_outgoing(self, sum):
    #     if sum > self.balance or sum <=0:
    #         return
    #     self.balance -= sum