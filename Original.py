# Bank Managment Project
import json
import random
import string
from pathlib import Path



class Bank:
    database = Path(__file__).parent / "data.json"
    data = []

    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.loads(fs.read())
        else:
            print("no Such File Exist")

    except Exception as err:
        print(f"an exception occured as {err}")

    @classmethod
    def __update(cls):
        with open(cls.database, 'w') as fs:
            fs.write(json.dumps(Bank.data))

    @classmethod
    def __accountgenerate(cls):
        alpha = random.choices(string.ascii_letters, k = 3)
        num = random.choices(string.digits, k = 3)
        spchar = random.choices("!@#$%^&*", k = 1)
        id = alpha + num + spchar
        random.shuffle(id)
        return "".join(id)



    def Createaccount(self):
        info = {
            "Name": input("Tell your Name: "),
            "Age": int(input("Tell your Age: ")),
            "E-mail": input("Tell your E-mail: "),
            "Pin": int(input("Tell your 4 Digit Pin: ")),
            "AccountNo.": Bank.__accountgenerate(), 
            "Balance": 0
        }
        if info['Age'] < 18 or len(str(info['Pin'])) != 4:
            print("Sorry you cannot Create your account")
        else:
            print("Account has been Created Successfully")
            for i in info:
                print(f"{i} : {info[i]}")
            print("Please note down your Account number")

            Bank.data.append(info)

            Bank.__update()


    def Depositmoney(self):
        account = input("Tell your Account Number: ")
        pin = int(input("Tell your Pin: "))
        
        userdata = [i for i in Bank.data if i['AccountNo.'] == account and i['Pin'] == pin]

        if userdata == False:
            print("Sorry!, no data found")
        else:
            amount = int(input("How much you want to deposite: "))
            if amount > 10000000 or amount < 0:
                print("Sorry the amount is too much you can deposite below 10000000 and above 0")
            else:
                userdata[0]['Balance'] += amount
                Bank.__update()
                print("Amount Deposited Successfully")

    def Withdrawmoney(self):
            account = input("Tell your Account Number: ")
            pin = int(input("Tell your Pin: "))
            
            userdata = [i for i in Bank.data if i['AccountNo.'] == account and i['Pin'] == pin]
    
            if userdata == False:
                print("Sorry!, no data found")
            else:
                amount = int(input("How much you want to Withdraw: "))
                if userdata[0]['Balance'] < amount:
                    print("Sorry you don't have that much money")
                elif amount > 1000000 or amount < 0:
                        print("Sorry the amount is too much you can withdraw below 1000000 and above 0")
                else:
                    userdata[0]['Balance'] -= amount
                    Bank.__update()
                    print("Amount Withdraw Successfully")

    def Bankbalance(self):
            account = input("Tell your Account Number: ")
            pin = int(input("Tell your Pin: "))
                
            userdata = [i for i in Bank.data if i['AccountNo.'] == account and i['Pin'] == pin]
        
            if userdata == False:
                print("Sorry!, no data found")
            else:
                print(f"Bank Balance is: {userdata[0]['Balance']}")

    def Details(self):
        account = input("Tell your Account Number: ")
        pin = int(input("Tell your Pin: "))
                        
        userdata = [i for i in Bank.data if i['AccountNo.'] == account and i['Pin'] == pin]
        if userdata == False:
            print("Sorry!, no data found")
        else:
            print("\n\nYour Information is:\n")
            for i in userdata[0]:
                print(f"{i} : {userdata[0][i]}")

    def Updatingdetails(self):
        account = input("Tell your Account Number: ")
        pin = int(input("Tell your Pin: "))
                                
        userdata = [i for i in Bank.data if i['AccountNo.'] == account and i['Pin'] == pin]

        if userdata == False:
            print("Sorry!, no data found")
        else:
            print("You Cannot Change Age and AccountNumber\n")
            print("Fill the details for changing or leave it empty if no change\n")

            newdata = {
                "Name": input("Please Tell Your new Name or press Enter to skip: "),
                "E-mail": input("Please Tell Your new E-mail or press Enter to skip: "),
                "Pin": input("Please Tell Your new Pin or press Enter to skip: ")
            }

            if newdata["Name"] == "":
                newdata["Name"] = userdata[0]["Name"]

            if newdata["E-mail"] == "":
                newdata["E-mail"] = userdata[0]["E-mail"]

            if newdata["Pin"] == "":
                newdata["Pin"] = userdata[0]["Pin"]

            newdata["Age"] = userdata[0]["Age"]
            newdata["AccountNo."] = userdata[0]["AccountNo."]
            newdata["Balance"] = userdata[0]["Balance"]

            if type(newdata["Pin"] == str):
                newdata["Pin"] = int(newdata["Pin"])

            for i in newdata:
                if newdata[i] == userdata[0][i]:
                    continue
                else:
                    userdata[0][i] = newdata[i]

            Bank.__update()
            print("Details Updated Successfully")

    def Deletingaccount(self):
        account = input("Tell your Account Number: ")
        pin = int(input("Tell your Pin: "))

        userdata = [
            i for i in Bank.data
            if i['AccountNo.'] == account and i['Pin'] == pin
        ]

        if userdata == False:
            print("Sorry!, no data found")
        else:
            check = input("Press y if you actually want to delete the account: ")

            if check == 'y' or check == 'Y':
                index = Bank.data.index(userdata[0])
                Bank.data.pop(index)

                print("Account Deleted Successfully!")

                Bank.__update()
            



user = Bank()

print("Press 1 for Creating an Account")
print("Press 2 for Depositing Money in the Bank")
print("Press 3 for Withdrawing the Money")
print("Press 4 for Check Bank Balance")
print("Press 5 for Details")
print("Press 6 for Updating the Details")
print("Press 7 for Deleting Account")

check = int(input("Tell Your Response: "))

if check == 1:
    user.Createaccount()

if check == 2:
    user.Depositmoney()

if check == 3:
    user.Withdrawmoney()

if check == 4:
    user.Bankbalance()

if check == 5:
    user.Details()

if check == 6:
    user.Updatingdetails()

if check == 7:
    user.Deletingaccount()