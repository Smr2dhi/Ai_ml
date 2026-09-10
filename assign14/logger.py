import logging
import os

log_path=os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "Assign14.log"
)

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
)

logger=logging.getLogger()