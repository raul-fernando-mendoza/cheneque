from google.cloud import storage
import logging

log = logging.getLogger("gs")

def gsList( bucket_name , data):
    log.debug("gsList has been called")
    paths = []
    try:
        storage_client = storage.Client()
        bucket =  storage_client.get_bucket(bucket_name)
        
        log.debug("exist:" + str(bucket.exists()))
        blobs = bucket.list_blobs(prefix=data["path"])

        for blob in blobs:
            log.debug(blob.name)
            if not blob.name.endswith("/"):
                log.debug(blob.name)
                paths.append({ "name":blob.name, "url":blob.public_url} )
    except Exception as e:
        log.error("Exception gsList:" + str(e) )
        raise
    finally:
        log.debug("gsList end") 
    return paths

def processRequest(req):
    log.debug("gs processRequest has been called")
    bucket = req["bucket"]
    data = req["data"]
    action = req["action"]
    if action == "list":
        #validateToken( req ) 
        return gsList( bucket, data )
    else:
        raise Exception("Action not recognized")
if __name__ == "__main__":
    print("hello mysql_connect")