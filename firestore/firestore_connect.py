from firebase_admin import firestore
import json
import logging
import uuid
import datetime
from google.api_core.datetime_helpers import DatetimeWithNanoseconds

log = logging.getLogger("cheneque")

db = firestore.client()


def isInExceptions( str:str, options):
    if options != None and "exceptions" in options:
        patterns = options["exceptions"]
        if isinstance(patterns,list):
            for pattern in patterns:
                if str.endswith( pattern ) == True:
                    log.debug("not coping:" + str)
                    return True
        else:
            raise Exception("exceptions shuld be a list of strings")
    
    return False


def addSingleSubCollectionToDoc( transaction, collectionId, parentDocRef, obj, idx):
    log.debug("addSingleSubCollectionToDoc")
    values = {}
    try:
        

        docRef = parentDocRef.collection(collectionId).document()
        values["id"] = docRef.id
        values[parentDocRef.parent.id + "_id"] = parentDocRef.id

        if "idx" in obj and obj["idx"] != None:
            values["idx"] = obj["idx"]
        else:
            #allDocs = parentDocRef.collection(collectionId).get()
            values["idx"] = idx
        
        for key in obj:
            if key != "id" and key != "idx" and not isinstance(obj[key],list) and not isinstance(obj[key],dict):
                values[key] = obj[key]

        transaction.create(docRef, values)                

        for key in obj:
            keyValue = obj[key]
            if isinstance(keyValue,list):
                values[key] = []
                for i in range(len(keyValue)):
                    element = keyValue[i]
                    subCollection = addSingleSubCollectionToDoc(transaction, key, docRef, element, i)
                    values[key].append(subCollection)
            elif isinstance(keyValue,dict):
                subCollection = addSingleSubCollectionToDoc(transaction, key, docRef, keyValue, 0)
                values[key] = subCollection

    except Exception as e:
        log.error("Exception addSubCollection:" + str(e) )
        raise
    finally:
        log.debug("addSingleSubCollectionToDoc end") 
    return values



def addSingleDocument(transaction, collectionId, obj):
    #create the reference to the new document
    values = { }
    try:
    
        docRef = db.collection(collectionId).document()
        values["id"] = docRef.id

        #copy all the fields that are not subcollections
        for key in obj:
            keyValue = obj[key]
            if key != "id" and not isinstance(keyValue,dict) and not isinstance(keyValue,list):
                values[key] = keyValue
             

        #now create the document
        transaction.create(docRef, values )

        #create all the subcollections
        for key in obj:
            keyValue = obj[key]
            if isinstance(keyValue,list):
                values[key] = []
                for i in range(len(keyValue)):
                    element = keyValue[i]
                    subCollection = addSingleSubCollectionToDoc(transaction, key, docRef, element, i)
                    values[key].append(subCollection)
            elif isinstance(keyValue,dict):
                subCollection = addSingleSubCollectionToDoc(transaction, key, docRef, keyValue, 0)
                values[key] = subCollection

    except Exception as e:
        log.error("Error addSingleDocument:" + str(e) )
        raise
    finally:
        log.debug("end") 
    return values

def addDocuments(obj):
    result = None   
    try:
        transaction = db.transaction()
        for collectionId in obj:
            data = obj[collectionId]
            if isinstance(data, list):
                result = []
                #this is a multiple insert 
                for element in data:
                    singleObject = addSingleDocument(transaction, collectionId, element)
                    result.append(singleObject)
            elif isinstance(data, dict):
                result = addSingleDocument(transaction, collectionId,data)
        transaction.commit()
    except Exception as e:
        log.error("Exception addObject:" + str(e) )
        raise
    finally:
        log.debug("end")  
    return result


def deleteRecursiveObject(transaction, docRef):
    for collection in docRef.collections():
        docs = collection.get()
        for doc in docs:
            deleteRecursiveObject(transaction, doc.reference) 
    transaction.delete( docRef )

