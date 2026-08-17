
from utils import save_documents,load_documents
import logging

logger=logging.getLogger("ActivityLogger")
logger.setLevel(logging.INFO)

handler=logging.FileHandler("Assign4/medium_2/Activity.log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

handler.setFormatter(formatter)
logger.addHandler(handler)



entries=load_documents("Assign4/log.json")
logger.info("Activity log loaded")

activity=input("What do you work on? ")
length=len(entries)+1
entry={
    "entry":length,
    "activity":activity
}
entries.append(entry)
logger.info("new entry added:",{activity})

save_documents(entries,"Assign4/log.json")

print(f"---Actiivity Log ({length}) entries-----")

for i in entries:
    print(i)


