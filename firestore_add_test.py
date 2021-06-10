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
    """
    def testAddObject(self):
            req = {
                    'service': 'firestore', 
                    'database': 'exam', 
                    'action': 'add', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "materia": "Espada",
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

    def testAddUser(self):
            req = {
                    'service': 'firestore', 
                    'database': 'user', 
                    'action': 'add', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "name": "Catalina",
                            "role":["admin","readonly"],
                            "otro":[
                                { "elemento1":"value1"},
                                { "elemento2":"value2"}
                            ]
                        }
                    
            }
            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )
    """
    def testAddExam(self):
            req = {
                    'service': 'firestore', 
                    'database': 'user', 
                    'action': 'add', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "ExamType":{
                                "label":"Tecnica XIII",
                                "parameters":[
                                    {
                                        "label":"parameter 1",
                                        "criterias":[
                                            {
                                                "label":"criteria 1-1",
                                                "aspects":[
                                                    {
                                                        "label":"aspecto 1-1-1",
                                                        "idx":1
                                                    },
                                                    {
                                                        "label":"aspecto 1-1-2",
                                                        "idx":2
                                                    }   
                                                ]                                             
                                            }
                                        ]
                                    },
                                    {
                                        "label":"parameter 2",
                                        "criterias":[
                                            {
                                                "label":"criteria 2-1",
                                                "aspects":{
                                                    "label":"aspecto 2-1-1"
                                                }
                                            },
                                            {
                                                "label":"criteria 2-2",
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


if __name__ == '__main__':
    unittest.main()