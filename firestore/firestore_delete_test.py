import unittest
import json
import logging

import firebase_admin
firebase_admin.initialize_app( )

import firestore_connect

log = logging.getLogger("cheneque")

class TestExamenObservations(unittest.TestCase):

    def testDeleteObject(self):

            req = {
                    'service': 'firestore', 
                    'database': 'not-used', 
                    'action': 'get', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "employee":{
                                "id":None,
                                "name":"Raul",
                                "profiles":[{
                                    "id":None,
                                    "name":None
                                }]
                            }                                                    
                        },

            }

            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )

            reqFind = {
                    'service': 'firestore', 
                    'database': 'not-userd', 
                    'action': 'delete', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "employee": {
                                "id":obj["id"],
                                "profiles":{
                                    "id":obj["profiles"][0]["id"]
                                }
                            }
                        }
                    
            }
            obj2 = firestore_connect.processRequest(reqFind)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )
            self.assertEqual( obj2["id"] ,obj["profiles"][0]["id"] , "the record was not found" )

  

if __name__ == '__main__':
    unittest.main()