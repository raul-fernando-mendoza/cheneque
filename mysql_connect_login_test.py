import unittest
from datetime import date
import json
import logging
import mysql_connect
logging.basicConfig( level=logging.DEBUG)
logging.debug('test has started') 

class TestExam(unittest.TestCase):

    """
    def testGetExamType(self):
        session = Session()
        examen = session.query(ExamType).filter_by(type_id=1).first()
        print( json.dumps(examen.toJSON(),  indent=4, sort_keys=True))
        session.close()
    """
    
    def testGet(self):
            data = {
                "user":{
                    "user_name":"claudia",
                    "password":"Argos4905",
                    "user_role":[{
                        "role_id":"" 
                    }],
                    "user_attribute(+)":{
                        "maestro_id":"",
                        "estudiante_id":""
                    }
                }
            }
            obj = mysql_connect.login(data)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )
    
if __name__ == '__main__':
    unittest.main()