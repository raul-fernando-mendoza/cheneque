import unittest
import json
import logging

import firebase_admin
import environments
firebase_admin.initialize_app()

import auth_connect

log = logging.getLogger("cheneque")


class TestExamenObservations(unittest.TestCase):

    def testaddClaim(self):
            req = {
                    'service': 'auth', 
                    'action': 'addClaim',
                    'data':{
                        "email":"admin-dev@hotmail.com", 
                        'claims':{
                            "admin":True
                        }
                    }
            }
                    

            obj = auth_connect.processRequest(req)
            log.debug( "obj %s", json.dumps(obj,  indent=4, sort_keys=True) )
    
            req = {
                    'service': 'auth', 
                    'action': 'getClaims',
                    "email":"admin-dev@hotmail.com", 
            }
                    

            obj = auth_connect.processRequest(req)
            log.debug( json.dumps(obj,  indent=4, sort_keys=True) )
if __name__ == '__main__':
    unittest.main()