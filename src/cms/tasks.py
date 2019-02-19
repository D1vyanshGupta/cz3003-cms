from __future__ import absolute_import
from celery.decorators import task
from celery.utils.log import get_task_logger
from celery import group
from celery.task.schedules import crontab
from celery.decorators import periodic_task

from datetime import timedelta
from utils.pullapis.dengue import DengueAPI
from utils.pullapis.weather import WeatherAPI
from utils.dispatchers.pmodispatcher import PMODispatcher
from utils.crisiscalculation.calculation import CrisisCalculator


logger = get_task_logger(__name__)


# @task(name="pmo-emailer", bind=True)
@periodic_task(run_every=(crontab(minute='*/1')), name="pmo-emailer", ignore_result=True)
def email_pmo():
    """
        Background task to send PMO email every half an hour
    """
    PMODispatcher().dispatch(True)
    return 'Success'


# @task(name="do-pull-apis", bind=True)
@periodic_task(run_every=(crontab(minute='*/1')), name="do-pull-apis", ignore_result=True)
def pull_apis():
    """
        Background task to periodically pull APIs for weather and dengue
    """
    apis = [WeatherAPI(), DengueAPI()]
    for api in apis:
        api.pull_update()
    return 'Success'


# @task(name="check-for-crisis", bind=True)
@periodic_task(run_every=(crontab(minute='*/1')), name="check-for-crisis", ignore_result=True)
def check_crisis():
    """
        Background task to periodically pull APIs for weather and dengue
    """
    CrisisCalculator().check_crisis()

# @task(name="save-map-screenshots", bind=True)
@periodic_task(run_every=(crontab(minute='*/1')), name="save-map-screenshots", ignore_result=True)
def pull_apis():
    """
        Background task to periodically save screenshots
    """
    return 'Success'
