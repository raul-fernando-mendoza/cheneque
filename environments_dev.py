import logging
from logging import handlers
import sys


logger = logging.getLogger("cheneque")
logger.setLevel(logging.DEBUG)

logging.basicConfig(format='**** -- %(asctime)-15s %(message)s', level=logging.ERROR)

log = logging.getLogger("cheneque")

config = {
    "user":"eApp",
    "database_host":"192.168.15.12",
    "database_password":"odroid",
    "database":"entities",
    "service_account_key":"cheneque-dev-4ee34-firebase-adminsdk-6vt8j-4f1667d511.json"
}