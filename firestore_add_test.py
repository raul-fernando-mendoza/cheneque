import unittest
import json
import logging
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
    """
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


if __name__ == '__main__':
    unittest.main()