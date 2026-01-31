from datetime import date
from bank.src.smtp.smtp import SMTPClient

class Account:
    def __init__(self):
        self.balance = 0
        self.history = []

    def transfer_ingoing(self, sum):
        if sum <= 0:
            return
        self.balance += sum
        self.history.append(sum)

    def transfer_outgoing(self, sum):
        if sum > self.balance or sum <=0:
            return
        self.balance -= sum
        self.history.append(sum * -1)

    message_content_prefix = "Account history"

    def send_history_via_email(self, email_address) -> bool:
        today = date.today().isoformat()
        subject = f"Account Transfer History {today}"
        text = f"{self.message_content_prefix}: {self.history}"

        smtp_client = SMTPClient()
        return smtp_client.send(subject, text, email_address)

    def to_dict(self):
        return {
            "name": getattr(self, "first_name", ""),
            "surname": getattr(self, "last_name", ""),
            "company_name": getattr(self, "company_name", None),
            "pesel": getattr(self, "pesel", None),
            "nip": getattr(self, "nip", None),
            "balance": self.balance,
            "history": self.history
        }