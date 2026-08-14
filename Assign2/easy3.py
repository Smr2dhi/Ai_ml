def annual_Premium(annual,installment):
    value=annual/installment
    round_num=round(value,2)
    
    print("Individual Installment: ",round_num)


while True:
    try:
        annualPremium = round(float(input("Enter annumal premium: ")),2)
        if annualPremium<=0:
            raise ValueError

        noOfInstallments=int(input("Enter the no of installments: "))
        if noOfInstallments<=0:
            raise ZeroDivisionError
        
        annual_Premium(annualPremium,noOfInstallments)
        break
    except ValueError:
        print("Please enter  positive number only!")
    except ZeroDivisionError:
        print("Installement cant be zero")
   
    finally:
        print("Attempt finished")