import unittest
import json
import logging
import firestore_connect

logging.basicConfig( level=logging.DEBUG)
logging.debug('test has started') 


class TestFireStore(unittest.TestCase):
    """
    def testArrayUnion(self):
            req = {
                    'service': 'firestore', 
                    'database': 'user', 
                    'action': 'ArrayUnion', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "id":"JpxtnUw60uh08WA98KxK",
                            "role":["student"]
                        }
                    
            }
            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )
    
    def testArrayRemove(self):
            req = {
                    'service': 'firestore', 
                    'database': 'user', 
                    'action': 'ArrayRemove', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "id":"JpxtnUw60uh08WA98KxK",
                            "role":["student"]
                        }
                    
            }
                    

            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )
    """
    def testArrayUnion(self):
            req = {
                    'service': 'firestore', 
                    'database': 'user', 
                    'action': 'ArrayRemove', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "id":"JpxtnUw60uh08WA98KxK",
                            "otro":[
                                {"elemento1":"value1"}
                            ]
                        }
                    
            }
            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )    


if __name__ == '__main__':
    unittest.main()