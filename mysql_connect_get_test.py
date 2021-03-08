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
                                "id": "",
                                "nombre": ""
                            }
                        }
                    ]
                },
                "database": "entities",
                "service": "cheneque",
                "token": "09fbfc96-ff4c-44b8-ac05-2bd62b5dc997"
            }
            
            obj = mysql_connect.processRequest(data)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )
    
if __name__ == '__main__':
    unittest.main()