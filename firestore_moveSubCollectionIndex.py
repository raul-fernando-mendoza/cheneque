import unittest
import json
import logging
import firebase_admin
from firebase_admin import credentials
cred = credentials.Certificate('celtic-bivouac-307316-firebase-adminsdk-pbsww-2ccfde6abd.json')
firebase_admin.initialize_app(cred)
import firestore_connect

logging.basicConfig( level=logging.DEBUG)
logging.debug('test has started') 


class TestMoveSubCollectionIndex(unittest.TestCase):
    
    def testMoveSubCollectionIndex(self):
            req = {
                    'service': 'firestore', 
                    'database': 'notused', 
                    'action': 'moveSubCollectionIndex', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                        "parameters":{
                            "id":"2e3e897d223d4972a387dc0415752e87",
                            "criterias":{
                                "id":"segundo",
                                "idx":2
                            }
                        }                       
                    }
            }
                    

            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )

if __name__ == '__main__':
    unittest.main()