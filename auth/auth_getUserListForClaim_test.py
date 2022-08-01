import unittest
import json
import logging

import firebase_admin
import environments
firebase_admin.initialize_app()

import auth_connect

log = logging.getLogger("cheneque")


class TestExamenObservations(unittest.TestCase):

    def testRemoveClaim(self):
            req = {
                    'service': 'auth', 
                    'action': 'getUserListForClaim',
                    'data':{
                        'claims':"evaluador"
                    }
            }
                    

            obj = auth_connect.processRequest(req)
            log.debug( "obj %s", json.dumps(obj,  indent=4, sort_keys=True) )

if __name__ == '__main__':
    unittest.main()