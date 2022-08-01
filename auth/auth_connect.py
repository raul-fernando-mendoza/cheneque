import logging
from firebase_admin import auth
import json

class LoginError(Exception):
    pass

log = logging.getLogger("cheneque")

def validateToken(request):
    log.debug("Validating token has been called")
    id_token = request["token"]  
    log.info("id_token:%s", id_token)

    decoded_token = auth.verify_id_token(id_token)
    log.debug("decoded_token %s", json.dumps(decoded_token,  indent=4, sort_keys=True))
    uid = decoded_token['uid']
    log.debug("uid:" + uid)
    email = decoded_token["email"]
    log.debug("email:" + email)

    #auth.set_custom_user_claims(uid, {'admin': True})


    user = auth.get_user(uid)
    log.debug("user %s", json.dumps(decoded_token,  indent=4, sort_keys=True))

    
    log.debug("user claims %s", json.dumps(user.custom_claims,  indent=4, sort_keys=True))

    if not email:
        log.error("Token not valid")
        raise LoginError("Token Expired")         


def addClaim(request):
    log.debug("addClaim has been called")
    log.debug("request: %s", json.dumps(request,  indent=4, sort_keys=True) )    
    
    obj = request["data"]

    email = obj["email"]
    newClaims = obj["claims"]
    log.debug("email %s", email)
    log.debug("newClaims %s", json.dumps(newClaims,  indent=4, sort_keys=True) )
    

    user = auth.get_user_by_email(email)
    #log.debug("user", str(user) )

    current_claims = {}
    if( user.custom_claims ):
        current_claims = user.custom_claims
    for key in newClaims:
        newClaimValue = newClaims[key]
        current_claims[key] = newClaimValue

    auth.set_custom_user_claims(user.uid, current_claims)

    return "Success"

def removeClaim(request):
    log.debug("removeClaim has been called")
    log.debug("request: %s", json.dumps(request,  indent=4, sort_keys=True) ) 
    
    obj = request["data"]

    email = obj["email"]
    claim = obj["claim"]

    

    user = auth.get_user_by_email(email)

    custom_claims = user.custom_claims

    if( custom_claims ):
        r = custom_claims.pop(claim, None)
        auth.set_custom_user_claims(user.uid, custom_claims) 
    
    return "Success"

def getClaims(request):

    log.debug("getClaims has been called")
    email = request["email"]
    user = auth.get_user_by_email(email)

    return user.custom_claims

def getUserList(req):
    log.debug("Auth getUserList has been called")
    userlist = []
    
    for user in auth.list_users().iterate_all():
        userlist.append( { 
            "uid":user.uid,
            "email":user.email,
            "claims":user.custom_claims,
            "displayName":user.display_name
            }
        )
    return userlist
    auth.set


def getUserListForClaim(req):
    claim = req["data"]["claims"]
    userlist = []
    log.debug("getUserListForClaim has been called")
    for user in auth.list_users().iterate_all():
        if claim:
            if user.custom_claims and claim in user.custom_claims:
                userlist.append( { 
                    "uid":user.uid,
                    "email":user.email,
                    "displayName":user.custom_claims["displayName"] if ("displayName" in user.custom_claims) else None ,
                    "claims":user.custom_claims
                    }
                )
    return userlist

def sendEmailVerification(request):
    log.debug("sendEmailVerification has been called")
    
    
    email = request["email"]

    link = auth.generate_email_verification_link(email)

    log.debug("link:" + link)
  

    return "OK"

def removeUser(request):
    log.debug("removeUser has been called")
    log.debug("request: %s", json.dumps(request,  indent=4, sort_keys=True) ) 
    
    email = request["data"]["email"]
 
    user = auth.get_user_by_email(email)
    
    auth.delete_user(user.uid)    
    return user.uid

def getUser(request):
    log.debug("retrive user data")
    uid = request["data"]["uid"]  

    user = auth.get_user(uid)
    return { 
        "uid":user.uid,
        "email":user.email,
        "displayName":user.custom_claims["displayName"] if ("displayName" in user.custom_claims) else None ,
        "claims":user.custom_claims
        }

def processRequest(req):
    log.debug("auth processRequest has been called")
    action = req["action"]
    #log.debug("Auth process request", str(json.dumps(action)))
    if action == "validateToken":
        return validateToken( req )
    elif action == "addClaim":
        return addClaim( req )
    elif action == "removeClaim":
        return removeClaim( req )
    elif action == "getClaims":
        return getClaims(req)
    elif action == "getUserList":
        return getUserList(req)
    elif action == "getUserListForClaim":
        return getUserListForClaim(req)
    elif action == "sendEmailVerification":
        return sendEmailVerification(req)
    elif action == "sendEmailVerification":
        return sendEmailVerification()
    elif action == "removeUser":
        return removeUser(req)
    elif action == "getUser":
        return getUser(req)

if __name__ == "__main__":
    print("hello auth_connect")
