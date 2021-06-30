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


class TestFireStore(unittest.TestCase):

    def test01_addDocument(self):
            req = {
                    'service': 'firestore', 
                    'database': 'user', 
                    'action': 'add', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "exams":{
                                "label":"Test1",
                                "parameters":[
                                    {
                                        "idx":1,
                                        "label":"parameter 1",
                                        "criterias":[
                                            {
                                                "idx":1,
                                                "label":"criteria 1-2",
                                                "initiallySelected":True,
                                                "aspects":[
                                                    {
                                                        "idx":1,
                                                        "label":"aspecto 1-2-1",
                                                    },
                                                    {
                                                        "idx":0,
                                                        "label":"aspecto 1-2-2",
                                                    }   
                                                ]                                             
                                            },
                                            {
                                                "idx":0,
                                                "label":"criteria 1-1",
                                                "initiallySelected":True,
                                                "aspects":[
                                                    {
                                                        "idx":1,
                                                        "label":"aspecto 1-1-2",
                                                    },
                                                    {
                                                        "idx":0,
                                                        "label":"aspecto 1-1-1",
                                                    }   
                                                ]                                             
                                            }                                            
                                        ]
                                    },
                                    {
                                        "idx":0,
                                        "label":"parameter 2",
                                        "criterias":[
                                            {
                                                "label":"criteria 2-1",
                                                "initiallySelected":True,
                                                "aspects":{
                                                    "label":"aspecto 2-1-1"
                                                }
                                            },
                                            {
                                                "label":"criteria 2-2",
                                                "initiallySelected":True,
                                                "aspects":{
                                                    "label":"aspecto 2-2-1"
                                                }
                                            }                                            
                                        ]
                                    }                                    
                                ]
                            } 
                    }
            }
            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )

            #self.assertTrue(obj["id"] == "test1")           



if __name__ == '__main__':
    unittest.main()