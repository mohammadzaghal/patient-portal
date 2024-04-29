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
from patient_db_config import PATIENT_COLUMN_NAMES

class Patient:
    def __init__(self, name, gender, age):
        self.patient_id = str(uuid.uuid4())
        self.patient_name = self._validate_name(name)
        self.patient_gender = self._validate_gender(gender)
        self.patient_age = self._validate_age(age)
        self.patient_checkin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.patient_checkout = None
        self.patient_ward = None
        self.patient_room = None

    def _validate_name(self, name):
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        return name

    def _validate_gender(self, gender):
        if gender not in GENDERS:
            raise ValueError("Invalid gender")
        return gender

    def _validate_age(self, age):
        if not isinstance(age, int) or age <= 0:
            raise ValueError("Age must be a positive integer")
        return age

    def _validate_ward(self, ward):
        if ward not in WARD_NUMBERS:
            raise ValueError("Invalid ward number")
        return ward

    def _validate_room(self, room):
        all_rooms = []
        for ward, rooms in ROOM_NUMBERS.items():
            all_rooms = all_rooms + rooms
        if str(room) not in all_rooms:
            raise ValueError("Invalid room number")
        return room
    
    def set_room(self, room):
        self.patient_room = self._validate_room(room)

    def set_ward(self, ward):
        self.patient_ward = self._validate_ward(ward)

    def update_room(self, room):
        self.patient_room = self._validate_room(room)

    def update_ward(self, ward):
        self.patient_ward = self._validate_ward(ward)

    def get_id(self):
        return self.patient_id
    
    def commit(self):
        patient_data = {
            "patient_name": self.patient_name,
            "patient_gender": self.patient_gender,
            "patient_age": self.patient_age,
            "patient_checkin": self.patient_checkin,
            "patient_ward": self.patient_ward,
            "patient_room": self.patient_room
        }
