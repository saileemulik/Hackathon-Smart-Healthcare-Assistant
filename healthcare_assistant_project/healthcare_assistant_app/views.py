from django.shortcuts import render, redirect, HttpResponse
from .models import Patient, Medication, Appointment
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from .forms import AppointmentForm
from .utils import send_notification_email

class PatientListView(ListView):
    model = Patient
    template_name = 'patient_list.html'

class PatientCreateView(CreateView):
    model = Patient
    template_name = 'patient_form.html'
    fields = ['name', 'email', 'phone']
    success_url = reverse_lazy('patient_list')

def index(request):
    patients = Patient.objects.all()
    medications = Medication.objects.all()
    appointments = Appointment.objects.all()
    context = {
        'patients': patients,
        'medications': medications,
        'appointments': appointments,
    }
    return render(request, 'index.html', context)

def get_reminders():
    reminders = []
    today = timezone.localtime().date()

    today_appointments = Appointment.objects.filter(date=today)

    for appointment in today_appointments:
        reminders.append(f"Reminder: Appointment for {appointment.patient.name} at {appointment.time}")

    return reminders

def get_appointments():
    appointments_info = []
    today = timezone.localtime().date()
    today_appointments = Appointment.objects.filter(date=today)
    for appointment in today_appointments:
        appointments_info.append(f"{appointment.patient.name} at {appointment.time}")
    return appointments_info

def get_medications():
    medications_info = []
    medications = Medication.objects.all()
    for medication in medications:
        medications_info.append(f"{medication.name} - {medication.dosage} - Schedule: {medication.schedule}")
    return medications_info

