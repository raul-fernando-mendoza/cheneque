import logging
from logging import handlers
import sys

logger = logging.getLogger("exam_app")
logger.setLevel(logging.ERROR)

logging.basicConfig(format='%(asctime)-15s %(message)s', level=logging.ERROR)

log = logging.getLogger("exam_app")

config = {
    "user":"eApp",
    #"database_host":"10.128.0.12",
    #"database_password":"Argos4905!",
    "database_host":"35.209.18.214",
    "database_password":"Argos4905",    
    "database":"entities"
}