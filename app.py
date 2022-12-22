# import necessary libraries and functions
from flask import Flask, jsonify, request
import json
import copy
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

class data:
    h = open('hospital.json')
    hospitals = json.load(h)
    p = open('patient.json')
    patient = json.load(p)
    h = open('hospital.json')
    doctors = json.load(h)
    hp = open('hospitalization.json')
    hospitalization = json.load(hp)


# creating a Flask app
app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("admin1234"),
    "abhay": generate_password_hash("abhay1234")
}

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False


@app.route('/get_patent_details/<phone_number>', methods = ['GET'])
@auth.login_required
def get_patent_details(phone_number):
    resp = data.patient[phone_number]
    return jsonify({'data': resp})


@app.route('/get_patent_records/<phone_number>', methods = ['GET'])
@auth.login_required
def get_patent_records(phone_number):
    hospitalization_temp = copy.deepcopy(data.hospitalization[phone_number])
    resp = []
    for i in hospitalization_temp:
        i['hospital'] = data.hospitals[i['hospital']]['name']
        i['doctor'] = data.doctors[i['doctor']]['name']
        resp.append(i)

    return jsonify({'data': resp})


@app.route('/get_hospital_details/<hospital_id>', methods = ['GET'])
@auth.login_required
def get_hospital_details(hospital_id):
    resp = data.hospitals[hospital_id]
    return jsonify({'data': resp})
  

@app.route('/doctor_hospital_details/<doc_id>', methods = ['GET'])
@auth.login_required
def doctor_hospital_details(doc_id):
    resp = data.doctors[doc_id]
    return jsonify({'data': resp})  
  
  
# driver function
if __name__ == '__main__':
  
    app.run(debug = True, port = "8080")