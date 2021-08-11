import unittest
import json
import logging

import firebase_admin
from firebase_admin import credentials
import environments

firebase_admin.initialize_app(environments.config["cred"])
import firestore_connect

logging.basicConfig( level=logging.DEBUG)
logging.debug('test has started') 


class TestExamen(unittest.TestCase):
    
    def testCopyObject(self):
            req = {
                    'service': 'firestore', 
                    'database': 'not-used', 
                    'action': 'get', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "test":{
                                "id":None,
                                "desc":"description"
                            }                                                    
                        },

            }

            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )


            req = {
                    'service': 'firestore', 
                    'database': 'not used', 
                    'action': 'dupDocument', 
                    'token': 'a3jbbKjmLHzkxmvNKJPt', 
                    'data':{
                            "test":{
                                "id":obj["id"]
                            }                                                    
                        },

            }

            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )

if __name__ == '__main__':
    unittest.main()