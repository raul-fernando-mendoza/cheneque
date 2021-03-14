import unittest
import json
import logging
import mysql_connect

logging.basicConfig( level=logging.DEBUG)
logging.debug('test has started') 


class TestExamenObservations(unittest.TestCase):

    
    def testReadObject(self):
            data = {
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
                                        "initially_selected": "",
                                        "label": ""
                                    }
                                ],
                                "exam_impro_type_id": "",
                                "id": "",
                                "label": ""
                            }
                        ],
                        "id": 4,
                        "label": ""
                    }
            }
            obj = mysql_connect.getObject(data)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )
    """
    def testReadObject(self):
            data = {
                "exam_impro_type":{
                    "id":"",
                    "label":"",
                    "exam_impro_parameter":{
                        "id":"",
                        "exam_impro_type_id":"",
                        "label":""
                    }
                },
                "orderBy":{
                    "exam_impro_parameter.label":"desc",
                    "exam_impro_type.id":"asc"
                    
                },
                "pagination":{
                    "limit":2,
                    "offset":2
                }
            }
            obj = mysql_connect.getObject(data)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )
    
    def testReadObject(self):
        data = {
            "exam_impro_criteria":{  
               id:17
            }
        }
        obj = mysql_connect.addObject(data)
        logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )
    
    def testReadObject(self):
        data = {
            "exam_impro_criteria":{  
                "label":"some new criteria 3",
                "exam_impro_parameter_id":2
            },
            "where":{
                "id":8
            }
        }
        obj = mysql_connect.updateObject(data)
        logging.debug( json.dumps(obj,  indent=4, sort_keys=False) )
    """

if __name__ == '__main__':
    unittest.main()