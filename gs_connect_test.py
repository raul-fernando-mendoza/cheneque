import unittest
import json
import logging

import firebase_admin
firebase_admin.initialize_app()

import gs_connect

logging.basicConfig( level=logging.DEBUG)
logging.debug('test has started') 


class TestFireStore(unittest.TestCase):

    def test01_addDocument(self):
            req = {
                    'service': 'gs', 
                    'bucket': 'cheneque-dev-videos', 
                    'action': 'list', 
                    'token': '7680ea3c-244b-4f4a-af3b-4cc1a475b3e8', 
                    'data':{
                        "path":"rax-academy/videos/"
                    }
            }
            obj = gs_connect.processRequest(req)
            logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )

            #self.assertTrue(obj["id"] == "test1")           



if __name__ == '__main__':
    unittest.main()