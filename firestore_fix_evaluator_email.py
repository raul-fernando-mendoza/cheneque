import json
import logging

import firebase_admin
import environments
from firebase_admin import auth
firebase_admin.initialize_app( )

import firestore_connect

log = logging.getLogger("cheneque")

from firebase_admin import firestore

"""
iterate over all the exams and parameters 
if evaluator_email does not exist 
    then retrieve the user using the evaluator_name 
    and update the email with the missing info
"""

if __name__ == '__main__':
    db = firestore.client()
    examGradesList = db.collection("examGrades").get()
    for examGrades in examGradesList:
        #examGrades.reference.update({"updateon":"2021-08-14"})
        examGrades_id = examGrades.get("id")
        parameterGradesList = examGrades.reference.collection("parameterGrades").get()
        for parameterGrades in parameterGradesList:
            obj = parameterGrades.to_dict()
            if( "evaluator_email" not in obj):
                uid = parameterGrades.get("evaluator_uid")
                user = auth.get_user(uid)
                #parameterGrades.reference.update({"evaluator_email":user.email})
                log.debug("updating:" + uid + " user.evaluator_name:" + parameterGrades.get("evaluator_name") +  " to:" + user.email)
                #parameterGrades.reference.update({"evaluator_email":user.email})
            

