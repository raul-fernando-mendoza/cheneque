import unittest
from datetime import date
import json
import logging
from json import JSONEncoder
import mysql_connect


logging.basicConfig( level=logging.DEBUG)
logging.debug('test has started') 

class TestExam(unittest.TestCase):

   
    def testGetExamType(self):
            data = {'exam_impro_ap': {'id': None, 'completado': False, 'fechaApplicacion': '2021-03-06', 'estudiante_id': 2, 'exam_impro_type_id': 1, 'exam_impro_ap_parameter': [{'id': None, 'exam_impro_ap_id': None, 'completado': False, 'exam_impro_parameter_id': 1, 'maestro_id': 2, 'exam_impro_ap_criteria': [{'id': None, 'exam_impro_ap_parameter_id': 1, 'exam_impro_criteria_id': 1, 'selected': 1}, {'id': None, 'exam_impro_ap_parameter_id': 1, 'exam_impro_criteria_id': 2, 'selected': 1}, {'id': None, 'exam_impro_ap_parameter_id': 1, 'exam_impro_criteria_id': 3, 'selected': 1}, {'id': None, 'exam_impro_ap_parameter_id': 1, 'exam_impro_criteria_id': 4, 'selected': 1}, {'id': None, 'exam_impro_ap_parameter_id': 1, 'exam_impro_criteria_id': 5, 'selected': 1}]}, {'id': None, 'exam_impro_ap_id': None, 'completado': False, 'exam_impro_parameter_id': 2, 'maestro_id': 2, 'exam_impro_ap_criteria': [{'id': None, 'exam_impro_ap_parameter_id': 2, 'exam_impro_criteria_id': 6, 'selected': 1}, {'id': None, 'exam_impro_ap_parameter_id': 2, 'exam_impro_criteria_id': 7, 'selected': 1}, {'id': None, 'exam_impro_ap_parameter_id': 2, 'exam_impro_criteria_id': 8, 'selected': 0}, {'id': None, 'exam_impro_ap_parameter_id': 2, 'exam_impro_criteria_id': 9, 'selected': 0}, {'id': None, 'exam_impro_ap_parameter_id': 2, 'exam_impro_criteria_id': 10, 'selected': 1}]}, {'id': None, 'exam_impro_ap_id': None, 'completado': False, 'exam_impro_parameter_id': 3, 'maestro_id': 85, 'exam_impro_ap_criteria': [{'id': None, 'exam_impro_ap_parameter_id': 3, 'exam_impro_criteria_id': 11, 'selected': 1}]}, {'id': None, 'exam_impro_ap_id': None, 'completado': False, 'exam_impro_parameter_id': 4, 'maestro_id': 85, 'exam_impro_ap_criteria': [{'id': None, 'exam_impro_ap_parameter_id': 4, 'exam_impro_criteria_id': 12, 'selected': 1}]}]}}
            result = mysql_connect.addObject(data)
            logging.debug( json.dumps(result,  indent=4, sort_keys=True) )
    
if __name__ == '__main__':
    unittest.main()