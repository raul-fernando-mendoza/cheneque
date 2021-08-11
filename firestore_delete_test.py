import unittest
import json
import logging
import firebase_admin
from firebase_admin import credentials
cred = credentials.Certificate('credentials.json')
firebase_admin.initialize_app(cred)
import firestore_connect

logging.basicConfig( level=logging.DEBUG)
logging.debug('test has started') 


class TestExamenObservations(unittest.TestCase):

    def testDeleteAspect(self):

            reqFind = {
                    'service': 'firestore', 
                    'database': 'not-userd', 
                    'action': 'get', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "test": {
                                "id":None,
                                "desc":"description"
                            }
                        }
                    
            }
            obj = firestore_connect.processRequest(reqFind)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )
            self.assertEqual( obj["desc"] ,"description" , "the record was not found" )


            reqDelete = {
                    'service': 'firestore', 
                    'database': 'not-userd', 
                    'action': 'delete', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "test": {
                                "id":obj["id"]
                            }
                        }
                    
            }
            objDeleted = firestore_connect.processRequest(reqDelete)
            logging.debug( json.dumps(objDeleted,  indent=4, sort_keys=True) )
            self.assertEqual( objDeleted["id"] ,obj["id"] , "the record was not found" )



            reqGet = {
                    'service': 'firestore', 
                    'database': 'not-userd', 
                    'action': 'get', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "test": {
                                "id":objDeleted["id"],
                            }
                        }
                    
            }
            objNotFound = firestore_connect.processRequest(reqGet)
            logging.debug( json.dumps(objNotFound,  indent=4, sort_keys=True) )
            self.assertIsNone( objNotFound , "the record was not removed and is still there" )
  

if __name__ == '__main__':
    unittest.main()