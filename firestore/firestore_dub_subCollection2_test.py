import unittest
import json
import logging

import firebase_admin
from firebase_admin import credentials
firebase_admin.initialize_app()

import firestore_connect

log = logging.getLogger("exam_app")


class TestExamen(unittest.TestCase):
    
    def testDupSubCollection(self):
            req = {
                'service': 'firestore', 
                'database': 'notused', 
                'action': 'dupSubCollection', 
                'token': 'a3jbbKjmLHzkxmvNKJPt', 
                'data':{
                        "materias":{
                                "id":'77b9d6a5-7c20-4f9d-b266-fe72945bba97',
                                "exams":
                                {
                                        "id":'f2621a0a-afb7-4258-8c41-bb5994c88967',
                                        "label":"test_geometria_copy" + "_copy"
                                }
                        
                        }
                }                                                                          
            }

            obj = firestore_connect.processRequest(req)
            log.debug( json.dumps(obj,  indent=4, sort_keys=True) )


if __name__ == '__main__':
    unittest.main()