def deleteSingleObject(transaction, doc, obj):
    try:
        result = {}
        isEnd = True

        #if there is more sub dicts follow them until there is no more 
        for key in obj:
            value = obj[key]
            if isinstance(value, dict):
                isEnd = False
                docList = doc.reference.collection(key).where("id", u'==', value["id"] ).get()
                if len(docList) < 1:
                    raise Exception("object collectionID:" + key + " id:" + str(value["id"]) + " not found")
                result = deleteSingleObject(transaction, docList[0], value) 
                    
        if isEnd == True:
            log.debug("removing object " + obj["id"])
            docJSON = doc.to_dict()
            if "idx" in docJSON:
                idx = doc.get("idx")
                if idx != None:
                    parentDoc = doc.reference.parent.parent
                    toMoveDocList = parentDoc.collection(doc.reference.parent.id).where(u"idx",u">",idx).get()
                    for toMoveDoc in toMoveDocList:
                        if toMoveDoc.get("id") != doc.get("id"):
                            transaction.update(toMoveDoc.reference,{"idx":toMoveDoc.get("idx") - 1})
                result = {"id":obj["id"], "idx":idx}
            else:
                result = {"id":obj["id"] }
            deleteRecursiveObject( transaction, doc.reference )
    except Exception as e:
        log.error("Exception deleteSingleObject:" + str(e) )
        raise
    finally:
        log.debug("end")  
    return result

def deleteObject(obj):
    logging.debug( "firestore deleteObject called")
    logging.debug( "obj:%s",json.dumps(obj,  indent=4, sort_keys=True) ) 


    result = {}
    try:
        transaction = db.transaction()
        for collectionId in obj:
            data = obj[collectionId]
            if isinstance(data, list):
                elements = data
                result = []
                for element in elements:
                    docList = db.collection(collectionId).where(u'id', u'==', element["id"]).get()
                    if len(docList) < 1:
                        raise Exception("document:" + str(collectionId) + " id:" + str(element["id"]) + "not found")
                    deleted = deleteSingleObject(transaction, docList[0], data)
                    result.append(deleted)
            elif isinstance(data, dict):
                docList = db.collection(collectionId).where(u'id', u'==', data["id"]).get()
                if len(docList) < 1:
                    raise Exception("document:" + str(collectionId) + " id:" + str(data["id"]) + "not found")
                result = deleteSingleObject(transaction, docList[0], data)

        transaction.commit()

    except Exception as e:
        log.error("Exception deleteObject:" + str(e) )
        raise
    finally:
        log.debug("end")  
    return result

#deletes all objects below a path
#obj{
#   collection:"employees/emp1234/jobs",
#   id:job123   
#}
def deleteCollectionObject(obj):
    logging.debug( "firestore deleteCollectionObject called")
    logging.debug( "obj:%s",json.dumps(obj,  indent=4, sort_keys=True) ) 


    result = {}
    try:
        transaction = db.transaction()
        collectionId = obj["collection"]
        id = obj["id"]

        sourceRef = db.collection(collectionId).document(id)
        sourceDoc = sourceRef.get()
        if not sourceDoc.exists:
            raise Exception("document:" + str(collectionId) + " id:" + str(id) + "not found")
        
        deleteRecursiveObject( transaction, sourceDoc.reference )

        transaction.commit()
        result = obj
    except Exception as e:
        log.error("Exception deleteCollectionObject:" + str(e) )
        raise
    finally:
        log.debug("end")  
    return result

def addSingleSubcollection(transaction, doc, obj):
        result = {}
        isEnd = True

        #if there is more sub dicts follow them until there is no more 
        for key in obj:
            value = obj[key]
            if isinstance(value, dict) and "id" in value and value["id"] != None:
                isEnd = False
                docList = doc.reference.collection(key).where("id", u'==', value["id"] ).get()
                if len(docList) < 1:
                    raise Exception("object collectionID:" + key + " id:" + str(value["id"]) + " not found")
                result = addSingleSubcollection(transaction, docList[0], value) 
            elif isinstance(value, dict) and ("id" not in value or value["id"] == None):
                log.debug( json.dumps(value,  indent=4, sort_keys=True) )
                result = value
                doc_ref = doc.reference.collection(key).document()
                alldocs = doc.reference.collection(key).get()

                result["id"] = doc_ref.id
                result[doc.reference.parent.id + "_id" ] = doc.reference.id
                result["idx"] = len(alldocs)
                doc_ref.set( result )  

        return result          


