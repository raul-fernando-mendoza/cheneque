import unittest
import json
import logging

import firebase_admin
firebase_admin.initialize_app()

import auth_connect

logging.basicConfig( level=logging.DEBUG)
logging.debug("test has started") 


class TestExamenObservations(unittest.TestCase):

    def testGetList(self):
            req = {
                    "service": "auth", 
                    "action": "getUser", 
                    "data":{
                        "uid":"uZP1VwpZJCg8zjMrnHNwh7s2Q3e2"
                    }
            }
                    

            obj = auth_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )


if __name__ == "__main__":
    unittest.main()