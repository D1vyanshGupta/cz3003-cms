"""
    Module to generate the report to send to the PMO
"""
import os
import time
import shutil
import requests

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.models import TrafficEvent, TerroristEvent, District


def get_traffic_info(request):
    """
        Get traffic information from the database
    """
    traffic_events = TrafficEvent.objects.all()
    response = {}
    num_vehicles = 0
    num_casualties = 0
    num_injuries = 0
    for traffic_event in traffic_events:
        event = traffic_event.event
        num_vehicles += traffic_event.num_vehicles
        num_casualties += event.num_casualties
        num_injuries += event.num_injured
    response['numTraffics'] = len(traffic_events)
    response['numVehicles'] = num_vehicles
    response['numCasualties'] = num_casualties
    response['numInjuries'] = num_injuries

    return JsonResponse(response, safe=False)


def get_terrorist_info(request):
    """
        Get terrorist information from the database
    """
    terrorist_events = TerroristEvent.objects.all()
    response = {}
    num_hostiles = 0
    num_casualties = 0
    num_injuries = 0
    attack_types = ""
    for terrorist_event in terrorist_events:
        event = terrorist_event.event
        num_hostiles += terrorist_event.num_hostiles
        num_casualties += event.num_casualties
        num_injuries += event.num_injured
        attack_types += terrorist_event.attack_type +','

    response['numAttacks'] = len(terrorist_events)
    response['numHostiles'] = num_hostiles
    response['numCasualties'] = num_casualties
    response['numInjuries'] = num_injuries
    response['attackTypes'] = attack_types

    return JsonResponse(response, safe=False)

def get_crisis_info(request):
    """
        Get the crisis information for each region
    """
    districts = District.objects.all()
    response = {}
    for d in districts:
        response[d.district] = d.crisis
    return JsonResponse(response, safe=False)


def get_map_image(request):
    """
        Get the image of Google Map
    """
    screenshot_dir_path = os.path.join(os.getcwd(), 'static', 'img', 'report')

    if os.path.isdir(screenshot_dir_path):
        shutil.rmtree(screenshot_dir_path)

    os.makedirs(screenshot_dir_path)

    try:
        browser = webdriver.Chrome("/usr/local/bin/chromedriver")

        print('capturing screenshots')

        browser.get('http://127.0.0.1:8000/utils/maps/crisis')
        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "done")))
        browser.save_screenshot(os.path.join(screenshot_dir_path, 'crisis_screenshot.png'))
        print('crisis done')

        browser.get('http://127.0.0.1:8000/utils/maps/traffic')
        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "done")))
        browser.save_screenshot(os.path.join(screenshot_dir_path, 'traffic_screenshot.png'))
        print('traffic done')

        browser.get('http://127.0.0.1:8000/utils/maps/terrorist')
        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "done")))
        browser.save_screenshot(os.path.join(screenshot_dir_path, 'terrorist_screenshot.png'))
        print('terrorist done')

        browser.get('http://127.0.0.1:8000/utils/maps/weather')
        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "done")))
        browser.save_screenshot(os.path.join(screenshot_dir_path, 'weather_screenshot.png'))
        print('weather done')

        browser.get('http://127.0.0.1:8000/utils/maps/dengue')
        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "done")))
        browser.save_screenshot(os.path.join(screenshot_dir_path, 'dengue_screenshot.png'))
        print('dengue done')

        browser.quit()
    except Exception as e:
        print(e)
    finally:
        return HttpResponse('done')
