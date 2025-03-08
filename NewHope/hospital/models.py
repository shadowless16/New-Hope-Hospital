from mongoengine import Document, StringField, IntField, DateField, ReferenceField, FloatField, BooleanField, SequenceField
from mongoengine import ValidationError, connect
import re
import datetime
from cryptography.fernet import Fernet

# Connect to MongoDB
connect(db='newhope', host='localhost', port=27017)  # Ensure MongoDB is running

# Phone number validator
def validate_phone(value):
    pattern = r'^\d{2}-\d{3}-\d{4}-\d{3}-\d{3}$'
    if not re.match(pattern, value):
        raise ValidationError("Phone number must be in format '11-111-1111-111-111'")

# Counter for auto-incrementing IDs
class IDCounter(Document):
    name = StringField(primary_key=True)
    sequence_value = IntField(default=0)

def get_next_id(name):
    counter = IDCounter.objects(name=name).first()
    if not counter:
        counter = IDCounter(name=name, sequence_value=1)
    else:
        counter.sequence_value += 1
    counter.save()
    return counter.sequence_value

# Generate a key for encryption and decryption
# You should store this key securely and not regenerate it every time
key = Fernet.generate_key()
cipher = Fernet(key)

# WardDetails
class WardDetails(Document):
    ward_id = IntField(primary_key=True, default=lambda: get_next_id('ward_id'))
    ward_name = StringField(choices=['OPD', 'ICU', 'CCU', 'Spl_Ward', 'General_Ward', 'Emergency'], required=True)
    total_beds = IntField(min_value=1, required=True)
    ward_charge = FloatField(min_value=0, required=True)
    avail_beds = IntField(min_value=0, required=True)

    meta = {'collection': 'ward_details'}

    def clean(self):
        if self.avail_beds > self.total_beds:
            raise ValidationError("Available beds cannot exceed total beds")

# DoctorDetails
class DoctorDetails(Document):
    doctor_id = IntField(primary_key=True, default=lambda: get_next_id('doctor_id'))
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    address = StringField(required=True)
    phone_num = StringField(required=True, validation=validate_phone)
    employment_type = StringField(choices=['Resident', 'Visiting'], required=True)
    ward = ReferenceField(WardDetails, required=True)
    specialization = StringField(required=True)

    meta = {'collection': 'doctor_details'}

# PatientDetails
class PatientDetails(Document):
    patient_id = IntField(primary_key=True, default=lambda: get_next_id('patient_id'))
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    address = StringField(required=True)
    age = IntField(min_value=0, required=True)
    height = IntField(min_value=0, required=True)
    weight = IntField(min_value=0, required=True)
    blood_grp = StringField(choices=['A', 'B', 'AB', 'O'], required=True)
    admit_date = DateField(required=True)
    discharge_date = DateField()
    treatment_type = StringField(required=True)
    doctor = ReferenceField(DoctorDetails, required=True)
    ward = ReferenceField(WardDetails, required=True)
    phone_num = StringField(required=True, validation=validate_phone)

    meta = {
        'collection': 'patient_details',
        'indexes': [
            'admit_date',
            'discharge_date',
        ]
    }

    def clean(self):
        if self.admit_date < datetime.date.today():
            raise ValidationError("Admit date cannot be in the past")
        if self.discharge_date and self.discharge_date < self.admit_date:
            raise ValidationError("Discharge date cannot be before admit date")

# MedicalHistory
class MedicalHistory(Document):
    record_id = IntField(primary_key=True, default=lambda: get_next_id('record_id'))
    patient = ReferenceField(PatientDetails, required=True)
    doctor = ReferenceField(DoctorDetails, required=True)
    disease = StringField(required=True)
    original_ward = ReferenceField(WardDetails, required=True)
    discharge_ward = ReferenceField(WardDetails, required=True)

    meta = {'collection': 'medical_history'}

# Payments
class Payments(Document):
    payment_id = IntField(primary_key=True, default=lambda: get_next_id('payment_id'))
    patient = ReferenceField(PatientDetails, required=True)
    payment_date = DateField(required=True)
    payment_method = StringField(choices=['Cash', 'Check', 'Credit_Card'], required=True)
    cc_num = StringField()
    card_holders_name = StringField()
    check_num = StringField()
    advance_payment = FloatField(min_value=0, required=True)
    final_payment = FloatField(min_value=0)
    payment_status = StringField(choices=['Paid', 'Pending'], required=True)

    meta = {
        'collection': 'payments',
        'indexes': [
            'payment_status',
        ]
    }

    def encrypt_cc_num(self):
        if self.cc_num:
            self.cc_num = cipher.encrypt(self.cc_num.encode()).decode()

    def decrypt_cc_num(self):
        if self.cc_num:
            return cipher.decrypt(self.cc_num.encode()).decode()

    def clean(self):
        if self.payment_date < datetime.date.today():
            raise ValidationError("Payment date cannot be in the past")
        if self.payment_method == 'Credit_Card' and (not self.cc_num or not self.card_holders_name):
            raise ValidationError("Credit card details required for Credit_Card payment")
        if self.payment_method == 'Check' and not self.check_num:
            raise ValidationError("Check number required for Check payment")

    def calculate_final_payment(self, total_bill):
        self.final_payment = total_bill - self.advance_payment
        self.save()


class HospitalUser(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)  # In production, hash this
    role = StringField(choices=['Admin', 'Developer'], required=True)

    meta = {'collection': 'hospital_users'}