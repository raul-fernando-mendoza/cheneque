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
            req = {
  "service": "firestore",
  "database": "notused",
  "action": "update",
  "token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjhmNDMyMDRhMTc5MTVlOGJlN2NjZDdjYjI2NGRmNmVhMzgzYzQ5YWIiLCJ0eXAiOiJKV1QifQ.eyJhZG1pbiI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2NlbHRpYy1iaXZvdWFjLTMwNzMxNiIsImF1ZCI6ImNlbHRpYy1iaXZvdWFjLTMwNzMxNiIsImF1dGhfdGltZSI6MTYyNjIyMzEzNCwidXNlcl9pZCI6IlIxbE8wSGRPRnBjWDFadXIyTlRGdzAzdkxlWTIiLCJzdWIiOiJSMWxPMEhkT0ZwY1gxWnVyMk5URncwM3ZMZVkyIiwiaWF0IjoxNjI2MjIzMTM0LCJleHAiOjE2MjYyMjY3MzQsImVtYWlsIjoicmF1bF9mZXJuYW5kb19tZW5kb3phQGhvdG1haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsicmF1bF9mZXJuYW5kb19tZW5kb3phQGhvdG1haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.obNwJCylqWd1RPFC3-B0cbMyPXlKwg9p8AGgR3HQah3YCrM9uJyYnSIsivDkt3uoUKxqeLFy08XWtMcaAg7QK5OzieG_Ij5u-VDgOGOPhdxSNmSuGnppPL7QgbV2e8N6B4hWzEHZi9BpW-t2RDRqQgchjYoln6Os9eOeYj5HludUCy1dSkzAMVTbuoPnPX4qCxcZFQzdfYPQT0tcsLFoJi2UYoijRCVUcqNV2oQuhYxgJvwqYuJIOu8zwfvxKtSBKFZamRCWUgI2SvTMno3UsE3-PNWzRJfa_1-wB1yfehwDd_XDRwMRMTZt7rNs6WpdVdKgE2I4HHXILcnUgHFIXw",
  "data": {
    "exams": {
      "id": "8VBfxo2oyQ9xEKF51Bf3",
      "label": "one",
      "description": ""
    }
  }
}
            obj = firestore_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )

if __name__ == '__main__':
    unittest.main()