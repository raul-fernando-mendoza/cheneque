import unittest
import json
import logging

import firebase_admin
import environments
firebase_admin.initialize_app(environments.config["cred"] )

import firestore_connect

log = logging.getLogger("cheneque")


class TestExamenObservations(unittest.TestCase):

    def testGetObject(self):
            req = {'service': 'firestore', 
            'database': 'notused', 
            'action': 'get', 
            'token': 'not used', 
            'data': {
                        "employee": {
                            "id":"cXwCNUiSnbehBwRjjgX4",
                            "name":None,
                            "profiles":[
                                {
                                    "name":None,
                                    "years":None
                                }
                            ]
                        }
                    }
            }
            obj = firestore_connect.processRequest(req)
            log.debug( json.dumps(obj,  indent=4, sort_keys=True) )   

            self.assertIsNotNone(obj)
            self.assertEqual( obj["id"], "cXwCNUiSnbehBwRjjgX4")
            self.assertEqual( obj["name"], "Raul") 
    

if __name__ == '__main__':
    unittest.main()