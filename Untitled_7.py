
class BankAccount:
    def __init__(self, owner, account_number, balance):
        self.owner = owner
        self.account_number = account_number
        self.balance = balance

class Bank:
    def __init__(self):
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)
        print("Рахунок створено!")

    def deposit(self, account_number, amount):
        for account in self.accounts:
            if account.account_number == account_number:
                if amount > 0:
                    account.balance += amount
                    print("Рахунок поповнено!")
                return
        print("Рахунок не знайдено!")

    def withdraw(self, account_number, amount):
        for account in self.accounts:
            if account.account_number == account_number:
                if 0 < amount <= account.balance:
                    account.balance -= amount
                    print("Кошти знято!")
                else:
                    print("Недостатньо коштів!")
                return
        print("Рахунок не знайдено!")

    def transfer(self, from_number, to_number, amount):
        sender = None
        receiver = None

        for account in self.accounts:
            if account.account_number == from_number:
                sender = account
            if account.account_number == to_number:
                receiver = account

        if sender and receiver and 0 < amount <= sender.balance:
            sender.balance -= amount
            receiver.balance += amount
            print("Переказ виконано!")
        else:
            print("Помилка переказу!")

    def show_accounts(self):
        for account in self.accounts:
            print(f"Власник: {account.owner}")
            print(f"Номер рахунку: {account.account_number}")
            print(f"Баланс: {account.balance} грн")
            print("-" * 30)

bank = Bank()

bank.add_account(BankAccount("Іван", "1001", 5000))
bank.add_account(BankAccount("Петро", "1002", 3000))

bank.deposit("1001", 1000)
bank.withdraw("1002", 500)
bank.transfer("1001", "1002", 2000)

bank.show_accounts()
