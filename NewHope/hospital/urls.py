from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('export_doctors/', views.export_doctors, name='export_doctors'),
    path('export_payments/', views.export_payments, name='export_payments'),
    path('create_users/', views.create_users, name='create_users'),
    path('add_sample_data/', views.add_sample_data, name='add_sample_data'),
    path('doctors/', views.doctors, name='doctors'),
    path('patients/', views.patients, name='patients'),
    path('wards/', views.wards, name='wards'),
    path('payments/', views.payments, name='payments'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('add_doctor/', views.add_doctor, name='add_doctor'),
    path('add_ward/', views.add_ward, name='add_ward'),
    path('ward_details/<int:ward_id>/', views.ward_details, name='ward_details'),
    path('patient_details/<int:patient_id>/', views.patient_details, name='patient_details'),
    path('add_patient/', views.add_patient, name='add_patient'),
]