import unittest
import json
import logging
import firestore_connect

logging.basicConfig( level=logging.DEBUG)
logging.debug('test has started') 


class TestExamenObservations(unittest.TestCase):

    def testUpdateObject(self):
            req = {
                    'service': 'firestore', 
                    'database': 'exam', 
                    'action': 'update', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "id":"EkQ7Vf5UBZOLVepLFtvJ",
                            "completado": True,
                            "score":8.0
                        }
                    
            }
                    

            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )


if __name__ == '__main__':
    unittest.main()