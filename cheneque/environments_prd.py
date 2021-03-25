import logging
from logging import handlers
import sys

logger = logging.getLogger("exam_app")
logger.setLevel(logging.DEBUG)

logging.basicConfig(format='%(asctime)-15s %(message)s', level=logging.DEBUG)

log = logging.getLogger("exam_app")

config = {
    "user":"eApp",
    #"database_host":"10.128.0.12",
    #"database_password":"Argos4905!",
    "database_host":"34.70.28.168",
    "database_password":"Argos4905",    
    "database":"entities"
}