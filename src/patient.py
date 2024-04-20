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
from config import GENDERS, WARD_NUMBERS, ROOM_NUMBERS, API_CONTROLLER_URL
import requests

class Patient:
    def __init__(self, name, gender, age):
        self.patient_id = str(uuid.uuid4())  # Generates a unique identifier for each patient
        self.name = name
        self.gender = self.validate_gender(gender)
        self.age = age
        self.checkin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Stores current date and time for checkin
        self.checkout = None
        self.ward = None
        self.room = None

    def validate_gender(self, gender):
        """Validates the gender against a predefined list of acceptable genders."""
        if gender not in GENDERS:
            raise ValueError(f"Invalid gender. Valid options are: {', '.join(GENDERS)}")
        return gender

    def set_room(self, room):
        """Sets the patient's room, ensuring it exists within the configured rooms for the ward."""
        if self.ward is not None and room in ROOM_NUMBERS[self.ward]:
            self.room = room
        else:
            raise ValueError("Invalid room for the assigned ward.")

    def set_ward(self, ward):
        """Sets the patient's ward, ensuring it is a valid ward."""
        if ward in WARD_NUMBERS:
            self.ward = ward
        else:
            raise ValueError("Invalid ward number.")

    def get_id(self):
        """Returns the patient's unique identifier."""
        return self.patient_id

    def commit(self):
        """Commits the patient data to the database via an API call."""
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
        response = requests.post(API_CONTROLLER_URL + "/patients", json=data)
        if response.status_code == 200:
            return {"status": "success", "data": response.json()}
        else:
            return {"status": "error", "message": response.text}

    def __str__(self):
        """Returns a string representation of the patient."""
        return f"Patient {self.name}, ID {self.patient_id}"

# Example Usage:
# patient = Patient("John Doe", "Male", 30)
# patient.set_ward(1)
# patient.set_room(101)
# print(patient.commit())
