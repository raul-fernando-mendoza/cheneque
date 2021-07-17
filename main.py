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
import firebase_admin
from firebase_admin import credentials
cred = credentials.Certificate('celtic-bivouac-307316-firebase-adminsdk-pbsww-2ccfde6abd.json')
firebase_admin.initialize_app(cred)
import firestore_connect
import auth_connect

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
    log.debug("main processRequest has been called")
    req = request.get_json(force=True)
    log.debug("data:" + str(req))

    
    try:
        if "cheneque" == req["service"]:#can be auth, cheneque, firestore)
            obj = mysql_connect.processRequest(req)
        elif "firestore" == req["service"]:
            obj = firestore_connect.processRequest(req)
        elif "auth" == req["service"]:
            obj = auth_connect.processRequest(req)
        log.debug( json.dumps(obj,  indent=4, sort_keys=True) )
    except Exception as e:
        log.error("Exception:" + str(e))
        log.error("req:" + json.dumps(req,  indent=4, sort_keys=True))
        abort(404, description=str(e))
    return json_response(result=obj)

if __name__ == '__main__':
    log.info('********************* Cheneque logger has started ************************')  
    app.run(host='0.0.0.0')