def addSubCollection(obj):
    result = None
    try:
        collectionId = list(obj.keys())[0]
        parentDocList = db.collection(collectionId).where(u'id', u'==', obj[collectionId]["id"]).get()
        if len(parentDocList) < 1:
            raise Exception("Parent doc not found")
        doc = parentDocList[0]
        parentData = obj[collectionId]

        transaction = db.transaction()

        result = addSingleSubcollection(transaction, doc, parentData )

        transaction.commit()
            
    except Exception as e:
        log.error("Exception addSubCollection:" + str(e) )
        raise
    finally:
        log.debug("end")  
    return result


def updateSingleObject(transaction, doc, data):
    values = {}
    for key in data:
        if key != "id":
            value = data[key]
            if isinstance(value, list):
                subCollectionData = value
                collectionId = key
                for element in subCollectionData:
                    subDocList = doc.reference.collection(collectionId).where("id", u'==', element["id"]).get()
                    if len(subDocList) < 1:
                        raise Exception("document:" + str(collectionId) + " id:" + str(element["id"]) + " not found" )
                    updateSingleObject( transaction, subDocList[0], element)
            elif isinstance(value, dict):
                subCollectionData = value
                collectionId = key
                subDocList = doc.reference.collection(collectionId).where("id", u'==', subCollectionData["id"]).get()
                if len(subDocList) < 1:
                    raise Exception("document:" + str(collectionId) + " id:" + str(subCollectionData["id"]) + " not found")
                updateSingleObject( transaction, subDocList[0], subCollectionData)
            else:
                values[key] = data[key]
    if len(values.keys()) > 0:
        transaction.update( doc.reference, values)

def updateObject(obj):
    try:
        transaction = db.transaction()    
        for collectionId in obj.keys():
            records = obj[collectionId]
            if isinstance(records, list):
                for element in records:
                    docList = db.collection(collectionId).where("id", u'==', element["id"]).get()
                    if len(docList) < 1:
                        raise Exception("document:" + str(collectionId) + " id:" + str(element["id"]) + " not found" )
                    updateSingleObject( transaction, docList[0], element)
            elif isinstance(records, dict):
                element = records
                docList = db.collection(collectionId).where("id", u'==', element["id"]).get()
                if len(docList) < 1:
                    raise Exception( "document:" + str(collectionId) + " id:" + str(element["id"]) + " not found" )
                updateSingleObject( transaction, docList[0], element)
        transaction.commit()

            
    except Exception as e:
        log.error("Exception updateSingleObject:" + str(e) )
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

def ArrayRemove(obj):
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

