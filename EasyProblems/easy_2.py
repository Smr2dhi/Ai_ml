age=int(input("Enter your age: "))
income=float(input("Enter  your annual income: "))

print("-----------------------------------")
print(f"Entered age: {age}")
print(f"Entered annual income: {income}")

if age>18 and income >1000000 :
    print("Premium Plan")
elif age>65 :
        print("Result: Eligible - Senior Plan (medical check required)")

elif 18<= age <=65 and income >= 300000:
        print("Eligible - Standard Plan ")
        
elif 18<= age <=65 and income <300000:
        print(" Eligible - Basic Plan ")
else:
        print("Not Eligible (Minor)")




