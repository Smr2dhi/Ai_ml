def add(a,b):
    return a+b

def sub(a,b):
    return a-b

def product(a,b):
    return a*b

def divide(a,b):
    try:
        if b==0:
            raise ZeroDivisionError("cannaot divide by zero")

        result=a/b
        return result
        
    except ZeroDivisionError as e:
        print(e)
            
def avg(a,b,c):
    return (a+b+c)/3
