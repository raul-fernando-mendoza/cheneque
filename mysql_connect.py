import sys
import datetime
import json
import logging
import mysql.connector
import decimal
import uuid

log = logging.getLogger("exam_app")

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class LoginError(Error):
    pass


class MySql:
    cnx = None

    def __init__(self):
        self.cnx = mysql.connector.connect(
        user="eApp",
        password="odroid",     
        host="localhost",
        
        database="entities"
        )
        log.debug(self.cnx)         

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
    def __init__(self,parentTableName, tableName, filter):
        log.debug( "new Table(%s,%s)", str(parentTableName) , str(tableName) ), 
        self.parentTableName = parentTableName
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
                    if where != "": 
                        where = where + " and "
                    if isinstance(value,str):
                        where = where + " " + self.tableName + "." + key + " = '" + str(value) + "'"
                    else:
                        where = where + " " + self.tableName + "." + key +  " = " + str(value) 
                
        return where

    def createObjectFromRow( self, row ):
        obj = {}
        for key in self.tableFilter.keys():
            value = self.tableFilter[key]
            if not isinstance(value,dict) and not isinstance(value,list):
                rowValue = row[self.tableName + "." + key]
                log.debug("createObjectFromRow key %s is a %s" , key, type(rowValue))
                if isinstance(rowValue , datetime.datetime):
                    obj[key] = rowValue.strftime("%Y/%m/%d %H:%M:%S")
                elif isinstance(rowValue , datetime.date):
                    obj[key] = rowValue.strftime("%Y/%m/%d") 
                elif isinstance(rowValue, decimal.Decimal ):
                    obj[key] = float( rowValue )                    
                else:
                    obj[key] = rowValue
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
                    self.createTableList( key, t.tableFilter )
        except Exception as e:
            log.error("Exception: createTableList" + str(e))
            raise

    def getTableByName(self,tableName):
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
                    #ensure there is a lastObject
                
                    if key not in obj:
                        log.debug("object %s is null creating new", key) 
                        if t.isList:
                            log.debug("objet %s is array creating new", key)
                            obj[key] = [] 
                            obj[key].append( newObj )                           
                        else:
                            log.debug("object %s is object creating new", key)
                            obj[key] = newObj
                        lastObject = newObj
                    else:
                        if t.isList:
                            log.debug("object %s was not null and array retring last", key)        
                            lastObject = obj[key][-1]
                        else:
                            log.debug("object %s was not null and object retrivig last")
                            lastObject = obj[key] 
                    #compare the new row to the previous one and if false then there should be a new row
                    log.debug("compare vs last Object")
                    if t.compareObjToRow( lastObject, objRow) == False:
                        log.debug("new row is different from last adding row")
                        obj[key].append( newObj )
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
            column_names = cursor.column_names 
            
            for row in cursor:
                objRow = dict(zip(column_names,row))
               
                #log.debug( json.dumps(obj,  indent=4, sort_keys=True) )
                for i in range(0,len(column_names)):
                    log.debug("%s:%s", column_names[i], objRow[column_names[i]] )

                
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
    try:
        q = Qry()
        log.debug("len( q.tables ):%i", len( q.tables ) )
        obj = q.executeQry( request )
        return obj
    except Exception as e:
        log.error("getObject error:" + str(e) )
        raise

def insertObject(connection, parent_id_field, parent_id, table, request):
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

        if( valuesExp != ""):
            valuesExp = valuesExp + ","
        

        value = request[key]
        if value == None:
            valuesExp = valuesExp + "null"
        elif isinstance(value, bool):
            if value == True:
                valuesExp = valuesExp + "1"
            else:
                valuesExp = valuesExp + "0"
        elif isinstance(value,str):                    
            valuesExp = valuesExp + "'" + value + "'"
        elif isinstance(value , datetime.datetime):
            valuesExp = valuesExp + "'" + value.strftime("%Y-%m-%d %H:%M:%S") + "'"
        elif isinstance(value , datetime.date):
            valuesExp = valuesExp + "'" + value.strftime("%Y-%m-%d")+ "'"             
        else:
            valuesExp = valuesExp + str(value)
                     
    sql = "INSERT INTO " + table + "(" + fieldsExp + ") values(" + valuesExp + ")"
    log.debug("sql:" + sql)
        
    cursor.execute(sql)

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


    

