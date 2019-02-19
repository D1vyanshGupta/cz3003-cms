"""
	Celery
"""
from __future__ import absolute_import
import os


from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cms.settings')

from django.conf import settings  # noqa


BROKER_URL = 'redis://localhost:6379/0'

cmscelery = Celery('cms')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
cmscelery.config_from_object('django.conf:settings')
cmscelery.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
