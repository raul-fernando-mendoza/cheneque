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
                    'data': {
                        'user': {
                            "uid":"abcd1234",
                            "displayName":"Paulina Rubio",
                            "email":"paulina.rubio@taxacademy.com"
                        }
                    }
            }
                    

            obj = mysql_connect.processRequest(data)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )


if __name__ == '__main__':
    unittest.main()