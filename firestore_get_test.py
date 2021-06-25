import unittest
import json
import logging

import firebase_admin
from firebase_admin import credentials
cred = credentials.Certificate('celtic-bivouac-307316-firebase-adminsdk-pbsww-2ccfde6abd.json')
firebase_admin.initialize_app(cred)
import firestore_connect

logging.basicConfig( level=logging.DEBUG)
logging.debug('test has started') 


class TestExamenObservations(unittest.TestCase):
    """
    def testGetDocument(self):
            req = {
                    'service': 'firestore', 
                    'database': 'exams', 
                    'action': 'get', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "exams":{
                                "id":"test1",
                                "label":None,
                                "parameters":[
                                    {
                                        "id":None,
                                        "idx":None,
                                        "label":None,
                                        "criterias":[
                                            {
                                                "id":None,
                                                "idx":None,
                                                "label":None,
                                                "aspects":[
                                                    {
                                                    "id":None,
                                                    "idx":None,
                                                    "label":None
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ],
                            },   
                            "orderBy":{
                                "label":"asc"
                            }                                                     
                        },

            }
                    

            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )
    """
    def testAddObject(self):

        req = {'service': 'firestore', 'database': 'notused', 'action': 'get', 'token': 'eyJhbGciOiJSUzI1NiIsImtpZCI6Ijg4ZGYxMzgwM2I3NDM2NjExYWQ0ODE0NmE4ZGExYjA3MTg2ZmQxZTkiLCJ0eXAiOiJKV1QifQ.eyJhZG1pbiI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2NlbHRpYy1iaXZvdWFjLTMwNzMxNiIsImF1ZCI6ImNlbHRpYy1iaXZvdWFjLTMwNzMxNiIsImF1dGhfdGltZSI6MTYyNDQ3MDk5NiwidXNlcl9pZCI6IlIxbE8wSGRPRnBjWDFadXIyTlRGdzAzdkxlWTIiLCJzdWIiOiJSMWxPMEhkT0ZwY1gxWnVyMk5URncwM3ZMZVkyIiwiaWF0IjoxNjI0NTYzOTI3LCJleHAiOjE2MjQ1Njc1MjcsImVtYWlsIjoicmF1bF9mZXJuYW5kb19tZW5kb3phQGhvdG1haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsicmF1bF9mZXJuYW5kb19tZW5kb3phQGhvdG1haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.DPm9-8smHnjTuAsV5I5kaJFswY4A8SwEDf3e8K7xtXUsUk6rLP2cUBIUqXHFbGwldXg3qvz3ZF_hIA2xXCDR3hk7B43WxGfDVyYycJOAGEXWIzusyG5tnTL6nx7AO8Utvf0RfYBHYWJFIFC5SsC0Bu5r-TFSUR1F7WE2kGd7Xxgw45ENDJQOAoDM2eaRRnroyF58dLCx4r6qCU84POcIA9RS2NELWUeuJI5q0ORSzmnSGhjUZjcUe_ka17uSWg4lNh391rwIg_LydwgHuZvxYOKDxzZKnYMllCekIxCPPvIXWLo-eLEsNwK8KzvzUro59HWzJh_90f3aQMMsKE0zzw', 'data': {'examGrades': [{'id': None, 'exam_id': None, 'exam_label': None, 'course': None, 'completed': None, 'applicationDate': None, 'student_uid': None, 'student_name': None, 'title': None, 'expression': None, 'score': None, 'parameterGrades': [{'id': None, 'idx': None, 'label': None, 'scoreType': None, 'score': None, 'evaluator_uid': None, 'evaluator_name': None, 'completed': None}]}], 'orderBy': {'applicationDate': 'asc', 'id': 'asc'}}}
                

        obj = firestore_connect.processRequest(req)
        logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )    
       

if __name__ == '__main__':
    unittest.main()