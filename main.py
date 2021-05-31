#to find the pid
#sudo netstat -tulnp | grep :5000
#kill pid
from datetime import datetime
from flask import Flask, request, abort, jsonify
from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask_cors import CORS, cross_origin

import logging
import json
import mysql_connect 
import os
import sys


log = logging.getLogger("exam_app")


app = Flask(__name__)
CORS(app, support_credentials=True)
#cors = CORS(app, resources={r"/exam-app/*": {"origins": "*"}})
FlaskJSON(app)

@app.route('/')
def get_time():
    logging.info('********************* Cheneque / was called ************************') 
    now = datetime.utcnow()
    is_gunicorn = "gunicorn" in os.environ.get("SERVER_SOFTWARE", "")
    python_version =  sys.prefix + " " + sys.version
    return json_response(result={ "time":now, "is_gunicorn":is_gunicorn, "python_version":python_version })


@app.route('/api', methods=['GET','POST'])
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
    log.info('********************* Cheneque logger has started ************************')  
    app.run(host='0.0.0.0')
