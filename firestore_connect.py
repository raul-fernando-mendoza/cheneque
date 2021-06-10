from firebase_admin import firestore
import json
import logging
import uuid

log = logging.getLogger("exam_app")

db = firestore.client()

def addSubCollectionToDoc(collectionName, recordset, obj):
    try:
        if isinstance(obj,list):
            for element in obj:    
                doc_ref = recordset.collection(collectionName).document()
                values = {}
                values["id"] = doc_ref.id
                for key in element:
                    keyValue = element[key]

                    if isinstance(keyValue,dict) or isinstance(keyValue,list):
                        subcollection = addSubCollectionToDoc(key, doc_ref, keyValue)
                    else:
                        if key != "id":
                            values[key] = keyValue
                doc_ref.set(values)
               
        elif isinstance(obj,dict):
        
            doc_ref = recordset.collection(collectionName).document()
            values = {}
            values["id"] = doc_ref.id
            for key in obj:
                keyValue = obj[key]

                if isinstance(keyValue,dict) or isinstance(keyValue,list):
                    addSubCollectionToDoc(key, doc_ref, keyValue)
                else:
                    if key != "id":
                        values[key] = keyValue                    
            doc_ref.set(values) 
                    

           
    except Exception as e:
        log.error("Exception addSubCollection:" + str(e) )
        raise
    finally:
        log.debug("end")  

def addObject(obj):
    values = {}    
    try:
        for collectionName in obj:
            doc_ref = db.collection(collectionName).document()
            values["id"] = doc_ref.id
            data = obj[collectionName]

            for key in data:
                    keyValue = data[key]
                    if isinstance(keyValue,dict) or isinstance(keyValue,list):
                        addSubCollectionToDoc(key, doc_ref, keyValue)
                    else:
                        if key != "id":
                            values[key] = keyValue
            doc_ref.set(values)

           
    except Exception as e:
        log.error("Exception addObject:" + str(e) )
        raise
    finally:
        log.debug("end")  
    return values


@firestore.transactional
def deleteSingleObject(transaction, collectionId, obj):
    collection = db.collection_group(collectionId).where("id", u'==', obj["id"])
        
    doc = collection.get(transaction=transaction)[0]
    transaction.delete( doc.reference )

def deleteObject(obj):
    logging.debug( "firestore deleteObject called")
    logging.debug( "obj:%s",json.dumps(obj,  indent=4, sort_keys=True) ) 

    transaction = db.transaction()

    try:
        for collection in obj:
            data = obj[collection]
            if isinstance(data, list):
                elements = data
                for element in elements:
                    deleteSingleObject(transaction, collection, element)
            else:
                element = data
                deleteSingleObject(transaction, collection, element)


    except Exception as e:
        log.error("Exception addObject:" + str(e) )
        raise
    finally:
        log.debug("end")  
    return obj

def addSubCollection(obj):
    result = None
    try:
        for collection in obj:
            recordset = db.collection_group(collection).where(u'id', u'==', obj[collection]["id"]).get()
            parent = recordset[0]
            parentData = obj[collection]
            for parentKey in parentData:
                if parentKey != "id":
                    result = parentData[parentKey]
                    doc_ref = parent.reference.collection(parentKey).document()
                    result["id"] = doc_ref.id
                    doc_ref.set( result )
            
    except Exception as e:
        log.error("Exception updateObject:" + str(e) )
        raise
    finally:
        log.debug("end")  
    return result


def updateSingleObject(transaction, collectionId, obj):
    
    collection = db.collection_group(collectionId).where("id", u'==', obj["id"])
        
    doc = collection.get(transaction=transaction)[0]
    transaction.update( doc.reference, obj)

def updateObject(obj):
    try:
        transaction = db.transaction()
        for collectionId in obj:
            records = obj[collectionId]
            if isinstance(records, list):
                for element in records:
                    updateSingleObject( transaction, collectionId, element)
            else:
                element = records
                updateSingleObject( transaction, collectionId, element)
        transaction.commit()

            
    except Exception as e:
        log.error("Exception updateObject:" + str(e) )
        raise
    finally:
        log.debug("end")  
    return obj

def ArrayUnion(obj):
    try:
        for parent in obj:
            parentData = obj[parent]
            parentset = db.collection_group(parent).where(u'id', u'==', parentData["id"]).get()
            parent = parentset[0]
            for childCollection in parentData:
                if childCollection != "id":
                    childData = parentData[childCollection]
                    values = {}
                    for key in childData:
                        if key != "id":
                            keyValue = childData[key]
                            values[key] = keyValue                    
                    parent.reference.update({childCollection: firestore.ArrayUnion([values])})

    except Exception as e:
        log.error("Exception ArrayUnion:" + str(e) )
        raise
    finally:
        log.debug("end")  
    return obj        

