from __future__ import absolute_import
from celery import Celery
from django.conf import settings

import configurations
import os


# set the default Django settings module for the 'celery' program.
if not ("DJANGO_SETTINGS_MODULE" in os.environ):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniq.settings')
configuration = os.getenv('DJANGO_CONFIGURATION', 'BaseConfiguration')
os.environ.setdefault('DJANGO_CONFIGURATION', configuration)

configurations.setup()

app = Celery('uniq')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