class MedicationCreateView(CreateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patients'] = Patient.objects.all()
        return context
    model = Medication
    template_name = 'medication_new.html'
    fields = ['name', 'dosage', 'schedule', 'patient']
    success_url = reverse_lazy('index')

def get_health_advice(message):
    if 'diet' in message:
        return "Make sure to include plenty of fruits and vegetables in your diet."
    elif 'exercise' in message:
        return "Regular exercise, such as brisk walking or swimming, can help improve your overall health."
    elif 'hydration' in message:
        return "Drink plenty of water throughout the day to stay hydrated."
    elif 'sleep' in message:
        return "Aim for 7-9 hours of sleep each night for optimal health and well-being."
    elif 'stress' in message or 'stress management' in message:
        return "Practice relaxation techniques like deep breathing or meditation to reduce stress."
    elif 'heart' in message or 'cardiovascular' in message:
        return "Include omega-3 fatty acids in your diet, found in fish like salmon, for heart health."
    elif 'bone' in message or 'osteoporosis' in message:
        return "Ensure adequate calcium intake from dairy products or fortified foods to support bone health."
    elif 'skin' in message or 'sunscreen' in message:
        return "Protect your skin from sun exposure by wearing sunscreen daily."
    elif 'mental health' in message or 'mental well-being' in message:
        return "Take breaks and engage in activities you enjoy to support mental well-being."
    elif 'vision' in message or 'eye health' in message:
        return "Schedule regular eye exams to maintain good vision health."
    elif 'digestive' in message or 'fiber' in message:
        return "Eat fiber-rich foods like whole grains and legumes to support digestive function."
    elif 'immune system' in message or 'immune health' in message:
        return "Boost your immune system with a balanced diet rich in vitamins and minerals."
    elif 'weight' in message or 'weight management' in message:
        return "Maintain a healthy weight through a combination of diet and exercise."
    elif 'respiratory' in message or 'lung health' in message:
        return "Avoid smoking and exposure to secondhand smoke to protect your lungs."
    elif 'dental' in message or 'oral hygiene' in message:
        return "Brush and floss your teeth daily to maintain good oral hygiene."
    elif 'joint health' in message or 'joint pain' in message:
        return "Engage in low-impact exercises like yoga or swimming to support joint health."
    elif 'cognitive function' in message or 'brain health' in message:
        return "Challenge your brain with puzzles or learning new skills to support cognitive function."
    elif 'diabetes' in message or 'blood sugar' in message:
        return "Limit sugary beverages and opt for whole fruits to manage blood sugar levels."
    elif 'allergy' in message or 'allergy management' in message:
        return "Identify and avoid triggers to manage allergy symptoms effectively."
    elif 'cancer' in message or 'cancer prevention' in message:
        return "Maintain a healthy lifestyle with regular screenings and a balanced diet to reduce cancer risks."
    elif 'chronic disease' in message:
        return "Managing chronic diseases requires consistent medical care and lifestyle adjustments. Here are some general tips:\n" \
               "- Monitor your condition regularly and follow your healthcare provider's advice.\n" \
               "- Take medications as prescribed and attend regular check-ups.\n" \
               "- Maintain a healthy diet and exercise regimen suitable for your condition.\n" \
               "- Manage stress through relaxation techniques and support groups.\n" \
               "- Educate yourself about your condition and its symptoms to better manage flare-ups."
    # Chronic diseases and their management advice
    elif 'asthma' in message:
        return "Manage asthma triggers and take medications as prescribed by your doctor. Keep a rescue inhaler with you at all times."
    elif 'arthritis' in message or 'joint pain' in message:
        return "Engage in low-impact exercises, maintain a healthy weight, and consider physical therapy to manage arthritis symptoms."
    elif 'hypertension' in message or 'high blood pressure' in message:
        return "Monitor your blood pressure regularly, reduce sodium intake, exercise regularly, and manage stress to control hypertension."
    elif 'osteoporosis' in message:
        return "Ensure adequate calcium and vitamin D intake, perform weight-bearing exercises, and avoid smoking and excessive alcohol consumption."
    elif 'chronic obstructive pulmonary disease' in message or 'copd' in message:
        return "Quit smoking if you smoke, participate in pulmonary rehabilitation programs, and use medications as prescribed to manage COPD."
    elif 'chronic kidney disease' in message:
        return "Control blood pressure and blood sugar levels, reduce sodium and protein intake, and follow a kidney-friendly diet."
    elif 'heart disease' in message or 'coronary artery disease' in message:
        return "Follow a heart-healthy diet, exercise regularly, manage stress, quit smoking, and take medications as prescribed to manage heart disease."
    elif 'diabetes' in message or 'type 2 diabetes' in message:
        return "Monitor blood sugar levels regularly, follow a balanced diet, engage in regular physical activity, and take medications as prescribed to manage diabetes."
    elif 'depression' in message or 'major depressive disorder' in message:
        return "Seek therapy or counseling, engage in regular physical activity, maintain social connections, and consider medication as recommended by a healthcare professional."
    else:
        return "I'm sorry, I can't provide advice on that topic yet. Please consult a healthcare professional."

@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', '').lower()

        response = ""

        if 'health advice' in message or 'advice' in message:
            advice = get_health_advice(message)
            response = advice
        elif 'reminder' in message or 'reminders' in message:
            reminders = get_reminders()
            if reminders:
                response = "Here are your reminders:\n" + "\n".join(reminders)
            else:
                response = "You have no reminders for today."
        elif 'appointment' in message or 'appointments' in message:
            appointments = get_appointments()
            if appointments:
                response = "You have the following appointments today:\n" + "\n".join(appointments)
            else:
                response = "You have no appointments for today."
        elif 'medication' in message or 'medications' in message:
            medications = get_medications()
            if medications:
                response = "Here are your medications:\n" + "\n".join(medications)
            else:
                response = "You have no medications."
        else:
            response = "I'm sorry, I don't understand your question. You can ask about your appointments, medications, or reminders."

        return JsonResponse({'response': response})

    return render(request, 'chatbot.html')

def debug_appointments(request):
    all_appointments = Appointment.objects.all()
    appointment_list = "\n".join([f"{appt.patient.name} - {appt.date} - {appt.time}" for appt in all_appointments])
    return HttpResponse(f"<pre>{appointment_list}</pre>")

def schedule_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to create an Appointment object
            # send_notification_email(appointment)  # Send email notification for the newly created appointment
            return redirect('index')
    else:
        form = AppointmentForm()
    return render(request, 'schedule_appointment.html', {'form': form})

def appointment_reminder():
    reminders = get_reminders()
    if reminders:
        # Implement notification mechanism here (e.g., send emails, SMS, etc.)
        pass
    else:
        print("No reminders to send.")

# def test_email(request):
#     send_mail(
#         'Subject here',
#         'Here is the message.',
#         'from@example.com',
#         ['to@example.com'],
#         fail_silently=False,
#     )
#     return HttpResponse('Test email sent.')
def doctor(request):
    return render(request,'doctor.html')

def dr_dashboard(request):
    patients = Patient.objects.all()
    medications = Medication.objects.all()
    appointments = Appointment.objects.all()
    context = {
        'patients': patients,
        'medications': medications,
        'appointments': appointments,
    }
    return render(request, 'dr_dashboard.html', context)

def home(request):
    return render(request,'home.html')

def medication_new(request):
    return render(request,'medication_new.html')