import unittest
import json
import logging

import firebase_admin
import environments
firebase_admin.initialize_app( )

import firestore_connect

log = logging.getLogger("cheneque")


class TestExamenObservations(unittest.TestCase):

    def testUpdateObject(self):
            req = {
              "service": "firestore",
              "database": "notused",
              "action": "update",
              "token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjhmNDMyMDRhMTc5MTVlOGJlN2NjZDdjYjI2NGRmNmVhMzgzYzQ5YWIiLCJ0eXAiOiJKV1QifQ.eyJhZG1pbiI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2NlbHRpYy1iaXZvdWFjLTMwNzMxNiIsImF1ZCI6ImNlbHRpYy1iaXZvdWFjLTMwNzMxNiIsImF1dGhfdGltZSI6MTYyNjIyMzEzNCwidXNlcl9pZCI6IlIxbE8wSGRPRnBjWDFadXIyTlRGdzAzdkxlWTIiLCJzdWIiOiJSMWxPMEhkT0ZwY1gxWnVyMk5URncwM3ZMZVkyIiwiaWF0IjoxNjI2MjIzMTM0LCJleHAiOjE2MjYyMjY3MzQsImVtYWlsIjoicmF1bF9mZXJuYW5kb19tZW5kb3phQGhvdG1haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsicmF1bF9mZXJuYW5kb19tZW5kb3phQGhvdG1haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.obNwJCylqWd1RPFC3-B0cbMyPXlKwg9p8AGgR3HQah3YCrM9uJyYnSIsivDkt3uoUKxqeLFy08XWtMcaAg7QK5OzieG_Ij5u-VDgOGOPhdxSNmSuGnppPL7QgbV2e8N6B4hWzEHZi9BpW-t2RDRqQgchjYoln6Os9eOeYj5HludUCy1dSkzAMVTbuoPnPX4qCxcZFQzdfYPQT0tcsLFoJi2UYoijRCVUcqNV2oQuhYxgJvwqYuJIOu8zwfvxKtSBKFZamRCWUgI2SvTMno3UsE3-PNWzRJfa_1-wB1yfehwDd_XDRwMRMTZt7rNs6WpdVdKgE2I4HHXILcnUgHFIXw",
              "data": {
                "employee": {
                  "id": "cXwCNUiSnbehBwRjjgX4",
                  "name": "raul mendoza",
                  "description": "Long time programmer",
                  "profiles":
                    {
                      "id":"bdUnhM39aWyTFsPMYhEj",
                      "years":8
                    }
                }
              }
            }
            obj = firestore_connect.processRequest(req)
            log.debug( json.dumps(obj,  indent=4, sort_keys=True) )


if __name__ == '__main__':
    unittest.main()