def getSubCollection( parentDoc, collectionId, filter):
    result = None
    try:
        if isinstance( filter, list ):
            filter = filter[0]
            result = []
        collectionset = parentDoc.reference.collection(collectionId)
        collections = parentDoc.reference.collections()
        for c in collections:
            log.debug("%s %s",c.id, c.get())
        #apply the filter if any
        for key in filter:
            keyValue = filter[key]
            if not isinstance(keyValue,list) and not isinstance(keyValue,dict) and keyValue!=None:
                collectionset = collectionset.where(key ,"==", keyValue )

        
        #retrieve the docs that comply with the where
        docs = collectionset.get()
        for doc in docs:
            values = {}
            documentJSON = doc.to_dict()

           
            #copy only the fields named in the filter
            for key in filter:
                keyValue = filter[key]
                if isinstance(keyValue,dict) or isinstance(keyValue,list):
                    subCollection = getSubCollection(doc, key, keyValue)
                    values[key] = subCollection
                else:
                    if key in documentJSON:
                        values[key] = documentJSON[key]
                    else:
                        values[key] = None

            if isinstance(result,list):
                result.append(values)
            elif result == None: 
                result = values
            else:
                raise Exception("multiple values found for key:" + key + " but only one requested")


    except Exception as e:
        log.error("Exception getSubCollection:" + collectionId + " " + str(e) )
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
#        },
#        orderBy:{
#            id : 'desc' 
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
        #the recordset has the where and the sortby now retrieve the data
        docs = recordset.get()
        for doc in docs:
            documentJSON = doc.to_dict()

            values = {}
            #if there is a subcollection to retrieve call it
            for key in data:
                keyValue = data[key]
                if isinstance(keyValue,dict) or isinstance(keyValue,list):                
                    subcollection = getSubCollection(doc,key, keyValue)
                    values[key] = subcollection

                elif key in documentJSON:
                    values[key] = documentJSON[key]
                else:
                    values[key] = None
            if isinstance(result, list):
                result.append(values)
            elif result == None:
                result = values
            else:
                raise Exception("multiple values found for collectionId:" + collectionId + " but only one requested" )
        #recordset has the where now add the sort
        if 'orderBy' in obj:
                orderBy = obj['orderBy'] 
                field = orderBy["field"]
                direction = "asc"
                if "direction" in orderBy:
                    direction = orderBy["direction"]
                useReverse = False
                if direction.lower() == 'desc':
                    useReverse=True
                
                result = sorted(result, key=lambda obj : obj[field], reverse=useReverse)
                startAfter=None
                if "startAfterId" in orderBy:
                    startAfter = orderBy["startAfterId"]
                    pageSize = 20
                    if "pageSize" in orderBy:
                        pageSize = orderBy["pageSize"]
                
                    page = []
                    index = 0
                    if startAfter:
                        for index, item in enumerate(result, start=0):   # Python indexes start at zero
                            if item["id"] == startAfter:
                                break
                    for i in range(1,pageSize):
                        if( index + i ) < len(result):
                            page.append(result[index+i])
                        else: 
                            break
                    result = page

            


    except Exception as e:
        log.error("Exception getObject:" + str(e) )
        raise
    finally:
        log.debug("end")  
    return result   

#only a new id is generated for each subcollection all other including idx is copies

def copySubCollection(transaction, parentDocRef, collectionId, sourceDoc, options):
    values = None
    try:
        log.debug( "copy:" + collectionId )
        
        newDocRef = parentDocRef.collection(collectionId).document()
        
        parent_id_key = parentDocRef.parent.id + "_id"

        values = {"id":newDocRef.id , parent_id_key: parentDocRef.id}    
        documentJSON = sourceDoc.to_dict()
        for key in documentJSON:
            if key != "id" and isInExceptions(key, options)==False:
                keyValue = documentJSON[key]
                if key != "id" and key != parent_id_key:
                    values[key] = documentJSON[key]
        transaction.create( newDocRef,values)
        #the new doc thas been created and now copy all the sub collections
        collections = sourceDoc.reference.collections()
        

        for subCollection in collections:
            if( isInExceptions(subCollection.id, options)==False ):
                log.debug("collection %s", subCollection.id)
                subDocs = subCollection.get()
                values[subCollection.id] = []
                for subDoc in subDocs:
                    newCollection = copySubCollection(transaction, newDocRef, subCollection.id, subDoc, options)
                    values[subCollection.id].append(newCollection)

    except Exception as e:
        log.error("Exception copySubCollection:" + str(e) )
        raise
    finally:
        log.debug("copySubCollection end")  
    return values


