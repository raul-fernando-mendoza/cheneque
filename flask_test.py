from flask import Flask, request, abort, jsonify
from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)
#cors = CORS(app, resources={r"/exam-app/*": {"origins": "*"}})
FlaskJSON(app)


@app.route('/')
def home():
    return json_response(data="hello from flask")

if __name__ == '__main__':
    app.run(host='0.0.0.0')    

