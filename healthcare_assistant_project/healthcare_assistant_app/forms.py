# healthcare_assistant_app/forms.py

from django import forms
from .models import Appointment,Medication

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'date', 'time', 'notes']
class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['patient','name', 'dosage', 'schedule']