
employees = ["John,IT", "Sara,HR", "Mike,Finance"]
try:

    with open("employee.txt","w")as f:
        f.write("\n".join(employees))

    print("Record saved")


    with open("employee.txt","a")as f:
        f.write("\nPriya, AI,Engineering")

    print("record appended")


    with open("employee.txt","r")as f:
        print("---Employee File----")
        count=0
        for line in f:
            count+=1
            line=line.rstrip()
            print(f"{count}: {line}")

except FileNotFoundError:
    print("File not found")

    # After chnagin file from "w" to "a"the file started to append in existing data that is append but
    # but in write mode it delete old adta and write new data  