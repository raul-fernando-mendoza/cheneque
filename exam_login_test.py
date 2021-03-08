import unittest
from datetime import date
import json
import logging
from json import JSONEncoder
import mysql_connect


logging.basicConfig( level=logging.DEBUG)
logging.debug('test has started') 

class TestExam(unittest.TestCase):

    """
    def testGetExamType(self):
            data = {
                "service":"cheneque",
                "database":"entities",
                "action":"login",
                "data":{
                    "user_name":"claudia",
                    "password":"Argos4905"
                }
            }
            result = mysql_connect.processRequest(data)
            logging.debug( json.dumps(result,  indent=4, sort_keys=True) )
    """
    def testGetExamType(self):

            data = {
                "service":"cheneque",
                "database":"entities",
                "action":"validateToken",
                "data":{
                    "token":"697af077-17eb-4bea-9485-a59ab76cb0af"
                }
            }
            result2 = mysql_connect.processRequest(data)
            logging.debug( json.dumps(result2,  indent=4, sort_keys=True) )
    

    
if __name__ == '__main__':
    unittest.main()