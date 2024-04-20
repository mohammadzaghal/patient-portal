"""
TODO: Implement the Patient class.
Please import and use the config and db config variables.

The attributes for this class should be the same as the columns in the PATIENTS_TABLE.

The Object Arguments should only be name , gender and age.
Rest of the attributes should be set within the class.

-> for id use uuid4 to generate a unique id for each patient.
-> for checkin and checkout use the current date and time.

There should be a method to update the patient's room and ward. validation should be used.(config is given)

Validation should be done for all of the variables in config and db_config.

There should be a method to commit that patient to the database using the api_controller.
"""

import uuid
from datetime import datetime
from config import GENDERS, WARD_NUMBERS, ROOM_NUMBERS
import requests

class Patient:
    def __init__(self, name, gender, age):
        self.patient_id = str(uuid.uuid4())
        self.name = name
        self.gender = self.validate_gender(gender)
        self.age = age
        self.checkin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.checkout = None
        self.ward = None
        self.room = None

    def validate_gender(self, gender):
        if gender not in GENDERS:
            raise ValueError(f"Invalid gender. Valid options are: {GENDERS}")
        return gender

    def update_room_and_ward(self, ward, room):
        if ward not in WARD_NUMBERS or room not in ROOM_NUMBERS[ward]:
            raise ValueError("Invalid ward or room for this patient.")
        self.ward = ward
        self.room = room

    def commit(self):
        data = {
            "patient_id": self.patient_id,
            "name": self.name,
            "gender": self.gender,
            "age": self.age,
            "checkin": self.checkin,
            "checkout": self.checkout,
            "ward": self.ward,
            "room": self.room
        }
        response = requests.post("http://127.0.0.1:5000/patients", json=data)
        return response.json()

    def __str__(self):
        return f"Patient {self.name}, ID {self.patient_id}"
