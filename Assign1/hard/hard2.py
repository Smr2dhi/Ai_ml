transactions = [
    ("ACC1", "deposit",  5000),
    ("ACC2", "deposit",  3000),
    ("ACC1", "withdraw", 1200),
    ("ACC1", "deposit",  800),
    ("ACC3", "deposit",  700),
    ("ACC2", "withdraw", 3500),
    ("ACC1", "withdraw", 2000),
]
balances={}
 
def build_balance():
    for account, str_type , amount in transactions:
        if account not in balances:
            balances[account]=0
           
        if str_type=="deposit":
            balances[account]+=amount
        elif str_type =="withdraw":
            balances[account]-=amount
    print("balance:",balances)
 
 
negBal=set()
def flag_overdrawn(balances):
    for account,balance in balances.items():
        if balance<0:
            negBal.add(account)
    print("Over drawn account:", negBal)
 
def account_report(transactions, reportId):
    balance = 0
 
    for id, txt_type, amount in transactions:
 
        if reportId.lower() == id.lower():
 
            print(txt_type, amount)
 
            if txt_type == "deposit":
                balance += amount
 
            elif txt_type == "withdraw":
                balance -= amount
 
    print("Final balance:", balance)
 
def largest_transaction():
    max_amount=0
    deposit=0
    withdraw=0
   
    for id,strType,amount in transactions:
        if amount>max_amount:
            max_amount=amount
           
        if strType =="deposit":
            deposit+=amount
        elif strType =="withdraw":
            withdraw-=amount
          
           
           
    print(id,strType,max_amount)
    print("Total deposit: ",deposit)
    print("Total withdrwa: ",withdraw)
       
       
build_balance()  
flag_overdrawn(balances)  
reportId=input("Enter account number for report: ")
account_report(transactions,reportId)
largest_transaction()
           
   
   
   
 
 
 
 