def addObject(request):
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
            
    except Exception as e:
        log.error("Exception addObject:" + str(e) )
        connection.rollback()
        raise
    finally:
        mydb.close()
    return request


def updateObject(request):

    try:
        mydb = MySql()
        connection = mydb.getConnection()
        cursor = connection.cursor()
        rowid = None        
        database = ""
        updateExp = ""
        whereExp = ""
        for key in request:
            if key != "where":
                database = key
                record = request[database]
                for field in record:
                    if updateExp != "":
                        updateExp = updateExp + "," 
                    value = record[field]
                    if isinstance(value,str):                    
                        updateExp = updateExp + field + "="+  "'" + value + "'"
                    else:
                        updateExp = updateExp + field + "="+  str(value)
        record = request["where"]
        for field in record:
            if whereExp != "":
                whereExp = whereExp + "," 
            value = record[field]
            if isinstance(value,str):                    
                whereExp = whereExp + field + "="+  "'" + value + "'"
            elif isinstance(value, bool):
                if value == True:
                    valuesExp = valuesExp + "1"
                else:
                    valuesExp = valuesExp + "0"
            elif isinstance(value,str):                    
                valuesExp = valuesExp + "'" + value + "'"
            elif isinstance(value , datetime.datetime):
                valuesExp = valuesExp + "'" + value.strftime("%Y-%m-%d %H:%M:%S") + "'"
            elif isinstance(value , datetime.date):
                valuesExp = valuesExp + "'" + value.strftime("%Y-%m-%d")+ "'"                   
            else:
                whereExp = whereExp + field + "="+  str(value)

        sql = "UPDATE " + database + " set " + updateExp + " WHERE " + whereExp
        log.debug("sql:" + sql)
        
        cursor.execute(sql)
        connection.commit()
    except Exception as e:
        log.error("Exception addObject:" + str(e) )
        cursor.close()
        connection.rollback()
        raise
    finally:
        mydb.close()
    return { "status":"OK"}

def login(request):
    user_name = request["user_name"]
    password = request["password"]
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

    request_user = {
        "user":{
            "id":user_id,
            "user_name":"",
            "user_role":[{
               "role_id":"" 
            }],
            "user_attribute":[{
                "attribute_name":"",
                "attribute_value":""
            }]
        }
    }
    result = getObject(request_user)

    result["token"] = token

    return result

def validateToken(request):
    token = request["token"]  

    token_request = {
        "credentials":{
            "token":token,
            "expirationDate":"",
            "user_id":""
        }
    } 

    result = getObject( token_request ) 
    if result == None :
        log.error("Token not found %s", token)
        raise LoginError("Token not found")

    t = datetime.datetime.now()
    e = datetime.datetime.strptime(result["expirationDate"], "%Y/%m/%d %H:%M:%S")
    if t > e:
        log.error("Token expired %s %s %s", token, t.strftime("%Y/%m/%d %H:%M:%S"), e.strftime("%Y/%m/%d %H:%M:%S"))
        raise LoginError("Token Expired")

    request_user = {
        "user":{
            "id":result["user_id"],
            "user_name":"",
            "user_role":[{
               "role_id":"" 
            }],
            "user_attribute":[{
                "attribute_name":"",
                "attribute_value":""
            }]
        }
    }
    result = getObject(request_user)

    result["token"] = token

    return result



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
        validateToken( data ) 
        return addObject( data )
    elif action == "update":
        validateToken( data ) 
        return updateObject( data )  
    elif action == "login":
        return login( data )   
                
    else:
        log.error("action not found %s", action)
        raise Exception("Action " + str(action) +" you probably want to use: get, add, update or remove")

if __name__ == "__main__":
    print("hello mysql_connect")