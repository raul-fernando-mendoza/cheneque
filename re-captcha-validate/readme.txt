*setup flask
from folder C:\projects\cheneque\re-captcha-validate
run 
flask -A  recaptcha_validate_test run  --debug

* test
from folder C:\projects\cheneque\re-captcha-validate
curl.exe -X POST -H "Content-Type:application/json" -d "@./data_test.json" http://127.0.0.1:5000/recaptchaServerValidate


#deploy function to cloud functions
#  YOU MUST RUN FROM THE FOLDER WHERE THE funtion is located. use change dir
gcloud functions deploy chenequeRequest --runtime python39 --trigger-http --allow-unauthenticated --security-level=secure-optional
