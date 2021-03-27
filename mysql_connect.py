#need to run before debuggin from visual studio
#gcloud login
#gcloud info
#gcloud auth application-default login
import sys
import datetime
import json
import logging
import pymysql as MySQLdb
import decimal
import uuid
import firebase_admin 
from firebase_admin import auth
from environments_prd import config


# Initialize the default app only in development
# export GOOGLE_APPLICATION_CREDENTIALS="/home/raul/cheneque/celtic-bivouac-307316-firebase-adminsdk-pbsww-2ccfde6abd.json"

#   GCP cloud
#database_host="10.128.0.12", 
#database_password="Argos4905!",

#local database        
#database_host="192.168.15.12"
#database_password="odroid"

default_app = firebase_admin.initialize_app()


print(default_app.name)  # "[DEFAULT]"

log = logging.getLogger("exam_app")

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class LoginError(Error):
    pass

class DeleteWithEmptyWhereError(Error):
    pass

def addFieldValueToExpresion(expresion, field, value, sep):
    if len(expresion) > 0:
        expresion = expresion + sep

    if value == None:
        expresion = expresion + field + "= null"
    elif isinstance(value,str):                    
        expresion = expresion + field + "="+  "'" + value + "'"
    elif isinstance(value, bool):
        if value==True:
            expresion = expresion + field + "=" + "1"
        else:
            expresion = expresion + field + "="  + "0"
    elif isinstance(value , datetime.datetime):
        expresion = expresion + field + "="  + "'" + value.strftime("%Y-%m-%d %H:%M:%S") + "'"
    elif isinstance(value , datetime.date):
        expresion = expresion + field + "=" + "'" + value.strftime("%Y-%m-%d")+ "'"                   
    else:
        expresion = expresion + field + "="+  str(value)
    return expresion

def getAddValueToExpresion(expresion,value,sep):
    if len(expresion) > 0:
        expresion = expresion + sep

    if value == None:
        expresion = expresion + "null"
    elif isinstance(value,str):                    
        expresion = expresion +  "'" + value + "'"
    elif isinstance(value, bool):
        if value==True:
            expresion = expresion + "1"
        else:
            expresion = expresion + "0"
    elif isinstance(value , datetime.datetime):
        expresion = expresion + "'" + value.strftime("%Y-%m-%d %H:%M:%S") + "'"
    elif isinstance(value , datetime.date):
        expresion = expresion + "'" + value.strftime("%Y-%m-%d")+ "'"                   
    else:
        expresion = expresion + str(value)
    return expresion



class MySql:
    cnx = None

    def __init__(self):
        try:
            self.cnx =  MySQLdb.connect(
            host=config["database_host"],
            user=config["user"],
            password=config["database_password"],       
            database=config["database"])
            log.debug(self.cnx)         
        except Exception as e:
            log.error("Exception connecting to database:" + str(e) ) 
            raise e

    def getConnection(self):
        return self.cnx
    
    def close(self):
        self.cnx.close()

    def getConstraints(self, childTable, parentTable):
        try:
            referenced_table_schema = []
            cursor = self.getConnection().cursor()            
            query = """
            SELECT TABLE_NAME,COLUMN_NAME,CONSTRAINT_NAME, REFERENCED_TABLE_NAME,REFERENCED_COLUMN_NAME
            FROM
            INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE
            REFERENCED_TABLE_SCHEMA = 'entities' AND
            TABLE_NAME = %s AND
            REFERENCED_TABLE_NAME = %s
            """
            cursor.execute(query, (childTable, parentTable))


            for (table_name, column_name, constraint_name, reference_table_name, referenced_column_name) in cursor:
                log.debug("constraint:{}, {} , {}, {}, {}".format(
                table_name, column_name, constraint_name, reference_table_name, referenced_column_name))
                obj = {
                    "table_name":table_name, 
                    "column_name":column_name, 
                    "constraint_name":constraint_name, 
                    "reference_table_name":reference_table_name, 
                    "referenced_column_name":referenced_column_name
                }
                referenced_table_schema.append(obj)
        except Exception as e:
            log.error("Exception getConstraints" + str(e))
              
        finally:
            cursor.close()

        return referenced_table_schema      



