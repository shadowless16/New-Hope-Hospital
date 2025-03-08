from django.http import HttpResponse, JsonResponse
from .models import DoctorDetails, Payments, WardDetails, PatientDetails, get_next_id
import datetime
from .models import HospitalUser
from django.shortcuts import render

def home(request):
    context = {'active_page': 'home'}
    return render(request, 'home.html', context)

def export_doctors(request):
    current_month = datetime.date.today().month
    doctors = DoctorDetails.objects(ward__ne=None)  # Get all doctors with a ward
    with open(f'doctors_{current_month}.txt', 'w') as f:
        for doctor in doctors:
            f.write(f"{doctor.first_name} {doctor.last_name} - Ward: {doctor.ward.ward_name}\n")
    return HttpResponse("Doctors exported successfully! Check doctors_{}.txt".format(current_month))

def export_payments(request):
    month = request.GET.get('month')
    year = request.GET.get('year')
    if month and year:
        start_date = datetime.datetime(int(year), int(month), 1)
        end_date = datetime.datetime(int(year), int(month) + 1, 1)
        payments = Payments.objects(payment_date__gte=start_date, payment_date__lt=end_date)
    else:
        payments = Payments.objects.all()
    with open(f'payments_{month}_{year}.txt', 'w') as f:
        for payment in payments:
            f.write(f"Patient: {payment.patient.patient_id}, Amount: {payment.final_payment}, Status: {payment.payment_status}\n")
    payments_list = [{
        'patient_id': payment.patient.patient_id,
        'amount': payment.final_payment,
        'status': payment.payment_status
    } for payment in payments]
    return JsonResponse(payments_list, safe=False)


def create_users(request):
    HospitalUser(username='James', password='password', role='Admin').save()
    HospitalUser(username='Bryan', password='password', role='Developer').save()
    HospitalUser(username='John', password='password', role='Developer').save()
    HospitalUser(username='Maria', password='password', role='Developer').save()
    return HttpResponse("Users created successfully!")

def add_sample_data(request):
    # Add a ward
    ward = WardDetails(
        ward_id=get_next_id('ward_id'),
        ward_name='ICU',
        total_beds=10,
        ward_charge=500.0,
        avail_beds=8
    )
    ward.save()

    # Add a doctor
    doctor = DoctorDetails(
        doctor_id=get_next_id('doctor_id'),
        first_name='Jane',
        last_name='Smith',
        address='123 Main St',
        phone_num='11-111-1111-111-111',
        employment_type='Resident',
        ward=ward,
        specialization='Cardiology'
    )
    doctor.save()

    # Add a patient
    patient = PatientDetails(
        patient_id=get_next_id('patient_id'),
        first_name='John',
        last_name='Doe',
        address='456 Oak Ave',
        age=30,
        height=170,
        weight=70,
        blood_grp='A',
        admit_date=datetime.date.today(),
        treatment_type='Heart Checkup',
        doctor=doctor,
        ward=ward,
        phone_num='22-222-2222-222-222'
    )
    patient.save()

    # Add a payment
    payment = Payments(
        payment_id=get_next_id('payment_id'),
        patient=patient,
        payment_date=datetime.date.today(),
        payment_method='Credit_Card',
        cc_num='1234-5678-9012',
        card_holders_name='John Doe',
        advance_payment=200.0,
        payment_status='Paid'
    )
    payment.encrypt_cc_num()  # Encrypt the credit card number
    payment.save()

    return HttpResponse("Sample data added successfully!")

def list_patients(request):
    patients = PatientDetails.objects.all()
    output = "<h1>Patients</h1><ul>"
    for patient in patients:
        output += f"<li>{patient.first_name} {patient.last_name} - Age: {patient.age}, Admitted: {patient.admit_date}</li>"
    output += "</ul>"
    return HttpResponse(output)

def list_wards(request):
    wards = WardDetails.objects.all()
    output = "<h1>Wards</h1><ul>"
    for ward in wards:
        output += f"<li>{ward.ward_name} - Total Beds: {ward.total_beds}, Available Beds: {ward.avail_beds}</li>"
    output += "</ul>"
    return HttpResponse(output)

def list_payments(request):
    payments = Payments.objects.all()
    output = "<h1>Payments</h1><ul>"
    for payment in payments:
        output += f"<li>Patient: {payment.patient.patient_id}, Amount: {payment.final_payment}, Status: {payment.payment_status}</li>"
    output += "</ul>"
    return HttpResponse(output)

def login_view(request):
    context = {'active_page': 'login'}
    return render(request, 'login.html', context)

def signup_view(request):
    context = {'active_page': 'signup'}
    return render(request, 'signup.html', context)

def doctors(request):
    doctors_list = DoctorDetails.objects.all()
    context = {
        'doctors': doctors_list,
        'active_page': 'doctors'
    }
    return render(request, 'doctors.html', context)

def patients(request):
    patients_list = PatientDetails.objects.all()
    context = {
        'patients': patients_list,
        'active_page': 'patients'
    }
    return render(request, 'patients.html', context)

def wards(request):
    wards_list = WardDetails.objects.all()
    context = {
        'wards': wards_list,
        'active_page': 'wards'
    }
    return render(request, 'wards.html', context)

def add_doctor(request):
    # Logic for adding a new doctor
    return render(request, 'add_doctor.html')

def add_ward(request):
    # Logic for adding a new ward
    return render(request, 'add_ward.html')

def add_patient(request):
    # Logic for adding a new patient
    return render(request, 'add_patient.html')

def ward_details(request, ward_id):
    ward = WardDetails.objects.get(pk=ward_id)
    context = {
        'ward': ward,
        'active_page': 'wards'
    }
    return render(request, 'ward_details.html', context)

def payments(request):
    context = {'active_page': 'payments'}
    return render(request, 'payments.html', context)

def patient_details(request, patient_id):
    patient = PatientDetails.objects.get(pk=patient_id)
    context = {
        'patient': patient,
        'active_page': 'patients'
    }
    return render(request, 'patient_details.html', context)

