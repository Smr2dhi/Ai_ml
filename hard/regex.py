import re
date_input = "[2025-08-01 14:23:11]"
email="smar2dhiya@gmail.com"
level_input="WARNING"
user="sam.yadav_23"

input= """
[2025-08-01 14:23:11] INFO User=john.doe Email=john@example.com IP=192.168.1.10 
[2025-08-01 14:25:40] ERROR User=alice Email=alice@example.org IP=10.0.0.1 
[2025-08-01 14:27:55] WARNING User=bob_smith Email=bob@sub.company.co.uk IP=172.16.0.5
"""

def date():
    date_data = r"\[\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\]"
    match= re.search(date_data,date_input)
    if match:
        print(match.group())
    else:
       print("Invalid")


def level():
    reg_level = r"^(INFO|WARNING|ERROR)$"
    match= re.search(reg_level,level_input)
    if match:
     print(match.group())
    else:
       print("invalid")

def username():
    reg_user=r"^[a-zA-Z._0-9]{3,20}$"
    match=re.search(reg_user,user)
    if match:
        print(match.group())
    else:
       print("invalid")


def matchingEmail():
    email_pattern=r"^[a-zA-Z0-9_.]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$"
    match= re.search(email_pattern,email)
    if match:
        print(match.group())
    else:
       print("Invalid")

def ipAddress():
   ip_regex=r"^IP=[0-255].[0-255].[0-255].[0-255]$"

date()
level()
username()
matchingEmail()
ipAddress()