import csv
import logging

data = [
    ["id", "name", "price", "quantity"],
    [1, "Laptop", 55000, 10],
    [2, "Mouse", "abc", 50],
    [3, "Keyboard", 1200, "thirty"],
    [4, "Monitor", 8500, 15],
    [5, "USB Cable", 150, 100]
]
with open("products.csv","w",newline='')as file:
    writer =csv.writer(file)
    writer.writerows(data)

logging.basicConfig(filename="inventory_errors.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s")

skipped=0
valid=0
totalValue=0

with open("products.csv","r")as file:
    user =csv.reader(file)
    header=next(user)
    
    for row in user:
        try:
            price=float(row[2])
            quantity=int(row[3])
            
        except ValueError:
            skipped+=1
         
            logging.error(f"Skipped corrupt row:{row}")
            print(f"Skipped row: {row}")
            
            continue
        valid+=1
        totalValue+=(price*quantity)

print(f"Valid row:{valid} ,skipped row: {skipped},total value:{totalValue}")
       

      
  
        
            