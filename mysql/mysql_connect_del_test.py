import unittest
import json
import logging
import mysql_connect

logging.basicConfig( level=logging.DEBUG)
logging.debug('test has started') 


class TestExamenObservations(unittest.TestCase):
    def testDeleteObject(self):
        data = {
            "user":{
                "uid":"abcd1234"
            }
        }
        obj = mysql_connect.deleteObject(data)
        logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )
    

if __name__ == '__main__':
    unittest.main()