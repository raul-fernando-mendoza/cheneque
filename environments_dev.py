import logging
from logging import handlers
import sys

logger = logging.getLogger("exam_app")
logger.setLevel(logging.DEBUG)

## Here we define our formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logHandler = handlers.TimedRotatingFileHandler( './log/exam_app.log', when='M', interval=1, backupCount=2)
logHandler.setLevel(logging.DEBUG)
## Here we set our logHandler's formatter
logHandler.setFormatter(formatter)

logger.addHandler(logHandler)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

logger.info('logger has started') 

logging.info("from logging")
sys.path.insert(0,'.')

log = logging.getLogger("exam_app")

config = {
    "user":"eApp",
    "database_host":"192.168.15.12",
    "database_password":"odroid",
    "database":"entities"
}