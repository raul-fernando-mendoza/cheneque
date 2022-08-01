to deploy
gcloud functions deploy organization-create --region=us-central1 --entry-point onExamGradesParameterDelete --runtime python39 --trigger-event "providers/cloud.firestore/eventTypes/document.delete"  --trigger-resource "projects/celtic-bivouac-307316/databases/(default)/documents/examGrades/{examGradeId}/parameterGrades/{parameterGradeId}" 

#deploy function to cloud functions
gcloud functions deploy processRequest --runtime python39 --trigger-http --allow-unauthenticated --security-level=secure-optional

curl -m 70 -X POST -H "Content-Type:application/json" -d "{\"certificateId\":\"raul_test\",\"studentName\":\"Claudia Gamboa\",\"materiaName\":\"Salsa\",\"label1\":\"Salsa\",\"label2\":\"X\",\"label3\":\"Otros\",\"label4\":\"www.rax.com\",\"color1\":\"blue\",\"color2\":\"red\"}" https://us-central1-thoth-qa.cloudfunctions.net/createCertificate 

{
    "certificateId":"raul_test" ,
    "studentName":"Claudia Gamboa",
    "materiaName":"Salsa",
    "label1":"Salsa",
    "label2":"X",
    "label3":"Otros",
    "label4":"www.rax.com",
    "color1":"blue",
    "color2":"red"
}