#copy object
#options if the name ends with any of the string it will not be copied
#option = { exceptions = ["Path", "secretInfo"] }
def dupDocument(obj, options):
    logging.debug( "firestore dupObject called")
    logging.debug( "obj:%s",json.dumps(obj,  indent=4, sort_keys=True) )
    values = None
    try:
        collectionId = None
        recordset = None
        data = None
        result = None
        collectionId = list(obj.keys())[0]

        docId = obj[collectionId]["id"]
        
        docList = db.collection(collectionId).where(u"id", u"==", docId).get()
        if len(docList) < 1:
            raise("document to copy not found:" + docId)
        transaction = db.transaction()
        sourceDoc = docList[0]

        newDocRef = db.collection(collectionId).document()
        values = {"id":newDocRef.id}  
        #now copy all the fields 
        documentJSON = sourceDoc.to_dict()
        for key in documentJSON:
            if key != "id" and isInExceptions(key, options)==False:
                keyValue = documentJSON[key]
                if key in obj[collectionId]: #the value can be overwritten from the source object
                    values[key] = obj[collectionId][key]
                else:
                    values[key] = documentJSON[key]
  

        transaction.create( newDocRef,values)
        for collection in sourceDoc.reference.collections():
            if( isInExceptions(collection.id,options) == False):
                values[collection.id] = []
                for subDoc in sourceDoc.reference.collection(collection.id).get():
                    subCollection = copySubCollection(transaction, newDocRef, collection.id, subDoc, options)
                    values[collection.id].append(subCollection)
        transaction.commit()
        
      
    except Exception as e:
        log.error("Exception dupDocument:" + str(e) )
        raise
    finally:
        log.debug("dupDocument end")  
    result = newDocRef.get().to_dict() 
    return values 

#create a new version of a document with and incremented version
# set the new version of the document as isCurrentVersion
# update the old version of the document isCurrentVersion as false
# update the updated_on with the date on both old a new version
# parameters: a json object with the following data
#  collectionPath of the document
#  id of the document to duplicate
#  versionKey usually "version"
#  isCurrentVersionKey usually "is_current_version"
#  updateOnKey usually "updated_on"
#  options to exclude some items in the duplication
# return the new id of the document
def createDocumentNewVersion(obj, options):
    logging.debug( "firestore createNewDocumentVersion called")
    logging.debug( "obj :%s",json.dumps(obj,  indent=4, sort_keys=True) )
    values = None
    try:
        collectionId = obj["collectionPath"]
        docId = obj["id"]
        versionKey = obj["versionKey"]
        isCurrentVersionKey = obj["isCurrentVersionKey"]
        updateOnKey = obj["updateOnKey"]
        newValues = obj["newValues"]
         
  
        recordset = None
        data = None
        result = None
       
       #find the document to generate a new version
        sourceRef = db.collection(collectionId).document(docId)
        sourceDoc = sourceRef.get()
        if not sourceDoc.exists:
            raise("document to copy not found:" + docId)
        documentJSON = sourceDoc.to_dict()

        transaction = db.transaction()
  

        newDocRef = db.collection(collectionId).document(docId.split("_")[0] + "_" + str(documentJSON[versionKey] + 1) )
        values = {"id":newDocRef.id}  
        #now copy all the fields 
        
        for key in documentJSON:
            if key != "id" and isInExceptions(key, options)==False:
                if key in newValues: #the value can be overwritten from the source object
                    values[key] = newValues[key]
                else:
                    values[key] = documentJSON[key]                
        
        #now update the values related to version
        dateTimeNow = datetime.datetime.now()
        timeNow = DatetimeWithNanoseconds(dateTimeNow.year, dateTimeNow.month, dateTimeNow.day, dateTimeNow.hour, dateTimeNow.minute, dateTimeNow.second, 0) 

        updateValues = {
            updateOnKey: timeNow,
            isCurrentVersionKey: False
        }
        transaction.update( sourceRef , updateValues )

        values[versionKey] = values[versionKey] + 1
        values[updateOnKey] = timeNow



        transaction.create( newDocRef,values)
        for collection in sourceDoc.reference.collections():
            if( isInExceptions(collection.id,options) == False):
                values[collection.id] = []
                for subDoc in sourceDoc.reference.collection(collection.id).get():
                    subCollection = copySubCollection(transaction, newDocRef, collection.id, subDoc, options)
                    values[collection.id].append(subCollection)

        transaction.commit()
        
      
    except Exception as e:
        log.error("Exception dupDocument:" + str(e) )
        raise
    finally:
        log.debug("dupDocument end")  
    return values 

