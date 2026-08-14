import logging

log= logging.getLogger("Add")
log.setLevel(logging.INFO)


def add(a,b):
    logging.info("Adding:a,b")
    return a+b


adding= add(10,20)  
print("Result",adding)