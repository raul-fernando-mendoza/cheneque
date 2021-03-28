import unittest
from datetime import date
import json
import logging
from mysql_connect import processRequest

logging = logging.getLogger("exam_app")
logging.debug("logging has started")


class TestExam(unittest.TestCase):

    """
    def testGetExamType(self):
        session = Session()
        examen = session.query(ExamType).filter_by(type_id=1).first()
        print( json.dumps(examen.toJSON(),  indent=4, sort_keys=True))
        session.close()
    """
    
    def testGet(self):
            request = {
                "action": "get",
                "database": "entities",
                "service": "cheneque",
                "token": "eyJhbGciOiJSUzI1NiIsImtpZCI6ImY4NDY2MjEyMTQxMjQ4NzUxOWJiZjhlYWQ4ZGZiYjM3ODYwMjk5ZDciLCJ0eXAiOiJKV1QifQ.eyJhZG1pbiI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2NlbHRpYy1iaXZvdWFjLTMwNzMxNiIsImF1ZCI6ImNlbHRpYy1iaXZvdWFjLTMwNzMxNiIsImF1dGhfdGltZSI6MTYxNjY5ODU1NSwidXNlcl9pZCI6InkyMHlHVmNDbTZWNkpyODZhQWR5VTdjSllsNTMiLCJzdWIiOiJ5MjB5R1ZjQ202VjZKcjg2YUFkeVU3Y0pZbDUzIiwiaWF0IjoxNjE2Njk4NTU1LCJleHAiOjE2MTY3MDIxNTUsImVtYWlsIjoiY2xhdWRpYS5nYW1ib2FAcmF4YWNhZGVteS5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsiY2xhdWRpYS5nYW1ib2FAcmF4YWNhZGVteS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.oZD3i4_RdV5wOiUDSOWf05FAfZzFQMWNhBpNWObAPZAFYEJjf_GdW95vpd1R-Cmmc7HPdNbtXmrEh8WnEWiTqIfkZtPHGBKGzJ2WQf0BQp0hnb6cb2cZtwBTwHjad09PWcqi0QhIvFJgwr2c1BWw05RpTqJirMUbb6fmzyKjKjbM7NxMlIudFUnP7KNTemNM0wQyarGhN3L5amUaX--d1A-9g1PJFEsithmh1nChoBFrNKr141V8FAuCWAQ4ySF5HkjbBtjM0swStaEfyuBPtJH-WZpaj_910Nm4uLU_NxGazW6xePrnNUzzqaEwjkuAb_iFa-Cnr-zMOPDVi9MPvA",
                "data": {
                        "exam_impro_ap_parameter":[{
                            "id":"",
                            "completado":"",
                            "maestro:user":{
                                "email":"",
                                "displayName":"" 
                            },
                            "exam_impro_ap":{
                                "fechaApplicacion":"",
                                "completado":"",
                                "materia":"",
                                "estudiante:user":{
                                    "email":"",
                                    "displayName":""
                                }
                            },
                            "exam_impro_parameter":{
                                "label":"",
                                "exam_impro_type":{
                                    "label":""
                                }  
                            }
                        }]
                    }
            }
            
            obj = processRequest(request)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )
    
if __name__ == '__main__':
    unittest.main()


#curl -d '{"action": "get","data": {"exam_impro_type": [{"id": "","label": ""}},"database": "entities","service": "cheneque","token": "eyJhbGciOiJSUzI1NiIsImtpZCI6ImY4NDY2MjEyMTQxMjQ4NzUxOWJiZjhlYWQ4ZGZiYjM3ODYwMjk5ZDciLCJ0eXAiOiJKV1QifQ.eyJhZG1pbiI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2NlbHRpYy1iaXZvdWFjLTMwNzMxNiIsImF1ZCI6ImNlbHRpYy1iaXZvdWFjLTMwNzMxNiIsImF1dGhfdGltZSI6MTYxNjY5ODU1NSwidXNlcl9pZCI6InkyMHlHVmNDbTZWNkpyODZhQWR5VTdjSllsNTMiLCJzdWIiOiJ5MjB5R1ZjQ202VjZKcjg2YUFkeVU3Y0pZbDUzIiwiaWF0IjoxNjE2Njk4NTU1LCJleHAiOjE2MTY3MDIxNTUsImVtYWlsIjoiY2xhdWRpYS5nYW1ib2FAcmF4YWNhZGVteS5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsiY2xhdWRpYS5nYW1ib2FAcmF4YWNhZGVteS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.oZD3i4_RdV5wOiUDSOWf05FAfZzFQMWNhBpNWObAPZAFYEJjf_GdW95vpd1R-Cmmc7HPdNbtXmrEh8WnEWiTqIfkZtPHGBKGzJ2WQf0BQp0hnb6cb2cZtwBTwHjad09PWcqi0QhIvFJgwr2c1BWw05RpTqJirMUbb6fmzyKjKjbM7NxMlIudFUnP7KNTemNM0wQyarGhN3L5amUaX--d1A-9g1PJFEsithmh1nChoBFrNKr141V8FAuCWAQ4ySF5HkjbBtjM0swStaEfyuBPtJH-WZpaj_910Nm4uLU_NxGazW6xePrnNUzzqaEwjkuAb_iFa-Cnr-zMOPDVi9MPvA"}' -H 'Content-Type: application/json' localhost:5000/api
#curl -d '{"action": "get","data": {"exam_impro_type": [{"id": "","label": ""}},"database": "entities","service": "cheneque","token": "eyJhbGciOiJSUzI1NiIsImtpZCI6ImY4NDY2MjEyMTQxMjQ4NzUxOWJiZjhlYWQ4ZGZiYjM3ODYwMjk5ZDciLCJ0eXAiOiJKV1QifQ.eyJhZG1pbiI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2NlbHRpYy1iaXZvdWFjLTMwNzMxNiIsImF1ZCI6ImNlbHRpYy1iaXZvdWFjLTMwNzMxNiIsImF1dGhfdGltZSI6MTYxNjY5ODU1NSwidXNlcl9pZCI6InkyMHlHVmNDbTZWNkpyODZhQWR5VTdjSllsNTMiLCJzdWIiOiJ5MjB5R1ZjQ202VjZKcjg2YUFkeVU3Y0pZbDUzIiwiaWF0IjoxNjE2Njk4NTU1LCJleHAiOjE2MTY3MDIxNTUsImVtYWlsIjoiY2xhdWRpYS5nYW1ib2FAcmF4YWNhZGVteS5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsiY2xhdWRpYS5nYW1ib2FAcmF4YWNhZGVteS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.oZD3i4_RdV5wOiUDSOWf05FAfZzFQMWNhBpNWObAPZAFYEJjf_GdW95vpd1R-Cmmc7HPdNbtXmrEh8WnEWiTqIfkZtPHGBKGzJ2WQf0BQp0hnb6cb2cZtwBTwHjad09PWcqi0QhIvFJgwr2c1BWw05RpTqJirMUbb6fmzyKjKjbM7NxMlIudFUnP7KNTemNM0wQyarGhN3L5amUaX--d1A-9g1PJFEsithmh1nChoBFrNKr141V8FAuCWAQ4ySF5HkjbBtjM0swStaEfyuBPtJH-WZpaj_910Nm4uLU_NxGazW6xePrnNUzzqaEwjkuAb_iFa-Cnr-zMOPDVi9MPvA"}' -H 'Content-Type: application/json' https://celtic-bivouac-307316.uc.r.appspot.com/api