import unittest
import json
import logging

import firebase_admin
import environments

firebase_admin.initialize_app( )

import firestore_connect

from datetime import date

log = logging.getLogger("cheneque")

db = firebase_admin.firestore.client()


class TestExamenObservations(unittest.TestCase):

    def testGetObject(self):

        recordset = db.collection("examGrades").where("course","==", "estadistica").order_by("id", direction=firebase_admin.firestore.Query.ASCENDING)

        docs = recordset.get()
        for doc in docs:
            documentJSON = doc.to_dict()
            log.debug( documentJSON["course"] ) 
    

if __name__ == '__main__':
    unittest.main()