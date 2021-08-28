import unittest
import json
import logging

import firebase_admin
from firebase_admin import credentials
import environments
firebase_admin.initialize_app(environments.config["cred"] )

import firestore_connect

log = logging.getLogger("cheneque")


class TestFireStore(unittest.TestCase):

    def test01_addDocument(self):
            req = {
                    'service': 'firestore', 
                    'database': 'not-used', 
                    'action': 'add', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "employee":{
                                "name":"Raul",
                                "salary":1000,
                                "profiles":[
                                    {
                                        "name":"programmer",
                                        "years":8,
                                        "projects":[
                                            {
                                                "name":"BookSystem",
                                                "year":1998
                                            },
                                            {
                                                "name":"DefectsSystem",
                                                "year":1999
                                            },
                                            {
                                                "name":"InvoiceSystem",
                                                "year":2000
                                            }
                                        ]
                                    },
                                    {
                                        "name":"tester",
                                        "years":2,
                                        "projects":[
                                            {
                                                "name":"BookSystemTest",
                                                "year":1998
                                            },
                                            {
                                                "name":"DefectsSystemTest",
                                                "year":1999
                                            },
                                            {
                                                "name":"InvoiceSystemTest",
                                                "year":2000
                                            }
                                        ]

                                    }
                                ]
                            }
                        }
            }
            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )

            self.assertIsNotNone( obj["id"] , "the record was not inserted" )

            req2 = {
                    'service': 'firestore', 
                    'database': 'not-userd', 
                    'action': 'get', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "employee": {
                                "id":obj["id"],
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
            obj2 = firestore_connect.processRequest(req2)
            logging.debug( json.dumps(obj2,  indent=4, sort_keys=True) )
            self.assertEqual(obj2["name"],"Raul")




if __name__ == '__main__':
    unittest.main()