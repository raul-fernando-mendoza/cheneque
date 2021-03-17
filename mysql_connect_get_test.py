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
            request = {
                "action": "get",
                "data": {
                    "exam_impro_type": {
                        "exam_impro_parameter(+)": [
                            {
                                "exam_impro_criteria(+)": [
                                    {
                                        "exam_impro_parameter_id": "",
                                        "exam_impro_question(+)": [
                                            {
                                                "description": "",
                                                "exam_impro_criteria_id": "",
                                                "id": "",
                                                "label": "",
                                                "points": ""
                                            }
                                        ],
                                        "id": "",
                                        "idx": "",
                                        "initially_selected": "",
                                        "label": ""
                                    }
                                ],
                                "exam_impro_type_id": "",
                                "id": "",
                                "label": ""
                            }
                        ],
                        "id": 16,
                        "label": ""
                    },
                    "orderBy":{
                        "exam_impro_criteria.idx":""
                    }
                },
                "database": "entities",
                "service": "cheneque",
                "token": "7680ea3c-244b-4f4a-af3b-4cc1a475b3e8"
            }
            
            obj = mysql_connect.processRequest(request)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )
    
if __name__ == '__main__':
    unittest.main()