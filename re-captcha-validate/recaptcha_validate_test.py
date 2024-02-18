from flask import Flask, request, abort, jsonify
from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask_cors import CORS, cross_origin
from main import recaptchaServerValidate

app = Flask(__name__)
CORS(app, support_credentials=True)
#cors = CORS(app, resources={r"/exam-app/*": {"origins": "*"}})
FlaskJSON(app)


@app.route('/')
def home():
    return json_response(data="hello from flask")

@app.route('/recaptchaServerValidate',methods=['GET','POST'])
def Validate():
    return recaptchaServerValidate(request)

if __name__ == '__main__':
    app.run(host='0.0.0.0')    

