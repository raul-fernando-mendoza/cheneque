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
    def testUpdateAspect(self):
            req = {
                    'service': 'firestore', 
                    'database': 'exam', 
                    'action': 'update', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                        "aspect":[
                            {
                            "id":"8TsBYXcOmlHNMX6lrp6M",
                            "idx":1,
                            "score":6.3
                            },
                            {
                            "id":"CrnaIf5lC9cI0ZQJaUgf",
                            "idx":2,
                            "score":9.4
                            }
                        ]                       
                    }
                    
            }
                    

            obj = firestore_connect.processRequest(req)
             logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )
    """
    def testUpdateAspect(self):
            req = {'service': 'firestore', 'database': 'notused', 'action': 'update', 'token': 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImFiMGNiMTk5Zjg3MGYyOGUyOTg5YWI0ODFjYzJlNDdlMGUyY2MxOWQiLCJ0eXAiOiJKV1QifQ.eyJhZG1pbiI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2NlbHRpYy1iaXZvdWFjLTMwNzMxNiIsImF1ZCI6ImNlbHRpYy1iaXZvdWFjLTMwNzMxNiIsImF1dGhfdGltZSI6MTYyMjY1MTU1MCwidXNlcl9pZCI6IlIxbE8wSGRPRnBjWDFadXIyTlRGdzAzdkxlWTIiLCJzdWIiOiJSMWxPMEhkT0ZwY1gxWnVyMk5URncwM3ZMZVkyIiwiaWF0IjoxNjIzMTYzMDczLCJleHAiOjE2MjMxNjY2NzMsImVtYWlsIjoicmF1bF9mZXJuYW5kb19tZW5kb3phQGhvdG1haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsicmF1bF9mZXJuYW5kb19tZW5kb3phQGhvdG1haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.fxqgjMRkAJX8PdIaHjULs1h4uDKAY7wOyutLHi0OQ4kk35oCwiBm_9b6YXELjsObRUli3c5xL0SY6dnXoGxvpE5sA7BTpOb_MhaRweOy-P6AVwwUDiF-gOT9nShDinq7c1EsEN4e3O-QfB6r8DoG6D3umB6d97QxMRU9Ij9Xevb5yr1Jw4d-AVjxnUx434d-Fe-f5ZAt-U_FaLn69zOfzwUbZrHFoViyqFD5aNWKuS2favQB9EbTXy37vaNDwT_U8plpkL7Pwm7yCGHDb07m8ttYPTixYNDFxidRLzhSq2lJGHGsfMyYcVPVXjCmy8Ut-RO3JXwujLlXROS6kTiP8A', 'data': {'examType': {'id': 'RXLwd610Xz32bXEz0TrO', 'label': 'Examen de tecnica'}}}
            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )

if __name__ == '__main__':
    unittest.main()