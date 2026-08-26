
import logging
import os

log_file=os.path.join(os.path.dirname(__file__),"hard_3.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s -%(levelname)s - %(message)s"

)

logger=logging.getLogger(__name__)