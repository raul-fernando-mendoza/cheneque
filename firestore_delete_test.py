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


class TestExamenObservations(unittest.TestCase):

    def testDeleteAspect(self):
            req = {
                    'service': 'firestore', 
                    'database': 'exam', 
                    'action': 'delete', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                        "aspect":[
                            {
                            "id":"8TsBYXcOmlHNMX6lrp6M",
                            "idx":1,
                            "score":6.3
                            },
                            {
                            "id":"CrnaIf5lC9cI0ZQJaUgf",
                            "idx":2,
                            "score":9.4
                            }
                        ]                       
                    }
                    
            }
                    

            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )

    def testDeleteAspect(self):
            req = {
                    'service': 'firestore', 
                    'database': 'exam', 
                    'action': 'delete', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                        "examGrades":
                            {
                            "id":"HCtewHljsFhWaulgKd5i",
                            }
                                               
                    }
                    
            }
                    

            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )    

if __name__ == '__main__':
    unittest.main()