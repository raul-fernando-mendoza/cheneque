#to find the pid
#sudo netstat -tulnp | grep :5000
#kill pid

#go inside envinments and change it to use dev or prd
import environments

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
#credentials.Certificate(environments.config["service_account_key"])
firebase_admin.initialize_app()
import firestore_connect
import auth_connect
import gs_connect
import identity_connect
import compute_connect

log = logging.getLogger("exam_app")

app = Flask(__name__)
CORS(app, support_credentials=True)
#cors = CORS(app, resources={r"/exam-app/*": {"origins": "*"}})
FlaskJSON(app)

import requests

@app.route('/')
def get_time():
    logging.info('********************* Cheneque 1.2/ was called ************************') 
    now = datetime.utcnow()
    is_gunicorn = "gunicorn" in os.environ.get("SERVER_SOFTWARE", "")
    python_version =  sys.prefix + " " + sys.version
    return json_response(result={ "cheneque_version":1.1, "time":now, "is_gunicorn":is_gunicorn, "python_version":python_version })


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
        elif "gs" == req["service"]:
            obj = gs_connect.processRequest(req)            
        elif "identity" == req["service"]:
            obj = identity_connect.processRequest(req)
        elif "compute" == req["service"]:
            obj = compute_connect.processRequest(req)                         
        else:
            raise Exception("service not found" + str(req["service"]))
        log.debug( json.dumps(obj,  indent=4, sort_keys=True) )
    except Exception as e:
        log.error("processRequest Exception:" + str(e))
        log.error("req:" + json.dumps(req,  indent=4, sort_keys=True))
        abort(404, description=str(e))
    return json_response(result=obj)


if __name__ == '__main__':
    log.info('********************* Cheneque logger has started ************************')  
    app.run(host='0.0.0.0')
