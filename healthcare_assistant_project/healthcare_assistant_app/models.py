# healthcare_assistant_app/models.py

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.utils import timezone

class Patient(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Medication(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    schedule = models.TextField()

    def __str__(self):
        return self.name

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.patient} - {self.date} - {self.time}"

# Signal receiver function to send email notification on new appointment creation
@receiver(post_save, sender=Appointment)
def appointment_saved(sender, instance, created, **kwargs):
    if created:
        send_notification_email(instance)

def send_notification_email(appointment):
    subject = f'Reminder: Appointment for {appointment.patient.name}'
    message = f'Hi {appointment.patient.name},\n\nThis is a reminder for your appointment on {appointment.date} at {appointment.time}.\n\nThank you!'
    sender_email = 'rashmitamhatre59@gmail.com'  # Replace with your email
    recipient_email = appointment.patient.email
    send_mail(subject, message, sender_email, [recipient_email])