def dupSubCollection(obj, options):
    values = {}
    try:
        transaction = db.transaction()
        collectionId = list(obj.keys())[0]
        data = obj[collectionId]
        docs = db.collection(collectionId).where("id", u'==', data["id"]).get()
        if len(docs) < 1:
            raise Exception("obj to dup not found")
        doc = docs[0]

         
        while collectionId != "":
            collectionId = ""
            for key in data:
                value = data[key]
                if isinstance( value, dict) and "id" in value:
                    collectionId = key
                    docList = doc.reference.collection(collectionId).where("id",u'==', value["id"]).get() 
                    if len(docList) < 1:
                        raise Exception("object collection" + key + " id:" + value["id"] + "not found")
                    doc = docList[0]
            if collectionId != "":
                data = data[collectionId]  

        log.debug( json.dumps(data,  indent=4, sort_keys=True) )       


        parentCollection = doc.reference.parent
        newDocRef = parentCollection.document()
        values["id"] = newDocRef.id
        allDocs = parentCollection.get()
        values["idx"] = len(allDocs)

        #now copy all the fields 
        documentJSON = doc.to_dict()
        for key in documentJSON:
            if key != "id" and key != "idx" and isInExceptions(key, options)==False:            
                keyValue = documentJSON[key]
                if key in data:
                    values[key] = data[key]
                else:
                    values[key] = documentJSON[key]

        #now copy all the subcollections
        transaction.create( newDocRef,values)
        for collection in doc.reference.collections():
            if isInExceptions(collection.id, options)==False:
                values[collection.id] = []
                for subDoc in doc.reference.collection(collection.id).get():
                    newSubCollection = copySubCollection(transaction, newDocRef, collection.id, subDoc, options)
                    values[collection.id].append(newSubCollection)
                
        transaction.commit()

    except Exception as e:
        log.error("Exception dupSubCollection:" + str(e) )
        raise
    finally:
        log.debug("dupSubCollection end")  

    return values
    
