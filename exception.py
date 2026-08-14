import re

import json
with open("transactions.json","r") as file:
    data=json.load(file)

print(data)

class TransactionError(Exception):
    pass
class ValidationError(TransactionError):
    pass
class InvalidUsernameError(ValidationError):
    pass
class InvalidAgeError(ValidationError):
    pass


try:
    for dta in data:
        # username=dta["username"]
        # if  username == re.fullmatch(r'^[0-9]+[a-zA-Z0-9]$',username):
        #     raise InvalidUsernameError
        
        try:
            try:
                age=dta["age"]
            except ValueError as e:
                raise InvalidAgeError("Age is not integer") from e
        
            if age<18:
        except ValueError as m:
            raise InvalidAgeError("Age is below 18")from m
            print("Error",e)

                
        
        
except InvalidUsernameError as e:
    print(e)

except InvalidAgeError as e:
    print(e)