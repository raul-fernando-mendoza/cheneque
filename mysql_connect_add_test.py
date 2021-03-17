import unittest
import json
import logging
import mysql_connect

logging.basicConfig( level=logging.DEBUG)
logging.debug('test has started') 


class TestExamenObservations(unittest.TestCase):

    def testAddObject(self):
            data = {'service': 'cheneque', 'database': 'entities', 'action': 'add', 'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 'data': {'exam_impro_ap': {'id': None, 'completado': False, 'fechaApplicacion': '2021-03-17', 'estudiante_id': 2, 'exam_impro_type_id': 16, 'materia': 'una mas', 'exam_impro_ap_parameter': [{'id': None, 'exam_impro_ap_id': None, 'completado': False, 'exam_impro_parameter_id': 58, 'maestro_id': None, 'exam_impro_ap_criteria': [{'id': None, 'exam_impro_ap_parameter_id': 58, 'exam_impro_criteria_id': 161, 'selected': 1}]}, {'id': None, 'exam_impro_ap_id': None, 'completado': False, 'exam_impro_parameter_id': 59, 'maestro_id': None, 'exam_impro_ap_criteria': [{'id': None, 'exam_impro_ap_parameter_id': 59, 'exam_impro_criteria_id': 174, 'selected': 1}, {'id': None, 'exam_impro_ap_parameter_id': 59, 'exam_impro_criteria_id': 175, 'selected': 1}]}, {'id': None, 'exam_impro_ap_id': None, 'completado': False, 'exam_impro_parameter_id': 60, 'maestro_id': None, 'exam_impro_ap_criteria': [{'id': None, 'exam_impro_ap_parameter_id': 60, 'exam_impro_criteria_id': 166, 'selected': 1}, {'id': None, 'exam_impro_ap_parameter_id': 60, 'exam_impro_criteria_id': 167, 'selected': 1}, {'id': None, 'exam_impro_ap_parameter_id': 60, 'exam_impro_criteria_id': 168, 'selected': 1}]}, {'id': None, 'exam_impro_ap_id': None, 'completado': False, 'exam_impro_parameter_id': 61, 'maestro_id': None, 'exam_impro_ap_criteria': [{'id': None, 'exam_impro_ap_parameter_id': 61, 'exam_impro_criteria_id': 169, 'selected': 1}, {'id': None, 'exam_impro_ap_parameter_id': 61, 'exam_impro_criteria_id': 170, 'selected': 1}, {'id': None, 'exam_impro_ap_parameter_id': 61, 'exam_impro_criteria_id': 171, 'selected': 1}, {'id': None, 'exam_impro_ap_parameter_id': 61, 'exam_impro_criteria_id': 172, 'selected': 1}]}]}}}

            obj = mysql_connect.processRequest(data)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )


if __name__ == '__main__':
    unittest.main()