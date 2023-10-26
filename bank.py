class BankAccount:
    account_number_gen = 1000
    total_available_balance = 0
    total_loan_amount = 0
    loan_enabled = True

    def __init__(self, name, email, address, account_type):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.balance = 0
        self.account_number = BankAccount.account_number_gen
        BankAccount.account_number_gen += 1
        self.loan_taken = 0
        self.transaction_history = []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            BankAccount.total_available_balance += amount
            self.transaction_history.append(f"Deposited: {amount}")
            return f"Amount {amount} deposited successfully."
        else:
            return "Invalid deposit amount."

    def withdraw(self, amount):

        if amount > self.balance:
            return "Withdrawal amount exceeded."
        elif amount > 0:
            self.balance -= amount
            BankAccount.total_available_balance -= amount
            self.transaction_history.append(f"Withdrew: {amount}")
            return f"Withdrawn: {amount}"
        elif amount <= 0:
            return "Invalid withdrawal amount."
        else:
            print("The bank is bankrupt!!!")

    def check_balance(self):
        return f"Available balance: {self.balance}"

    def check_transaction_history(self):
        return self.transaction_history

    def take_loan(self, amount):
        if self.loan_taken < 2 and BankAccount.loan_enabled:
            self.balance += amount
            self.loan_taken += 1
            BankAccount.total_loan_amount += amount
            self.transaction_history.append(f"Loan taken: {amount}")
            return f"Loan of {amount} credited to your account."
        else:
            return "You are not eligible for a loan at the moment."

    def transfer(self, recipient, amount):
        if recipient and recipient.account_number != self.account_number:
            if amount <= self.balance and amount > 0:
                self.balance -= amount
                recipient.balance += amount
                self.transaction_history.append(
                    f"Transferred: {amount} to {recipient.name} ({recipient.account_number})")
                recipient.transaction_history.append(f"Received: {amount} from {self.name} ({self.account_number})")
                return f"Transferred {amount} to {recipient.name} ({recipient.account_number}) successfully."
            else:
                return "Invalid transfer amount or insufficient balance."
        else:
            return "Invalid recipient account or cannot transfer to the same account."


class Admin:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        self.accounts = []
        default_user = BankAccount("saif", "saif@gmail.com", "Dhaka", "s")
        self.accounts.append(default_user)

    def create_account(self, name, email, address, account_type):
        account = BankAccount(name, email, address, account_type)

        if account_type.lower() == 's' or account_type.lower() == 'c':
            self.accounts.append(account)
            print("Account created successfully.")
        else:
            print("Account type doesn't match")
        return account

    def delete_account(self, account):
        BankAccount.total_available_balance -= account.balance
        self.accounts.remove(account)

    def list_all_accounts(self):
        account_details = []
        for account in self.accounts:
            if account.account_type.lower() == 's':
                account_details.append(f"Account Number: {account.account_number}, Name: {account.name}, Balance: {account.balance}, Type: Savings")
            elif account.account_type.lower() == 'c':
                account_details.append(f"Account Number: {account.account_number}, Name: {account.name}, Balance: {account.balance}, Type: Current")
        return account_details

    def check_total_available_balance(self):
        return f"Total available balance in the bank: {BankAccount.total_available_balance}"

    def check_total_loan_amount(self):
        return f"Total loan amount in the bank: {BankAccount.total_loan_amount}"

    def toggle_loan_feature(self, status):
        BankAccount.loan_enabled = status

    def user_login(self):
        name = input("Enter your account name: ")
        user_account_number = int(input("Enter your account number: "))
        user = next((acc for acc in self.accounts if acc.name == name and acc.account_number == user_account_number), None)
        if user:
            print(f"Login as {name} successful!")
            return user
        else:
            print("Invalid user. Please try again.")
            return None


admin_system = Admin('saiful', 1111)

while True:
    print("\nWelcome to the Bank IBBL!")
    print("1. Login as Admin")
    print("2. Login as User")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        entered_name = input("Enter Admin username: ")
        entered_pin = input("Enter Admin PIN: ")
        if entered_name == admin_system.name and entered_pin == str(admin_system.pin):
            print("Admin login successful!")
            while True:
                print("\nAdmin Menu:")
                print("1. Create Account")
                print("2. Delete Account")
                print("3. List All Accounts")
                print("4. Check Total Available Balance")
                print("5. Check Total Loan Amount")
                print("6. Toggle Loan Feature")
                print("7. Logout")
                admin_choice = input("Enter your choice: ")

                if admin_choice == "1":
                    name = input("Enter user's name: ")
                    email = input("Enter user's email: ")
                    address = input("Enter user's address: ")
                    account_type = input("Enter account type (S for Savings/ C for Current): ")
                    admin_system.create_account(name, email, address, account_type)

                elif admin_choice == "2":
                    account_number = int(input("Enter account number to delete: "))
                    account_to_delete = next((acc for acc in admin_system.accounts if acc.account_number == account_number), None)
                    if account_to_delete:
                        admin_system.delete_account(account_to_delete)
                        print("Account deleted successfully.")
                    else:
                        print("Account not found.")

                elif admin_choice == "3":
                    accounts_list = admin_system.list_all_accounts()
                    for account in accounts_list:
                        print(account)

                elif admin_choice == "4":
                    print(admin_system.check_total_available_balance())

                elif admin_choice == "5":
                    print(admin_system.check_total_loan_amount())

                elif admin_choice == "6":
                    status = input("Enter 'on' to enable loan feature, 'off' to disable: ")
                    if status == 'off':
                        print('Loan feature OFF successfully!')
                    elif status == 'on':
                        print('Loan feature ON successfully!')
                    admin_system.toggle_loan_feature(status.lower() == 'on')
                elif admin_choice == "7":
                    break
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("Incorrect information! try again")

    elif choice == "2":
        user = admin_system.user_login()
        if user:
            while True:
                print("\nUser Menu:")
                print("1. Deposit")
                print("2. Withdraw")
                print("3. Check Balance")
                print("4. Take Loan")
                print("5. Transfer Money")
                print("6. View Transaction History")
                print("7. Logout")
                user_choice = input("Enter your choice: ")

                if user_choice == "1":
                    try:
                        amount = float(input("Enter deposit amount: "))
                        print(user.deposit(amount))
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")

                elif user_choice == "2":
                    try:
                        amount = float(input("Enter deposit amount: "))
                        print(user.withdraw(amount))
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")

                elif user_choice == "3":
                    print(user.check_balance())

                elif user_choice == "4":
                    try:
                        amount = float(input("Enter loan amount: "))
                        print(user.take_loan(amount))
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")

                elif user_choice == "5":
                    recipient_account_number = int(input("Enter recipient's account number: "))
                    recipient = next((acc for acc in admin_system.accounts if acc.account_number == recipient_account_number), None)
                    if recipient:
                        try:
                            amount = float(input("Enter transfer amount: "))
                            print(user.transfer(recipient, amount))
                        except ValueError:
                            print("Invalid input. Please enter a valid number.")
                    else:
                        print("Account does not exist.")

                elif user_choice == "6":
                    print(user.check_transaction_history())

                elif user_choice == "7":
                    break

    elif choice == "3":
        print("Thank you for using the Bank IBBL. Goodbye!")
        break

    else:
        print("Invalid choice. Please try again.")


"""
--------------- Login ---------------
Login as Admin: name= saiful, pin= 1111
Login as User: name= saif, account= 1000 (counted 1st account number)

"""