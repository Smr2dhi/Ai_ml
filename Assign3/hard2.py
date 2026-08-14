import requests
import json
import logging

url="https://jsonplaceholder.typicode.com"


logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s -%(levelname)s -%(message)s"
)

logger=logging.getLogger(__name__)
def fetchApi(url):
    try:
        response =requests.get(url, timeout=10)

        response.raise_for_status()

        data =response.json()
        return data
    except requests.exceptions.RequestException as e:
        logger.error("Api rew failed: ",e)


def main():
    logger.info("Progrma started...")

    try:
        todo=fetchApi(url+ "/todos")
        users=fetchApi(url+"/users")

    except requests.exceptions.RequestException as e:
        logger.error("Error request failed: ",e)

    else:
        count={}
        for i in todo:
            userId=i["userId"]
            currrentCount=count.get(userId,{
                "completed":0,
                "pending":0
            })

            
            if i["completed"]:
                currrentCount["completed"]+=1
            else:
                currrentCount["pending"]+=1

            count[userId]=currrentCount
        

    def userApi():
        userData={}
        for user in users:
            userData[user["id"]]=user["name"]
        return userData

    userData=userApi()
        
    mergedDict={}
    logger.info("Merging lib  started...")

    for userId in count:
        mergedDict[userId]={
            "name":userData[userId],
            **count[userId]
        }
    logger.info("Lib merged...")
    
    countComp=0
    countPend=0
    percentage=0

    mostProductive=""
    HighPercrnt=0

    for i in mergedDict:
        name=mergedDict[i]["name"]
        completed=mergedDict[i]["completed"]
        pending=mergedDict[i]["pending"]
        total=completed+pending
        percentage=round(completed/(total)*100,2)

        if percentage>HighPercrnt:
            HighPercrnt=percentage
            mostProductive=name

        print(f"name: {name}  completed: {completed}  pending: {pending}  percentage: {percentage}")
    print(f"most productive: {mostProductive},({completed} task completed)")

    userApi()
    try:
        with open("productivity_report.json","w") as file:
            json.dump(mergedDict,file,indent=4)

            logger.info("Report file saved to productivity_report.json")
    except(OSError,TypeError)as e:
        logger.error("Error while writing report: ",e)

    logger.info("program finished...")
if __name__ == "__main__":
    main()