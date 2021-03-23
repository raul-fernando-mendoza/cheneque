from datetime import datetime
from flask import Flask, request, abort, jsonify
from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask_cors import CORS, cross_origin

import logging
import json
import mysql_connect
from logging import handlers
import sys



#logging.basicConfig(filename='/var/www/cgi-bin/exam_app.log', format='%(asctime)-15s %(message)s', level=logging.DEBUG)
logger = logging.getLogger("exam_app")
logger.setLevel(logging.DEBUG)

## Here we define our formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logHandler = handlers.TimedRotatingFileHandler( './log/exam_app.log', when='M', interval=1, backupCount=2)
logHandler.setLevel(logging.DEBUG)
## Here we set our logHandler's formatter
logHandler.setFormatter(formatter)

logger.addHandler(logHandler)
logger.info('logger has started') 

logging.info("from logging")
sys.path.insert(0,'.')

log = logging.getLogger("exam_app")

app = Flask(__name__)
CORS(app, support_credentials=True)
#cors = CORS(app, resources={r"/exam-app/*": {"origins": "*"}})
FlaskJSON(app)

@app.route('/')
def get_time():
    now = datetime.utcnow()
    return json_response(time=now)


@app.route('/api', methods=['POST'])
@cross_origin(supports_credentials=True)
def processRequest():
    # We use 'force' to skip mimetype checking to have shorter curl command.
    log.debug("processRequest has been called")
    data = request.get_json(force=True)
    log.debug("data:" + str(data))
    try:
        obj = mysql_connect.processRequest(data)
        log.debug( json.dumps(obj,  indent=4, sort_keys=True) )
    except mysql_connect.LoginError as le:
        log.error("Exception:" + str(le))
        log.error("data:" + json.dumps(data,  indent=4, sort_keys=True))
        abort(401, description=str(le))        
    except Exception as e:
        log.error("Exception:" + str(e))
        log.error("data:" + json.dumps(data,  indent=4, sort_keys=True))
        abort(404, description=str(e))
    return json_response(result=obj)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('logger has started')  
    app.run(host='0.0.0.0')