class Table:
    parentTableName = None
    tableName = None
    tableFilter = None
    isList = False
    isOuterJoin = False
    def __init__(self,parentTableName, tableName, filter):
        log.debug( "new Table(%s,%s)", str(parentTableName) , str(tableName) ) 
        self.parentTableName = parentTableName
        if tableName.endswith("(+)") == True:
            l = len(tableName) - 3
            self.tableName = tableName[0:l] 
            self.isOuterJoin = True
        else:
            self.tableName = tableName
        
        if isinstance( filter, list ):
            self.tableFilter = filter[0]
            self.isList = True
        else:
            self.tableFilter = filter 

        log.debug("tableFilter:%s", self.tableFilter)       

    def getSelect(self):
        exp = ""
        for key in self.tableFilter.keys():
            value = self.tableFilter[key]
            if not isinstance(value,dict) and not isinstance(value,list):
                if exp != "":
                    exp = exp + ", "
                exp = exp + self.tableName + "." + str(key) + " as '" + self.tableName + "." + str(key) + "'"
        return exp

    def getWhereExpression(self):
        where = ""

        for key in self.tableFilter.keys():
            value = self.tableFilter[key]
            if value != "":
                if not isinstance(value,dict) and not isinstance(value,list): 
                    where = addFieldValueToExpresion(where, self.tableName + "." + key, value, " and ")
                
        return where

    def createObjectFromRow( self, row ):
        isNullObject = True
        obj = {}
        for key in self.tableFilter.keys():
            value = self.tableFilter[key]
            if not isinstance(value,dict) and not isinstance(value,list):
                rowValue = row[self.tableName + "." + key]
                log.debug("createObjectFromRow key %s is a %s" , key, type(rowValue))
                if rowValue!=None:
                    isNullObject = False
                if isinstance(rowValue , datetime.datetime):
                    obj[key] = rowValue.strftime("%Y/%m/%d %H:%M:%S")
                elif isinstance(rowValue , datetime.date):
                    obj[key] = rowValue.strftime("%Y/%m/%d") 
                elif isinstance(rowValue, decimal.Decimal ):
                    obj[key] = float( rowValue )                    
                else:
                    obj[key] = rowValue
        if isNullObject:
            return None
        else:
            return obj
    
    def compareObjToRow(self, obj, row ):
        for key in self.tableFilter.keys():
            value = self.tableFilter[key]
            if not isinstance(value,dict) and not isinstance(value,list):
                rowValue = row[self.tableName + "." + key]
                
                if isinstance(rowValue , datetime.datetime):
                    v = rowValue.strftime("%Y/%m/%d %H:%M:%S")
                elif isinstance(rowValue , datetime.date):
                    v = rowValue.strftime("%Y/%m/%d")   
                elif isinstance(rowValue, decimal.Decimal ):
                    v = float( rowValue )                                      
                else:
                    v = rowValue                
                
                if obj[key] != v:
                    return False
        return True        

