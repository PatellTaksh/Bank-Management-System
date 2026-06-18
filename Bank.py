import json
import random
import re
from pathlib import Path
from datetime import datetime


class Bank:

    DATABASE = Path(__file__).parent / "data.json"

    def __init__(self):
        self.data = self.load_data()

    # DATABASE
    def load_data(self):

        if self.DATABASE.exists():

            try:
                with open(self.DATABASE, "r") as file:
                    return json.load(file)

            except Exception:
                return []

        return []

    def save_data(self):

        with open(self.DATABASE, "w") as file:
            json.dump(
                self.data,
                file,
                indent=4
            )

    # VALIDATIONS
    def validate_email(self, email):

        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        return re.match(pattern, email)

    def validate_pin(self, pin):

        return pin.isdigit() and len(pin) == 4

    def email_exists(self, email):

        return any(
            user["Email"].lower() == email.lower()
            for user in self.data
        )

    # ACCOUNT NUMBER
    def generate_account_number(self):

        while True:

            account_number = str(
                random.randint(
                    1000000,
                    9999999
                )
            )

            exists = any(
                user["AccountNo"] == account_number
                for user in self.data
            )

            if not exists:
                return account_number

    # FIND USER
    def find_user(self, account_no, pin):

        for user in self.data:

            if (
                user["AccountNo"] == account_no
                and user["Pin"] == pin
            ):
                return user

        return None

    # CREATE ACCOUNT
    def create_account(
        self,
        name,
        age,
        email,
        pin
    ):

        if name.strip() == "":
            return False, "Name cannot be empty"

        if age < 18:
            return False, "Age must be 18 or above"

        if not self.validate_email(email):
            return False, "Invalid Email"

        if self.email_exists(email):
            return False, "Email already registered"

        if not self.validate_pin(pin):
            return False, "PIN must be exactly 4 digits"

        account_no = self.generate_account_number()

        user = {

            "Name": name,
            "Age": age,
            "Email": email,
            "Pin": pin,
            "AccountNo": account_no,
            "Balance": 0,
            "Transactions": []

        }

        self.data.append(user)

        self.save_data()

        return (
            True,
            f"Account Created Successfully! Account Number: {account_no}"
        )

    # DEPOSIT
    def deposit(
        self,
        account_no,
        pin,
        amount
    ):

        user = self.find_user(
            account_no,
            pin
        )

        if not user:
            return False, "Invalid Account Number or PIN"

        if amount <= 0:
            return False, "Amount must be greater than 0"

        user["Balance"] += amount

        user["Transactions"].append(
            {
                "Type": "Deposit",
                "Amount": amount,
                "Date": datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                )
            }
        )

        self.save_data()

        return True, "Amount Deposited Successfully"

    # WITHDRAW
    def withdraw(
        self,
        account_no,
        pin,
        amount
    ):

        user = self.find_user(
            account_no,
            pin
        )

        if not user:
            return False, "Invalid Account Number or PIN"

        if amount <= 0:
            return False, "Invalid Amount"

        if amount > user["Balance"]:
            return False, "Insufficient Balance"

        user["Balance"] -= amount

        user["Transactions"].append(
            {
                "Type": "Withdraw",
                "Amount": amount,
                "Date": datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                )
            }
        )

        self.save_data()

        return True, "Amount Withdrawn Successfully"

    # BALANCE
    def check_balance(
        self,
        account_no,
        pin
    ):

        user = self.find_user(
            account_no,
            pin
        )

        if not user:
            return False, "Invalid Account Number or PIN"

        return True, user["Balance"]

    # ACCOUNT DETAILS
    def account_details(
        self,
        account_no,
        pin
    ):

        user = self.find_user(
            account_no,
            pin
        )

        if not user:
            return False, "Invalid Account Number or PIN"

        return True, user

    # UPDATE ACCOUNT
    def update_account(
        self,
        account_no,
        pin,
        new_name=None,
        new_email=None,
        new_pin=None
    ):

        user = self.find_user(
            account_no,
            pin
        )

        if not user:
            return False, "Invalid Account Number or PIN"

        if new_name:
            user["Name"] = new_name

        if new_email:

            if not self.validate_email(
                new_email
            ):
                return False, "Invalid Email"

            for existing_user in self.data:

                if (
                    existing_user["Email"].lower()
                    == new_email.lower()
                    and existing_user["AccountNo"]
                    != account_no
                ):
                    return False, "Email already registered"

            user["Email"] = new_email

        if new_pin:

            if not self.validate_pin(
                new_pin
            ):
                return False, "PIN must be 4 digits"

            user["Pin"] = new_pin

        self.save_data()

        return True, "Account Updated Successfully"

    # DELETE ACCOUNT
    def delete_account(
        self,
        account_no,
        pin
    ):

        user = self.find_user(
            account_no,
            pin
        )

        if not user:
            return False, "Invalid Account Number or PIN"

        self.data.remove(user)

        self.save_data()

        return True, "Account Deleted Successfully"

    # TRANSACTION HISTORY
    def get_transactions(
        self,
        account_no,
        pin
    ):

        user = self.find_user(
            account_no,
            pin
        )

        if not user:
            return False, "Invalid Account Number or PIN"

        return True, user["Transactions"]

    

if __name__ == "__main__":

    bank = Bank()

    while True:

        print("\n===== BANK MANAGEMENT SYSTEM =====")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Account Details")
        print("6. Exit")

        choice = input("\nEnter Choice: ")

        if choice == "1":

            name = input("Name: ")
            age = int(input("Age: "))
            email = input("Email: ")
            pin = input("PIN (4 digits): ")

            status, message = bank.create_account(
                name,
                age,
                email,
                pin
            )

            print(message)

        elif choice == "2":

            account = input("Account Number: ")
            pin = input("PIN: ")
            amount = float(input("Amount: "))

            status, message = bank.deposit(
                account,
                pin,
                amount
            )

            print(message)

        elif choice == "3":

            account = input("Account Number: ")
            pin = input("PIN: ")
            amount = float(input("Amount: "))

            status, message = bank.withdraw(
                account,
                pin,
                amount
            )

            print(message)

        elif choice == "4":

            account = input("Account Number: ")
            pin = input("PIN: ")

            status, message = bank.check_balance(
                account,
                pin
            )

            print(message)

        elif choice == "5":

            account = input("Account Number: ")
            pin = input("PIN: ")

            status, data = bank.account_details(
                account,
                pin
            )

            if status:
                print(data)
            else:
                print(data)

        elif choice == "6":
            print("Thank You!")
            break

        else:
            print("Invalid Choice")