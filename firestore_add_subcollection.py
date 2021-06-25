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


class TestFireStore(unittest.TestCase):
    
    def testAddSubCollection(self):
            req = {
                    'service': 'firestore', 
                    'database': 'user', 
                    'action': 'addSubCollection', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "criterias":{
                                "id":"A0b0TUX3OBbVJqnk9apJ",
                                "aspects":{
                                        "label":"2-1-2",
                                }
                            } 
                    }
            }
            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )
    """
    def testAddExamParameter(self):
            req = {'service': 'firestore', 'database': 'notused', 'action': 'addSubCollection', 'token': 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImFiMGNiMTk5Zjg3MGYyOGUyOTg5YWI0ODFjYzJlNDdlMGUyY2MxOWQiLCJ0eXAiOiJKV1QifQ.eyJhZG1pbiI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2NlbHRpYy1iaXZvdWFjLTMwNzMxNiIsImF1ZCI6ImNlbHRpYy1iaXZvdWFjLTMwNzMxNiIsImF1dGhfdGltZSI6MTYyMjY1MTU1MCwidXNlcl9pZCI6IlIxbE8wSGRPRnBjWDFadXIyTlRGdzAzdkxlWTIiLCJzdWIiOiJSMWxPMEhkT0ZwY1gxWnVyMk5URncwM3ZMZVkyIiwiaWF0IjoxNjIzMDAwODMyLCJleHAiOjE2MjMwMDQ0MzIsImVtYWlsIjoicmF1bF9mZXJuYW5kb19tZW5kb3phQGhvdG1haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsicmF1bF9mZXJuYW5kb19tZW5kb3phQGhvdG1haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.qMarIyriyCopiViNbUQaxZNdN4T0NiBr_eim_P0AtgKoqeTpCWinZ4vgfvVUVUarxh8O7TiVzFI2E9kfIyK6JJv8DFLQIag8zsbU8PDo3ojc6eBEh6ADVltnYDsQM6QEBYk6uZpAp57sBy6UayB9yZjb7j2nf_0K54hey_jwhn5wNrkofADYCDSmsWRWsBaDk9TYVsShkL5Ktpt-RT_8XcjWjAQdLmW6MKjodOTGSbk1BnjFMKK98MEjLflLEFf5zvb5KSj-SdyGYAqkTJcs-0jz02L5_-WLrXhjIFo3Fa5E_qqH8701iabpAtKNH3y3e3ZxoXIqHWuRvR65wDrTxg', 'data': {'exam_impro_type': {'id': 'IA7ifDVfb6g8PJDJdEVO', 'exam_impro_parameter': {'id': None, 'label': 'Parameter_1', 'exam_impro_type_id': 'IA7ifDVfb6g8PJDJdEVO', 'idx': 0}}}}
            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )
    """
if __name__ == '__main__':
    unittest.main()