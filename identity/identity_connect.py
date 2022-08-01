import logging
import json
from google.oauth2 import id_token
from google.auth.transport import requests

import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

log = logging.getLogger("cheneque")

# (Receive token by HTTPS POST)
# ...
def getUserByToken(token, client_id):
    result = None
    try:

        # Specify the CLIENT_ID of the app that accesses the backend:
        log.debug("Validating token for {token}")
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), client_id)
        
        if not idinfo:
            raise Exception( "getUserByToken: token could not be verified:" + str(token))

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        email = idinfo['email']
        log.debug("token was verified for email:" + str(email) )

        user = auth.get_user_by_email(email)
        if not user:
            raise Exception("firebase user not found for email:" + str(email) )

        log.debug("firebase user found:" + str(user))
        result = {
            "disabled": user.disabled,
            "display_name": user.display_name,
            "email":user.email,
            "email_verified":user.email_verified,
            "phone_number":user.phone_number,
            "photo_url":user.photo_url,
            "provider_id":user.provider_id,
            "tenant_id":user.tenant_id,
            "tokens_valid_after_timestamp":user.tokens_valid_after_timestamp,
            "uid":user.uid,
            "custom_claims":[]
        } 
        if user.custom_claims: 
            for key in user.custom_claims:
                result["custom_claims"].append({key:user.custom_claims[key]})

        log.debug("user claims %s", json.dumps(result,  indent=4, sort_keys=True))

        return result
    except ValueError as e:
        # Invalid token
        log.error( "getUserByToken Error:" + str(e) )
        raise
    except Exception as e:
        log.error("getUsetByToken Exception" + str(e))
        raise
    

def processRequest(req):
    log.debug("identity processRequest has been called")

    action = req["action"]
    if action == "getUserByToken":
        #validateToken( req ) 
        token = req["token"]
        clientId = req["clientId"]
        return getUserByToken( token , clientId)
    else:
        raise Exception("Action not recognized")

if __name__ == "__main__":
    print("hello mysql_connect")