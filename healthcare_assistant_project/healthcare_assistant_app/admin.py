from django.contrib import admin

# Register your models here.
from .models import Patient,Medication,Appointment
# Register your models here.
admin.site.register(Patient)
admin.site.register(Medication)
admin.site.register(Appointment)