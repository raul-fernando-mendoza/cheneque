import unittest
import json
import logging

import firebase_admin
from firebase_admin import credentials
cred = credentials.Certificate('celtic-bivouac-307316-firebase-adminsdk-pbsww-2ccfde6abd.json')
firebase_admin.initialize_app(cred)

import auth_connect

logging.basicConfig( level=logging.DEBUG)
logging.debug('test has started') 


class TestExamenObservations(unittest.TestCase):

    def testRemoveClaim(self):
            req = {
                    'service': 'auth', 
                    'action': 'removeClaim',
                    'data':{
                        "email":"evaluador5@raxacademy.com", 
                        'claim':"readonly"
                    }
            }
                    

            obj = auth_connect.processRequest(req)
            logging.debug( "obj %s", json.dumps(obj,  indent=4, sort_keys=True) )

            req = {
                    'service': 'auth', 
                    'action': 'getClaims',
                    "email":"evaluador5@raxacademy.com", 
            }
                    

            obj = auth_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )
if __name__ == '__main__':
    unittest.main()