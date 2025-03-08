from django.contrib import admin
from django.urls import path, include
from hospital import views  # Import views from hospital app

urlpatterns = [
    path('admin/', admin.site.urls),        # Admin interface
    path('', include('hospital.urls')),     # Include hospital URLs without a prefix
    path('doctors/', views.doctors, name='doctors'),
    path('patients/', views.patients, name='patients'),
    path('wards/', views.wards, name='wards'),
]