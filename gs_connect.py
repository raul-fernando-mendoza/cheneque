from firebase_admin import storage

from datetime import timedelta
import json
import logging
import uuid

from google.oauth2 import service_account

log = logging.getLogger("exam_app")



def gsList( bucket_name , data):
    log.debug("gsList has been called")
    paths = []
    try:
        bucket = storage.bucket(bucket_name)
        log.debug("exist:" + str(bucket.exists()))
        blobs = bucket.list_blobs(prefix=data["path"])

        import firebase_admin
        expiration = timedelta(3) # valid for 3 days
        

        for blob in blobs:
            log.debug(blob.name)
            if not blob.name.endswith("/"):
                url = blob.generate_signed_url(expiration, method="GET")
                log.debug(url)
                paths.append({ "name":blob.name, "url":url} )
    except Exception as e:
        log.error("Exception gsList:" + str(e) )
        raise
    finally:
        log.debug("gsList end") 
    return paths

def processRequest(req):
    log.debug("gs processRequest has been called")
    bucket = req["bucket"]
    obj = req["data"]
    action = req["action"]
    if action == "list":
        #validateToken( req ) 
        return gsList( bucket, obj )
    else:
        raise Exception("Action not recognized")
if __name__ == "__main__":
    print("hello mysql_connect")