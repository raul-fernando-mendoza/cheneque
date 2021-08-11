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


class TestFireStore(unittest.TestCase):

    def test01_addDocument(self):
            req = {
                    'service': 'firestore', 
                    'database': 'not-used', 
                    'action': 'add', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "test":{
                                "desc":"description",
                                "subtest":{
                                    "desc":"subdescription",
                                    "subsubtest":{
                                        "desc":"subsubdescription"
                                    }
                                }
                            }
                        }
                    
            }
            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )

            self.assertIsNotNone( obj["id"] , "the record was not inserted" )

            req2 = {
                    'service': 'firestore', 
                    'database': 'not-userd', 
                    'action': 'get', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "test": {
                                "id":obj["id"],
                                "desc":None,
                                "subtest":{
                                    "desc":None
                                }
                            }
                        }
                    
            }
            obj2 = firestore_connect.processRequest(req2)
            logging.debug( json.dumps(obj2,  indent=4, sort_keys=True) )
            self.assertEqual(obj2["desc"],"description")




if __name__ == '__main__':
    unittest.main()