class Qry:
    tables = []
    reservedWords = ("orderBy","pagination")

    def __init__(self):
        self.tables = []

    def createTableList(self, parentTable, request):
        try:
            for key in request.keys():
                if (isinstance(request[key],dict) or isinstance(request[key],list) ) and key not in self.reservedWords:
                    t = Table(parentTable, key, request[key])
                    self.tables.append( t )
                    self.createTableList( t.tableName, t.tableFilter )
        except Exception as e:
            log.error("Exception: createTableList" + str(e))
            raise

    def getTableByName(self,tableName):

        if tableName.endswith("(+)") == True:
            l = len(tableName) - 3
            tableName = tableName[0:l] 
        else:
            tableName = tableName

        for i in range(0,len(self.tables)):
            if self.tables[i].tableName == tableName :
                return self.tables[i]
        return None

    def fillObjectFromRow(self, obj, objRow,  request):
        try:
            for key in request.keys():
                log.debug("filling object key %s", key)
                keyValue = request[key]
                log.debug("key %s is a %s" , key, type(keyValue))
                if isinstance(keyValue,dict) or isinstance(keyValue,list):
                    if isinstance(keyValue,list):
                        filter = keyValue[0]
                    elif isinstance(keyValue,dict):
                        filter = keyValue                
                    t = self.getTableByName(key)
                    newObj = t.createObjectFromRow( objRow )
                    if t.tableName not in obj:
                        log.debug("object %s is null creating new", key) 
                        if t.isList:
                            log.debug("objet %s is array creating new", key)
                            obj[t.tableName] = []
                            if newObj != None:
                                obj[t.tableName].append( newObj )                           
                        else:
                            log.debug("object %s is object creating new", key)
                            obj[t.tableName] = newObj
                        lastObject = newObj
                    else:
                        if t.isList:
                            log.debug("object %s was not null and array retring last", key) 
                            if len(obj[t.tableName]) > 0:
                                lastObject = obj[t.tableName][-1]
                            else:
                                lastObject = None
                        else:
                            log.debug("object %s was not null and object retrivig last")
                            lastObject = obj[t.tableName] 
                    #compare the new row to the previous one and if false then there should be a new row
                    log.debug("compare vs last Object")
                    if lastObject != None:
                        if t.compareObjToRow( lastObject, objRow) == False:
                            log.debug("new row is different from last adding row")
                            obj[t.tableName].append( newObj )
                            lastObject = newObj
                        log.debug("call for sub filters")
                        self.fillObjectFromRow( lastObject, objRow, filter) 
        except Exception as e:
            log.error("fillObjectFromRow:" + str(e))
            raise                
    
    def buildQry(self, request):
        try:
            mydb = MySql()    
            self.createTableList( None, request)

            log.debug("self.tables length %i", len(self.tables))
            select = "SELECT "
            for i in range(0, len(self.tables)):
                t = self.tables[i]
                if i != 0:
                    select = select + ","
                select = select + t.getSelect() + "\n"
                log.debug("select %i table:%s temp:%s",i, t.tableName, select )

            log.debug("select:" + select)

            log.debug("creating join")

            join = ""
            for i in range(0, len(self.tables)):
                
                t = self.tables[i]
                if i == 0:
                    join = "FROM " + t.tableName 
                else:
                    if t.isOuterJoin:
                        join = join + " LEFT JOIN " + t.tableName + " ON ("
                    else:
                        join = join + " JOIN " + t.tableName + " ON ("
                
                    constraints = mydb.getConstraints( t.parentTableName, t.tableName )

                    if len(constraints) == 0 :
                        constraints = mydb.getConstraints( t.tableName, t.parentTableName )

                    if len(constraints) == 0:
                        raise Exception("no FK found for tables "+ t.tableName + " and " + t.parentTableName)

                    for j in range(0,len(constraints)):
                        c = constraints[j]
                        if j != 0:
                            join = join + " AND "
                        join = join + c["table_name"] + "." + c["column_name"] + " = " + c["reference_table_name"] + "." + c["referenced_column_name"]
                    join = join + ")"

            log.debug( "join:" + join )

            qry = select + join
            log.debug("qry:%s", qry)

            log.debug("creating where")
            where = ""
            for i in range(0, len(self.tables)):
                t = self.tables[i]
                w = t.getWhereExpression()
                if w != "":
                    if where != "":
                        where = where + " and " + w
                    else:
                        where = w

            log.debug( "where:" + where )

            if where !="" :
                qry = qry + "\nWHERE " +  where

            orderExp = ""
            if "orderBy" in request:
                orderBy = request["orderBy"] 
                for key in orderBy:
                    if orderExp != "":
                        orderExp = orderExp + ","
                    orderExp = orderExp + key + " " + orderBy[key]

            if orderExp != "":
                qry = qry + "\nORDER BY " + orderExp

            paginationExp = ""
            if "pagination" in request:
                pagination = request["pagination"] 
                if "limit" in pagination:
                    limit =  pagination["limit"]
                    paginationExp = "limit " + str(limit) 
                if "offset" in pagination:
                    offset =  pagination["offset"]
                    paginationExp = paginationExp + " offset " + str(offset) 

            if paginationExp != "":
                qry = qry + "\n" + paginationExp

            log.debug("qry:%s", qry)
            return qry
            
        except Exception as e:
            log.error("Exception executeQry %s",str(e))
            raise
        finally:
            mydb.close()

    def buildObject(self, request, query):
        try:
            result = None
            mydb = MySql()
            cursor = mydb.getConnection().cursor()
            log.debug("Executing query: %s", query)            
            cursor.execute(query)
            column_names =  [field[0] for field in cursor.description] 
            
            for row in cursor:
                objRow = dict(zip(column_names,row))
               
                #log.debug( json.dumps(obj,  indent=4, sort_keys=True) )
                for i in range(0,len(column_names)):
                    log.debug("%s:%s", column_names[i], str( objRow[column_names[i]] ) )

                
                for key in request.keys():
                    keyValue = request[key]
                    if ( isinstance(keyValue,dict) or isinstance(keyValue,list) ) and key not in self.reservedWords:
                        log.debug("creating object for:%s", key)
                        if isinstance(keyValue,list):
                            filter = keyValue[0]
                        elif isinstance(keyValue,dict):
                            filter = keyValue
                        t = self.getTableByName(key)
                        newObj = t.createObjectFromRow( objRow )
                        #ensure there is a lastObject
                        
                        if result == None: 
                            log.debug("key %s is null creating new", key)
                            if t.isList:
                                log.debug("key %s is array creating new", t.tableName)
                                result = [] 
                                result.append( newObj )                           
                            else:
                                log.debug("key %s is object creating new", key)
                                result = newObj
                            lastObject = newObj
                        else:
                            log.debug("key %s is not null retring last", key)
                            if t.isList:        
                                lastObject = result[-1]
                            else:
                                lastObject = result 
                        #compare the new row to the previous one and if false then there should be a new row
                        log.debug("comparing objects")
                        if t.compareObjToRow( lastObject, objRow) == False:
                            log.debug("last object is not the same creating new row")
                            result.append( newObj )
                            lastObject = newObj

                        self.fillObjectFromRow( lastObject, objRow, filter) 
            cursor.close()
        except Exception as e:
            log.error("Exception buildObject:" + str(e))
            raise
              
        finally:
            
            mydb.close()

        return result


    def executeQry(self,request):
        qry = self.buildQry(request)
        obj = self.buildObject(request, qry)
        return obj
       
    def toJSON(self):
        return self.data        

