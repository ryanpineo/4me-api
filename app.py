import os

import requests
from flask import Flask, request
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields


app = Flask(__name__)
ma = Marshmallow(app)

FHIR_TOKEN = os.environ['FHIR_TOKEN']
FHIR_URL = "https://hackhlth2019-4me.azurehealthcareapis.com"
fhir_session = requests.Session()
fhir_session.headers = {'Authorization': f'Bearer {FHIR_TOKEN}'}


class PatientSchema(Schema):
    first_name = fields.Str()
    last_name = fields.Str()
    gender = fields.Str()


@app.route("/api/v1/patients", methods=["GET", "POST"])
def patients():
    if request.method == 'GET':
        response = fhir_session.get(f"{FHIR_URL}/Patient")
        return response.json()
    elif request.method == "POST":
        schema = PatientSchema()
        data = schema.load(request.json)
        response = fhir_session.post(
            f"{FHIR_URL}/Patient",
            json={
                "resourceType": "Patient",
                "active": True,
                "name": [
                    {
                        "use": "official",
                        "family": data["first_name"],
                        "given": data["last_name"]
                    }
                ],
                "gender": data["gender"]
            }
        )
        return response.json()


@app.route("/api/v1/patients/<patient_id>", methods=["GET"])
def patients_detail(patient_id):
    if request.method == 'GET':
        response = fhir_session.get(f"{FHIR_URL}/Patient/{patient_id}")
        return response.json()
