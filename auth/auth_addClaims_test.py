import unittest
import json
import logging

import firebase_admin
firebase_admin.initialize_app()

import auth_connect

log = logging.getLogger("cheneque")
log.setLevel(logging.DEBUG)


class TestExamenObservations(unittest.TestCase):

    def testaddClaim(self):
            req = {
                    'service': 'auth', 
                    'action': 'addClaim',
                    'data':{
                        "email":"admin-dev@raxacademy.com", 
                        'claims':{
                            "role-admin-autocad":True
                        }
                    }
            }
                    

            obj = auth_connect.processRequest(req)
            log.debug( "obj %s", json.dumps(obj,  indent=4, sort_keys=True) )
    
            req = {
                    'service': 'auth', 
                    'action': 'getClaims',
                    "email":"admin-dev@raxacademy.com", 
            }
                    

            obj = auth_connect.processRequest(req)
            log.debug( json.dumps(obj,  indent=4, sort_keys=True) )
if __name__ == '__main__':
    unittest.main()