import unittest
import json
import logging

import firebase_admin
import environments
firebase_admin.initialize_app()

import firestore_connect

logging.basicConfig( level=logging.DEBUG)
logging.debug('test has started') 


class TestFireStore(unittest.TestCase):
    
    def testAddSubCollection(self):

            req = {
                    'service': 'firestore', 
                    'database': 'not-used', 
                    'action': 'get', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "employee": {
                                "id":None,
                                "name":"Raul",
                                "profiles":{
                                        "id":None,
                                        "name":"tester",
                                        "projects":{
                                                "id":"None",
                                                "name":"InvoiceSystemTest"
                                        }
                                }
                            }
                        }
                    
            }
            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )



            req = {
                    'service': 'firestore', 
                    'database': 'not-used', 
                    'action': 'addSubCollection', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "employee": {
                                "id":obj["id"],
                                "profiles":{
                                        "id":obj["profiles"]["id"],
                                        "projects":{     
                                                "id":None,                                           
                                                "name":"npmProject",
                                                "year":2019
                                        }
                                }
                            }
                        }
                    
            }
            obj2 = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )

            self.assertIsNotNone( obj2["id"] , "the record was not found" )

if __name__ == '__main__':
    unittest.main()