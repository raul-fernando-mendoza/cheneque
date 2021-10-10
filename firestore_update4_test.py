import unittest
import json
import logging

import firebase_admin
import environments
firebase_admin.initialize_app()

import firestore_connect

log = logging.getLogger("cheneque")


class TestExamenObservations(unittest.TestCase):

    def testUpdateObject(self):
            req = {
                    'service': 'firestore', 
                    'database': 'not-used', 
                    'action': 'update', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "employee":{
                                "id":"ECOWU1wqv26TaoMYykZU",
                                "profiles":[
                                    {
                                        "id":"DpkLLHjjknNEKjkNWQz0",
                                        "years":1.2,
                                    },
                                    {
                                        "id":"TGiJbHmWRNlKGrOTeYsD",
                                        "years":2.2
                                    }
                                ]
                            }
                        }
            }
            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )

            self.assertIsNotNone( obj["id"] , "the record was not inserted" )




if __name__ == '__main__':
    unittest.main()