def getObject(request):
    log.info("GetObject Called")
    try:
        q = Qry()
        obj = q.executeQry( request )
        
    except Exception as e:
        log.error("getObject error:" + str(e) )
        raise
    log.info("GetObject Called ended")
    return obj

def insertObject(connection, parent_id_field, parent_id, table, request):
    log.info("Insertobject called")
    cursor = connection.cursor()
    rowid = None
    fieldsExp = ""
    valuesExp = ""

    if parent_id_field != None :
        request[parent_id_field]=parent_id

    for key in request:
        keyValue = request[key]
        log.debug("key %s is instance of %s",key, type(keyValue) )
        if ( isinstance(keyValue,dict) or isinstance(keyValue,list) ):
            continue  

        if( fieldsExp != ""):
            fieldsExp = fieldsExp + ","
        fieldsExp = fieldsExp + key

        valuesExp = getAddValueToExpresion(valuesExp,request[key],"," )
                    
    sql = "INSERT INTO " + table + "(" + fieldsExp + ") values(" + valuesExp + ")"
    log.debug("sql:" + sql)
        
    cursor.execute(sql)
    log.debug("insert ended")

    rowid= cursor.lastrowid

    if "id" in request and rowid:
        request["id"] = rowid

    #now call recursivelly to insert all child 
    for key in request:
        keyValue = request[key]
        if isinstance(keyValue,dict):
            insertObject( table + "_id", rowid, key, keyValue) 
        elif isinstance(keyValue,list):
            for i in range(0, len(keyValue)):
                insertObject( connection, table + "_id", rowid, key, keyValue[i])
    log.debug("Insertobject ended")
    return request


    

def addObject(request):
    log.info("AddObject called")
    try:
        mydb = MySql()
        connection = mydb.getConnection()

        for key in request:
            keyValue = request[key]
            if isinstance(keyValue,dict):
                insertObject(connection, None, None, key, keyValue) 
            elif isinstance(keyValue,list):
                for i in range(0, len(keyValue)):
                    insertObject(connection, None, None, key, keyValue[i])            

        connection.commit()
        log.debug("end object called")
            
    except Exception as e:
        log.error("Exception addObject:" + str(e) )
        connection.rollback()
        raise
    finally:
        mydb.close()
    log.info("AddObject  ended")
    return request

