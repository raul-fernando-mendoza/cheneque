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


class TestExamen(unittest.TestCase):
    
    def testDupSubCollection(self):
            req = {
                    'service': 'firestore', 
                    'database': 'notused', 
                    'action': 'dupSubCollection', 
                    'token': 'a3jbbKjmLHzkxmvNKJPt', 
                    'data':{
                            "parameters":{
                                "id":"Rudyh2AmUORtBBX65NqR"
                            }                                
                    }                                                                        
                       

            }

            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )
    

if __name__ == '__main__':
    unittest.main()