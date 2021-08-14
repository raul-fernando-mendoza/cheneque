import json
import logging

import firebase_admin
import environments
firebase_admin.initialize_app(environments.config["cred"] )

import firestore_connect

log = logging.getLogger("cheneque")

from firebase_admin import firestore


if __name__ == '__main__':
    db = firestore.client()
    examGradesList = db.collection("examGrades").get()
    for examGrades in examGradesList:
        examGrades.reference.update({"updateon":"2021-08-14"})
        examGrades_id = examGrades.get("id")
        parameterGradesList = examGrades.reference.collection("parameterGrades").get()
        for parameterGrades in parameterGradesList:
            parameterGrades.reference.update({"examGrades_id":examGrades_id})
            parameterGrades_id = parameterGrades.get("id")
            criteriaGradesList = parameterGrades.reference.collection("criteriaGrades").get()
            for criteriaGrades in criteriaGradesList:
                criteriaGrades.reference.update({"parameterGrades_id":parameterGrades_id})
                criteriaGrades_id = criteriaGrades.get("id")
                aspectGradesList = criteriaGrades.reference.collection("aspectGrades").get()
                for aspectsGrades in aspectGradesList:
                    aspectsGrades.reference.update({"criteriaGrades_id":criteriaGrades_id}) 
                    aspectsGrades.reference.update({"updateon":"2021-08-14"})