def ArrayRemove(collection, obj):
    try:
        for parent in obj:
            data = obj[parent]
            parentset = db.collection_group(parent).where(u'id', u'==', data["id"]).get()
            parent = parentset[0]
            for childCollection in data:
                if childCollection != "id":
                    childData = data[childCollection]
                    parent.reference.update({childCollection: firestore.ArrayRemove([childData])})                   

                           


    except Exception as e:
        log.error("Exception ArrayRemove:" + str(e) )
        raise
    finally:
        log.debug("end")  
    return obj    

def getSubCollection(collectionName, parent, filter):
    result = None  
    try:
        if filter == None:
            result = None
        elif isinstance(filter,list):
            #the filter shows a list so get the filter from the first element
            result = []
            filter = filter[0]
            collectionset = parent.collection(collectionName)
            doc_ref = collectionset
            #apply the filter if any
            for key in filter:
                keyValue = filter[key]
                if not isinstance(keyValue,list) and not isinstance(keyValue,dict) and keyValue!=None:
                    doc_ref = doc_ref.where(key ,"==", keyValue )

            #check that every element in the collection comply with the filter and copy only those
            for doc in doc_ref.stream():
                documentJSON = doc.to_dict()

                values = {}
                #copy only the fields named in the filter
                for key in filter:
                    keyValue = filter[key]
                    if isinstance(keyValue,dict) or isinstance(keyValue,list):
                        subCollection = getSubCollection(key, collectionset.document(documentJSON["id"]), keyValue)
                        values[key] = subCollection
                    elif key in documentJSON:
                        values[key] = documentJSON[key]
                    else: 
                        values[key] = None
                    
                        
                        
                result.append(values)
        elif isinstance(filter,dict):
                collectionset = parent.collection(collectionName)
                doc_ref = collectionset

                for key in filter:
                    keyValue = filter[key]
                    if not isinstance(keyValue,list) and not isinstance(keyValue,dict) and keyValue!=None:
                        doc_ref = doc_ref.where(key ,"==", keyValue )
                
                for doc in doc_ref.stream():
                    documentJSON = doc.to_dict()

                    values = {}

                    for key in filter:
                        keyValue = filter[key]
                        if isinstance(keyValue,dict) or isinstance(keyValue,list):
                            subCollection = getSubCollection(key, collectionset.document(documentJSON["id"]), keyValue)
                            values[key] = subCollection
                        elif key in documentJSON:
                            values[key] = documentJSON[key]
                        else:
                            values[key] = None
                       

                    result = values


    except Exception as e:
        log.error("Exception getSubCollection:" + collectionName + " " + str(e) )
        raise
    finally:
        log.debug("getSubCollection end")  
    return result                 

#retrieve the datasubcollection described in the obj
#obj = {
#   exams = {
#        id : "123"
#        parameter = {
#            id : "123-p1"
#            criteria = {
#                id : "123-p1-c1"
#            }
#        }
#   }    
#}
def getObject(obj):
    logging.debug( "firestore getObject called")
    logging.debug( "obj:%s",json.dumps(obj,  indent=4, sort_keys=True) )
    result = None
    try:
        collectionId = None
        recordset = None
        data = None
        result = None
        for key in obj:
            if key not in ["orderBy"]:
                collectionId = key
                collectionset = db.collection(collectionId)
                data = obj[collectionId]
                if isinstance(data, list):
                    result = []
                    data = data[0]

                recordset = collectionset

                for field in data:
                    fieldValue = data[field]
                    if not isinstance(fieldValue,dict) and not isinstance(fieldValue,list) and fieldValue != None:
                        recordset = recordset.where(field, u"==", fieldValue)
        #recordset has the where now add the sort

        if 'orderBy' in obj:
                orderBy = obj['orderBy'] 
                for orderField in orderBy:
                    orderValue = orderBy[orderField]
                    if orderValue == "asc":
                        recordset = recordset.order_by(orderField,direction=firestore.Query.ASCENDING)    
                    else:
                        recordset = recordset.order_by(orderField, direction=firestore.Query.DESCENDING)
        #the recordset has the where and the sortby now retrieve the data
        docs = recordset.get()
        for doc in docs:
            documentJSON = doc.to_dict()

            values = {}
            #if there is a subcollection to retrieve call it
            for key in data:
                keyValue = data[key]
                if isinstance(keyValue,dict) or isinstance(keyValue,list):                
                    subcollection = getSubCollection(key, collectionset.document(documentJSON["id"]), keyValue)
                    values[key] = subcollection
                elif key in documentJSON:
                    values[key] = documentJSON[key]
                else:
                    values[key] = None
            if result == None:
                result = values
            else:
                result.append(values)
        #do the sort

    except Exception as e:
        log.error("Exception addObject:" + str(e) )
        raise
    finally:
        log.debug("end")  
    return result   

