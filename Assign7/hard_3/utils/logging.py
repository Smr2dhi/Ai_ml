import logging

root_logger=logging.getLogger()
root_logger.setLevel(logging.DEBUG)

app_handler=logging.FileHandler("app.log")
app_handler.setLevel(logging.WARNING)
root_logger.addHandler(app_handler)

