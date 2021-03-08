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
            data = {'service': 'cheneque', 'database': 'entities', 'action': 'get', 'data': {'exam_impro_ap_parameter': [{'id': '', 'completado': '', 'maestro': {'id': '2', 'nombre': '', 'apellidoPaterno': '', 'apellidoMaterno': ''}, 'exam_impro_ap': {'fechaApplicacion': '', 'completado': '', 'materia': '', 'estudiante': {'nombre': '', 'apellidoPaterno': '', 'apellidoMaterno': ''}}, 'exam_impro_parameter': {'label': '', 'exam_impro_type': {'label': ''}}}]}}
            
            obj = mysql_connect.processRequest(data)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )
    
if __name__ == '__main__':
    unittest.main()