def moveSubCollectionIndex(obj):
    result = None
    try:
        transaction = db.transaction()
        collectionId = list(obj.keys())[0]
        data = obj[collectionId]
        docs = db.collection(collectionId).where("id", u'==', data["id"]).get()
        if len(docs) < 1:
            raise Exception("obj to dup not found")
        doc = docs[0]

         
        while collectionId != "":
            collectionId = ""
            for key in data:
                value = data[key]
                if isinstance( value, dict) and "id" in value:
                    collectionId = key
                    docList = doc.reference.collection(collectionId).where("id",u'==', value["id"]).get() 
                    if len(docList) < 1:
                        raise Exception("object collection" + key + " id:" + value["id"] + "not found")
                    doc = docList[0]
            if collectionId != "":
                data = data[collectionId]  

        log.debug( json.dumps(data,  indent=4, sort_keys=True) )       

                   
        sourceDoc = doc
        sourceIndex = doc.get("idx")
        newIndex = data["idx"]
        parentDocRef = doc.reference.parent.parent

        count = len(parentDocRef.collection(doc.reference.parent.id).get())
        if  newIndex < 0 or newIndex >= count:
            raise Exception("new index:" + str(newIndex) + " is invalid for collection size:" + str(count))


        if newIndex < sourceIndex :
            toMoveDocRefs = parentDocRef.collection(doc.reference.parent.id).where(u"idx",u">=",newIndex)
            for toMoveDoc in toMoveDocRefs.get():
                if toMoveDoc.get("id") != sourceDoc.get("id"):
                    transaction.update(toMoveDoc.reference,{"idx":toMoveDoc.get("idx") + 1})
        elif newIndex > sourceIndex :
            toMoveDocList = parentDocRef.collection(doc.reference.parent.id).where(u"idx",u">",sourceIndex).where(u"idx",u"<=",newIndex).get()
            for toMoveDoc in toMoveDocList:
                if toMoveDoc.get("id") != sourceDoc.get("id"):
                    transaction.update(toMoveDoc.reference,{"idx":toMoveDoc.get("idx") - 1})

        transaction.update(sourceDoc.reference,{"idx":newIndex})
        result = {"id":doc.id, "idx":newIndex}

        transaction.commit()

    except Exception as e:
        log.error("Exception moveSubCollectionIndex:" + str(e) )
        raise
    finally:
        log.debug("end moveSubCollectionIndex")  

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
#        },
#        orderBy:{
#            id : 'desc' 
#        },
#        paginatedBy:{
#           pageIndex: 0,
#           pageSize:0,
#           length:0  
#        }
#   }    
#}
# return value
#   {
#     resultSet:{
#        id=100,
#        label:"El cascanueces"       
#     }
#     info:{
#        totalNumRows:100
#     }
#   } 
def getPaginatedObject(obj):
    logging.debug( "firestore getObject called")
    logging.debug( "obj:%s",json.dumps(obj,  indent=4, sort_keys=True) )
    result = None
    pageIndex = 0
    pageSize = 0  
    totalNumRows = 0 
    afterId = None
    try:
        collectionId = None
        recordset = None
        data = None
        result = None
        for key in obj:
            if key not in ["orderBy", "paginatedBy"]:
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
                orderField = orderBy["field"]                
                orderValue = orderBy["direction"]
                if orderValue == "asc":
                    recordset = recordset.order_by(orderField,direction=firestore.Query.ASCENDING)    
                else:
                    recordset = recordset.order_by(orderField, direction=firestore.Query.DESCENDING)

        if 'paginatedBy' in obj:
                paginatedBy = obj['paginatedBy'] 
                afterId = paginatedBy['startAtId']
                if afterId != None:
                    recordset = recordset.start_at({u'id':afterId})


        #the recordset has the where and the sortby now retrieve the data
        docs = recordset.get()
        totalNumRows = docs.size()
        for doc in docs:
            documentJSON = doc.to_dict()

            values = {}
            #if there is a subcollection to retrieve call it
            for key in data:
                keyValue = data[key]
                if isinstance(keyValue,dict) or isinstance(keyValue,list):                
                    subcollection = getSubCollection(doc,key, keyValue)
                    values[key] = subcollection

                elif key in documentJSON:
                    values[key] = documentJSON[key]
                else:
                    values[key] = None
            if isinstance(result, list):
                result.append(values)
            elif result == None:
                result = values
            else:
                raise Exception("multiple values found for collectionId:" + collectionId + " but only one requested" )
        #create the info object
        info = {
            totalNumRows:totalNumRows
        } 
        result = {
            
        }           


    except Exception as e:
        log.error("Exception getObject:" + str(e) )
        raise
    finally:
        log.debug("end")  
    return result   


def processRequest(req):
    log.debug("firestore processRequest has been called")
    database = req["database"]
    obj = req["data"]
    action = req["action"]
    options = None
    if "options" in req:
        options = req["options"]

    if action == "add":
        #validateToken( req ) 

        return addDocuments( obj )
    elif action == "addSubCollection":
        return addSubCollection( obj )
    elif action == "delete":
        #validateToken( req ) 
        return deleteObject( obj )        
    elif action == "get":
        #validateToken( req ) 
        return getObject( obj )  

    elif action == "dupDocument":
        #validateToken( req ) 
        return dupDocument( obj , options) 
    elif action == "dupSubCollection":
        #validateToken( req ) 
        return dupSubCollection( obj, options )
    elif action == "createDocumentNewVersion":
        #validateToken( req ) 
        return createDocumentNewVersion( obj, options )    
    elif action == "update":
        #validateToken( req ) 
        return updateObject( obj )   
    elif action == "ArrayUnion":
        #validateToken( req ) 
        return ArrayUnion( obj )   
    elif action == "ArrayRemove":
        #validateToken( req ) 
        return ArrayRemove( obj )                       
    elif action == "moveSubCollectionIndex":
        #validateToken( req ) 
        return moveSubCollectionIndex( obj ) 
    elif action == "deleteCollectionObject":
        return deleteCollectionObject( obj )
    else:
        raise Exception("Action not recognized")

if __name__ == "__main__":
    print("hello mysql_connect")