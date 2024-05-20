################################
# Name: Pravesh Bhandari
# Section: 1 Mechanical
# Student ID Number: 02230270
################################
# REFERENCES
# https://www.w3schools.com/python/python_classes.asp
# https://www.geeksforgeeks.org/python-classes-and-objects/
# https://www.geeksforgeeks.org/python-program-to-create-bankaccount-class-with-deposit-withdraw-function/
# https://youtu.be/ZQkA44lDtIk?si=1jlcJhPR0QtwwB_x
# https://youtu.be/xTh-ln2XhgU?si=1pfSFDgPvfl2kSQy
################################


import random

# Base BankAccount class
class BankAccount:
    def __init__(self, account_number, account_type):
        self.account_number = account_number
        self.balance = 0.0
        self.account_type = account_type

    def deposit_money(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw_money(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def to_string(self):
        return f"{self.account_number},{self.balance},{self.account_type}"

    @classmethod
    def from_string(cls, account_str):
        account_number, balance, account_type = account_str.strip().split(',')
        if account_type.lower() == 'personal':
            account = PersonalBankAccount(account_number)
        elif account_type.lower() == 'business':
            account = BusinessBankAccount(account_number)
        else:
            raise ValueError("Unknown account type")
        account.balance = float(balance)
        return account

# PersonalBankAccount subclass
class PersonalBankAccount(BankAccount):
    def __init__(self, account_number):
        super().__init__(account_number, 'Personal')

# BusinessBankAccount subclass
class BusinessBankAccount(BankAccount):
    def __init__(self, account_number):
        super().__init__(account_number, 'Business')

# Bank class to manage all accounts
class Bank:
    def __init__(self):
        self.accounts = {}
        self.load_accounts_from_file()

    def create_new_account(self, account_type):
        account_number = str(random.randint(100000, 999999))
        account_type = account_type.lower()
        if account_type == 'personal':
            account = PersonalBankAccount(account_number)
        elif account_type == 'business':
            account = BusinessBankAccount(account_number)
        else:
            raise ValueError("Unknown account type")
        password = str(random.randint(1000, 9999))
        self.accounts[account_number] = {'account': account, 'password': password}
        self.save_accounts_to_file()
        return account_number, password

    def authenticate(self, account_number, password):
        account_info = self.accounts.get(account_number)
        if account_info and account_info['password'] == password:
            return account_info['account']
        return None

    def transfer_funds(self, from_account, to_account_number, amount):
        to_account_info = self.accounts.get(to_account_number)
        if to_account_info and from_account.withdraw_money(amount):
            to_account_info['account'].deposit_money(amount)
            self.save_accounts_to_file()
            return True
        return False

    def delete_account(self, account_number):
        if self.accounts.pop(account_number, None):
            self.save_accounts_to_file()
            return True
        return False

    def save_accounts_to_file(self):
        with open('accounts.txt', 'w') as file:
            for acc_number, acc_info in self.accounts.items():
                account_str = acc_info['account'].to_string()
                password = acc_info['password']
                file.write(f"Account Number: {acc_number}\n")
                file.write(f"Balance: {acc_info['account'].balance}\n")
                file.write(f"Account Type: {acc_info['account'].account_type}\n")
                file.write(f"Password: {password}\n")
                file.write("\n")  # Newline for readability

    def load_accounts_from_file(self):
        try:
            with open('accounts.txt', 'r') as file:
                lines = file.readlines()
                for i in range(0, len(lines), 5):
                    account_number = lines[i].strip().split(": ")[1]
                    balance = float(lines[i+1].strip().split(": ")[1])
                    account_type = lines[i+2].strip().split(": ")[1]
                    password = lines[i+3].strip().split(": ")[1]

                    if account_type.lower() == 'personal':
                        account = PersonalBankAccount(account_number)
                    elif account_type.lower() == 'business':
                        account = BusinessBankAccount(account_number)
                    else:
                        raise ValueError("Unknown account type")
                    account.balance = balance
                    self.accounts[account_number] = {'account': account, 'password': password}
        except FileNotFoundError:
            pass
        except IndexError:
            print("File format is incorrect or incomplete.")

# Main function for user interaction
def main():
    bank = Bank()

    while True:
        print("\n--- Bank Application Menu ---")
        choice = input("1. Create Account\n2. Login\n3. Exit\nEnter choice: ")

        if choice == '1':
            account_type = input("Enter account type (Personal/Business): ").strip().lower()
            if account_type not in ['personal', 'business']:
                print("Invalid account type. Please enter 'Personal' or 'Business'.")
                continue
            acc_num, pwd = bank.create_new_account(account_type)
            print(f"Account created. Account Number: {acc_num}, Password: {pwd}")

        elif choice == '2':
            acc_num = input("Enter account number: ")
            pwd = input("Enter password: ")
            account = bank.authenticate(acc_num, pwd)
            if account:
                while True:
                    print("\n--- Account Menu ---")
                    acc_choice = input("1. Deposit Money\n2. Withdraw Money\n3. Check Balance\n4. Transfer Funds\n5. Delete Account\n6. Logout\nEnter choice: ")

                    if acc_choice == '1':
                        amount = float(input("Enter amount to deposit: "))
                        if account.deposit_money(amount):
                            bank.save_accounts_to_file()
                            print("Deposit successful.")
                        else:
                            print("Deposit failed.")

                    elif acc_choice == '2':
                        amount = float(input("Enter amount to withdraw: "))
                        if account.withdraw_money(amount):
                            bank.save_accounts_to_file()
                            print("Withdrawal successful.")
                        else:
                            print("Insufficient funds.")

                    elif acc_choice == '3':
                        print(f"Balance: {account.balance}")

                    elif acc_choice == '4':
                        to_acc_num = input("Enter account number to transfer to: ")
                        amount = float(input("Enter amount to transfer: "))
                        if bank.transfer_funds(account, to_acc_num, amount):
                            print("Transfer successful.")
                        else:
                            print("Transfer failed.")

                    elif acc_choice == '5':
                        if bank.delete_account(acc_num):
                            print("Account deleted successfully.")
                            break
                        else:
                            print("Account deletion failed.")

                    elif acc_choice == '6':
                        break

                    else:
                        print("Invalid choice.")

            else:
                print("Login failed. Invalid account number or password.")

        elif choice == '3':
            print("Exiting...")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
