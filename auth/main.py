
from google.cloud import firestore
import json
import logging
import firebase_admin

firebase_admin.initialize_app()
import auth_connect

logging.basicConfig(format='**** -- %(asctime)-15s %(message)s', level=logging.ERROR)

log = logging.getLogger("exams")
log.setLevel(logging.ERROR)


def authRequest(request):
    log.error("**** create cheneque receive:" + str(request))
    log.error("**** create cheneque type:" + str(type(request)))
    log.error("**** create cheneque method:" + str(request.method))
    log.error("**** create cheneque content-type:" + str(request.content_type))
    log.error("**** create cheneque mimetype:" + str(request.mimetype))    
    log.error("**** create cheneque is_json:" + str(request.is_json))      
    log.error("**** create cheneque get content_encoding:" + str(request.content_encoding))    
    log.error("**** create cheneque get data:" + str(type(request.get_data())))
    log.error("**** create cheneque decode:" + str(request.get_data().decode()))

    # For more information about CORS and CORS preflight requests, see:
    # https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request

    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    obj = None
    try:
        log.debug("main processRequest has been called")
        req = request.get_json(force=True)
        log.debug("data:" + str(req))


        if "auth" == req["service"]:
            obj = auth_connect.processRequest(req)
        else:
            raise Exception("service not found" + str(req["service"]))
        log.debug( json.dumps(obj,  indent=4, sort_keys=True) )
    except Exception as e:
        log.error("**** processRequest Exception:" + str(e))
        return ({"error":str(e)}, 200, headers)
    return ({"result":obj}, 200, headers)
