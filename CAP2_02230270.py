import random

class Account:
    def __init__(self, account_number, account_type):
        self.account_number = account_number
        self.balance = 0.0
        self.account_type = account_type

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def to_str(self):
        return f"{self.account_number},{self.balance},{self.account_type}"

    @classmethod
    def from_str(cls, account_str):
        account_number, balance, account_type = account_str.strip().split(',')
        account = cls(account_number, account_type)
        account.balance = float(balance)
        return account

class PersonalAccount(Account):
    def __init__(self, account_number):
        super().__init__(account_number, 'Personal')

class BusinessAccount(Account):
    def __init__(self, account_number):
        super().__init__(account_number, 'Business')

class Bank:
    def __init__(self):
        self.accounts = {}
        self.load_accounts()

    def create_account(self, account_type):
        account_number = str(random.randint(100000, 999999))
        if account_type == 'Personal':
            account = PersonalAccount(account_number)
        else:
            account = BusinessAccount(account_number)
        password = str(random.randint(1000, 9999))
        self.accounts[account_number] = {'account': account, 'password': password}
        self.save_accounts()
        return account_number, password

    def login(self, account_number, password):
        account_info = self.accounts.get(account_number)
        if account_info and account_info['password'] == password:
            return account_info['account']
        return None

    def transfer_money(self, from_account, to_account_number, amount):
        to_account_info = self.accounts.get(to_account_number)
        if to_account_info and from_account.withdraw(amount):
            to_account_info['account'].deposit(amount)
            self.save_accounts()
            return True
        return False

    def delete_account(self, account_number):
        if self.accounts.pop(account_number, None):
            self.save_accounts()
            return True
        return False

    def save_accounts(self):
        with open('accounts.txt', 'w') as file:
            for acc_number, acc_info in self.accounts.items():
                account_str = acc_info['account'].to_str()
                password = acc_info['password']
                file.write(f"{account_str},{password}\n")

    def load_accounts(self):
        try:
            with open('accounts.txt', 'r') as file:
                for line in file:
                    account_str, password = line.strip().rsplit(',', 1)
                    account = Account.from_str(account_str)
                    self.accounts[account.account_number] = {'account': account, 'password': password}
        except FileNotFoundError:
            pass

def main():
    bank = Bank()

    while True:
        print("\n--- Bank Application Menu ---")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            account_type = input("Enter account type (Personal/Business): ")
            acc_num, pwd = bank.create_account(account_type)
            print(f"Account created. Account Number: {acc_num}, Password: {pwd}")

        elif choice == '2':
            acc_num = input("Enter account number: ")
            pwd = input("Enter password: ")
            account = bank.login(acc_num, pwd)
            if account:
                while True:
                    print("\n--- Account Menu ---")
                    print("1. Deposit")
                    print("2. Withdraw")
                    print("3. Check Balance")
                    print("4. Transfer Money")
                    print("5. Delete Account")
                    print("6. Logout")
                    acc_choice = input("Enter choice: ")

                    if acc_choice == '1':
                        amount = float(input("Enter amount to deposit: "))
                        if account.deposit(amount):
                            print("Deposit successful.")
                        else:
                            print("Deposit failed. Please enter a positive amount.")

                    elif acc_choice == '2':
                        amount = float(input("Enter amount to withdraw: "))
                        if account.withdraw(amount):
                            print("Withdrawal successful.")
                        else:
                            print("Insufficient funds or invalid amount.")

                    elif acc_choice == '3':
                        print(f"Balance: {account.balance}")

                    elif acc_choice == '4':
                        to_acc_num = input("Enter account number to transfer to: ")
                        amount = float(input("Enter amount to transfer: "))
                        if bank.transfer_money(account, to_acc_num, amount):
                            print("Transfer successful.")
                        else:
                            print("Transfer failed. Please check the details and try again.")

                    elif acc_choice == '5':
                        if bank.delete_account(acc_num):
                            print("Account deleted successfully.")
                            break
                        else:
                            print("Account deletion failed.")

                    elif acc_choice == '6':
                        print("Logged out.")
                        break

                    else:
                        print("Invalid choice. Please try again.")

            else:
                print("Login failed. Invalid account number or password.")

        elif choice == '3':
            print("Exiting... Thank you for using our bank services!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
