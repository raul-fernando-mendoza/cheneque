import unittest
from datetime import date
import json
import logging
from cheneque.mysql_connect import processRequest

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
                "data": {
                    "exam_impro_ap_parameter": [
                        {
                            "completado": "",
                            "exam_impro_ap": {
                                "completado": "",
                                "estudiante": {
                                    "apellidoMaterno": "",
                                    "apellidoPaterno": "",
                                    "nombre": ""
                                },
                                "fechaApplicacion": "",
                                "materia": ""
                            },
                            "exam_impro_parameter": {
                                "exam_impro_type": {
                                    "label": ""
                                },
                                "label": ""
                            },
                            "id": "",
                            "maestro": {
                                "apellidoMaterno": "",
                                "apellidoPaterno": "",
                                "email": "",
                                "nombre": ""
                            }
                        }
                    ]
                },
                "database": "entities",
                "service": "cheneque",
                "token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjRlMDBlOGZlNWYyYzg4Y2YwYzcwNDRmMzA3ZjdlNzM5Nzg4ZTRmMWUiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vY2VsdGljLWJpdm91YWMtMzA3MzE2IiwiYXVkIjoiY2VsdGljLWJpdm91YWMtMzA3MzE2IiwiYXV0aF90aW1lIjoxNjE2NDUzNDA2LCJ1c2VyX2lkIjoieTIweUdWY0NtNlY2SnI4NmFBZHlVN2NKWWw1MyIsInN1YiI6InkyMHlHVmNDbTZWNkpyODZhQWR5VTdjSllsNTMiLCJpYXQiOjE2MTY0NTM0MDcsImV4cCI6MTYxNjQ1NzAwNywiZW1haWwiOiJjbGF1ZGlhLmdhbWJvYUByYXhhY2FkZW15LmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJjbGF1ZGlhLmdhbWJvYUByYXhhY2FkZW15LmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.XjCzMvgtXHyoJGUYuQqcw7Le8Vs0pT16co5fOhV4FBqN7vPX9kzwJXZ018FV6eLJb4FSigdTsTvFc_FSD_9bCj9pRJv5_ROjG80YCtfxxokxUp8J2DUHJsce6FLIaWwb0q_z2cHcgeuMB5IE7zQYM6A4RsRjNtCPwveVR3rpDGc0Kr3vYxw1VuiRUHktwgxpDyITTzOAuEF5c1hk5mhtxS6GR6EzetTUEjyCZKUKqq-TB41fCNe0QPShdiBbFpYUtDTMNqvC3kiCFNpEvCXt9Phh0RElweRcgzNAmfKZGafcprkFlZ-67f_2D6Krn5PBChV3NJEr9JdjAxjf5NcF5Q"
            }
            
            obj = processRequest(request)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )
    
if __name__ == '__main__':
    unittest.main()


curl -d '{json}' -H 'Content-Type: application/json' https://example.com/login