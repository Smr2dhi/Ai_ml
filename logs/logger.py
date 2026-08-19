import logging
import os
import sys


GLOBAL_LOG_FILE=os.path.join(os.path.dirname(__file__),"global.log")

SESSION_DIR=os.path.dirname(os.path.abspath(sys.argv[0]))
SESSION_LOG_FILE=os.path.join(SESSION_DIR,"session.log")


class GlobalLogger(logging.Logger):

    def __init__(self,name="GLOBAL"):
        super().__init__(name,logging.WARNING)


class SessionLogger(logging.Logger):

    def __init__(self,name="SESSION"):
        super().__init__(name,logging.DEBUG)


formatter=logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)


global_logger=GlobalLogger()

global_handler=logging.FileHandler(GLOBAL_LOG_FILE)
global_handler.setLevel(logging.WARNING)
global_handler.setFormatter(formatter)

global_logger.addHandler(global_handler)


session_logger=SessionLogger()

session_handler=logging.FileHandler(SESSION_LOG_FILE)
session_handler.setLevel(logging.DEBUG)
session_handler.setFormatter(formatter)

session_logger.addHandler(session_handler)