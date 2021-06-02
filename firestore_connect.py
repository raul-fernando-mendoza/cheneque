import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import logging

log = logging.getLogger("exam_app")

cred = credentials.Certificate('celtic-bivouac-307316-firebase-adminsdk-pbsww-2ccfde6abd.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def addObject(collection, obj):
    try:
        doc_ref = db.collection(collection).document()
        obj["id"] = doc_ref.id
        doc_ref.set(obj)
           
    except Exception as e:
        log.error("Exception addObject:" + str(e) )
        raise
    finally:
        log.error("end")  
    return obj


def deleteObject(collection, obj):
    try:
        doc_ref = db.collection(collection).document(obj["id"]).delete()
           
    except Exception as e:
        log.error("Exception addObject:" + str(e) )
        raise
    finally:
        log.error("end")  
    return obj


def updateObject(collection, obj):
    try:
        doc_ref = db.collection(collection).document(obj["id"])
        doc_ref.update(obj)
            
    except Exception as e:
        log.error("Exception updateObject:" + str(e) )
        raise
    finally:
        log.error("end")  
    return obj

def ArrayUnion(collection, obj):
    try:
        doc_ref = db.collection(collection).document(obj["id"])
        for key in obj:
            if key != "id":
                keyvalue = obj[key]
                doc_ref.update({key: firestore.ArrayUnion(keyvalue)})
    except Exception as e:
        log.error("Exception ArrayUnion:" + str(e) )
        raise
    finally:
        log.error("end")  
    return obj        

def ArrayRemove(collection, obj):
    try:
        doc_ref = db.collection(collection).document(obj["id"])
        for key in obj:
            if key != "id":
                keyvalue = obj[key]
                doc_ref.update({key: firestore.ArrayRemove(keyvalue)})
    except Exception as e:
        log.error("Exception ArrayRemove:" + str(e) )
        raise
    finally:
        log.error("end")  
    return obj    

def getObject(collection, obj):
    
    recordset = db.collection(collection)
    try:
        for key in obj:
            keyvalue = obj[key]
            if key != 'orderby':
                recordset = recordset.where(key, u"==", keyvalue)
            else:
                orderBy = obj[key]
                for orderKey in orderBy:
                    orderKeyValue = orderBy[orderKey]
                    if orderKeyValue == "asc":
                        recordset = recordset.order_by(orderKey,"ASCENDING")    
                    else:
                        recordset = recordset.order_by(orderKey, "DESCENDING")

        docs = []
        for doc in recordset.stream():
            docs.append(doc.to_dict())
    
        return docs
           
    except Exception as e:
        log.error("Exception addObject:" + str(e) )
        raise
    finally:
        log.error("end")  
    return obj    

def processRequest(req):
    collection = req["database"]
    obj = req["data"]
    action = req["action"]
    if action == "add":
        #validateToken( req ) 
        return addObject( collection, obj )
    if action == "get":
        #validateToken( req ) 
        return getObject( collection, obj )         
    if action == "update":
        #validateToken( req ) 
        return updateObject( collection, obj )   
    if action == "ArrayUnion":
        #validateToken( req ) 
        return ArrayUnion( collection, obj )   
    if action == "ArrayRemove":
        #validateToken( req ) 
        return ArrayRemove( collection, obj )                       

if __name__ == "__main__":
    print("hello mysql_connect")