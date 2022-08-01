from flask import Flask, request, abort, jsonify
from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask_cors import CORS, cross_origin

import pymysql as MySQLdb

app = Flask(__name__)
CORS(app, support_credentials=True)
#cors = CORS(app, resources={r"/exam-app/*": {"origins": "*"}})
FlaskJSON(app)


@app.route('/')
def home():
    try:
        # Open database connection
        #db = MySQLdb.connect("192.168.15.12","eApp","odroid","entities" )
        db = MySQLdb.connect("34.70.28.168","eApp","Argos4905","entities" )

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        # execute SQL query using execute() method.
        cursor.execute("show tables")

        # Fetch a single row using fetchone() method.
        data = cursor.fetchall()
        print (data)

        # disconnect from server
        db.close()
    except Exception as e:
        abort(404, description=str(e))

    return json_response(data=str(data))

if __name__ == '__main__':
    app.run(host='0.0.0.0')    

