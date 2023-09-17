import unittest
import json
import logging

import firebase_admin
#takes the connection from the environment variable FIREBASE_CONFIG make sure is development
firebase_admin.initialize_app( )
import firestore_connect 

logging.basicConfig( level=logging.DEBUG)
logging.debug('test has started') 


class TestExamen(unittest.TestCase):
    
    def testNewVersionObject(self):
            req = {
                    'service': 'firestore', 
                    'database': 'not-used', 
                    'action': 'createDocumentNewVersion', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                        "collectionPath":"examGrades/3d280a4e-3cae-4a99-a362-426f1c27707b/parameterGrades",
                        "id":"17676553-8c63-4d97-af96-91d2b7793d06_1",
                        "versionKey":"version",
                        "isCurrentVersionKey":"isCurrentVersion",
                        "updateOnKey":"updated_on",
                        "newValues":{
                             "isCompleted":False
                        },                        
                        "options":{}
                                          
                    }
            }

            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True, default=str) )

if __name__ == '__main__':
    unittest.main()