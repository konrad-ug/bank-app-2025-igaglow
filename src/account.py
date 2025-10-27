class Account:
    def __init__(self):
        self.balance = 0

    def transfer_ingoing(self, sum):
        if sum <= 0:
            return
        self.balance += sum

    def transfer_outgoing(self, sum):
        if sum > self.balance or sum <=0:
            return
        self.balance -= sum