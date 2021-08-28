import unittest
import json
import logging
import compute_connect

log = logging.getLogger("cheneque")

class TestFireStore(unittest.TestCase):

    def test01_computeStart(self):
        list = compute_connect.getComputeInstanceList( project="cheneque-dev-4ee34", zone="us-central1-a" )
        self.assertIsNotNone( list )
        log.debug( json.dumps(list,  indent=4, sort_keys=True) )
        
        start = compute_connect.getComputeInstanceStart( "cheneque-dev-4ee34", "us-central1-a", list[0]["name"] )
        log.debug( start )

    def _test02_computeStop(self):
        list = compute_connect.getComputeInstanceList( project="cheneque-dev-4ee34", zone="us-central1-a" )
        self.assertIsNotNone( list )
        log.debug( json.dumps(list,  indent=4, sort_keys=True) )
        
        start = compute_connect.getComputeInstanceStop( "cheneque-dev-4ee34", "us-central1-a", list[0]["name"] )
        log.debug( start )


if __name__ == '__main__':
    unittest.main()