import unittest
import json
import logging

import firebase_admin
firebase_admin.initialize_app( )

import firestore_connect

log = logging.getLogger("cheneque")

class TestDeleteCollection(unittest.TestCase):

    def testDeleteCollectionObject(self):

            req = {
                    'service': 'firestore', 
                    'database': 'not-used', 
                    'action': 'deleteCollectionObject', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "collection":"employee/123/jobs",
                            "id":"abc"                                        
                        },

            }

            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )

if __name__ == '__main__':
    unittest.main()