def update(cursor, table, record):
    updateExp = ""
    whereExp = ""
    for key in record:
        if key != "where":
            updateExp = addFieldValueToExpresion(updateExp, key, record[key],",")                                                  
        elif key == "where":
            where = record[key]
            for field in where:
                whereExp = addFieldValueToExpresion(whereExp, field, where[field]," and ")

    sql = "UPDATE " + table + " set " + updateExp + " WHERE " + whereExp
    log.debug("sql:" + sql)

    cursor.execute(sql)


def updateObject(request):
    log.info("UpdateObject called")
    try:
        mydb = MySql()
        connection = mydb.getConnection()
        cursor = connection.cursor()

        for table in request:
            value = request[table]
            if isinstance(value,list):
                for r in value:
                    update(cursor, table, r)
            else:
                update(cursor, table, value)
            
        connection.commit()
    except Exception as e:
        log.error("Exception addObject:" + str(e) )
        cursor.close()
        connection.rollback()
        raise
    finally:
        mydb.close()
    log.info("UpdateObject ended")
    return { "status":"OK"}

def deleteObject(request):
    log.info("DeleteObject called")
    try:
        
        mydb = MySql()
        connection = mydb.getConnection()
        cursor = connection.cursor()
        table = ""
        whereExp = ""
        for key in request:
            table = key
            record = request[table]
            for field in record:
                if whereExp != "":
                    whereExp = whereExp + "," 
                value = record[field]
                if isinstance(value,str):                    
                    whereExp = whereExp + field + "="+  "'" + value + "'"
                else:
                    whereExp = whereExp + field + "="+  str(value)

        if whereExp == "":
            raise DeleteWithEmptyWhereError("where can not be null in delete")
        sql = "DELETE FROM " + table + " WHERE " + whereExp
        log.debug("sql:" + sql)
        
        cursor.execute(sql)
        log.debug("delete completed")
        connection.commit()
    except Exception as e:
        log.error("Exception removeObject:" + str(e) )
        connection.rollback()
        raise
    finally:
        mydb.close()
    log.info("DeleteObject called")
    return { "status":"OK"}



def login(request):
    user_name = request["user"]["user_name"]
    password = request["user"]["password"]
    login_request = {
        "user":{
            "id":"",
            "user_name":user_name,
            "password":password
        }
    }
    login_result = getObject( login_request )
    if login_result == None or password != login_result["password"]:
        log.error("invalid login for %s", user_name)
        raise LoginError("invalid user_name or password")
    
    token = str(uuid.uuid4())
    t = datetime.datetime.now() + datetime.timedelta(days=1) 
    user_id = login_result["id"]

    token_request = {
        "credentials":{
            "token":token,
            "expirationDate": t.strftime("%Y/%m/%d %H:%M:%S"),
            "user_id":user_id
        }
    }

    addObject( token_request )
    result = getObject(request)

    result["token"] = token
    result["password"] = ""

    return result

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

    if( user.custom_claims ):
        user.custom_claims.pop(role, None)
        auth.set_custom_user_claims(user.uid, user.custom_claims) 
    
    return "Success"

def getClaims(request):

    log.debug("getClaims has been called")
    email = request["user"]["email"]
    user = auth.get_user_by_email(email)

    return user.custom_claims
    

def processRequest(req):
    service = req["service"]  #always cheneque
    database = req["database"]
    action = req["action"] # get put(insert else update) remove
    data = req["data"]

    log.debug("processRequest service:%s database:%s action:%s data:%s", service, database, action, data )

    if action == "get":
        validateToken( req ) 
        return getObject( data )
    elif action == "add":
        validateToken( req ) 
        return addObject( data )
    elif action == "update":
        validateToken( req ) 
        return updateObject( data )  
    elif action == "delete":
        validateToken( req ) 
        return deleteObject( data ) 
    elif action == "createUser":
        return addObject( data )         
    elif action == "deleteUser":
        return deleteObject( data )
    elif action == "addClaim":
        return addClaim( data )
    elif action == "removeClaim":
        return removeClaim( data )
    elif action == "getClaims":
        return getClaims( data )        


    elif action == "login":
        return login( data )   
                
    else:
        log.error("action not found %s", action)
        return("Action not found" + str(action) +" you probably want to use: get, add, update or remove")

if __name__ == "__main__":
    print("hello mysql_connect")