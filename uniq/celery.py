from __future__ import absolute_import
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

import configurations
import os

from celery.schedules import crontab

CELERY_IMPORTS = ('uniq.tasks',)

# set the default Django settings module for the 'celery' program.
if not ("DJANGO_SETTINGS_MODULE" in os.environ):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniq.settings')
configuration = os.getenv('DJANGO_CONFIGURATION', 'BaseConfiguration')
os.environ.setdefault('DJANGO_CONFIGURATION', configuration)

configurations.setup()

app = Celery('uniq')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
