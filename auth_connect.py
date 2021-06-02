import logging
from firebase_admin import auth

class LoginError(Exception):
    pass

log = logging.getLogger("exam_app")

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
    
    email = request["user"]["email"]
    role = request["user"]["role"]

    user = auth.get_user_by_email(email)

    current_claims = {}
    if( user.custom_claims ):
        current_claims = user.custom_claims

    current_claims[role] = True

    auth.set_custom_user_claims(user.uid, current_claims)

    return "Success"

def removeClaim(request):
    log.debug("removeClaim has been called")
    
    email = request["user"]["email"]
    role = request["user"]["role"]

    user = auth.get_user_by_email(email)

    custom_claims = user.custom_claims

    if( custom_claims ):
        r = custom_claims.pop(role, None)
        auth.set_custom_user_claims(user.uid, custom_claims) 
    
    return "Success"

def getClaims(request):

    log.debug("getClaims has been called")
    email = request["user"]["email"]
    user = auth.get_user_by_email(email)

    return user.custom_claims

def getUserList(req):
    log.debug("Auth getUserList has been called")
    userlist = []
    
    for user in auth.list_users().iterate_all():
        userlist.append( { 
            "uid":user.uid,
            "email":user.email,
            "roles":user.claims
            }
        )
    return userlist


def getUserListForClaim(req):
    claim = req["user"]["role"]
    userlist = []
    log.debug("getUserListForClaim has been called")
    for user in auth.list_users().iterate_all():
        if claim:
            if user.custom_claims and claim in user.custom_claims:
                userlist.append( { 
                    "uid":user.uid,
                    "display_name":user.display_name,
                    "email":user.email
                    }
                )
        else:
            userlist.append( { 
                "uid":user.uid,
                "email":user.email,
                "roles":user.claims
                }
            )
    return userlist

def sendEmailVerification(request):
    log.debug("sendEmailVerification has been called")
    
    email = request["user"]["email"]

    link = auth.generate_email_verification_link(email)

    log.debug("link:" + link)
  

    return "OK"

def removeUser(request):
    log.debug("removeUser has been called")
    email = request["user"]["email"]
    uid = None
    user = auth.get_user_by_email(email)
    
    auth.delete_user(uid)    
    return uid

def processRequest(req):
    action = req["action"]
    log.debug("Auth process request", action)
    if action == "validateToken":
        return validateToken( req )
    elif action == "validateToken":
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

if __name__ == "__main__":
    print("hello auth_connect")
