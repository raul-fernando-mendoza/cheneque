import unittest
import json
import logging
import mysql_connect

logging.basicConfig( level=logging.DEBUG)
logging.debug('test has started') 


class TestExamenObservations(unittest.TestCase):

    def testUpdateSingleObject(self):
            data = {'service': 'cheneque', 'database': 'entities', 'action': 'update', 'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 'data': {'exam_impro_criteria': {'label': 'Espacio Criterio 1', 'initially_selected': "1", 'where': {'id': 174}}}}

            obj = mysql_connect.processRequest(data)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )
"""    
    def updateMultipleObject(self):
            data = {
                "exam_impro_criteria":[
                    {
                        "idx":1,
                        "where":{
                            "id":142
                        }
                    },
                    {
                        "idx":2,
                        "where":{
                            "id":143
                        }
                    }
                ]
            }
            obj = mysql_connect.updateObject(data)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )
"""

if __name__ == '__main__':
    unittest.main()