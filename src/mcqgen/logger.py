# what ever thing I am exicute I want to log that 
import logging
import os

from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

log_path = os.path.join(os.getcwd(),"logs")

os.makedirs(log_path,exist_ok=True)

LOG_FILEPATH = os.path.join(log_path,LOG_FILE)

logging.basicConfig(
    level = logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',# CURRENTTIME,LINENUMBER,LABELNAME,MESAGE
    filename = LOG_FILEPATH
)