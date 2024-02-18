#gcloud functions deploy processRequest --region=us-central1 --entry-point examgradesparameterupdate --runtime python39 --source . --trigger-event "providers/cloud.firestore/eventTypes/document.update"  --trigger-resource "projects/celtic-bivouac-307316/databases/(default)/documents/examGrades/{examGradeId}/parameterGrades/{parameterGradeId}" 
import json
import logging
from urllib.parse import urlencode
from urllib.request import urlopen
import json

logging.basicConfig(format='**** -- %(asctime)-15s %(message)s', level=logging.ERROR)

log = logging.getLogger("re-captcha-srv")
log.setLevel(logging.INFO)


def recaptchaServerValidate(request):
    log.info("**** create cheneque receive:" + str(request))
    log.info("**** create cheneque type:" + str(type(request)))
    log.info("**** create cheneque method:" + str(request.method))
    log.info("**** create cheneque content-type:" + str(request.content_type))
    log.info("**** create cheneque mimetype:" + str(request.mimetype))    
    log.info("**** create cheneque is_json:" + str(request.is_json))      
    log.info("**** create cheneque get content_encoding:" + str(request.content_encoding))    
    log.info("**** create cheneque get data:" + str(type(request.get_data())))
    log.info("**** create cheneque decode:" + str(request.get_data().decode()))

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
    req = None
    try:
        log.debug("main processRequest has been called")
        req = request.get_json(force=True)
        log.debug("data:" + str(req))


        URIReCaptcha = 'https://www.google.com/recaptcha/api/siteverify'
        secret = req['secret']
        recaptchaToken = req["recaptchaToken"]
      
        params = urlencode({
            'secret': secret,
            'response': recaptchaToken
        })

        data = urlopen(URIReCaptcha, params.encode('utf-8')).read()
        result = json.loads(data)
        success = result.get('success', None)

        if success == True:
            log.debug('reCaptcha passed')
        else:
            log.debug('recaptcha failed')       

          
        
    except Exception as e:
        log.error( json.dumps(req,  indent=4, sort_keys=True) )
        log.error("**** processRequest Exception:" + str(e))
        return ({"error":str(e)}, 200, headers)
    return ({"result":obj}, 200, headers)