#

def dupSubDoc(transaction, parentDocRef, collectionId, sourceDoc):
    newDocRef = None

    log.debug( "copy:" + collectionId )
    
    newId = uuid.uuid4().hex
    if parentDocRef == None:
        newDocRef = db.collection(collectionId).document( newId )
    else:
        newDocRef = parentDocRef.collection(collectionId).document( newId )
    
    values = {"id":newId}
    documentJSON = sourceDoc.to_dict()
    for key in documentJSON:
        keyValue = documentJSON[key]
        if key != "id":
            values[key] = documentJSON[key]
    transaction.create( newDocRef,values)
    #the new doc thas been created and now copy all the sub collections
    collections = sourceDoc.reference.collections()
    

    for subCollection in collections:
        log.debug("collection %s", subCollection.id)
        subDocs = subCollection.get()
        for subDoc in subDocs:
            dupSubDoc(transaction, newDocRef, subCollection.id, subDoc)
    return newDocRef


#copy object
def dupObject(obj):
    logging.debug( "firestore copyObject called")
    logging.debug( "obj:%s",json.dumps(obj,  indent=4, sort_keys=True) )
    result = None
    try:
        collectionId = None
        recordset = None
        data = None
        result = None
        for key in obj:
            collectionId = key
            collectionset = db.collection(collectionId)
            data = obj[collectionId]
            recordset = collectionset
            recordset = recordset.where(u"id", u"==",  data["id"])

        #the recordset has the source record, now retrieve the data and copy all data to the new doc
        docs = recordset.get()
        sourceDoc = docs[0]
       
     
        transaction = db.transaction()
        

        newDocRef = dupSubDoc(transaction, None, collectionId, sourceDoc)

        transaction.commit()
      
    except Exception as e:
        log.error("Exception addObject:" + str(e) )
        raise
    finally:
        log.debug("end")  
    result = newDocRef.get().to_dict() 
    return result 

def dupSubCollection(obj):

    try:
        for parentCollectionId in obj:
            parentData = obj[parentCollectionId]
            parentDocRef = db.collection_group(parentCollectionId).where("id", u'==', parentData["id"])
            parentDoc = parentDocRef.get()[0]
            for key in parentData:
                if key != "id":
                    childCollectionId = key
                    childData = parentData[key]
                    
                    transaction = db.transaction()
                    childId = childData["id"]

                    resultSet = parentDoc.reference.collection(childCollectionId).where(u"id",u"==",childData["id"])
                    sourceDoc = resultSet.get()[0]

                    

                    resultRef = dupSubDoc(transaction, parentDoc.reference, childCollectionId, sourceDoc)

                    transaction.commit()
    except Exception as e:
        log.error("Exception dupSubCollection:" + str(e) )
        raise
    finally:
        log.debug("end dupSubCollection")  

    return resultRef.get().to_dict()

def processRequest(req):
    log.debug("firestore processRequest has been called")
    collection = req["database"]
    obj = req["data"]
    action = req["action"]
    if action == "add":
        #validateToken( req ) 
        return addObject( obj )
    if action == "addSubCollection":
        return addSubCollection( obj )
    if action == "delete":
        #validateToken( req ) 
        return deleteObject( obj )        
    if action == "get":
        #validateToken( req ) 
        return getObject( obj )  
    if action == "dupObject":
        #validateToken( req ) 
        return dupObject( obj ) 
    if action == "dupSubCollection":
        #validateToken( req ) 
        return dupSubCollection( obj )
                        
    if action == "update":
        #validateToken( req ) 
        return updateObject( obj )   
    if action == "ArrayUnion":
        #validateToken( req ) 
        return ArrayUnion( obj )   
    if action == "ArrayRemove":
        #validateToken( req ) 
        return ArrayRemove( collection, obj )                       

if __name__ == "__main__":
    print("hello mysql_connect")