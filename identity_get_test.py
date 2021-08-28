import unittest
import json
import logging

import firebase_admin
from firebase_admin import credentials
import environments

firebase_admin.initialize_app(environments.config["cred"] )

log = logging.getLogger("cheneque")
log.setLevel(logging.DEBUG)

import identity_connect

class TestFireStore(unittest.TestCase):

    def disable_test01_get(self):
        token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjgxOWQxZTYxNDI5ZGQzZDNjYWVmMTI5YzBhYzJiYWU4YzZkNDZmYmMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJuYmYiOjE2Mjk4NDY1MDMsImF1ZCI6IjY3MTE3MzQwOTQ4Ni0zb250ZmpmcGozMmJqZm10bXBwOXRlY2xudGRwOWp2Yi5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjEwMDEwNTA1MjgwNDkxMDg4MDYwMCIsImVtYWlsIjoicmZtaDI0aHJAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF6cCI6IjY3MTE3MzQwOTQ4Ni0zb250ZmpmcGozMmJqZm10bXBwOXRlY2xudGRwOWp2Yi5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsIm5hbWUiOiJyZm1oMjRociBNZW5kb3phIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FBVFhBSnhBLWF2cVlxRHJhWVAzci1iRGt5ajZKaGpEaExEdFFhNTRKcXhQPXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6InJmbWgyNGhyIiwiZmFtaWx5X25hbWUiOiJNZW5kb3phIiwiaWF0IjoxNjI5ODQ2ODAzLCJleHAiOjE2Mjk4NTA0MDMsImp0aSI6IjAwNWFlNTJmMTg1OGRkMmY3ZjI4NDUzZGU2NWE2ODk2ZDdjNzdlMGMifQ.I6gKEPTSoHbgn87d6QnyhRRosO-y7S7ZOi4CATPBicbp1-Zd4YOhu4dlmQO6scAxghVSQmsChSTxpCyRzglwi2MLBQHzAwVGrh2Wy4SsxUGzD3dHqxvrXw67sxXNo6lpp0_QuR7uzwjsEVTIloCvYM1P5qeR2wKQ4GQpzEHhkk_mxCNrV5OEbUz9sLU3O5_OrgL7UbsrZVoBhDDNuoDiDefL5Zr4eqLbbsyqcHEQQJQlBvQbnhzHtLMw3j-bzESojvoz2teVwGdLsWe9ueEkk0UYFKs98UFXMT5nFAO-alnetqC6QwGHRKIGhDmjZhmwtf_fXlg9nkPpNLI2aH2cqw"
        clientId = "671173409486-3ontfjfpj32bjfmtmpp9teclntdp9jvb.apps.googleusercontent.com"
        user = identity_connect.getUserByToken(token,clientId)
        log.debug( user)
        self.assertIsNotNone( user )
        log.debug("user claims %s", json.dumps(user,  indent=4, sort_keys=True))

    def test_get(self):
        token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjZlZjRiZDkwODU5MWY2OTdhOGE5Yjg5M2IwM2U2YTc3ZWIwNGU1MWYiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJuYmYiOjE2Mjk4NTE4ODgsImF1ZCI6IjY3MTE3MzQwOTQ4Ni0zb250ZmpmcGozMmJqZm10bXBwOXRlY2xudGRwOWp2Yi5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjEwMDEwNTA1MjgwNDkxMDg4MDYwMCIsImVtYWlsIjoicmZtaDI0aHJAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF6cCI6IjY3MTE3MzQwOTQ4Ni0zb250ZmpmcGozMmJqZm10bXBwOXRlY2xudGRwOWp2Yi5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsIm5hbWUiOiJyZm1oMjRociBNZW5kb3phIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FBVFhBSnhBLWF2cVlxRHJhWVAzci1iRGt5ajZKaGpEaExEdFFhNTRKcXhQPXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6InJmbWgyNGhyIiwiZmFtaWx5X25hbWUiOiJNZW5kb3phIiwiaWF0IjoxNjI5ODUyMTg4LCJleHAiOjE2Mjk4NTU3ODgsImp0aSI6IjkwZjg3N2JmYjc2OTA2YjhiNjJmNmFiYTNlMGRkODkzZjAzNWI4YjIifQ.Idy3K4W0q-Sq6_Gk38m4pLBmt-ca6AKlluT8rUBM5dpzHZPn41OPnvobZG8jT06pobkKIvdC0XfB_KW7eABny_BFObGDY8YeRSK54_cg581flh5QMegMWlBH2CaexkG_SwbnwgheTbILwP_5wDLvLEIDYOHy9xsj-OHWhDPkIDRmQi7uGoNsDxsEXo0jgxKtM7_cZJK8RnzcOh88GfhGYUPuPF-JHOQYjjJcDwHTHVtQ1X0l-OzfrlP_vdqiq80ihmuZZf9CKU9XUxndj4zqtQpE-D_M8avvVSkseg3WOXUNtDhztWmglXsQ-DK25xFLGxvp9VmabYuyHOD95M3RKg"
        clientId = "671173409486-3ontfjfpj32bjfmtmpp9teclntdp9jvb.apps.googleusercontent.com"

        req = {
                'service': 'identity', 
                'action': 'getUserByToken', 
                'token': token,
                'clientId': clientId
        }
        obj = identity_connect.processRequest(req)
        logging.debug( json.dumps(obj,  indent=4, sort_keys=True) )



if __name__ == '__main__':
    unittest.main()