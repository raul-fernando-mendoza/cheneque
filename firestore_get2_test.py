import unittest
import json
import logging

import firebase_admin
import environments
firebase_admin.initialize_app(environments.config["cred"] )

import firestore_connect

from datetime import date

log = logging.getLogger("cheneque")


class TestExamenObservations(unittest.TestCase):

    def testGetObject(self):

            d = date.fromisoformat("2021-12-01")
            req = {
                'service': 'firestore', 
                'database': 'notused', 
                'action': 'get', 
                'token': 'not used', 
                'data': {

                    "examGrades":[
                        {
                        "id":None,
                        "exam_id":None,
                        "exam_label":None,

                        "course": None,
                        "completed": None,
                        "applicationDate":None,
                    
                        "student_uid":None,
                        "student_name":None,
                    
                        "title":None,
                        "expression":None,

                        "score":None,
                        "certificate_url":None,
                    
                        "parameterGrades":[
                            {
                                "id": None,
                                "idx": None,
                                "label": None,
                                "scoreType": None,
                                "score":None,
                                "evaluator_uid":None,
                                "evaluator_name":None,
                            
                                "completed":None
                            
                            }
                        ]
                        }
                    ]
                    ,
                    "orderBy": {
                    "applicationDate": "asc",
                    "id": "asc"
                    }
                }
            }
            obj = firestore_connect.processRequest(req)
            log.debug( json.dumps(obj,  indent=4, sort_keys=True) )   

            self.assertIsNotNone(obj)

    

if __name__ == '__main__':
    unittest.main()