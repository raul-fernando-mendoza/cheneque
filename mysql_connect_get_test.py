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
                    "exam_impro_ap_parameter": [
                        {
                            "completado": True,
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
                                "nombre": ""
                            }
                        }
                    ]
                },
                "database": "entities",
                "service": "cheneque",
                "token": "bc193bee-69f6-4eb0-9cba-e79df446857a"
            }
            
            obj = mysql_connect.processRequest(request)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )
    
if __name__ == '__main__':
    unittest.main()