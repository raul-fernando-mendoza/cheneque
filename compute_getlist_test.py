import unittest
import json
import logging
import compute_connect
import environments


log = logging.getLogger("cheneque")

class TestFireStore(unittest.TestCase):



    def _test01_computeList(self):
        list = compute_connect.getComputeInstanceList( project="cheneque-dev-4ee34", zone="us-central1-a" )
        self.assertIsNotNone( list )
        log.debug( json.dumps(list,  indent=4, sort_keys=True) )

    def test02_request(self):
        req = {
            "service":"compute",
            "action":"computeInstanceList",
            "project":"cheneque-dev-4ee34",
            "zone":"us-central1-a"           
        }
        list = compute_connect.processRequest(req)
        self.assertIsNotNone( list )
        log.debug( json.dumps(list,  indent=4, sort_keys=True) )        


if __name__ == '__main__':
    unittest.main()