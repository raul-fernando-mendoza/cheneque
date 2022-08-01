import json
import logging

import firebase_admin
import environments
firebase_admin.initialize_app( )

import firestore_connect

log = logging.getLogger("cheneque")

from firebase_admin import firestore


if __name__ == '__main__':
    db = firestore.client()
    exams = db.collection("exams").get()
    for e in exams:
        print( e.get("label"))
        e.reference.update({"organization_id":"GmRu94210Q73Jc5tagWw","isDeleted":False})





