import logging 
 
# GLOBAL / ROOT HANDLER 
root_logger = logging.getLogger() 

 
app_handler = logging.FileHandler("app.log") 
app_handler.setLevel(logging.WARNING) 
root_logger.addHandler(app_handler) 
 
 
# LOCAL HANDLER: only for payment_service 
payment_logger = logging.getLogger("payment_service") 
payment_logger.setLevel(logging.DEBUG) 
 
payment_handler = logging.FileHandler("payment.log") 
payment_handler.setLevel(logging.DEBUG) 
payment_logger.addHandler(payment_handler) 
 
# Prevent payment messages from being written twice 
payment_logger.propagate = False 
 