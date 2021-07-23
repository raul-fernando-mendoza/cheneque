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
<<<<<<< HEAD
    """
    def testAddObject(self):
            req = {
                    'service': 'firestore', 
                    'database': 'exam', 
                    'action': 'add', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "test_data": "Espada",
                            "title":"uno mas",
                            "student":{
                                "uid":"YMPmHz85tcNpOqvUwCdZlciDVRs2",
                                "displayName":"Jimena Hernandez",
                                "email":"pedro.torres@hotmail.com"
                            },
                            "teacher":{
                                "uid":"YMPmHz85tcNpOqvUwCdZlciDVRs1",
                                "displayName":"Claudia Gamboa",
                                "email":"claudia.gamboa@hotmail.com"
                            },
                            "test":{
                                "id":"TecnicaII",
                                "label":"Tecnica III"
                            },
                            "parameter":{
                                "id":"ejercicio_1",
                                "label":"ejercicio 1"
                            },
                            "applicationDate": "2021-03-27",
                            "completado": False,
                            "score":10.0
                        }
                    
            }
                    

            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )
    """
    def testAddUser(self):
=======

    def test01_addDocument(self):
>>>>>>> de09ebfeb47ca2d54fa500ff44f04723edddf813
            req = {
                    'service': 'firestore', 
                    'database': 'not-userd', 
                    'action': 'add', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
<<<<<<< HEAD
                            "test_data": {
                                "id":"one",
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
                    'action': 'delete', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "test_data": {
                                "id":obj["id"]
                            }
                        }
                    
=======
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
>>>>>>> de09ebfeb47ca2d54fa500ff44f04723edddf813
            }
            obj2 = firestore_connect.processRequest(req2)
            logging.debug( json.dumps(obj2,  indent=4, sort_keys=True) )

            req2 = {
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
            obj2 = firestore_connect.processRequest(req2)
            logging.debug( json.dumps(obj2,  indent=4, sort_keys=True) )
            self.assertIsNone( obj , "the record was not removed" )

            #self.assertTrue(obj["id"] == "test1")           



if __name__ == '__main__':
    unittest.main()