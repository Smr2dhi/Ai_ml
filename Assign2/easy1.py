
class BankAccount:
    count_account=0
    def __init__(self,Account_number,owner,balance):
        BankAccount.count_account+=1
        self.Account_number=Account_number
        self.owner =owner
        self.balance=balance
        

    def deposit(self,amount):
        self.balance+=amount
        print(f"Amount deposited={amount}: ",self.balance)

    def withdraw(self,amount):
        if self.balance<amount:
            print("Insufficient amount= balance is:",self.balance)
        else:
            self.balance-=amount
            print("Amount withdraw =",amount,": Balance is: ",self.balance-amount)

    def checkBalance(self):
        print(f"{self.owner} {(self.Account_number)} balance is: {self.balance}")

p1=BankAccount("ACC1001","Sam",8000)

p2=BankAccount("Acc1002","Shruti",0)



p1.deposit(500)
p1.withdraw(200)
p1.checkBalance()
print("\n")

p2.deposit(300)
p2.withdraw(200)
p2.checkBalance()




print("Total account=",BankAccount.count_account)