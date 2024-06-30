# celery.py

import os
from celery import Celery
# celery.py

from celery import Celery
from celery.schedules import crontab

app = Celery('healthcare_assistant_project')

# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all apps listed in INSTALLED_APPS
app.autodiscover_tasks()

# Schedule the periodic task
app.conf.beat_schedule = {
    'send-reminders-every-day': {
        'task': 'healthcare_assistant_app.tasks.send_reminders',
        'schedule': crontab(hour=8, minute=0),  # Adjust time as needed
    },
}

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_assistant_project.settings')

# Initialize Celery application
app = Celery('healthcare_assistant_project')

# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all apps listed in INSTALLED_APPS
app.autodiscover_tasks()
