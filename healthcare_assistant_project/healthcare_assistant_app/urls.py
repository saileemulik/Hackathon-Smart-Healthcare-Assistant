# healthcare_assistant_app/urls.py

from django.urls import path
from . import views
# from .views import chatbot_view
urlpatterns = [
     path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('doctor/', views.doctor, name='doctor'),
     path('dr_dashboard/', views.dr_dashboard, name='dr_dashboard'),
   path('medication/new/', views.MedicationCreateView.as_view(), name='medication_new'),
    path('patients/', views.PatientListView.as_view(), name='patient_list'),
    path('patient/new/', views.PatientCreateView.as_view(), name='patient_new'),
     path('chatbot/',views.chatbot_view, name='chatbot_view'),
     path('debug/appointments/', views.debug_appointments, name='debug_appointments'),
     path('schedule_appointment/', views.schedule_appointment, name='schedule_appointment'),
     path('appointment_reminder/', views.appointment_reminder, name='appointment_reminder'),
    #  path('get_medications/', views.get_medications, name='get_medications'),
    # Add more paths for medications, appointments, etc.
]
