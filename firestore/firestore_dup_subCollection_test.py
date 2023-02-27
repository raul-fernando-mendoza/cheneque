import unittest
import json
import logging

import firebase_admin
from firebase_admin import credentials
firebase_admin.initialize_app()

import firestore_connect

log = logging.getLogger("exam_app")


class TestExamen(unittest.TestCase):
    
    def testDupSubCollection1(self):

            req = {
                    'service': 'firestore', 
                    'database': 'not-used', 
                    'action': 'get', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "employee":{
                                "id":None,
                                "name":"Raul",
                                "profiles":{
                                        "id":None,
                                        "name":"programmer"
                                }
                            }                                                    
                        },

            }

            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )


            req = {
                    'service': 'firestore', 
                    'database': 'notused', 
                    'action': 'dupSubCollection', 
                    'token': 'a3jbbKjmLHzkxmvNKJPt', 
                    'data':{
                            "employee":{
                                "id":obj["id"],
                                "profiles":{
                                        "id":obj["profiles"]["id"],
                                        "name":"otro mas"
                                }
                            }                                
                    },
                    "options":{
                        "exceptions":["years"]
                    }    
                       

            }

            obj = firestore_connect.processRequest(req)
            log.debug( json.dumps(obj,  indent=4, sort_keys=True) )

if __name__ == '__main__':
    unittest.main()