class BankAccount:
    def __init__(self, account_number: str, balance: float = 0.0):
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount: float):
        if amount > 0:
            self.balance += amount
            print(self.balance)
        else:
            print("Сума поповнення має бути більшою за 0.")

    def withdraw(self, amount: float):
        if amount > self.balance:
            print("Недостатньо коштів на рахунку!")
        elif amount <= 0:
            print("Сума зняття має бути більшою за 0.")
        else:
            self.balance -= amount
            print(self.balance)