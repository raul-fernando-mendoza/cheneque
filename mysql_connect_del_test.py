import unittest
import json
import logging
import mysql_connect

logging.basicConfig( level=logging.DEBUG)
logging.debug('test has started') 


class TestExamenObservations(unittest.TestCase):
    def testDeleteObject(self):
        data = {
            "exam_impro_question":{
                "id":45
            }
        }
        obj = mysql_connect.deleteObject(data)
        logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )
    

if __name__ == '__main__':
    unittest.main()