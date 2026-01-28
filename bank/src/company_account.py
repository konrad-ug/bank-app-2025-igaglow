import os
import requests
from datetime import date
from bank.src.account import Account

class CompanyAccount(Account):
    def __init__(self, company_name, nip):
        self.company_name = company_name
        self.nip = nip if self.is_nip_valid(nip) else "Invalid"
        self.history = []
        self.balance = 0.0

        if self.is_nip_valid(nip):
            if not self.check_nip_with_mf(nip):
                raise ValueError("Company not registered!!")

    def is_nip_valid(self, nip):
        return isinstance(nip, str) and len(nip) == 10

    def check_nip_with_mf(self, nip):
        """Sprawdza NIP w bazie MF. Zwraca True jeśli statusVat == 'Czynny'."""
        mf_url = os.getenv("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl")
        today = date.today().isoformat()
        url = f"{mf_url}/api/search/nip/{nip}?date={today}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            print("MF API response:", data)  # logujemy dla przejrzystości

            # MF API – jeśli znajdzie VAT status
            status_vat = data.get("result", [{}])[0].get("statusVat", "")
            return status_vat == "Czynny"
        except Exception as e:
            print("Error calling MF API:", e)
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