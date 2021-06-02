import unittest
import json
import logging
import firestore_connect

logging.basicConfig( level=logging.DEBUG)
logging.debug('test has started') 


class TestExamenObservations(unittest.TestCase):

    def testAddObject(self):
            req = {
                    'service': 'firestore', 
                    'database': 'exam', 
                    'action': 'get', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "completado": False,
                            "applicationDate":"2021-03-27",
                            "orderby":{
                                "materia":"asc"
                            }                            
                        },

            }
                    

            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )


if __name__ == '__main__':
    unittest.main()