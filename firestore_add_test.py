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
                            "test_data": {
                                "description":"desc"
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
                            "test_data": {
                                "id":obj["id"],
                                "description":"desc"
                            }
                        }
                    
            }
            obj2 = firestore_connect.processRequest(req2)
            logging.debug( json.dumps(obj2,  indent=4, sort_keys=True) )
            self.assertEqual(obj2["description"],"desc")

            req3 = {
                    'service': 'firestore', 
                    'database': 'not-userd', 
                    'action': 'delete', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "test_data": {
                                "id":obj["id"]
                            }
                        }
                    
            }
            obj3 = firestore_connect.processRequest(req3)
            logging.debug( json.dumps(obj3,  indent=4, sort_keys=True) )
            self.assertEqual( obj3["id"] , obj["id"] , "the record was not removed" )

            req4 = {
                    'service': 'firestore', 
                    'database': 'not-userd', 
                    'action': 'get', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "test_data": {
                                "id":obj["id"]
                            }
                        }
                    
            }
            obj4 = firestore_connect.processRequest(req4)
            logging.debug( json.dumps(obj4,  indent=4, sort_keys=True) )
            self.assertIsNone( obj4 , "the record was not removed and is still there" )



if __name__ == '__main__':
    unittest.main()