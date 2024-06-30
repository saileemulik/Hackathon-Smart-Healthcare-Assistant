from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

def send_notification_email(appointment):
    try:
        subject = f'Reminder: Appointment for {appointment.patient.name}'
        message = f'Hi {appointment.patient.name},\n\nThis is a reminder for your appointment on {appointment.date} at {appointment.time}.\n\nThank you!'
        sender_email = 'rashmitamhatre59@gmail.com' # Replace with your email
        recipient_email = appointment.patient.email
        
        send_mail(subject, message, sender_email, [recipient_email])
        return HttpResponse('Email sent successfully.')
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    except Exception as e:
        return HttpResponse(f'Error: {e}')
