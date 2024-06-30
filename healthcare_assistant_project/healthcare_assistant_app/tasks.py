# healthcare_assistant_app/tasks.py

from celery import shared_task
from django.utils import timezone
from .models import Appointment
from django.core.mail import send_mail
from .utils import send_notification_email  # Import your email function

@shared_task
def send_reminders():
    today = timezone.localtime().date()
    today_appointments = Appointment.objects.filter(date=today)
    
    for appointment in today_appointments:
        send_notification_email(appointment)
