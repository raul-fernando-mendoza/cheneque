import unittest
import json
import logging
import mysql_connect

logging.basicConfig( level=logging.DEBUG)
logging.debug('test has started') 


class TestExamenObservations(unittest.TestCase):

    def testAddObject(self):
            data = {
                    'service': 'cheneque', 
                    'database': 'entities', 
                    'action': 'createUser', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                        "exam_impro_ap":{
                            "id": null,
                            "completado": false,
                            "fechaApplicacion": "2021-03-27T06:00:00.000Z",
                            "estudiante_uid": "h9FxYWKzqZezL6E5iCnVBM3avgI2",
                            "exam_impro_type_id": 16,
                            "materia": "alguna materia",
                            "exam_impro_ap_parameter": [
                                {
                                "id": null,
                                "exam_impro_ap_id": null,
                                "completado": false,
                                "exam_impro_parameter_id": 58,
                                "maestro_uid": "YMPmHz85tcNpOqvUwCdZlciDVRs1",
                                "exam_impro_ap_criteria": [
                                    {
                                    "id": null,
                                    "exam_impro_ap_parameter_id": 58,
                                    "exam_impro_criteria_id": 176,
                                    "selected": 1
                                    }
                                ]
                                },
                                {
                                "id": null,
                                "exam_impro_ap_id": null,
                                "completado": false,
                                "exam_impro_parameter_id": 59,
                                "maestro_uid": "pA7edq1jlQYtDZm7ZBlLdGAQuzf1",
                                "exam_impro_ap_criteria": [
                                    {
                                    "id": null,
                                    "exam_impro_ap_parameter_id": 59,
                                    "exam_impro_criteria_id": 177,
                                    "selected": 0
                                    },
                                    {
                                    "id": null,
                                    "exam_impro_ap_parameter_id": 59,
                                    "exam_impro_criteria_id": 178,
                                    "selected": 1
                                    }
                                ]
                                },
                                {
                                "id": null,
                                "exam_impro_ap_id": null,
                                "completado": false,
                                "exam_impro_parameter_id": 60,
                                "maestro_uid": "YMPmHz85tcNpOqvUwCdZlciDVRs1",
                                "exam_impro_ap_criteria": [
                                    {
                                    "id": null,
                                    "exam_impro_ap_parameter_id": 60,
                                    "exam_impro_criteria_id": 166,
                                    "selected": 0
                                    },
                                    {
                                    "id": null,
                                    "exam_impro_ap_parameter_id": 60,
                                    "exam_impro_criteria_id": 167,
                                    "selected": 0
                                    },
                                    {
                                    "id": null,
                                    "exam_impro_ap_parameter_id": 60,
                                    "exam_impro_criteria_id": 168,
                                    "selected": 1
                                    }
                                ]
                                },
                                {
                                "id": null,
                                "exam_impro_ap_id": null,
                                "completado": false,
                                "exam_impro_parameter_id": 63,
                                "maestro_uid": "pA7edq1jlQYtDZm7ZBlLdGAQuzf1",
                                "exam_impro_ap_criteria": [
                                    {
                                    "id": null,
                                    "exam_impro_ap_parameter_id": 63,
                                    "exam_impro_criteria_id": 179,
                                    "selected": 1
                                    },
                                    {
                                    "id": null,
                                    "exam_impro_ap_parameter_id": 63,
                                    "exam_impro_criteria_id": 180,
                                    "selected": 0
                                    },
                                    {
                                    "id": null,
                                    "exam_impro_ap_parameter_id": 63,
                                    "exam_impro_criteria_id": 181,
                                    "selected": 0
                                    },
                                    {
                                    "id": null,
                                    "exam_impro_ap_parameter_id": 63,
                                    "exam_impro_criteria_id": 182,
                                    "selected": 0
                                    }
                                ]
                                }
                            ]
                        }
                    }
            }
                    

            obj = mysql_connect.processRequest(data)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )


if __name__ == '__main__':
    unittest.main()