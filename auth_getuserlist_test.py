import unittest
import json
import logging

import firebase_admin
import environments
firebase_admin.initialize_app()

import auth_connect

logging.basicConfig( level=logging.DEBUG)
logging.debug('test has started') 


class TestExamenObservations(unittest.TestCase):

    def testaddClaim(self):
            req = {
                    'service': 'auth', 
                    'action': 'getUserList'
            }
                    

            obj = auth_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )
if __name__ == '__main__':
    unittest.main()