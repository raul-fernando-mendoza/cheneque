import unittest
import json
import logging
import firebase_admin
from firebase_admin import credentials
import environments
firebase_admin.initialize_app(environments.config["cred"] )

import firestore_connect

logging.basicConfig( level=logging.DEBUG)
logging.debug('test has started') 


class TestMoveSubCollectionIndex(unittest.TestCase):
    
    def testMoveSubCollectionIndex(self):
            req = {
                    'service': 'firestore', 
                    'database': 'not-used', 
                    'action': 'get', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "employee":{
                                "id":None,
                                "name":"Raul",
                                "profiles":{
                                    "id":None,
                                    "name":"programmer",
                                    "projects":{
                                        "id":None,
                                        "name":"InvoiceSystem"
                                    }
                                }
                            }                                                    
                        },
            }

            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )

            req2 = {
                    'service': 'firestore', 
                    'database': 'not-used', 
                    'action': 'moveSubCollectionIndex', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "employee":{
                                "id":obj["id"],
                                "profiles":{
                                    "id":obj["profiles"]["id"],
                                    "projects":{
                                        "id":obj["profiles"]["projects"]["id"],
                                        "idx":0
                                    }
                                }
                            }                                                    
                        },
            }

            obj2 = firestore_connect.processRequest(req2)
            logging.debug( json.dumps(obj2,  indent=4, sort_keys=True) )            
if __name__ == '__main__':
    unittest.main()