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
    def testAddObject(self):
            req = {
                    'service': 'firestore', 
                    'database': 'ex_type', 
                    'action': 'get', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                            "ExamType":{
                                "id":None,
                                "label":None,
                                "parameters":[
                                    {
                                        "id":None,
                                        "label":None,
                                        "criterias":[
                                            {
                                                "id":None,
                                                "label":None,
                                                "aspects":{
                                                    "id":None,
                                                    "label":None,
                                                    "idx":None
                                                }
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
            req = {'service': 
            'firestore', 
            'database': 'notused', 
            'action': 'get', 
            'token': 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImFiMGNiMTk5Zjg3MGYyOGUyOTg5YWI0ODFjYzJlNDdlMGUyY2MxOWQiLCJ0eXAiOiJKV1QifQ.eyJhZG1pbiI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2NlbHRpYy1iaXZvdWFjLTMwNzMxNiIsImF1ZCI6ImNlbHRpYy1iaXZvdWFjLTMwNzMxNiIsImF1dGhfdGltZSI6MTYyMjY1MTU1MCwidXNlcl9pZCI6IlIxbE8wSGRPRnBjWDFadXIyTlRGdzAzdkxlWTIiLCJzdWIiOiJSMWxPMEhkT0ZwY1gxWnVyMk5URncwM3ZMZVkyIiwiaWF0IjoxNjIzMTA1MjQ5LCJleHAiOjE2MjMxMDg4NDksImVtYWlsIjoicmF1bF9mZXJuYW5kb19tZW5kb3phQGhvdG1haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsicmF1bF9mZXJuYW5kb19tZW5kb3phQGhvdG1haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.TG8UnCC7Ypdj6BzXcxfeViTW-CYIynPE29LqU3X2u6TpVZYXgJ3rWBiTkOQLZn3CcZwIci-NxbcwT_TiobX-lbQvtutASCcjKm5ciGzt3e4YfRCkN8dW3RnqaUm76HsysSPA0w0StIq90dNI69AG5khEJfZ0jlKZq_ohYj9uC83MDgiBAB1pPoNwWeekLjrTxCcnuj2tdHovHNS5Sl-WAz8gRvPI7wAzZK3Yd0JR1-J-sQiUSP66lFzx0t-Iua5oUcfdooyVx_aby_ZrZuiytuYom_N5CIkJQX2CDI9YTYlN1bqCYEd6SZEfCc2lzRjNj-EDH0KSc2Q2DXwcsbjHLw', 
            'data': {
                'ExamType': [
                    {
                        'id': None, 
                        'label': None, 
                        'description': None, 
                        'parameters': None
                    }
                ], 
                'orderBy': {
                    'label':'asc'
                }
            }
            }
                    

            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )    
    

if __name__ == '__main__':
    unittest.main()