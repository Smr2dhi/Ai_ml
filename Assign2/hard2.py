import json
import logging

logging.basicConfig(filename="bank.log",
    level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s")

try:
    with open('accounts.json','r')as file:
        data =json.load(file)

except FileNotFoundError:
    print("File not found")


class InsufficientFundsError(Exception):
    pass
class BankAccount:

    def __init__(self,account_number,owner,balance):
        self.account_number=account_number
        self.owner=owner
        self.balance=balance

        self.account=[]

    def createAccount(self):
        account_number =input("Enter your account number:")
        owner =input("Enter account holder name:")
        
        


    def deposit(self,amount):
        try:
            if amount<0:
                raise ValueError("Value can't be negative")
            
            self.balance+=amount

        except ValueError as e:
            print("Deposit Error:",e)
            logging.error("Deposit error log: ",e)


    def withdrawAmount(self,amount):
            try:
                if amount<=0:
                    raise ValueError("value can't be negative")
                elif self.balance<amount:
                    raise InsufficientFundsError("Amount is less")

                self.balance-=amount
                print("Withdrawn done")

            except InsufficientFundsError as e:
                print("Amount withdraw Error: ",e)
                logging.error("Withdraw log error: ",e)

            except ValueError as e :
                print("Amount value Error: ",e)
                logging.error("withdraw error: ",e)

              
    def checkBalance(self,account_number):
        accounts={
            "account_numeber":"BankAccount"
        }
print("""
            1. Create Account, 
            2. Deposit, 
            3. Withdraw, 
            4. Check Balance,
              5. Exit. 

""")      

while True:
    choice=int(input("enter your choice:"))
    if choice == 1:
        createAccount()

    elif choice == 2:
        depositAmount()

    elif choice ==3:
        withdrawAmount()

    elif choice == 4:
        checkBalance()

    elif choice == 5:
        break

    else:
        print("Invalid choice-----")