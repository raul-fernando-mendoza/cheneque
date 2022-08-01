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
    examGradesList = db.collection("examGrades").get()
    for examGrades in examGradesList:
        print( examGrades.get("id"))
        #examGrades.reference.update({"updateon":"2021-09-11"})
        parameterGradesList = examGrades.reference.collection("parameterGrades").get()
        for parameterGrades in parameterGradesList:
            completed = parameterGrades.get("completed")
            scoreType = parameterGrades.get("scoreType")
            #parameterGrades.reference.update({"updateon":"2021-09-11"})
            criteriaGradesList = parameterGrades.reference.collection("criteriaGrades").get()
            for criteriaGrades in criteriaGradesList:
                #criteriaGrades.reference.update({"updateon":"2021-09-11"})
                aspectGradesList = criteriaGrades.reference.collection("aspectGrades").get()
                for aspectsGrades in aspectGradesList:
                    #aspectsGrades.reference.update({"updateon":"2021-08-14"})
                    id = aspectsGrades.get("id")
                    score = aspectsGrades.get("score")
                   
                    if( scoreType =="starts" and score==None and completed == True):
                        print(" updating " + str(id) + " completed:" + str(completed) + " scoreType:" + scoreType + " score=" + str(score) + " to 1")
                        #aspectsGrades.reference.update({"score":0.95})
                    #else:
                    #    print("leaving  " + str(id) + " completed:" + str(completed) + " scoreType:" + scoreType + " score=" + str(score) )





