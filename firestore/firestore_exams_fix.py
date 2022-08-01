import json
import logging

logging.basicConfig( level=logging.DEBUG)
logging.debug("test has started") 

import firebase_admin
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
    examsSet = db.collection("exams") \
        .where("materia_id","==",'77b9d6a5-7c20-4f9d-b266-fe72945bba97') \
        .get()
    for indexExam, exam in enumerate(examsSet):
        log.debug("exam" , indexExam,  str(exam.to_dict()) )

        targetMateria = db.collection("materias").document(exam.get("materia_id")).get()
        counter = db.collection("materias/" + exam.get("materia_id") + "/exams").get()
        exam_ref = targetMateria.reference.collection('exams').document(exam.id)
        examValues = exam.to_dict()
        examValues["idx"] = len(counter)
        exam_ref.set( examValues )        

        parameterSet = exam.reference.collection("parameters").get()
        for parameter in parameterSet:
            log.debug("parameter:" +  str(parameter.to_dict()) )

            parameter_ref = exam_ref.collection('parameters').document(parameter.id)
            parameter_ref.set( parameter.to_dict() )        

            criteriaSet = parameter.reference.collection("criterias").get()
            for criteria in criteriaSet:
                log.debug("criteria:" + str(criteria.to_dict()) )

                criteria_ref = parameter_ref.collection('criterias').document(criteria.id)
                criteria_ref.set( criteria.to_dict() )        

                aspectSet = criteria.reference.collection("aspects").get()
                for aspect in aspectSet:
                    log.debug("aspect:" + str( aspect.to_dict() ))
                    aspect_ref = criteria_ref.collection('aspects').document(aspect.id)
                    aspect_ref.set( aspect.to_dict() )                       
            

