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
    """
    def testGetDocument(self):
            req = {
                    'service': 'firestore', 
                    'database': 'exams', 
                    'action': 'get', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "exams":{
                                "id":"test1",
                                "label":None,
                                "parameters":[
                                    {
                                        "id":None,
                                        "idx":None,
                                        "label":None,
                                        "criterias":[
                                            {
                                                "id":None,
                                                "idx":None,
                                                "label":None,
                                                "aspects":[
                                                    {
                                                    "id":None,
                                                    "idx":None,
                                                    "label":None
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ],
                            },   
                            "orderBy":{
                                "label":"asc"
                            }                                                     
                        },

            }
                    

            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )
    """
    def testAddObject(self):
            req = {'service': 'firestore', 
            'database': 'notused', 
            'action': 'get', 
            'token': 'not used', 
            'data': {
                'test_data': 
                    {
                        'id': 'test1', 
                        'label': None, 
                        'description': None, 
                    }
                }
            }
            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )   

            self.assertIsNotNone(obj)
            self.assertEqual( obj["id"], "test1")
            self.assertEqual( obj["label"], "label1") 
            self.assertEqual( obj["description"], "description1") 
    

if __name__ == '__main__':
    unittest.main()