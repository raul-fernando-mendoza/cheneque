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


class TestFireStore(unittest.TestCase):
    
    def testAddSubCollection(self):

            req = {
                    'service': 'firestore', 
                    'database': 'not-used', 
                    'action': 'addSubCollection', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "employee": {
                                "id":"pMWEXP2tqY33OEhFX7bw",
                                "profiles":{
                                        "id":"RUJdrf1mDmKCiqzKb3aC",
                                        "details":{
                                                "place":"Mexico",
                                                "year":2019
                                        }
                                }
                            }
                        }
                    
            }
            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )

            self.assertIsNotNone( obj["id"] , "the record was not found" )

if __name__ == '__main__':
    unittest.main()